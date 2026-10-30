#!/usr/bin/env python3
"""Client en ligne de commande de l'API ElevenLabs, bibliothèque standard uniquement.

Sous-commandes :
  compte      verifier, modeles, consommation, historique, recuperer
  voix        voix, voix-info, bibliotheque, ajouter-voix, concevoir-voix, remixer-voix, creer-voix, cloner
  générer     parole, dialogue, bruitage, musique, plan-musique
  traitement  changer-voix, isoler, separer-pistes, transcrire, aligner
  divers      brut, inspecter
La clé est lue dans la variable d'environnement ELEVENLABS_API_KEY ; elle n'est jamais affichée.
Lancer `elevenlabs.py <sous-commande> --help` pour les options, et voir ../SKILL.md pour l'usage.
"""

import argparse
import base64
import datetime
import hashlib
import http.client
import io
import json
import math
import os
import re
import shlex
import socket
import ssl
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile

API_BASE_DEFAUT = "https://api.elevenlabs.io"
MODELE_PAROLE_DEFAUT = "eleven_multilingual_v2"
MODELE_DIALOGUE_DEFAUT = "eleven_v3"
MODELE_BRUITAGE_DEFAUT = "eleven_text_to_sound_v2"
MODELES_BRUITAGE = ("eleven_text_to_sound_v2", "eleven_text_to_sound_v3")
MODELE_MUSIQUE_DEFAUT = "music_v1"
MODELES_MUSIQUE = ("music_v1", "music_v2", "music_v2_5")
MODELE_CHANGEUR_DEFAUT = "eleven_multilingual_sts_v2"
MODELE_CONCEPTION_DEFAUT = "eleven_multilingual_ttv_v2"
MODELES_CONCEPTION = ("eleven_multilingual_ttv_v2", "eleven_ttv_v3")
MODELE_TRANSCRIPTION_DEFAUT = "scribe_v2"
# Longueur maximale d'une requête de synthèse selon le modèle (documentation des modèles, octobre 2026).
# Pour un modèle absent de la table, l'API seule décide.
LONGUEUR_MAX_TEXTE = {
    "eleven_v3": 5000,
    "eleven_multilingual_v2": 10000,
    "eleven_flash_v2_5": 40000,
    "eleven_turbo_v2_5": 40000,
    "eleven_flash_v2": 30000,
    "eleven_turbo_v2": 30000,
}
CARACTERES_DIALOGUE_FIABLES = 2000
VOIX_MAX_DIALOGUE = 10
# Une extension de --sortie donne le format demandé à l'API. Un .wav est demandé en PCM brut puis
# enveloppé ici dans un en-tête WAV : la musique et la séparation de pistes n'ont pas de format wav_*.
FORMAT_PAR_EXTENSION = {".mp3": "mp3_44100_128", ".wav": "pcm_44100", ".opus": "opus_48000_96",
                        ".pcm": "pcm_44100"}
EXTENSION_PAR_CODEC = {"mp3": ".mp3", "wav": ".wav", "pcm": ".pcm", "opus": ".opus",
                       "ulaw": ".ulaw", "alaw": ".alaw"}
GODOT_NE_LIT_PAS = (".opus", ".pcm", ".ulaw", ".alaw")
EXTENSIONS_AUDIO = (".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac", ".opus", ".webm", ".mp4", ".mov",
                    ".mkv", ".aiff", ".aif", ".pcm")
TYPES_MIME = {
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".ogg": "audio/ogg", ".flac": "audio/flac",
    ".m4a": "audio/mp4", ".aac": "audio/aac", ".opus": "audio/ogg", ".webm": "audio/webm",
    ".mp4": "video/mp4", ".mov": "video/quicktime", ".mkv": "video/x-matroska",
    ".aiff": "audio/aiff", ".aif": "audio/aiff", ".pcm": "application/octet-stream",
}
ATTENTES_LIMITE = (10, 20, 40, 60, 60, 60, 60)
AGENT = "elevenlabs-plugin-quiche-lorraine-games/1"
RE_ID_VOIX = re.compile(r"[A-Za-z0-9]{20}")

# Codes de sortie (voir SKILL.md, section « Erreurs »)
OK = 0
ERREUR = 1           # erreur API inattendue, réponse illisible, fichier invalide
USAGE = 2            # argument invalide, refusé localement ou par la validation de l'API (422)
CLE = 3              # ELEVENLABS_API_KEY absente ou refusée
CREDITS = 4          # crédits du compte épuisés (quota_exceeded)
RESEAU = 5           # hôte bloqué par la politique réseau ou injoignable
PERMISSION = 6       # la clé n'a pas la permission demandée par l'endpoint (missing_permissions)
DELAI = 7            # délai de réponse dépassé (la génération a pu aboutir et être facturée)
CONTENU_REFUSE = 8   # texte, prompt ou audio refusé par la modération
LIMITE = 9           # trop de requêtes simultanées ou service saturé (HTTP 429), malgré les nouveaux essais


class ErreurEleven(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def pause_reessai(secondes):
    """Attente avant un nouvel essai ; ELEVENLABS_PAUSE_REESSAI la multiplie (les tests la mettent à 0)."""
    try:
        facteur = float(os.environ.get("ELEVENLABS_PAUSE_REESSAI", "1"))
    except ValueError:
        facteur = 1.0
    time.sleep(max(secondes * facteur, 0.0))


# ---------------------------------------------------------------------------
# Sortie : tout texte affiché passe par masquer(), pour que la clé n'apparaisse jamais.
# ---------------------------------------------------------------------------

def masquer(texte):
    texte = str(texte)
    cle = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if cle:
        texte = texte.replace(cle, "***")
    return texte


def dire(texte=""):
    print(masquer(texte), flush=True)


def signaler(texte):
    print(masquer(texte), file=sys.stderr, flush=True)


def lire_cle():
    cle = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not cle:
        raise ErreurEleven(CLE, (
            "ELEVENLABS_API_KEY n'est pas définie. Ajoute la clé ElevenLabs en secret de l'environnement "
            "(variable ELEVENLABS_API_KEY), puis ouvre une nouvelle session. Ne la colle pas dans le chat."))
    return cle


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class _SansRedirection(urllib.request.HTTPRedirectHandler):
    """Aucune redirection n'est suivie : l'en-tête xi-api-key ne part jamais vers un autre hôte."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OUVREUR = urllib.request.build_opener(_SansRedirection())


def hote(url):
    return urllib.parse.urlsplit(url).hostname or url


def _erreur_reseau(url, exc):
    nom = hote(url)
    raison = getattr(exc, "reason", exc)
    texte = str(raison)
    if "Tunnel connection failed: 403" in texte:
        return ErreurEleven(RESEAU, (
            f"Le domaine {nom} est bloqué par la politique réseau de l'environnement (403 du proxy). "
            f"Ajoute {nom} aux domaines autorisés de l'environnement, puis relance."))
    if "Tunnel connection failed" in texte:
        return ErreurEleven(RESEAU, (
            f"Le proxy n'a pas pu joindre {nom} ({texte}). Vérifie que ce domaine existe et qu'il est "
            "autorisé dans la politique réseau de l'environnement."))
    if isinstance(raison, socket.gaierror):
        return ErreurEleven(RESEAU, f"Hôte {nom} introuvable (DNS). Vérifie l'accès réseau de l'environnement.")
    if isinstance(raison, (socket.timeout, TimeoutError)):
        return ErreurEleven(DELAI, f"{nom} n'a pas répondu dans le délai imparti.")
    if isinstance(raison, (ConnectionResetError, ConnectionAbortedError, BrokenPipeError,
                           http.client.IncompleteRead, http.client.RemoteDisconnected, ssl.SSLEOFError)):
        return ErreurEleven(RESEAU, f"Connexion avec {nom} coupée en cours de transfert ({texte}).")
    if isinstance(raison, ssl.SSLError):
        return ErreurEleven(RESEAU, f"Échec TLS avec {nom} ({texte}). Vérifie les certificats de l'environnement.")
    return ErreurEleven(RESEAU, f"Impossible de joindre {nom} : {texte}.")


def requete(methode, url, corps=None, entetes=None, delai=60):
    """Renvoie (statut HTTP, en-têtes, corps en octets) sans lever sur les statuts >= 400."""
    req = urllib.request.Request(url, data=corps, method=methode, headers=dict(entetes or {}))
    req.add_header("User-Agent", AGENT)
    try:
        with _OUVREUR.open(req, timeout=delai) as rep:
            return rep.status, rep.headers, rep.read()
    except urllib.error.HTTPError as exc:
        try:
            brut = exc.read() or b""
        except (OSError, http.client.HTTPException):
            brut = b""
        return exc.code, exc.headers, brut
    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
        raise _erreur_reseau(url, exc) from None


class Reponse:
    def __init__(self, statut, entetes, corps):
        self.statut = statut
        self.entetes = entetes
        self.corps = corps

    def entete(self, nom):
        return self.entetes.get(nom) if self.entetes else None

    def json(self):
        try:
            return json.loads(self.corps.decode("utf-8")) if self.corps else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ErreurEleven(ERREUR, (
                f"Réponse illisible de l'API ElevenLabs (HTTP {self.statut}) : "
                f"{self.corps[:200].decode('utf-8', errors='replace')}")) from None


class Api:
    def __init__(self, base, cle):
        self.base = base.rstrip("/")
        self.cle = cle

    def url(self, chemin, params=None):
        url = self.base + chemin
        if params:
            url += "?" + urllib.parse.urlencode(params, doseq=True)
        return url

    def appel(self, methode, chemin, json_corps=None, multipart=None, params=None, delai=60, payant=False):
        entetes = {"xi-api-key": self.cle, "Accept": "*/*"}
        corps = None
        if json_corps is not None:
            corps = json.dumps(json_corps).encode("utf-8")
            entetes["Content-Type"] = "application/json"
        elif multipart is not None:
            corps, type_contenu = multipart
            entetes["Content-Type"] = type_contenu
        url = self.url(chemin, params)
        essai = 0
        while True:
            try:
                statut, rep_entetes, brut = requete(methode, url, corps, entetes, delai)
            except ErreurEleven as exc:
                if exc.code == DELAI and payant:
                    exc.message += (" La génération a pu aboutir côté ElevenLabs et être facturée : regarde "
                                    "`historique` (parole, dialogue, changement de voix) avant de relancer.")
                elif exc.code == DELAI:
                    exc.message += " Réessaie plus tard."
                raise
            # Un 429 (trop de requêtes simultanées, service saturé) est refusé avant tout traitement :
            # rien n'est facturé, on peut réessayer. Un 5xx sur une génération payante, non : elle a pu aboutir.
            if statut == 429 and essai < len(ATTENTES_LIMITE):
                attente = _attente_retry(rep_entetes, ATTENTES_LIMITE[essai])
                signaler(f"ElevenLabs limite les requêtes (HTTP 429) : nouvel essai dans {attente:.0f} s.")
                pause_reessai(attente)
                essai += 1
                continue
            if statut in (502, 503, 504) and not payant and essai < 2:
                pause_reessai(2 * (essai + 1))
                essai += 1
                continue
            break
        if statut >= 400:
            raise _erreur_api(statut, rep_entetes, brut, payant)
        return Reponse(statut, rep_entetes, brut)


def _attente_retry(entetes, defaut):
    valeur = entetes.get("Retry-After") if entetes else None
    try:
        return min(max(float(valeur), 1.0), 60.0)
    except (TypeError, ValueError):
        return float(defaut)


def _erreur_cle():
    return ErreurEleven(CLE, (
        "ElevenLabs refuse la clé ELEVENLABS_API_KEY (401). Vérifie-la dans les réglages ElevenLabs "
        "(Developers, API Keys), mets à jour le secret de l'environnement, puis ouvre une nouvelle session."))


MOTS_MODERATION = ("moderation", "content_against_policy", "against our", "terms of service", "violat",
                   "unsafe", "prohibited", "not allowed to generate", "blocked_content")


def _erreur_api(statut, entetes, brut, payant=False):
    texte = brut.decode("utf-8", errors="replace")
    try:
        charge = json.loads(texte) if texte else {}
    except json.JSONDecodeError:
        charge = None
    detail = charge.get("detail") if isinstance(charge, dict) else None
    etat, message, requete_id = "", "", ""
    if isinstance(detail, dict):
        etat = str(detail.get("status") or detail.get("code") or "")
        message = str(detail.get("message") or "")
        requete_id = str(detail.get("request_id") or "")
    elif isinstance(detail, list):
        morceaux = []
        for item in detail[:5]:
            if isinstance(item, dict):
                lieu = ".".join(str(x) for x in item.get("loc", []) if x != "body")
                morceaux.append(f"{lieu} : {item.get('msg')}" if lieu else str(item.get("msg")))
        message = " ; ".join(morceaux)
        etat = "validation"
    elif isinstance(detail, str):
        message = detail
    elif charge is None:
        message = texte[:200]
    requete_id = requete_id or (entetes.get("request-id") if entetes else "") or ""
    suffixe = f" (requête {requete_id})" if requete_id else ""
    bas = (etat + " " + message).lower()

    if etat in ("invalid_api_key", "needs_authorization"):
        return _erreur_cle()
    if etat == "missing_permissions":
        trouve = re.search(r"permission (\w+)", message)
        nom = trouve.group(1) if trouve else "demandée"
        return ErreurEleven(PERMISSION, (
            f"La clé ElevenLabs n'a pas la permission {nom}. Ajoute-la à la clé dans les réglages ElevenLabs "
            "(Developers, API Keys, modifier la clé) ; la valeur de la clé ne change pas, inutile de toucher "
            "au secret de l'environnement."))
    if etat == "quota_exceeded" or "quota" in bas or "insufficient credits" in bas or "not enough credits" in bas:
        return ErreurEleven(CREDITS, (
            "Le compte ElevenLabs n'a plus assez de crédits pour cette requête ; rien n'a été généré. "
            f"Recharge ou change d'offre dans les réglages ElevenLabs (Subscription).{suffixe}"))
    if statut == 429:
        return ErreurEleven(LIMITE, (
            f"ElevenLabs refuse encore la requête après environ 5 minutes d'essais (HTTP 429, {etat or 'limite'}). "
            "Rien n'a été facturé. Lance une seule requête à la fois, puis réessaie plus tard."))
    if any(mot in bas for mot in MOTS_MODERATION):
        return ErreurEleven(CONTENU_REFUSE, (
            f"ElevenLabs refuse l'entrée au titre de sa politique de contenu : {message}. "
            f"Reformule le texte ou le prompt.{suffixe}"))
    if statut == 401:
        if etat == "detected_unusual_activity":
            return ErreurEleven(CLE, (
                "ElevenLabs a bloqué l'offre gratuite de ce compte pour activité inhabituelle (souvent un "
                f"réseau partagé ou un proxy). Une offre payante lève ce blocage.{suffixe}"))
        return _erreur_cle()
    if etat == "voice_not_found" or (statut == 404 and "voice" in bas):
        return ErreurEleven(ERREUR, (
            f"Voix introuvable : {message or etat}. Vérifie l'identifiant avec `voix` ou `voix-info`.{suffixe}"))
    if statut == 422 or etat == "validation":
        return ErreurEleven(USAGE, f"L'API refuse les paramètres (HTTP {statut}) : {message}{suffixe}")
    complement = ""
    if payant and statut >= 500:
        complement = (" La génération a pu aboutir malgré l'erreur : regarde `historique` (parole, dialogue, "
                      "changement de voix) avant de relancer.")
    elif "output_format" in bas or "tier" in bas or "subscription" in bas:
        complement = " Ce réglage demande sans doute une offre supérieure : essaie un autre --format (mp3_44100_128)."
    corps = message or etat or texte[:200]
    return ErreurEleven(ERREUR, f"Erreur de l'API ElevenLabs (HTTP {statut}) : {corps}{suffixe}{complement}")


def multipart(champs):
    """champs : liste de (nom, valeur) ; valeur est un texte ou ("fichier", chemin)."""
    frontiere = "----elevenlabs" + uuid.uuid4().hex
    morceaux = []
    for nom, valeur in champs:
        morceaux.append(f"--{frontiere}\r\n".encode())
        if isinstance(valeur, tuple) and valeur[0] == "fichier":
            chemin = valeur[1]
            ext = os.path.splitext(chemin)[1].lower()
            nom_fichier = os.path.basename(chemin).replace('"', "_")
            morceaux.append((f'Content-Disposition: form-data; name="{nom}"; filename="{nom_fichier}"\r\n'
                             f"Content-Type: {TYPES_MIME.get(ext, 'application/octet-stream')}\r\n\r\n").encode())
            with open(chemin, "rb") as f:
                morceaux.append(f.read())
        else:
            morceaux.append(f'Content-Disposition: form-data; name="{nom}"\r\n\r\n'.encode())
            morceaux.append(str(valeur).encode("utf-8"))
        morceaux.append(b"\r\n")
    morceaux.append(f"--{frontiere}--\r\n".encode())
    return b"".join(morceaux), f"multipart/form-data; boundary={frontiere}"


# ---------------------------------------------------------------------------
# Audio : enveloppe WAV, analyse MP3 et WAV
# ---------------------------------------------------------------------------

def envelopper_pcm(octets, frequence, canaux=1, bits=16):
    """PCM brut (s16le, ce que renvoie l'API pour pcm_*) → fichier WAV."""
    if len(octets) % 2:
        octets = octets[:-1]
    bloc = canaux * bits // 8
    return (b"RIFF" + struct.pack("<I", 36 + len(octets)) + b"WAVE"
            + b"fmt " + struct.pack("<IHHIIHH", 16, 1, canaux, frequence, frequence * bloc, bloc, bits)
            + b"data" + struct.pack("<I", len(octets)) + octets)


def _niveaux_pcm16(donnees):
    nombre = len(donnees) // 2
    if not nombre:
        return None, None
    echantillons = struct.unpack(f"<{nombre}h", donnees[:nombre * 2])
    crete = max(abs(e) for e in echantillons)
    rms = math.sqrt(sum(e * e for e in echantillons) / nombre)

    def db(v):
        return round(20 * math.log10(v / 32768), 1) if v > 0 else None

    return db(crete), db(rms)


def analyser_wav(donnees):
    if len(donnees) < 12 or donnees[:4] != b"RIFF" or donnees[8:12] != b"WAVE":
        raise ValueError("en-tête WAV absent")
    pos, fmt, data = 12, None, None
    while pos + 8 <= len(donnees):
        ident, taille = struct.unpack("<4sI", donnees[pos:pos + 8])
        contenu = donnees[pos + 8:pos + 8 + taille]
        if ident == b"fmt ":
            fmt = struct.unpack("<HHIIHH", contenu[:16])
        elif ident == b"data":
            data = contenu
        pos += 8 + taille + (taille % 2)
    if not fmt or data is None:
        raise ValueError("bloc fmt ou data manquant")
    codage, canaux, frequence, octets_s, _, bits = fmt
    info = {"format": "wav", "frequence_hz": frequence, "canaux": canaux, "bits": bits,
            "duree_s": round(len(data) / octets_s, 3) if octets_s else None}
    if codage == 1 and bits == 16:
        info["crete_dbfs"], info["rms_dbfs"] = _niveaux_pcm16(data)
    return info


_DEBITS_MPEG1_L3 = (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320)
_DEBITS_MPEG2_L3 = (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160)
_FREQUENCES = {3: (44100, 48000, 32000), 2: (22050, 24000, 16000), 0: (11025, 12000, 8000)}


def analyser_mp3(donnees):
    pos = 0
    if donnees[:3] == b"ID3" and len(donnees) >= 10:
        taille = 0
        for octet in donnees[6:10]:
            taille = (taille << 7) | (octet & 0x7F)
        pos = 10 + taille
    trames, echantillons, frequence, canaux, debits = 0, 0, None, None, []
    while pos + 4 <= len(donnees):
        entete = struct.unpack(">I", donnees[pos:pos + 4])[0]
        version = (entete >> 19) & 3
        couche = (entete >> 17) & 3
        idx_debit = (entete >> 12) & 0xF
        idx_freq = (entete >> 10) & 3
        if (entete >> 21) != 0x7FF or version == 1 or couche != 1 or idx_debit in (0, 15) or idx_freq == 3:
            pos += 1
            continue
        debit = (_DEBITS_MPEG1_L3 if version == 3 else _DEBITS_MPEG2_L3)[idx_debit] * 1000
        freq = _FREQUENCES[version][idx_freq]
        par_trame = 1152 if version == 3 else 576
        longueur = (par_trame // 8) * debit // freq + ((entete >> 9) & 1)
        if longueur <= 4:
            pos += 1
            continue
        trames += 1
        echantillons += par_trame
        frequence = freq
        canaux = 1 if ((entete >> 6) & 3) == 3 else 2
        debits.append(debit)
        pos += longueur
    if not trames:
        raise ValueError("aucune trame MP3 reconnue")
    return {"format": "mp3", "frequence_hz": frequence, "canaux": canaux,
            "debit_kbps": round(sum(debits) / len(debits) / 1000),
            "duree_s": round(echantillons / frequence, 3)}


def analyser_audio(chemin):
    with open(chemin, "rb") as f:
        donnees = f.read()
    controle = {"taille_octets": len(donnees)}
    ext = os.path.splitext(chemin)[1].lower()
    try:
        if donnees[:4] == b"RIFF":
            controle.update(analyser_wav(donnees))
        elif ext == ".mp3" or donnees[:3] == b"ID3" or donnees[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
            controle.update(analyser_mp3(donnees))
        else:
            controle["format"] = ext.lstrip(".") or "inconnu"
    except ValueError as exc:
        controle["avertissement"] = f"fichier illisible comme {ext or 'audio'} : {exc}"
    return controle


def resume_controle(controle):
    morceaux = [_taille_lisible(controle.get("taille_octets", 0))]
    if controle.get("duree_s") is not None:
        morceaux.append(f"{controle['duree_s']:.2f} s")
    if controle.get("frequence_hz"):
        morceaux.append(f"{controle['frequence_hz']} Hz")
    if controle.get("canaux"):
        morceaux.append("mono" if controle["canaux"] == 1 else f"{controle['canaux']} canaux")
    if controle.get("debit_kbps"):
        morceaux.append(f"{controle['debit_kbps']} kb/s")
    if controle.get("crete_dbfs") is not None:
        morceaux.append(f"crête {controle['crete_dbfs']} dBFS, RMS {controle['rms_dbfs']} dBFS")
    texte = f"{controle.get('format', '?').upper()} : " + ", ".join(morceaux)
    if controle.get("avertissement"):
        texte += f" ⚠ {controle['avertissement']}"
    return texte


def _taille_lisible(octets):
    for unite in ("o", "Ko", "Mo", "Go"):
        if octets < 1024 or unite == "Go":
            return f"{octets:.0f} {unite}" if unite == "o" else f"{octets:.1f} {unite}"
        octets /= 1024


# ---------------------------------------------------------------------------
# Fiche .elevenlabs.json
# ---------------------------------------------------------------------------

def chemin_fiche(sortie):
    racine, ext = os.path.splitext(sortie.rstrip("/\\"))
    if os.path.isdir(sortie):
        racine = sortie.rstrip("/\\")
    return racine + ".elevenlabs.json"


def ecrire_fiche(sortie, fiche):
    chemin = chemin_fiche(sortie)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(masquer(json.dumps(fiche, ensure_ascii=False, indent=2)) + "\n")
    return chemin


def maintenant():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


def _sous(chemin, racine):
    try:
        return os.path.commonpath([chemin, racine]) == racine
    except ValueError:
        return False


def empreinte(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def entree_pour_fiche(chemin, sortie):
    """Fichier d'entrée relatif au dossier de la fiche ; hors du projet (dossier courant), seul son nom
    reste, avec l'empreinte SHA-256, pour ne pas exposer l'arborescence locale."""
    absolu = os.path.abspath(chemin)
    dossier = os.path.dirname(os.path.abspath(sortie.rstrip("/\\")))
    racine = os.getcwd()
    entree = {"taille_octets": os.path.getsize(chemin), "sha256": empreinte(chemin)}
    if _sous(absolu, racine) and _sous(dossier, racine):
        entree["fichier"] = os.path.relpath(absolu, dossier)
    else:
        entree["nom"] = os.path.basename(absolu)
    return entree


def relatif_a_fiche(chemin, sortie):
    dossier = os.path.dirname(os.path.abspath(chemin_fiche(sortie)))
    return os.path.relpath(os.path.abspath(chemin), dossier)


# ---------------------------------------------------------------------------
# Outils communs aux commandes
# ---------------------------------------------------------------------------

def base_api(args):
    return getattr(args, "api", None) or os.environ.get("ELEVENLABS_API_BASE") or API_BASE_DEFAUT


def _api(args):
    return Api(base_api(args), lire_cle())


def _verifier_sortie(sortie, ecraser, extensions=None):
    if extensions and not sortie.lower().endswith(tuple(extensions)):
        raise ErreurEleven(USAGE, f"--sortie doit finir par {' ou '.join(extensions)}.")
    if os.path.exists(sortie) and not ecraser:
        raise ErreurEleven(USAGE, f"{sortie} existe déjà. Choisis un autre nom ou ajoute --ecraser.")


def _ecrire_binaire(chemin, octets):
    dossier = os.path.dirname(os.path.abspath(chemin))
    os.makedirs(dossier, exist_ok=True)
    temporaire = chemin + ".partiel"
    with open(temporaire, "wb") as f:
        f.write(octets)
    os.replace(temporaire, chemin)


def _fichier_entree(chemin, extensions=EXTENSIONS_AUDIO):
    if not os.path.isfile(chemin):
        raise ErreurEleven(USAGE, f"Fichier introuvable : {chemin}")
    if extensions and not chemin.lower().endswith(extensions):
        raise ErreurEleven(USAGE, f"{chemin} : extension non prise en charge (attendu : {', '.join(extensions)}).")
    return chemin


def _valeur_param(valeur):
    try:
        return json.loads(valeur)
    except json.JSONDecodeError:
        return valeur


def _ajouter_params(corps, params):
    for brut in params or []:
        if "=" not in brut:
            raise ErreurEleven(USAGE, f"--param attend CLE=VALEUR, pas « {brut} ».")
        cle, valeur = brut.split("=", 1)
        cle = cle.strip()
        if cle in corps:
            raise ErreurEleven(USAGE, f"Le paramètre « {cle} » est déjà fixé par une option de la commande.")
        corps[cle] = _valeur_param(valeur)
    return corps


def _champs_params(champs, params):
    deja = {nom for nom, _ in champs}
    for brut in params or []:
        if "=" not in brut:
            raise ErreurEleven(USAGE, f"--param attend CLE=VALEUR, pas « {brut} ».")
        cle, valeur = brut.split("=", 1)
        if cle.strip() in deja:
            raise ErreurEleven(USAGE, f"Le paramètre « {cle.strip()} » est déjà fixé par une option de la commande.")
        champs.append((cle.strip(), valeur))
    return champs


def _sans_vides(dico):
    return {k: v for k, v in dico.items() if v is not None}


def _texte(args, attribut="texte", fichier="fichier_texte"):
    texte = getattr(args, attribut, None)
    chemin = getattr(args, fichier, None)
    if texte and chemin:
        raise ErreurEleven(USAGE, f"Donne le texte directement ou par --fichier-texte, pas les deux.")
    if chemin:
        with open(_fichier_entree(chemin, None), encoding="utf-8") as f:
            texte = f.read().strip()
    if not texte:
        raise ErreurEleven(USAGE, "Texte vide : donne-le en argument ou par --fichier-texte.")
    return texte


def format_sortie(sortie, format_demande, formats_wav=True):
    """Renvoie (output_format envoyé à l'API, fréquence à envelopper en WAV ou None)."""
    ext = os.path.splitext(sortie)[1].lower()
    if format_demande:
        codec = format_demande.split("_")[0]
        attendue = EXTENSION_PAR_CODEC.get(codec)
        if attendue is None:
            raise ErreurEleven(USAGE, f"Format inconnu : {format_demande}.")
        if codec == "pcm" and ext == ".wav":
            return format_demande, int(format_demande.split("_")[1])
        if codec == "wav" and not formats_wav:
            raise ErreurEleven(USAGE, (f"Cet endpoint n'a pas de format wav_* : demande pcm_{format_demande[4:]} "
                                       "avec une --sortie en .wav, le script l'enveloppe en WAV."))
        if ext != attendue:
            raise ErreurEleven(USAGE, f"--format {format_demande} produit un fichier {attendue}, pas {ext or 'sans extension'}.")
        return format_demande, None
    if ext not in FORMAT_PAR_EXTENSION:
        raise ErreurEleven(USAGE, f"--sortie doit finir par {', '.join(FORMAT_PAR_EXTENSION)} (ou passe --format).")
    fmt = FORMAT_PAR_EXTENSION[ext]
    return fmt, (int(fmt.split("_")[1]) if ext == ".wav" else None)


def resoudre_voix(api, valeur, cache=None):
    """Accepte un voice_id (20 caractères alphanumériques) ou le nom exact d'une voix du compte."""
    if RE_ID_VOIX.fullmatch(valeur):
        return valeur, None
    if cache is not None and valeur in cache:
        return cache[valeur]
    if api is None:
        return f"<voix:{valeur}>", valeur
    rep = api.appel("GET", "/v2/voices", params={"search": valeur, "page_size": 100}).json()
    cible = valeur.strip().lower()
    trouvees = []
    for voix in rep.get("voices", []):
        nom = str(voix.get("name", ""))
        if nom.lower() == cible or nom.lower().split(" - ")[0].strip() == cible:
            trouvees.append((voix.get("voice_id"), nom))
    if not trouvees:
        raise ErreurEleven(USAGE, (f"Aucune voix du compte ne s'appelle « {valeur} ». Liste les voix avec `voix`, "
                                   "ou passe directement un voice_id."))
    if len(trouvees) > 1:
        liste = ", ".join(f"{nom} ({vid})" for vid, nom in trouvees)
        raise ErreurEleven(USAGE, f"Plusieurs voix s'appellent « {valeur} » : {liste}. Passe le voice_id.")
    if cache is not None:
        cache[valeur] = trouvees[0]
    return trouvees[0]


def facteur_cout(modele):
    return 0.5 if ("flash" in modele or "turbo" in modele) else 1.0


def estimer_caracteres(texte, modele):
    facteur = facteur_cout(modele)
    return f"≈ {math.ceil(len(texte) * facteur)} crédits ({len(texte)} caractères × {facteur:g}, modèle {modele})"


def _a_blanc(methode, chemin, corps=None, params=None, estimation=None):
    cible = chemin + ("?" + urllib.parse.urlencode(params, doseq=True) if params else "")
    dire(f"À blanc : {methode} {cible}")
    if corps is not None:
        dire(json.dumps(corps, ensure_ascii=False, indent=2))
    if estimation:
        dire(f"Coût estimé : {estimation}")
    dire("Aucune requête envoyée, aucun crédit consommé.")
    return OK


def _reglages_voix(args, dialogue=False):
    if dialogue:
        reglages = _sans_vides({"stability": args.stabilite})
    else:
        reglages = _sans_vides({
            "stability": args.stabilite, "similarity_boost": args.similarite, "style": args.style,
            "speed": args.vitesse, "use_speaker_boost": False if args.sans_boost else None})
    for nom, valeur in reglages.items():
        if nom in ("stability", "similarity_boost") and not 0 <= valeur <= 1:
            raise ErreurEleven(USAGE, f"{nom} doit être entre 0 et 1.")
        if nom == "speed" and not 0.7 <= valeur <= 1.2:
            raise ErreurEleven(USAGE, "--vitesse doit être entre 0,7 et 1,2.")
    return reglages or None


def _meta_reponse(rep):
    meta = {}
    for entete, cle in (("request-id", "request_id"), ("history-item-id", "history_item_id"),
                        ("song-id", "song_id"), ("character-cost", "credits")):
        valeur = rep.entete(entete)
        if valeur:
            try:
                meta[cle] = int(valeur) if cle == "credits" else valeur
            except ValueError:
                meta[cle] = valeur
    return meta


def finaliser_audio(args, sortie, octets, wav_hz, fiche, rep=None, json_attendu=False):
    if rep is not None and not json_attendu:
        type_contenu = (rep.entete("Content-Type") or "").lower()
        if type_contenu.startswith("application/json"):
            raise ErreurEleven(ERREUR, f"L'API a renvoyé du JSON au lieu d'audio : {octets[:200]!r}")
    if wav_hz:
        octets = envelopper_pcm(octets, wav_hz)
    _ecrire_binaire(sortie, octets)
    controle = analyser_audio(sortie)
    if rep is not None:
        fiche.update(_meta_reponse(rep))
    fiche["sorties"] = [relatif_a_fiche(sortie, sortie)] + fiche.get("sorties", [])
    fiche["controle"] = controle
    chemin = ecrire_fiche(sortie, fiche)
    dire(f"✓ {sortie}")
    dire(f"  {resume_controle(controle)}")
    if fiche.get("credits") is not None:
        dire(f"  Crédits débités : {fiche['credits']}")
    if fiche.get("history_item_id"):
        dire(f"  history_item_id : {fiche['history_item_id']}")
    dire(f"  Fiche : {chemin}")
    if sortie.lower().endswith(GODOT_NE_LIT_PAS):
        dire(f"  ⚠ Godot n'importe pas les fichiers {os.path.splitext(sortie)[1]} : préfère .wav, .mp3 ou .ogg.")
    return controle


def fiche_de_base(operation, **champs):
    fiche = {"outil": "elevenlabs", "operation": operation, "date": maintenant()}
    fiche.update(_sans_vides(champs))
    return fiche


# ---------------------------------------------------------------------------
# Compte
# ---------------------------------------------------------------------------

SONDES_PERMISSIONS = (
    ("user_read", "GET", "/v1/user/subscription", {}, "solde et abonnement"),
    ("text_to_speech", "GET", "/v1/audio-effects/catalog", {}, "parole et dialogue"),
    ("voices_read", "GET", "/v2/voices", {"page_size": 1}, "liste des voix, voix par nom"),
    ("models_read", "GET", "/v1/models", {}, "liste des modèles"),
    ("speech_history_read", "GET", "/v1/history", {"page_size": 1}, "historique, reprise d'un audio"),
)


def _dire_abonnement(abo):
    utilises, limite = abo.get("character_count"), abo.get("character_limit")
    reste = limite - utilises if isinstance(utilises, int) and isinstance(limite, int) else "?"
    ligne = (f"✓ Clé acceptée. Offre {abo.get('tier')} ({abo.get('status')}) : "
             f"{utilises} crédits utilisés sur {limite}, reste {reste}.")
    remise = abo.get("next_character_count_reset_unix")
    if remise:
        date = datetime.datetime.fromtimestamp(remise, datetime.timezone.utc).date().isoformat()
        ligne += f" Remise à zéro le {date}."
    dire(ligne)
    if abo.get("tier") == "free":
        dire("  ⚠ Offre gratuite : l'audio produit n'est pas utilisable commercialement (voir le README).")


def cmd_verifier(args):
    premier_echec = None

    def echec(code):
        nonlocal premier_echec
        if premier_echec is None:
            premier_echec = code

    cle = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if cle:
        dire("✓ ELEVENLABS_API_KEY est définie (valeur masquée).")
    else:
        dire("✗ ELEVENLABS_API_KEY n'est pas définie : ajoute-la en secret de l'environnement, "
             "puis ouvre une nouvelle session.")
        echec(CLE)

    base = base_api(args)
    joignable = False
    try:
        statut, _, _ = requete("GET", base.rstrip("/") + "/", delai=15)
        dire(f"✓ {hote(base)} est joignable (HTTP {statut}).")
        joignable = True
    except ErreurEleven as exc:
        dire(f"✗ {hote(base)} : {exc.message}")
        echec(exc.code)

    if cle and joignable:
        api = Api(base, cle)
        manquantes, acceptee = [], False
        for permission, methode, chemin, params, usage in SONDES_PERMISSIONS:
            try:
                rep = api.appel(methode, chemin, params=params, delai=20)
            except ErreurEleven as exc:
                if exc.code == PERMISSION:
                    # Une permission refusée prouve que la clé elle-même est valide.
                    manquantes.append((permission, usage))
                    acceptee = True
                    continue
                dire(f"✗ {exc.message}")
                echec(exc.code)
                break
            acceptee = True
            if permission == "user_read":
                _dire_abonnement(rep.json())
        if acceptee:
            if "user_read" in {nom for nom, _ in manquantes}:
                dire("✓ Clé acceptée par l'API (solde illisible sans la permission user_read).")
            if manquantes:
                dire("⚠ Permissions absentes de la clé (à ajouter dans les réglages ElevenLabs si besoin) :")
                for permission, usage in manquantes:
                    dire(f"  - {permission} : {usage}")
            dire("  Les permissions de génération (bruitages, musique, transcription, isolation, changement "
                 "de voix, conception de voix) ne se testent pas sans payer : une permission manquante "
                 "sortira en code 6 à la première requête.")
    return premier_echec or OK


def cmd_modeles(args):
    modeles = _api(args).appel("GET", "/v1/models").json()
    for m in modeles:
        usages = [nom for cle, nom in (("can_do_text_to_speech", "parole"), ("can_do_voice_conversion", "changer-voix"))
                  if m.get(cle)]
        dire(f"{m.get('model_id')} — {m.get('name')} | {', '.join(usages) or '-'} | coût ×{m.get('token_cost_factor', '?')}"
             f" | {m.get('max_characters_request_subscribed_user', '?')} car. max | {len(m.get('languages') or [])} langues")
    return OK


def cmd_consommation(args):
    fin = int(time.time() * 1000)
    debut = fin - args.jours * 86400 * 1000
    rep = _api(args).appel("GET", "/v1/usage/character-stats",
                           params={"start_unix": debut, "end_unix": fin, "aggregation_interval": "day"}).json()
    jours = rep.get("time") or []
    series = rep.get("usage") or {}
    total = 0
    for nom, valeurs in series.items():
        somme = sum(v for v in valeurs if isinstance(v, (int, float)))
        total += somme
        dire(f"{nom} : {somme:g} crédits sur {args.jours} jours")
        for t, v in zip(jours, valeurs):
            if v:
                date = datetime.datetime.fromtimestamp(t / 1000, datetime.timezone.utc).date().isoformat()
                dire(f"  {date} : {v:g}")
    if len(series) > 1:
        dire(f"Total : {total:g}")
    if not series:
        dire("Aucune consommation sur la période.")
    return OK


def cmd_historique(args):
    params = _sans_vides({"page_size": args.limite, "voice_id": args.voix, "search": args.recherche})
    rep = _api(args).appel("GET", "/v1/history", params=params).json()
    elements = rep.get("history") or []
    for e in elements:
        date = datetime.datetime.fromtimestamp(e.get("date_unix", 0), datetime.timezone.utc).isoformat()
        avant, apres = e.get("character_count_change_from"), e.get("character_count_change_to")
        cout = apres - avant if isinstance(avant, int) and isinstance(apres, int) else "?"
        texte = (e.get("text") or "").replace("\n", " ")
        dire(f"{e.get('history_item_id')} | {date} | {e.get('voice_name')} | {e.get('model_id')} | "
             f"{cout} crédits | {texte[:70]}")
    if not elements:
        dire("Historique vide.")
    dire("Les bruitages et la musique n'apparaissent pas dans l'historique de l'API.")
    return OK


def cmd_recuperer(args):
    _verifier_sortie(args.sortie, args.ecraser, (".mp3",))
    api = _api(args)
    item = api.appel("GET", f"/v1/history/{args.history_item_id}").json()
    rep = api.appel("GET", f"/v1/history/{args.history_item_id}/audio", delai=args.delai)
    fiche = fiche_de_base(f"GET /v1/history/{args.history_item_id}/audio",
                          history_item_id=args.history_item_id, request_id=item.get("request_id"),
                          voix=_sans_vides({"id": item.get("voice_id"), "nom": item.get("voice_name")}),
                          modele=item.get("model_id"), texte=item.get("text"),
                          parametres=item.get("settings"), origine="historique")
    finaliser_audio(args, args.sortie, rep.corps, None, fiche, rep)
    return OK


# ---------------------------------------------------------------------------
# Voix
# ---------------------------------------------------------------------------

def _etiquettes(voix):
    labels = voix.get("labels") or {}
    return ", ".join(f"{k}={v}" for k, v in labels.items() if v)


def cmd_voix(args):
    params = _sans_vides({"search": args.recherche, "voice_type": args.type, "category": args.categorie,
                          "page_size": args.limite})
    rep = _api(args).appel("GET", "/v2/voices", params=params).json()
    for v in rep.get("voices", []):
        dire(f"{v.get('voice_id')} | {v.get('name')} | {v.get('category')} | {_etiquettes(v)}")
    if rep.get("has_more"):
        dire(f"… {rep.get('total_count', 'd’autres')} voix au total : affine avec --recherche ou augmente --limite.")
    return OK


def cmd_voix_info(args):
    api = _api(args)
    voice_id, _ = resoudre_voix(api, args.voix)
    v = api.appel("GET", f"/v1/voices/{voice_id}").json()
    resume = {cle: v.get(cle) for cle in ("voice_id", "name", "category", "description", "labels", "settings",
                                          "preview_url", "available_for_tiers", "high_quality_base_model_ids",
                                          "verified_languages") if v.get(cle) not in (None, [], {})}
    dire(json.dumps(resume, ensure_ascii=False, indent=2))
    return OK


def cmd_bibliotheque(args):
    params = _sans_vides({"search": args.recherche, "gender": args.genre, "age": args.age, "accent": args.accent,
                          "language": args.langue, "use_cases": args.usage, "category": args.categorie,
                          "page_size": args.limite})
    rep = _api(args).appel("GET", "/v1/shared-voices", params=params).json()
    for v in rep.get("voices", []):
        dire(f"{v.get('public_owner_id')} {v.get('voice_id')} | {v.get('name')} | {v.get('gender')}, {v.get('age')}, "
             f"{v.get('accent')}, {v.get('language')} | {v.get('use_case')} | {(v.get('description') or '')[:60]}")
    if rep.get("voices"):
        dire("Pour l'ajouter au compte : ajouter-voix <public_owner_id> <voice_id> --nom \"Nom\" "
             "(regarde d'abord sa notice : certaines voix de la bibliothèque ont un tarif propre).")
    else:
        dire("Aucune voix trouvée.")
    return OK


def cmd_ajouter_voix(args):
    chemin = f"/v1/voices/add/{args.public_owner_id}/{args.voice_id}"
    corps = {"new_name": args.nom}
    if args.a_blanc:
        return _a_blanc("POST", chemin, corps)
    rep = _api(args).appel("POST", chemin, json_corps=corps).json()
    dire(f"✓ Voix ajoutée au compte : {rep.get('voice_id')} ({args.nom}).")
    return OK


def _previsualiser(args, chemin, corps):
    _verifier_sortie(args.sortie, args.ecraser, (".mp3",))
    if args.a_blanc:
        return _a_blanc("POST", chemin, corps)
    rep = _api(args).appel("POST", chemin, json_corps=corps, delai=args.delai, payant=True)
    donnees = rep.json()
    racine, ext = os.path.splitext(args.sortie)
    apercus = []
    for i, apercu in enumerate(donnees.get("previews") or [], 1):
        fichier = f"{racine}_{i}{ext}"
        if os.path.exists(fichier) and not args.ecraser:
            raise ErreurEleven(USAGE, f"{fichier} existe déjà. Choisis un autre nom ou ajoute --ecraser.")
        _ecrire_binaire(fichier, base64.b64decode(apercu.get("audio_base_64") or ""))
        apercus.append({"fichier": relatif_a_fiche(fichier, args.sortie),
                        "generated_voice_id": apercu.get("generated_voice_id"),
                        "duree_s": apercu.get("duration_secs"), "langue": apercu.get("language")})
    if not apercus:
        raise ErreurEleven(ERREUR, "L'API n'a renvoyé aucun aperçu de voix.")
    fiche = fiche_de_base(f"POST {chemin}", description=corps.get("voice_description"),
                          modele=corps.get("model_id"), texte=donnees.get("text"),
                          parametres={k: v for k, v in corps.items() if k not in ("voice_description", "text")},
                          apercus=apercus, **_meta_reponse(rep))
    fiche_chemin = ecrire_fiche(args.sortie, fiche)
    for a in apercus:
        dire(f"✓ {a['fichier']} : generated_voice_id {a['generated_voice_id']} ({a.get('duree_s')} s)")
    dire(f"  Texte lu : {donnees.get('text', '')[:120]}")
    dire(f"  Fiche : {fiche_chemin}")
    dire("  Fais écouter les aperçus, puis garde le choisi : creer-voix <generated_voice_id> --nom … --description …")
    return OK


def _verifier_description(description, minimum):
    if not minimum <= len(description) <= 1000:
        raise ErreurEleven(USAGE, f"La description doit faire de {minimum} à 1 000 caractères ({len(description)}).")


def _corps_apercu(args, corps):
    if args.texte:
        if not 100 <= len(args.texte) <= 1000:
            raise ErreurEleven(USAGE, f"--texte doit faire de 100 à 1 000 caractères ({len(args.texte)}).")
        corps["text"] = args.texte
    else:
        corps["auto_generate_text"] = True
    corps.update(_sans_vides({"seed": args.graine, "loudness": args.volume, "guidance_scale": args.guidage}))
    return _ajouter_params(corps, args.param)


def cmd_concevoir_voix(args):
    _verifier_description(args.description, 20)
    corps = {"voice_description": args.description, "model_id": args.modele}
    if args.ameliorer:
        corps["should_enhance"] = True
    return _previsualiser(args, "/v1/text-to-voice/design", _corps_apercu(args, corps))


def cmd_remixer_voix(args):
    _verifier_description(args.description, 5)
    voice_id = args.voix if args.a_blanc else resoudre_voix(_api(args), args.voix)[0]
    corps = _corps_apercu(args, {"voice_description": args.description})
    return _previsualiser(args, f"/v1/text-to-voice/{voice_id}/remix", corps)


def cmd_creer_voix(args):
    _verifier_description(args.description, 20)
    corps = {"voice_name": args.nom, "voice_description": args.description,
             "generated_voice_id": args.generated_voice_id}
    etiquettes = {}
    for brut in args.etiquette or []:
        if "=" not in brut:
            raise ErreurEleven(USAGE, f"--etiquette attend CLE=VALEUR, pas « {brut} ».")
        cle, valeur = brut.split("=", 1)
        etiquettes[cle.strip()] = valeur.strip()
    if etiquettes:
        corps["labels"] = etiquettes
    if args.a_blanc:
        return _a_blanc("POST", "/v1/text-to-voice", corps)
    rep = _api(args).appel("POST", "/v1/text-to-voice", json_corps=corps).json()
    dire(f"✓ Voix créée : {rep.get('voice_id')} ({args.nom}). Note ce voice_id dans le casting du projet.")
    return OK


def cmd_cloner(args):
    if not args.consentement:
        raise ErreurEleven(USAGE, (
            "Le clonage exige --consentement : il confirme que la personne enregistrée a donné son accord écrit "
            "pour le clonage de sa voix et l'usage prévu. Sans cet accord, ne clone pas."))
    fichiers = [_fichier_entree(f) for f in args.fichiers]
    champs = [("name", args.nom)] + [("files", ("fichier", f)) for f in fichiers]
    if args.description:
        champs.append(("description", args.description))
    if args.debruiter:
        champs.append(("remove_background_noise", "true"))
    champs = _champs_params(champs, args.param)
    if args.a_blanc:
        return _a_blanc("POST", "/v1/voices/add", {n: (os.path.basename(v[1]) if isinstance(v, tuple) else v)
                                                    for n, v in champs})
    rep = _api(args).appel("POST", "/v1/voices/add", multipart=multipart(champs), delai=args.delai).json()
    dire(f"✓ Voix clonée : {rep.get('voice_id')} ({args.nom}).")
    if rep.get("requires_verification"):
        dire("  ⚠ ElevenLabs demande une vérification de cette voix avant usage.")
    return OK


# ---------------------------------------------------------------------------
# Générer
# ---------------------------------------------------------------------------

def _ecrire_alignement(sortie, alignement, texte, voice_segments=None):
    if not alignement:
        return None
    caracteres = alignement.get("characters") or []
    debuts = alignement.get("character_start_times_seconds") or []
    fins = alignement.get("character_end_times_seconds") or []
    mots, courant = [], None
    for c, d, f in zip(caracteres, debuts, fins):
        if c.isspace():
            if courant:
                mots.append(courant)
            courant = None
            continue
        if courant is None:
            courant = {"mot": c, "debut": d, "fin": f}
        else:
            courant["mot"] += c
            courant["fin"] = f
    if courant:
        mots.append(courant)
    racine, _ = os.path.splitext(sortie)
    chemin = racine + ".alignement.json"
    contenu = {"texte": texte, "mots": mots, "caracteres": alignement}
    if voice_segments:
        contenu["segments_voix"] = voice_segments
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(contenu, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return chemin


def _generer(args, chemin, corps, params, fiche, wav_hz, estimation=None, horodatage=False, texte=None):
    if args.a_blanc:
        return _a_blanc("POST", chemin, corps, params, estimation)
    if estimation:
        signaler(f"Coût estimé : {estimation}")
    rep = _api(args).appel("POST", chemin, json_corps=corps, params=params, delai=args.delai, payant=True)
    if horodatage:
        donnees = rep.json()
        octets = base64.b64decode(donnees.get("audio_base64") or "")
        alignement = _ecrire_alignement(args.sortie, donnees.get("alignment"), texte, donnees.get("voice_segments"))
        if alignement:
            fiche["sorties"] = [relatif_a_fiche(alignement, args.sortie)]
        finaliser_audio(args, args.sortie, octets, wav_hz, fiche, rep, json_attendu=True)
        if alignement:
            dire(f"  Alignement : {alignement}")
        return OK
    finaliser_audio(args, args.sortie, rep.corps, wav_hz, fiche, rep)
    return OK


def cmd_parole(args):
    texte = _texte(args)
    maximum = LONGUEUR_MAX_TEXTE.get(args.modele)
    if maximum and len(texte) > maximum:
        raise ErreurEleven(USAGE, (f"Texte de {len(texte)} caractères : {args.modele} en accepte {maximum} par "
                                   "requête. Découpe-le (avec --texte-avant et --texte-apres pour la continuité)."))
    _verifier_sortie(args.sortie, args.ecraser)
    fmt, wav_hz = format_sortie(args.sortie, args.format)
    voice_id, nom = resoudre_voix(None if args.a_blanc else _api(args), args.voix)
    corps = _sans_vides({"text": texte, "model_id": args.modele, "language_code": args.langue,
                         "voice_settings": _reglages_voix(args), "seed": args.graine,
                         "previous_text": args.texte_avant, "next_text": args.texte_apres,
                         "apply_text_normalization": args.normalisation})
    _ajouter_params(corps, args.param)
    chemin = f"/v1/text-to-speech/{voice_id}" + ("/with-timestamps" if args.horodatage else "")
    fiche = fiche_de_base(f"POST {chemin}", voix=_sans_vides({"id": voice_id, "nom": nom}), modele=args.modele,
                          texte=texte, format=fmt,
                          parametres={k: v for k, v in corps.items() if k not in ("text", "model_id")})
    return _generer(args, chemin, corps, {"output_format": fmt}, fiche, wav_hz,
                    estimer_caracteres(texte, args.modele), args.horodatage, texte)


def _lire_script(chemin):
    with open(_fichier_entree(chemin, (".json",)), encoding="utf-8") as f:
        try:
            lignes = json.load(f)
        except json.JSONDecodeError as exc:
            raise ErreurEleven(USAGE, f"{chemin} n'est pas un JSON valide : {exc}") from None
    if isinstance(lignes, dict):
        lignes = lignes.get("repliques") or lignes.get("inputs") or []
    repliques = []
    for ligne in lignes:
        voix = ligne.get("voix") or ligne.get("voice_id") if isinstance(ligne, dict) else None
        texte = ligne.get("texte") or ligne.get("text") if isinstance(ligne, dict) else None
        if not voix or not texte:
            raise ErreurEleven(USAGE, f"{chemin} : chaque réplique doit avoir « voix » et « texte ».")
        repliques.append((voix, texte))
    return repliques


def cmd_dialogue(args):
    repliques = []
    for brut in args.replique or []:
        if "=" not in brut:
            raise ErreurEleven(USAGE, f"--replique attend VOIX=TEXTE, pas « {brut} ».")
        voix, texte = brut.split("=", 1)
        repliques.append((voix.strip(), texte.strip()))
    if args.script:
        repliques += _lire_script(args.script)
    if not repliques:
        raise ErreurEleven(USAGE, "Aucune réplique : passe --replique VOIX=TEXTE (répétable) ou --script.")
    _verifier_sortie(args.sortie, args.ecraser)
    fmt, wav_hz = format_sortie(args.sortie, args.format)
    api = None if args.a_blanc else _api(args)
    cache, entrees, voix = {}, [], {}
    for v, texte in repliques:
        voice_id, nom = resoudre_voix(api, v, cache)
        voix[voice_id] = nom or v
        entrees.append({"text": texte, "voice_id": voice_id})
    if len(voix) > VOIX_MAX_DIALOGUE:
        raise ErreurEleven(USAGE, f"{len(voix)} voix différentes : l'API en accepte {VOIX_MAX_DIALOGUE} par dialogue.")
    total = "".join(e["text"] for e in entrees)
    if len(total) > CARACTERES_DIALOGUE_FIABLES:
        signaler(f"⚠ {len(total)} caractères : au-delà de {CARACTERES_DIALOGUE_FIABLES}, l'API peut couper le "
                 "dialogue ou le refuser. Découpe-le en scènes.")
    corps = _sans_vides({"inputs": entrees, "model_id": args.modele, "language_code": args.langue,
                         "settings": _reglages_voix(args, dialogue=True), "seed": args.graine})
    _ajouter_params(corps, args.param)
    chemin = "/v1/text-to-dialogue" + ("/with-timestamps" if args.horodatage else "")
    fiche = fiche_de_base(f"POST {chemin}", modele=args.modele, format=fmt,
                          voix=[{"id": i, "nom": n} for i, n in voix.items()], repliques=entrees,
                          parametres={k: v for k, v in corps.items() if k not in ("inputs", "model_id")})
    return _generer(args, chemin, corps, {"output_format": fmt}, fiche, wav_hz,
                    estimer_caracteres(total, args.modele), args.horodatage, "\n".join(e["text"] for e in entrees))


def cmd_bruitage(args):
    if args.duree is not None and not 0.5 <= args.duree <= 30:
        raise ErreurEleven(USAGE, "--duree doit être entre 0,5 et 30 secondes.")
    if args.influence is not None and not 0 <= args.influence <= 1:
        raise ErreurEleven(USAGE, "--influence doit être entre 0 et 1.")
    _verifier_sortie(args.sortie, args.ecraser)
    fmt, wav_hz = format_sortie(args.sortie, args.format)
    corps = _sans_vides({"text": args.prompt, "model_id": args.modele, "duration_seconds": args.duree,
                         "prompt_influence": args.influence, "loop": True if args.boucle else None})
    _ajouter_params(corps, args.param)
    fiche = fiche_de_base("POST /v1/sound-generation", prompt=args.prompt, modele=args.modele, format=fmt,
                          parametres={k: v for k, v in corps.items() if k not in ("text", "model_id")})
    code = _generer(args, "/v1/sound-generation", corps, {"output_format": fmt}, fiche, wav_hz)
    if not args.a_blanc and args.duree:
        duree = fiche.get("controle", {}).get("duree_s")
        if duree and abs(duree - args.duree) > max(0.25, args.duree * 0.1):
            dire(f"  ⚠ Durée obtenue {duree:.2f} s pour {args.duree:g} s demandées.")
    return code


def cmd_musique(args):
    if bool(args.prompt) == bool(args.plan):
        raise ErreurEleven(USAGE, "Donne soit un prompt, soit --plan (plan de composition JSON), pas les deux.")
    if args.duree is not None and not 3 <= args.duree <= 600:
        raise ErreurEleven(USAGE, "--duree doit être entre 3 et 600 secondes.")
    if args.plan and args.duree is not None:
        raise ErreurEleven(USAGE, "--duree ne s'applique qu'à un prompt : avec --plan, les sections fixent la durée.")
    _verifier_sortie(args.sortie, args.ecraser)
    fmt, wav_hz = format_sortie(args.sortie, args.format, formats_wav=False)
    corps = {"model_id": args.modele}
    if args.plan:
        with open(_fichier_entree(args.plan, (".json",)), encoding="utf-8") as f:
            plan = json.load(f)
        corps["composition_plan"] = plan.get("composition_plan", plan) if isinstance(plan, dict) else plan
    else:
        corps["prompt"] = args.prompt
        corps.update(_sans_vides({"music_length_ms": int(args.duree * 1000) if args.duree else None,
                                  "force_instrumental": True if args.instrumental else None}))
    corps.update(_sans_vides({"seed": args.graine}))
    _ajouter_params(corps, args.param)
    fiche = fiche_de_base("POST /v1/music", prompt=args.prompt, modele=args.modele, format=fmt,
                          plan=entree_pour_fiche(args.plan, args.sortie) if args.plan else None,
                          parametres={k: v for k, v in corps.items() if k not in ("prompt", "model_id")})
    return _generer(args, "/v1/music", corps, {"output_format": fmt}, fiche, wav_hz)


def cmd_plan_musique(args):
    _verifier_sortie(args.sortie, args.ecraser, (".json",))
    if args.duree is not None and not 3 <= args.duree <= 600:
        raise ErreurEleven(USAGE, "--duree doit être entre 3 et 600 secondes.")
    corps = _sans_vides({"prompt": args.prompt, "model_id": args.modele,
                         "music_length_ms": int(args.duree * 1000) if args.duree else None})
    _ajouter_params(corps, args.param)
    if args.a_blanc:
        return _a_blanc("POST", "/v1/music/plan", corps)
    plan = _api(args).appel("POST", "/v1/music/plan", json_corps=corps, delai=args.delai).json()
    os.makedirs(os.path.dirname(os.path.abspath(args.sortie)), exist_ok=True)
    with open(args.sortie, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
        f.write("\n")
    sections = plan.get("sections") or []
    duree = sum(s.get("duration_ms", 0) for s in sections) / 1000
    dire(f"✓ {args.sortie} : {len(sections)} sections, {duree:g} s")
    for s in sections:
        dire(f"  - {s.get('section_name')} ({s.get('duration_ms', 0) / 1000:g} s) : "
             f"{', '.join(s.get('positive_local_styles') or [])}")
    dire("  Relis ou modifie le plan, puis : musique --plan " + shlex.quote(args.sortie) + " --sortie …")
    return OK


# ---------------------------------------------------------------------------
# Traitement
# ---------------------------------------------------------------------------

def cmd_changer_voix(args):
    entree = _fichier_entree(args.entree)
    _verifier_sortie(args.sortie, args.ecraser)
    fmt, wav_hz = format_sortie(args.sortie, args.format)
    voice_id, nom = resoudre_voix(None if args.a_blanc else _api(args), args.voix)
    champs = [("audio", ("fichier", entree)), ("model_id", args.modele)]
    reglages = _reglages_voix(args)
    if reglages:
        champs.append(("voice_settings", json.dumps(reglages)))
    if args.graine is not None:
        champs.append(("seed", str(args.graine)))
    if args.debruiter:
        champs.append(("remove_background_noise", "true"))
    champs = _champs_params(champs, args.param)
    chemin = f"/v1/voice-changer/{voice_id}"
    if args.a_blanc:
        return _a_blanc("POST", chemin, {n: (os.path.basename(v[1]) if isinstance(v, tuple) else v) for n, v in champs},
                        {"output_format": fmt})
    rep = _api(args).appel("POST", chemin, multipart=multipart(champs), params={"output_format": fmt},
                           delai=args.delai, payant=True)
    fiche = fiche_de_base(f"POST {chemin}", voix=_sans_vides({"id": voice_id, "nom": nom}), modele=args.modele,
                          format=fmt, entree=entree_pour_fiche(entree, args.sortie),
                          parametres={n: v for n, v in champs if n not in ("audio", "model_id")})
    finaliser_audio(args, args.sortie, rep.corps, wav_hz, fiche, rep)
    return OK


def cmd_isoler(args):
    entree = _fichier_entree(args.entree)
    _verifier_sortie(args.sortie, args.ecraser, (".mp3",))
    champs = _champs_params([("audio", ("fichier", entree))], args.param)
    if args.a_blanc:
        return _a_blanc("POST", "/v1/audio-isolation", {"audio": os.path.basename(entree)})
    rep = _api(args).appel("POST", "/v1/audio-isolation", multipart=multipart(champs), delai=args.delai, payant=True)
    fiche = fiche_de_base("POST /v1/audio-isolation", entree=entree_pour_fiche(entree, args.sortie))
    finaliser_audio(args, args.sortie, rep.corps, None, fiche, rep)
    return OK


def cmd_separer_pistes(args):
    entree = _fichier_entree(args.entree)
    dossier = args.sortie.rstrip("/\\")
    if os.path.exists(dossier) and os.listdir(dossier) and not args.ecraser:
        raise ErreurEleven(USAGE, f"{dossier} existe et n'est pas vide. Choisis un autre dossier ou ajoute --ecraser.")
    fmt = args.format or "mp3_44100_128"
    if fmt.startswith("wav"):
        raise ErreurEleven(USAGE, "La séparation n'a pas de format wav_* : utilise mp3_44100_128 ou pcm_44100.")
    variante = "two_stems_v1" if args.deux_pistes else "six_stems_v1"
    champs = _champs_params([("file", ("fichier", entree)), ("stem_variation_id", variante)], args.param)
    if args.a_blanc:
        return _a_blanc("POST", "/v1/music/stem-separation", {"file": os.path.basename(entree),
                                                              "stem_variation_id": variante}, {"output_format": fmt})
    rep = _api(args).appel("POST", "/v1/music/stem-separation", multipart=multipart(champs),
                           params={"output_format": fmt}, delai=args.delai, payant=True)
    try:
        archive = zipfile.ZipFile(io.BytesIO(rep.corps))
    except zipfile.BadZipFile:
        raise ErreurEleven(ERREUR, "La réponse de la séparation n'est pas une archive ZIP lisible.") from None
    os.makedirs(dossier, exist_ok=True)
    pistes = []
    for membre in archive.infolist():
        if membre.is_dir():
            continue
        nom = os.path.basename(membre.filename)
        if not nom or nom.startswith("."):
            continue
        octets = archive.read(membre)
        if fmt.startswith("pcm") and not nom.lower().endswith(".wav"):
            octets = envelopper_pcm(octets, int(fmt.split("_")[1]))
            nom = os.path.splitext(nom)[0] + ".wav"
        destination = os.path.join(dossier, nom)
        _ecrire_binaire(destination, octets)
        controle = analyser_audio(destination)
        pistes.append({"fichier": relatif_a_fiche(destination, dossier), "controle": controle})
        dire(f"✓ {destination} — {resume_controle(controle)}")
    fiche = fiche_de_base("POST /v1/music/stem-separation", entree=entree_pour_fiche(entree, dossier),
                          format=fmt, parametres={"stem_variation_id": variante}, pistes=pistes,
                          **_meta_reponse(rep))
    dire(f"  Fiche : {ecrire_fiche(dossier, fiche)}")
    return OK


def cmd_transcrire(args):
    _verifier_sortie(args.sortie, args.ecraser, (".json",))
    champs = [("model_id", args.modele)]
    if re.match(r"https?://", args.entree):
        champs.append(("source_url", args.entree))
        entree_fiche = {"url": args.entree}
    else:
        entree = _fichier_entree(args.entree)
        champs.append(("file", ("fichier", entree)))
        entree_fiche = entree_pour_fiche(entree, args.sortie)
    if args.langue:
        champs.append(("language_code", args.langue))
    if args.locuteurs:
        champs += [("diarize", "true"), ("num_speakers", str(args.locuteurs))]
    if args.sans_evenements:
        champs.append(("tag_audio_events", "false"))
    if args.srt:
        champs.append(("additional_formats", json.dumps([{"format": "srt"}])))
    for terme in args.terme or []:
        champs.append(("keyterms", terme))
    champs = _champs_params(champs, args.param)
    if args.a_blanc:
        return _a_blanc("POST", "/v1/speech-to-text", {n: (os.path.basename(v[1]) if isinstance(v, tuple) else v)
                                                        for n, v in champs})
    rep = _api(args).appel("POST", "/v1/speech-to-text", multipart=multipart(champs), delai=args.delai, payant=True)
    donnees = rep.json()
    os.makedirs(os.path.dirname(os.path.abspath(args.sortie)), exist_ok=True)
    sorties = []
    for extra in donnees.get("additional_formats") or []:
        if not isinstance(extra, dict) or not extra.get("content"):
            continue
        fichier = os.path.splitext(args.sortie)[0] + "." + (extra.get("file_extension") or "txt").lstrip(".")
        contenu = extra["content"]
        octets = base64.b64decode(contenu) if extra.get("is_base64_encoded") else contenu.encode("utf-8")
        _ecrire_binaire(fichier, octets)
        sorties.append(relatif_a_fiche(fichier, args.sortie))
        extra["content"] = f"(écrit dans {os.path.basename(fichier)})"
    with open(args.sortie, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)
        f.write("\n")
    fiche = fiche_de_base("POST /v1/speech-to-text", modele=args.modele, entree=entree_fiche,
                          parametres={n: v for n, v in champs if n not in ("file", "model_id", "source_url")},
                          sorties=[relatif_a_fiche(args.sortie, args.sortie)] + sorties,
                          langue=donnees.get("language_code"), duree_s=donnees.get("audio_duration_secs"),
                          **_meta_reponse(rep))
    texte = donnees.get("text") or ""
    dire(f"✓ {args.sortie} ({donnees.get('language_code')}, {len(donnees.get('words') or [])} mots)")
    for s in sorties:
        dire(f"✓ {s}")
    dire(f"  Fiche : {ecrire_fiche(args.sortie, fiche)}")
    dire(f"  {texte[:500]}{'…' if len(texte) > 500 else ''}")
    return OK


def cmd_aligner(args):
    entree = _fichier_entree(args.audio)
    texte = _texte(args)
    _verifier_sortie(args.sortie, args.ecraser, (".json",))
    champs = _champs_params([("file", ("fichier", entree)), ("text", texte)], args.param)
    if args.a_blanc:
        return _a_blanc("POST", "/v1/forced-alignment", {"file": os.path.basename(entree), "text": texte})
    rep = _api(args).appel("POST", "/v1/forced-alignment", multipart=multipart(champs), delai=args.delai, payant=True)
    donnees = rep.json()
    os.makedirs(os.path.dirname(os.path.abspath(args.sortie)), exist_ok=True)
    with open(args.sortie, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)
        f.write("\n")
    fiche = fiche_de_base("POST /v1/forced-alignment", texte=texte, entree=entree_pour_fiche(entree, args.sortie),
                          sorties=[relatif_a_fiche(args.sortie, args.sortie)], **_meta_reponse(rep))
    mots = donnees.get("words") or []
    dire(f"✓ {args.sortie} : {len(mots)} mots alignés (perte {donnees.get('loss')})")
    if mots:
        dire(f"  du premier mot à {mots[0].get('start')} s au dernier à {mots[-1].get('end')} s")
    dire(f"  Fiche : {ecrire_fiche(args.sortie, fiche)}")
    return OK


# ---------------------------------------------------------------------------
# Divers
# ---------------------------------------------------------------------------

def cmd_brut(args):
    methode = args.methode.upper()
    if not args.chemin.startswith("/"):
        raise ErreurEleven(USAGE, "Le chemin doit commencer par / (ex. /v1/user).")
    corps = None
    if args.corps:
        source = args.corps
        if source.startswith("@"):
            with open(source[1:], encoding="utf-8") as f:
                source = f.read()
        try:
            corps = json.loads(source)
        except json.JSONDecodeError as exc:
            raise ErreurEleven(USAGE, f"--corps n'est pas un JSON valide : {exc}") from None
    params = {}
    for brut in args.requete or []:
        if "=" not in brut:
            raise ErreurEleven(USAGE, f"--requete attend CLE=VALEUR, pas « {brut} ».")
        cle, valeur = brut.split("=", 1)
        params.setdefault(cle, []).append(valeur)
    if args.sortie:
        _verifier_sortie(args.sortie, args.ecraser)
    if args.a_blanc:
        return _a_blanc(methode, args.chemin, corps, params)
    rep = _api(args).appel(methode, args.chemin, json_corps=corps, params=params, delai=args.delai,
                           payant=methode != "GET")
    type_contenu = (rep.entete("Content-Type") or "").lower()
    if args.sortie:
        _ecrire_binaire(args.sortie, rep.corps)
        dire(f"✓ {args.sortie} ({_taille_lisible(len(rep.corps))}, {type_contenu or 'type inconnu'})")
        if type_contenu.startswith("audio/"):
            dire(f"  {resume_controle(analyser_audio(args.sortie))}")
    elif type_contenu.startswith("application/json") or not rep.corps:
        dire(json.dumps(rep.json(), ensure_ascii=False, indent=2))
    else:
        raise ErreurEleven(USAGE, f"Réponse binaire ({type_contenu}, {len(rep.corps)} octets) : relance avec --sortie.")
    meta = _meta_reponse(rep)
    if meta.get("credits") is not None:
        dire(f"  Crédits débités : {meta['credits']}")
    return OK


def cmd_inspecter(args):
    _fichier_entree(args.fichier, None)
    controle = analyser_audio(args.fichier)
    dire(resume_controle(controle))
    dire(json.dumps(controle, ensure_ascii=False, indent=2))
    return OK


# ---------------------------------------------------------------------------
# Ligne de commande
# ---------------------------------------------------------------------------

def analyseur():
    p = argparse.ArgumentParser(prog="elevenlabs.py", description="Client de l'API ElevenLabs (voir SKILL.md).")
    p.add_argument("--api", help="URL de base de l'API (défaut : ELEVENLABS_API_BASE ou https://api.elevenlabs.io)")
    sous = p.add_subparsers(dest="commande", required=True, metavar="commande")

    def commande(nom, fonction, aide, sortie=None, generation=False, delai=120):
        sp = sous.add_parser(nom, help=aide, description=aide)
        sp.set_defaults(fonction=fonction)
        sp.add_argument("--api", help=argparse.SUPPRESS, default=argparse.SUPPRESS)
        if sortie:
            sp.add_argument("--sortie", required=True, help=sortie)
            sp.add_argument("--ecraser", action="store_true", help="remplacer un fichier existant")
        if generation:
            sp.add_argument("--a-blanc", action="store_true", help="afficher la requête sans l'envoyer")
            sp.add_argument("--param", action="append", metavar="CLE=VALEUR",
                            help="champ de l'API sans option dédiée (valeur JSON, sinon texte) ; répétable")
            sp.add_argument("--delai", type=float, default=delai, help=f"délai de réponse en secondes ({delai:g})")
        return sp

    def format_audio(sp):
        sp.add_argument("--format", help="output_format de l'API (défaut : selon l'extension de --sortie, "
                                         ".mp3 → mp3_44100_128, .wav → pcm_44100 enveloppé en WAV)")

    def reglages(sp, complet=True):
        sp.add_argument("--stabilite", type=float, help="stabilité 0–1 (bas : plus expressif, plus variable)")
        if complet:
            sp.add_argument("--similarite", type=float, help="fidélité à la voix 0–1")
            sp.add_argument("--style", type=float, help="exagération du style 0–1 (coûte en latence et stabilité)")
            sp.add_argument("--vitesse", type=float, help="vitesse 0,7–1,2")
            sp.add_argument("--sans-boost", action="store_true", help="désactiver use_speaker_boost")
        sp.add_argument("--graine", type=int, help="graine, pour refaire un résultat proche")

    # Compte
    commande("verifier", cmd_verifier, "vérifier la clé, l'accès réseau, le solde et les permissions de la clé")
    commande("modeles", cmd_modeles, "lister les modèles et leur coût relatif")
    sp = commande("consommation", cmd_consommation, "crédits consommés par jour")
    sp.add_argument("--jours", type=int, default=30)
    sp = commande("historique", cmd_historique, "dernières générations de parole (gratuit)")
    sp.add_argument("--limite", type=int, default=20)
    sp.add_argument("--voix", help="voice_id")
    sp.add_argument("--recherche")
    sp = commande("recuperer", cmd_recuperer, "retélécharger l'audio d'un élément de l'historique (gratuit)",
                  sortie="fichier .mp3 à écrire", delai=120)
    sp.add_argument("history_item_id")
    sp.add_argument("--delai", type=float, default=120)

    # Voix
    sp = commande("voix", cmd_voix, "lister les voix du compte")
    sp.add_argument("--recherche")
    sp.add_argument("--type", help="personal, community, default, workspace, non-default, saved")
    sp.add_argument("--categorie", help="premade, cloned, generated, professional")
    sp.add_argument("--limite", type=int, default=30)
    sp = commande("voix-info", cmd_voix_info, "détails d'une voix (réglages, étiquettes, aperçu)")
    sp.add_argument("voix", help="voice_id ou nom exact")
    sp = commande("bibliotheque", cmd_bibliotheque, "chercher dans la bibliothèque de voix partagées")
    sp.add_argument("--recherche")
    sp.add_argument("--genre", help="male, female, neutral")
    sp.add_argument("--age", help="young, middle_aged, old")
    sp.add_argument("--accent")
    sp.add_argument("--langue", help="code ISO 639-1, ex. fr")
    sp.add_argument("--usage", action="append", help="characters_animation, narrative_story, conversational…")
    sp.add_argument("--categorie", choices=("professional", "famous", "high_quality"))
    sp.add_argument("--limite", type=int, default=20)
    sp = commande("ajouter-voix", cmd_ajouter_voix, "ajouter au compte une voix de la bibliothèque", generation=True)
    sp.add_argument("public_owner_id")
    sp.add_argument("voice_id")
    sp.add_argument("--nom", required=True)

    for nom, fonction, aide in (
            ("concevoir-voix", cmd_concevoir_voix, "créer des aperçus de voix depuis une description"),
            ("remixer-voix", cmd_remixer_voix, "créer des aperçus de variantes d'une voix existante")):
        sp = commande(nom, fonction, aide, sortie="base des aperçus .mp3 (écrits en <base>_1.mp3, _2…)",
                      generation=True, delai=180)
        if nom == "remixer-voix":
            sp.add_argument("voix", help="voice_id ou nom exact de la voix à remixer")
            sp.add_argument("description", help="changements voulus, 5 à 1 000 caractères")
        else:
            sp.add_argument("description", help="description de la voix, 20 à 1 000 caractères")
            sp.add_argument("--modele", default=MODELE_CONCEPTION_DEFAUT, choices=MODELES_CONCEPTION)
            sp.add_argument("--ameliorer", action="store_true", help="laisser l'IA enrichir la description")
        sp.add_argument("--texte", help="texte lu par les aperçus, 100 à 1 000 caractères (sinon généré)")
        sp.add_argument("--graine", type=int)
        sp.add_argument("--volume", type=float, help="loudness -1–1 (0 ≈ -24 LUFS)")
        sp.add_argument("--guidage", type=float, help="guidance_scale : fidélité à la description")
    sp = commande("creer-voix", cmd_creer_voix, "garder un aperçu comme voix du compte", generation=True)
    sp.add_argument("generated_voice_id")
    sp.add_argument("--nom", required=True)
    sp.add_argument("--description", required=True, help="20 à 1 000 caractères")
    sp.add_argument("--etiquette", action="append", metavar="CLE=VALEUR", help="étiquette (language, gender, age…)")
    sp = commande("cloner", cmd_cloner, "cloner une voix (clonage instantané) depuis des enregistrements",
                  generation=True, delai=180)
    sp.add_argument("fichiers", nargs="+", help="enregistrements de la voix")
    sp.add_argument("--nom", required=True)
    sp.add_argument("--description")
    sp.add_argument("--debruiter", action="store_true", help="retirer le bruit de fond des échantillons")
    sp.add_argument("--consentement", action="store_true",
                    help="confirme l'accord écrit de la personne enregistrée (obligatoire)")

    # Générer
    sp = commande("parole", cmd_parole, "synthèse vocale d'une réplique",
                  sortie="fichier audio (.mp3 ou .wav)", generation=True)
    sp.add_argument("voix", help="voice_id ou nom exact d'une voix du compte")
    sp.add_argument("texte", nargs="?")
    sp.add_argument("--fichier-texte")
    sp.add_argument("--modele", default=MODELE_PAROLE_DEFAUT,
                    help=f"{MODELE_PAROLE_DEFAUT} (défaut), eleven_v3 (expressif, balises [whispers]…), "
                         "eleven_flash_v2_5 (moitié prix)")
    sp.add_argument("--langue", help="code ISO 639-1 imposé, ex. fr")
    reglages(sp)
    sp.add_argument("--texte-avant", help="texte qui précède, pour la continuité de l'intonation")
    sp.add_argument("--texte-apres", help="texte qui suit")
    sp.add_argument("--normalisation", choices=("auto", "on", "off"))
    sp.add_argument("--horodatage", action="store_true", help="écrire aussi <nom>.alignement.json (mots et temps)")
    format_audio(sp)

    sp = commande("dialogue", cmd_dialogue, "dialogue à plusieurs voix en un seul fichier",
                  sortie="fichier audio (.mp3 ou .wav)", generation=True, delai=300)
    sp.add_argument("--replique", action="append", metavar="VOIX=TEXTE", help="réplique, dans l'ordre ; répétable")
    sp.add_argument("--script", help="JSON : liste de {\"voix\": …, \"texte\": …}")
    sp.add_argument("--modele", default=MODELE_DIALOGUE_DEFAUT)
    sp.add_argument("--langue")
    reglages(sp, complet=False)
    sp.add_argument("--horodatage", action="store_true", help="écrire aussi <nom>.alignement.json")
    format_audio(sp)

    sp = commande("bruitage", cmd_bruitage, "effet sonore depuis une description",
                  sortie="fichier audio (.wav conseillé pour Godot, ou .mp3)", generation=True)
    sp.add_argument("prompt", help="description du son, en anglais de préférence")
    sp.add_argument("--duree", type=float, help="durée en secondes, 0,5 à 30 (sinon choisie par le modèle)")
    sp.add_argument("--boucle", action="store_true", help="son qui boucle sans raccord audible")
    sp.add_argument("--influence", type=float, help="prompt_influence 0–1 (0,3 par défaut côté API)")
    sp.add_argument("--modele", default=MODELE_BRUITAGE_DEFAUT, choices=MODELES_BRUITAGE)
    format_audio(sp)

    sp = commande("musique", cmd_musique, "morceau de musique depuis un prompt ou un plan de composition",
                  sortie="fichier audio (.mp3 ou .wav)", generation=True, delai=600)
    sp.add_argument("prompt", nargs="?")
    sp.add_argument("--plan", help="plan de composition JSON (sortie de plan-musique, éventuellement retouchée)")
    sp.add_argument("--duree", type=float, help="durée en secondes, 3 à 600 (avec un prompt)")
    sp.add_argument("--instrumental", action="store_true", help="garantir un morceau sans voix")
    sp.add_argument("--modele", default=MODELE_MUSIQUE_DEFAUT, choices=MODELES_MUSIQUE)
    sp.add_argument("--graine", type=int)
    format_audio(sp)

    sp = commande("plan-musique", cmd_plan_musique, "plan de composition (sections, styles) à relire avant musique",
                  sortie="fichier .json", generation=True)
    sp.add_argument("prompt")
    sp.add_argument("--duree", type=float, help="durée en secondes, 3 à 600")
    sp.add_argument("--modele", default=MODELE_MUSIQUE_DEFAUT, choices=MODELES_MUSIQUE)

    # Traitement
    sp = commande("changer-voix", cmd_changer_voix, "rejouer un enregistrement avec une autre voix",
                  sortie="fichier audio (.mp3 ou .wav)", generation=True, delai=300)
    sp.add_argument("entree", help="enregistrement source")
    sp.add_argument("voix", help="voice_id ou nom exact de la voix cible")
    sp.add_argument("--modele", default=MODELE_CHANGEUR_DEFAUT)
    sp.add_argument("--debruiter", action="store_true", help="retirer le bruit de fond de la source")
    reglages(sp)
    format_audio(sp)

    sp = commande("isoler", cmd_isoler, "isoler la voix d'un enregistrement (retirer bruit et musique)",
                  sortie="fichier .mp3", generation=True, delai=300)
    sp.add_argument("entree")

    sp = commande("separer-pistes", cmd_separer_pistes, "séparer un morceau en pistes (voix, batterie, basse…)",
                  sortie="dossier où écrire les pistes", generation=True, delai=600)
    sp.add_argument("entree")
    sp.add_argument("--deux-pistes", action="store_true", help="voix et accompagnement seulement")
    sp.add_argument("--format", help="mp3_44100_128 (défaut) ou pcm_44100 (pistes écrites en WAV)")

    sp = commande("transcrire", cmd_transcrire, "transcrire un audio ou une vidéo (sous-titres avec --srt)",
                  sortie="fichier .json", generation=True, delai=600)
    sp.add_argument("entree", help="fichier local ou URL")
    sp.add_argument("--modele", default=MODELE_TRANSCRIPTION_DEFAUT)
    sp.add_argument("--langue", help="code ISO 639-1 ou 639-3")
    sp.add_argument("--locuteurs", type=int, help="nombre maximal de locuteurs (active la diarisation)")
    sp.add_argument("--sans-evenements", action="store_true", help="ne pas noter (rires), (pas)…")
    sp.add_argument("--srt", action="store_true", help="écrire aussi <nom>.srt")
    sp.add_argument("--terme", action="append", help="mot ou nom propre à privilégier ; répétable")

    sp = commande("aligner", cmd_aligner, "temps de chaque mot d'un texte dans un audio (sous-titres, lip sync)",
                  sortie="fichier .json", generation=True, delai=300)
    sp.add_argument("audio")
    sp.add_argument("texte", nargs="?")
    sp.add_argument("--fichier-texte")

    # Divers
    sp = commande("brut", cmd_brut, "appeler un endpoint que le script ne connaît pas", generation=True)
    sp.add_argument("methode", help="GET, POST, PATCH, DELETE…")
    sp.add_argument("chemin", help="ex. /v1/voices/settings/default")
    sp.add_argument("--corps", help="corps JSON, ou @fichier.json")
    sp.add_argument("--requete", action="append", metavar="CLE=VALEUR", help="paramètre d'URL ; répétable")
    sp.add_argument("--sortie", help="écrire la réponse dans ce fichier (obligatoire pour une réponse binaire)")
    sp.add_argument("--ecraser", action="store_true")
    sp = commande("inspecter", cmd_inspecter, "contrôler un fichier audio local (durée, format, niveaux)")
    sp.add_argument("fichier")
    return p


def main(argv=None):
    args = analyseur().parse_args(sys.argv[1:] if argv is None else argv)
    try:
        return args.fonction(args)
    except ErreurEleven as exc:
        signaler(exc.message)
        return exc.code
    except KeyboardInterrupt:
        signaler("Interrompu.")
        return ERREUR
    except Exception as exc:  # dernier filet : message court, clé masquée
        signaler(f"Erreur inattendue : {type(exc).__name__} : {exc}")
        return ERREUR


if __name__ == "__main__":
    sys.exit(main())
