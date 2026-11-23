#!/usr/bin/env python3
"""Client en ligne de commande de l'API Uthana (GraphQL), bibliothèque standard uniquement.

Sous-commandes :
  compte       verifier, prix, depenses
  personnages  personnages, importer, telecharger-personnage
  animations   texte, video, locomotion, styles, boucler, enchainer
  reprise      telecharger, statut, taches, animations
  divers       brut, inspecter
La clé est lue dans la variable d'environnement UTHANA_API_KEY ; elle n'est jamais affichée.
Lancer `uthana.py <sous-commande> --help` pour les options, et voir ../SKILL.md pour l'usage.
"""

import argparse
import base64
import datetime
import hashlib
import http.client
import json
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

API_BASE_DEFAUT = "https://uthana.com"
AGENT = "uthana-plugin-quiche-lorraine-games/1"

# Personnages fournis à tous les comptes (client Python officiel, UthanaCharacters).
PERSONNAGES_FOURNIS = {
    "tar": "cXi2eAP19XwQ",
    "ava": "cmEE2fT4aSaC",
    "manny": "c43tbGks3crJ",
    "quinn": "czCjWEMtWxt8",
}
PERSONNAGE_DEFAUT = "tar"

# Modèles de texte → animation. Les modèles 3.0 passent par une tâche à suivre ;
# 1.0 et 2.0 répondent tout de suite (noms d'API du client officiel).
MODELES_TEXTE = {
    "3.0": "text-to-motion-3.0",
    "3.0-lite": "text-to-motion-3.0-lite",
    "3.0-mini": "text-to-motion-3.0-mini",
    "2.0": "text-to-motion-bucmd",
    "1.0": "text-to-motion",
}
MODELES_TEXTE_TACHE = ("3.0", "3.0-lite", "3.0-mini")
MODELE_TEXTE_DEFAUT = "3.0"
DUREES_TEXTE = {"3.0": (4, 10, 4), "3.0-lite": (5, 10, 5), "3.0-mini": (5, 10, 5)}  # min, max, défaut
MODELES_VIDEO = ("video-to-motion-3.0", "video-to-motion-2.1", "video-to-motion-2.0")

# Barème relevé le 23/11/2026 sur uthana.com/pricing, en dollars ; sert à l'estimation affichée
# avant l'envoi. Le débit réel se lit dans le solde du compte (verifier, depenses).
PRIX = {
    "3.0": 0.10, "3.0-lite": 0.10, "3.0-mini": 0.075, "2.0": 0.03, "1.0": 0.02,
    "video-to-motion-3.0": 0.06, "video-to-motion-2.1": 0.05, "video-to-motion-2.0": 0.05,
    "locomotion": 0.02, "boucle": 0.01, "rig": 0.15,
}

FORMATS_ANIMATION = (".glb", ".fbx", ".bvh")
FORMATS_PERSONNAGE = (".glb", ".fbx")
EXTENSIONS_PERSONNAGE = (".glb", ".gltf", ".fbx")
EXTENSIONS_VIDEO = (".mp4", ".mov", ".avi", ".webm")
TYPES_MIME = {
    ".glb": "model/gltf-binary", ".gltf": "model/gltf+json", ".fbx": "application/octet-stream",
    ".mp4": "video/mp4", ".mov": "video/quicktime", ".avi": "video/x-msvideo", ".webm": "video/webm",
}
TAILLE_MAX_PERSONNAGE = 30 * 1024 * 1024
TAILLE_MAX_VIDEO = 128 * 1024 * 1024
FPS_ACCEPTES = (24, 30, 60)
STATUTS_FINAUX = ("FINISHED", "FAILED")
ATTENTES_LIMITE = (10, 20, 30, 60, 60, 60, 60)

# Codes de sortie (voir SKILL.md, section « Erreurs »)
OK = 0
ERREUR = 1           # erreur API inattendue, réponse illisible, fichier invalide
USAGE = 2            # argument invalide, refusé localement ou par la validation de l'API
CLE = 3              # UTHANA_API_KEY absente ou refusée (401)
CREDITS = 4          # solde insuffisant, ou quota de téléchargement d'un ancien abonnement
RESEAU = 5           # hôte bloqué par la politique réseau ou injoignable
TACHE_ECHOUEE = 6    # tâche FAILED
DELAI = 7            # délai dépassé ou réponse incertaine : la tâche a pu être acceptée
LIMITE = 9           # trop de tâches simultanées (429 job_limit_exceeded), malgré les nouveaux essais


class ErreurUthana(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


def pause(secondes):
    """Attente ; UTHANA_PAUSE la multiplie (les tests la mettent à 0)."""
    try:
        facteur = float(os.environ.get("UTHANA_PAUSE", "1"))
    except ValueError:
        facteur = 1.0
    time.sleep(max(secondes * facteur, 0.0))


# ---------------------------------------------------------------------------
# Sortie : tout texte affiché passe par masquer(), pour que la clé n'apparaisse jamais.
# ---------------------------------------------------------------------------

def masquer(texte):
    texte = str(texte)
    cle = os.environ.get("UTHANA_API_KEY", "").strip()
    if cle:
        texte = texte.replace(cle, "***")
        texte = texte.replace(base64.b64encode(f"{cle}:".encode()).decode(), "***")
    return texte


def dire(texte=""):
    print(masquer(texte), flush=True)


def signaler(texte):
    print(masquer(texte), file=sys.stderr, flush=True)


def lire_cle():
    cle = os.environ.get("UTHANA_API_KEY", "").strip()
    if not cle:
        raise ErreurUthana(CLE, (
            "UTHANA_API_KEY n'est pas définie. Ajoute la clé Uthana en variable d'environnement "
            "(UTHANA_API_KEY) dans les réglages de l'environnement, puis ouvre une nouvelle session. "
            "Ne la colle pas dans le chat."))
    return cle


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class _SansRedirection(urllib.request.HTTPRedirectHandler):
    """Aucune redirection n'est suivie : l'en-tête d'authentification ne part jamais ailleurs."""

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
        return ErreurUthana(RESEAU, (
            f"Le domaine {nom} est bloqué par la politique réseau de l'environnement (403 du proxy). "
            f"Ajoute {nom} aux domaines autorisés de l'environnement, puis relance."))
    if "Tunnel connection failed" in texte:
        return ErreurUthana(RESEAU, (
            f"Le proxy n'a pas pu joindre {nom} ({texte}). Vérifie que ce domaine est autorisé "
            "dans la politique réseau de l'environnement."))
    if isinstance(raison, socket.gaierror):
        return ErreurUthana(RESEAU, f"Hôte {nom} introuvable (DNS). Vérifie l'accès réseau de l'environnement.")
    if isinstance(raison, (socket.timeout, TimeoutError)):
        return ErreurUthana(DELAI, f"{nom} n'a pas répondu dans le délai imparti.")
    if isinstance(raison, (ConnectionResetError, ConnectionAbortedError, BrokenPipeError,
                           http.client.IncompleteRead, http.client.RemoteDisconnected, ssl.SSLEOFError)):
        return ErreurUthana(RESEAU, f"Connexion avec {nom} coupée en cours de transfert ({texte}).")
    if isinstance(raison, ssl.SSLError):
        return ErreurUthana(RESEAU, f"Échec TLS avec {nom} ({texte}).")
    return ErreurUthana(RESEAU, f"Impossible de joindre {nom} : {texte}.")


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


def multipart(operations, fichier):
    """Corps multipart de la spécification GraphQL multipart request (un seul fichier)."""
    frontiere = "----uthana" + uuid.uuid4().hex
    nom = os.path.basename(fichier).replace('"', "_")
    ext = os.path.splitext(fichier)[1].lower()
    with open(fichier, "rb") as f:
        contenu = f.read()
    morceaux = [
        f"--{frontiere}\r\nContent-Disposition: form-data; name=\"operations\"\r\n\r\n".encode(),
        json.dumps(operations).encode("utf-8"), b"\r\n",
        f"--{frontiere}\r\nContent-Disposition: form-data; name=\"map\"\r\n\r\n".encode(),
        json.dumps({"0": ["variables.file"]}).encode(), b"\r\n",
        (f"--{frontiere}\r\nContent-Disposition: form-data; name=\"0\"; filename=\"{nom}\"\r\n"
         f"Content-Type: {TYPES_MIME.get(ext, 'application/octet-stream')}\r\n\r\n").encode(),
        contenu, b"\r\n", f"--{frontiere}--\r\n".encode(),
    ]
    return b"".join(morceaux), f"multipart/form-data; boundary={frontiere}"


class Api:
    def __init__(self, base, cle):
        self.base = base.rstrip("/")
        self.cle = cle

    def _entetes(self):
        jeton = base64.b64encode(f"{self.cle}:".encode()).decode()
        return {"Authorization": f"Basic {jeton}"}

    def graphql(self, query, variables=None, fichier=None, delai=120, payant=False):
        """Exécute une opération ; renvoie `data`. Réessaie seulement un 429 job_limit_exceeded,
        qui garantit qu'aucune tâche n'a été acceptée."""
        entetes = self._entetes()
        operation = {"query": query, "variables": variables or {}}
        if fichier:
            operation["variables"]["file"] = None
            corps, type_contenu = multipart(operation, fichier)
        else:
            corps, type_contenu = json.dumps(operation).encode("utf-8"), "application/json"
        entetes["Content-Type"] = type_contenu
        url = self.base + "/graphql"
        for essai in range(len(ATTENTES_LIMITE) + 1):
            try:
                statut, _, brut = requete("POST", url, corps, entetes, delai)
            except ErreurUthana as exc:
                if exc.code == DELAI and payant:
                    exc.message += (" La requête a pu être acceptée et facturée : regarde `taches` ou "
                                    "`animations` avant de relancer quoi que ce soit.")
                raise
            charge = _json(brut, statut)
            erreurs = charge.get("errors") if isinstance(charge, dict) else None
            if statut == 429 and _code_erreur(erreurs) == "job_limit_exceeded" and essai < len(ATTENTES_LIMITE):
                attente = ATTENTES_LIMITE[essai]
                signaler(f"Uthana limite les tâches simultanées : nouvel essai dans {attente} s.")
                pause(attente)
                continue
            break
        if statut >= 400 or erreurs:
            raise _erreur_api(statut, erreurs, charge, payant)
        return charge.get("data") or {}

    def telecharger(self, url, delai=300):
        statut, entetes, brut = requete("GET", url, None, self._entetes(), delai)
        if statut >= 400:
            raise _erreur_telechargement(statut, brut, url)
        return brut, entetes


def _json(brut, statut):
    if not brut:
        return {}
    try:
        return json.loads(brut.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        if statut == 401:
            raise _erreur_cle() from None
        raise ErreurUthana(ERREUR, (
            f"Réponse illisible de l'API Uthana (HTTP {statut}) : "
            f"{brut[:200].decode('utf-8', errors='replace')}")) from None


def _code_erreur(erreurs):
    for e in erreurs or []:
        ext = e.get("extensions") if isinstance(e, dict) else None
        if isinstance(ext, dict) and ext.get("code"):
            return str(ext["code"])
        if isinstance(e, dict) and e.get("code"):
            return str(e["code"])
    return ""


def _erreur_cle():
    return ErreurUthana(CLE, (
        "Uthana refuse la clé UTHANA_API_KEY (401). Vérifie-la sur uthana.com/app/account, mets à jour "
        "la variable de l'environnement, puis ouvre une nouvelle session."))


def _erreur_api(statut, erreurs, charge, payant):
    messages = "; ".join(str(e.get("message", e)) for e in (erreurs or []) if isinstance(e, dict))
    if not messages and isinstance(charge, dict):
        messages = str(charge)[:200]
    code = _code_erreur(erreurs)
    bas = (messages + " " + code).lower()
    if statut == 401 or "not logged in" in bas or "unauthorized" in bas or "invalid api key" in bas:
        return _erreur_cle()
    if statut == 429:
        if code == "job_limit_exceeded":
            return ErreurUthana(LIMITE, (
                "Uthana refuse encore la tâche après environ 5 minutes d'essais : trop de tâches en cours "
                "(4 par type sans moyen de paiement enregistré). Rien n'a été accepté ni facturé. "
                "Attends la fin des tâches en cours (`taches`), puis relance une seule tâche."))
        return ErreurUthana(DELAI, (
            f"Uthana a répondu 429 sans le code job_limit_exceeded ({messages}). La requête a pu être "
            "acceptée : regarde `taches` ou `animations` avant de relancer."))
    if any(mot in bas for mot in ("insufficient", "balance", "not enough credit", "payment required",
                                   "add credit", "top up", "wallet")) or statut == 402:
        return ErreurUthana(CREDITS, (
            f"Solde Uthana insuffisant pour cette opération ; rien n'a été généré : {messages}. "
            "Ajoute du crédit sur uthana.com/app/account (Billing), puis relance."))
    if "maximum number of characters" in bas:
        return ErreurUthana(CREDITS, f"Limite de personnages du compte atteinte : {messages}.")
    if statut >= 500 and payant:
        return ErreurUthana(DELAI, (
            f"Erreur du serveur Uthana (HTTP {statut}) : {messages}. L'opération a pu être acceptée : "
            "regarde `taches` ou `animations` avant de relancer."))
    if statut in (400, 422) or "argument" in bas or "invalid" in bas or "must be" in bas:
        return ErreurUthana(USAGE, f"L'API refuse les paramètres (HTTP {statut}) : {messages}")
    return ErreurUthana(ERREUR, f"Erreur de l'API Uthana (HTTP {statut}) : {messages}")


def _erreur_telechargement(statut, brut, url):
    detail = brut[:200].decode("utf-8", errors="replace").strip()
    if statut == 401:
        return _erreur_cle()
    if statut == 403:
        return ErreurUthana(CREDITS, (
            f"Téléchargement refusé (403 : quota d'un ancien abonnement, ou droits) : {detail}"))
    if statut == 404:
        return ErreurUthana(USAGE, "Animation ou personnage introuvable, ou sans accès (404). Vérifie les identifiants.")
    if statut == 400:
        return ErreurUthana(USAGE, f"Options de téléchargement refusées (400) : {detail}")
    return ErreurUthana(ERREUR, f"Téléchargement impossible (HTTP {statut}) : {detail}")


# ---------------------------------------------------------------------------
# Inspection des GLB : animations, squelette, maillages
# ---------------------------------------------------------------------------

def lire_glb(donnees):
    if len(donnees) < 20 or donnees[:4] != b"glTF":
        raise ValueError("en-tête « glTF » absent")
    longueur, type_bloc = struct.unpack("<II", donnees[12:20])
    if type_bloc != 0x4E4F534A:
        raise ValueError("premier bloc non JSON")
    gltf = json.loads(donnees[20:20 + longueur].decode("utf-8"))
    binaire = b""
    debut = 20 + longueur
    if len(donnees) >= debut + 8:
        lg, type_bin = struct.unpack("<II", donnees[debut:debut + 8])
        if type_bin == 0x004E4942:
            binaire = donnees[debut + 8:debut + 8 + lg]
    return gltf, binaire


def inspecter_glb(chemin):
    with open(chemin, "rb") as f:
        donnees = f.read()
    controle = {"taille_octets": len(donnees)}
    try:
        gltf, _ = lire_glb(donnees)
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        controle["avertissement"] = f"GLB illisible : {exc}"
        return controle
    accesseurs = gltf.get("accessors", [])
    animations = []
    for anim in gltf.get("animations", []):
        duree = 0.0
        for echantillon in anim.get("samplers", []):
            acc = accesseurs[echantillon.get("input", 0)] if echantillon.get("input", 0) < len(accesseurs) else {}
            if acc.get("max"):
                duree = max(duree, float(acc["max"][0]))
            if acc.get("count"):
                controle["_images"] = max(controle.get("_images", 0), int(acc["count"]))
        animations.append({"nom": anim.get("name") or "", "duree_s": round(duree, 3),
                           "canaux": len(anim.get("channels", []))})
    images = controle.pop("_images", 0)
    controle["animations"] = animations
    if animations and animations[0]["duree_s"] > 0 and images > 1:
        controle["images_par_seconde"] = round((images - 1) / animations[0]["duree_s"])
    controle["squelettes"] = len(gltf.get("skins", []))
    controle["os"] = sum(len(s.get("joints", [])) for s in gltf.get("skins", []))
    controle["maillages"] = len(gltf.get("meshes", []))
    noeuds = gltf.get("nodes", [])
    noms = [n.get("name", "") for s in gltf.get("skins", []) for j in s.get("joints", [])[:1]
            for n in [noeuds[j] if j < len(noeuds) else {}]]
    if noms:
        controle["os_racine"] = noms[0]
    return controle


def resume_controle(controle):
    if controle.get("avertissement"):
        return f"⚠ {controle['avertissement']}"
    morceaux = [_taille_lisible(controle.get("taille_octets", 0))]
    for a in controle.get("animations", []):
        morceaux.append(f"animation « {a['nom']} » {a['duree_s']:.2f} s")
    if controle.get("images_par_seconde"):
        morceaux.append(f"{controle['images_par_seconde']} i/s")
    morceaux.append(f"{controle.get('os', 0)} os")
    morceaux.append(f"{controle.get('maillages', 0)} maillage(s)")
    return ", ".join(morceaux)


def _taille_lisible(octets):
    for unite in ("o", "Ko", "Mo", "Go"):
        if octets < 1024 or unite == "Go":
            return f"{octets:.0f} {unite}" if unite == "o" else f"{octets:.1f} {unite}"
        octets /= 1024


# ---------------------------------------------------------------------------
# Fiche .uthana.json
# ---------------------------------------------------------------------------

def chemin_fiche(sortie):
    return os.path.splitext(sortie)[0] + ".uthana.json"


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


def entree_pour_fiche(chemin, sortie):
    absolu = os.path.abspath(chemin)
    dossier = os.path.dirname(os.path.abspath(sortie))
    racine = os.getcwd()
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    entree = {"taille_octets": os.path.getsize(chemin), "sha256": h.hexdigest()}
    if _sous(absolu, racine) and _sous(dossier, racine):
        entree["fichier"] = os.path.relpath(absolu, dossier)
    else:
        entree["nom"] = os.path.basename(absolu)
    return entree


def _sans_vides(dico):
    return {k: v for k, v in dico.items() if v is not None}


# ---------------------------------------------------------------------------
# Outils communs
# ---------------------------------------------------------------------------

def base_api(args):
    return getattr(args, "api", None) or os.environ.get("UTHANA_API_BASE") or API_BASE_DEFAUT


def _api(args):
    return Api(base_api(args), lire_cle())


def personnage(valeur):
    """Accepte un identifiant Uthana ou le nom d'un personnage fourni (tar, ava, manny, quinn)."""
    if not valeur:
        return PERSONNAGES_FOURNIS[PERSONNAGE_DEFAUT]
    return PERSONNAGES_FOURNIS.get(valeur.lower(), valeur)


def _verifier_sortie(sortie, ecraser, extensions):
    if not sortie.lower().endswith(extensions):
        raise ErreurUthana(USAGE, f"--sortie doit finir par {' ou '.join(extensions)}.")
    if os.path.exists(sortie) and not ecraser:
        raise ErreurUthana(USAGE, f"{sortie} existe déjà. Choisis un autre nom ou ajoute --ecraser.")


def _fichier_entree(chemin, extensions, taille_max):
    if not os.path.isfile(chemin):
        raise ErreurUthana(USAGE, f"Fichier introuvable : {chemin}")
    if not chemin.lower().endswith(extensions):
        raise ErreurUthana(USAGE, f"{chemin} : extension non prise en charge (attendu : {', '.join(extensions)}).")
    taille = os.path.getsize(chemin)
    if taille > taille_max:
        raise ErreurUthana(USAGE, f"{chemin} fait {_taille_lisible(taille)} : la limite est {_taille_lisible(taille_max)}.")
    return chemin


def _ecrire_binaire(chemin, octets):
    os.makedirs(os.path.dirname(os.path.abspath(chemin)), exist_ok=True)
    temporaire = chemin + ".partiel"
    with open(temporaire, "wb") as f:
        f.write(octets)
    os.replace(temporaire, chemin)


def _a_blanc(query, variables, estimation=None, fichier=None):
    dire("À blanc : POST /graphql")
    dire(query.strip())
    if fichier:
        dire(f"Fichier envoyé : {fichier}")
    dire(json.dumps(variables, ensure_ascii=False, indent=2))
    if estimation:
        dire(f"Coût estimé : {estimation}")
    dire("Aucune requête envoyée, aucun crédit consommé.")
    return OK


def solde(api):
    try:
        org = api.graphql("query { org { payg_enabled payg_total_usd } }").get("org") or {}
    except ErreurUthana:
        return None
    if not org.get("payg_enabled"):
        return None
    try:
        return float(org.get("payg_total_usd"))
    except (TypeError, ValueError):
        return None


def url_animation(base, character_id, motion_id, ext, args):
    url = f"{base.rstrip('/')}/motion/file/motion_viewer/{character_id}/{motion_id}/{ext}/{character_id}-{motion_id}.{ext}"
    options = []
    if getattr(args, "fps", None):
        options.append(f"fps={args.fps}")
    if getattr(args, "sans_maillage", False):
        options.append("no_mesh=true")
    for option, cle in (("sur_place", "in_place"), ("torse", "torso_only")):
        if getattr(args, option, False):
            options.append(f"{cle}=true")
    if getattr(args, "vitesse_lecture", None):
        options.append(f"speed_multiplier={args.vitesse_lecture:g}")
    return url + ("?" + "&".join(options) if options else "")


def _verifier_options_telechargement(args):
    if args.fps and args.fps not in FPS_ACCEPTES:
        raise ErreurUthana(USAGE, "--fps doit valoir 24, 30 ou 60.")
    if args.vitesse_lecture is not None and not 0 < args.vitesse_lecture <= 2:
        raise ErreurUthana(USAGE, "--vitesse-lecture doit être supérieure à 0 et au plus 2.")


def telecharger_animation(args, api, character_id, motion_id, fiche, solde_avant=None):
    """Télécharge l'animation (gratuit), écrit la fiche et affiche le contrôle."""
    ext = os.path.splitext(args.sortie)[1].lower().lstrip(".")
    url = url_animation(api.base, character_id, motion_id, ext, args)
    fiche.update({"motion_id": motion_id, "character_id": character_id,
                  "telechargement": _sans_vides({"format": ext, "fps": args.fps,
                                                 "sans_maillage": args.sans_maillage or None,
                                                 "sur_place": args.sur_place or None,
                                                 "torse": args.torse or None,
                                                 "vitesse_lecture": args.vitesse_lecture})})
    try:
        octets, _ = api.telecharger(url, delai=args.delai)
    except ErreurUthana as exc:
        fiche["etat"] = "a_telecharger"
        ecrire_fiche(args.sortie, fiche)
        exc.message += f"\nL'animation existe : reprends gratuitement avec\n  {commande_reprise(motion_id, character_id, args)}"
        raise
    _ecrire_binaire(args.sortie, octets)
    controle = inspecter_glb(args.sortie) if ext == "glb" else {"taille_octets": len(octets)}
    fiche["controle"] = controle
    fiche["sorties"] = [os.path.basename(args.sortie)]
    if solde_avant is not None:
        apres = solde(api)
        if apres is not None:
            fiche["solde_usd"] = {"avant": solde_avant, "apres": apres}
            fiche["debit_usd"] = round(solde_avant - apres, 4)
    chemin = ecrire_fiche(args.sortie, fiche)
    dire(f"✓ {args.sortie}")
    dire(f"  {resume_controle(controle)}" if ext == "glb" else f"  {_taille_lisible(len(octets))}")
    dire(f"  motion_id {motion_id}, character_id {character_id}")
    if fiche.get("debit_usd") is not None:
        dire(f"  Solde : {fiche['solde_usd']['avant']:.2f} $ → {fiche['solde_usd']['apres']:.2f} $ "
             f"(débit {fiche['debit_usd']:.2f} $, autres opérations en cours comprises)")
    dire(f"  Fiche : {chemin}")
    return OK


def commande_reprise(motion_id, character_id, args):
    options = []
    if args.fps:
        options.append(f"--fps {args.fps}")
    for opt in ("sans_maillage", "sur_place", "torse"):
        if getattr(args, opt, False):
            options.append("--" + opt.replace("_", "-"))
    if args.vitesse_lecture:
        options.append(f"--vitesse-lecture {args.vitesse_lecture:g}")
    return " ".join(["uthana.py telecharger", motion_id, "--personnage", character_id,
                     "--sortie", shlex.quote(args.sortie)] + options)


def attendre_tache(api, job_id, delai, intervalle=5.0):
    """Suit une tâche jusqu'à FINISHED ou FAILED ; renvoie la tâche."""
    fin = time.monotonic() + delai
    attente = intervalle
    dernier = None
    while True:
        tache = api.graphql("query ($job_id: String!) { job(job_id: $job_id) { id status method model result "
                            "est_processing_time } }", {"job_id": job_id}).get("job")
        if not tache:
            raise ErreurUthana(ERREUR, f"Tâche {job_id} introuvable.")
        statut = tache.get("status")
        if statut != dernier:
            signaler(f"Tâche {job_id} : {statut}")
            dernier = statut
        if statut == "FINISHED":
            return tache
        if statut == "FAILED":
            raise ErreurUthana(TACHE_ECHOUEE, (
                f"La tâche {job_id} a échoué : {json.dumps(tache.get('result'), ensure_ascii=False)[:400]}. "
                "Une tâche échouée n'est pas facturée ; propose une autre entrée (prompt, vidéo plus courte)."))
        if time.monotonic() >= fin:
            raise ErreurUthana(DELAI, (
                f"La tâche {job_id} tourne encore côté Uthana ({statut}). Ne relance pas la génération : "
                f"reprends plus tard avec `statut {job_id}`, puis `telecharger`."))
        pause(attente)
        attente = min(attente * 1.5, 15.0)


def motion_id_de_tache(tache):
    resultat = tache.get("result") or {}
    for chemin in (("result", "id"), ("motion", "id"), ("id",)):
        valeur = resultat
        for cle in chemin:
            valeur = valeur.get(cle) if isinstance(valeur, dict) else None
        if isinstance(valeur, str) and valeur:
            return valeur
    ids = resultat.get("result", {}).get("ids") if isinstance(resultat.get("result"), dict) else None
    if isinstance(ids, list) and ids:
        return ids[0]
    raise ErreurUthana(ERREUR, f"Tâche terminée sans identifiant d'animation lisible : {json.dumps(resultat)[:300]}")


# ---------------------------------------------------------------------------
# Compte
# ---------------------------------------------------------------------------

def cmd_verifier(args):
    code = OK
    cle = os.environ.get("UTHANA_API_KEY", "").strip()
    if cle:
        dire("✓ UTHANA_API_KEY est définie (valeur masquée).")
    else:
        dire("✗ UTHANA_API_KEY n'est pas définie : ajoute-la dans les variables de l'environnement, "
             "puis ouvre une nouvelle session.")
        code = CLE
    base = base_api(args)
    try:
        statut, _, _ = requete("GET", base.rstrip("/") + "/graphql", delai=15)
        dire(f"✓ {hote(base)} est joignable (HTTP {statut}).")
    except ErreurUthana as exc:
        dire(f"✗ {hote(base)} : {exc.message}")
        return exc.code
    if not cle:
        return code
    try:
        org = Api(base, cle).graphql(
            "query { org { name payg_enabled payg_total_usd motion_download_secs_per_month_remaining "
            "characters_allowed_remaining } }").get("org") or {}
    except ErreurUthana as exc:
        dire(f"✗ {exc.message}")
        return exc.code
    dire(f"✓ Clé acceptée (organisation « {org.get('name')} »).")
    if org.get("payg_enabled"):
        dire(f"  Paiement à l'usage actif, solde : {org.get('payg_total_usd')} $.")
    else:
        dire("  ⚠ Paiement à l'usage non activé : active-le sur uthana.com/app/account (Billing) pour "
             "générer par l'API (les nouveaux comptes reçoivent 5 $ de crédit).")
        if org.get("motion_download_secs_per_month_remaining") is not None:
            dire(f"  Ancien abonnement : {org.get('motion_download_secs_per_month_remaining')} s de "
                 "téléchargement restantes ce mois-ci.")
    return OK


def cmd_prix(args):
    prix = _api(args).graphql("query { payg_prices { model_key billing_unit unit_price } }").get("payg_prices") or []
    for p in prix:
        dire(f"{p.get('model_key')} : {p.get('unit_price')} $ / {p.get('billing_unit')}")
    return OK


def cmd_depenses(args):
    entrees = _api(args).graphql(
        "query ($limit: Int) { payg_ledger(limit: $limit) { created type total_usd balance_after model "
        "quantity billing_unit job_id } }", {"limit": args.limite}).get("payg_ledger") or []
    for e in entrees:
        dire(f"{e.get('created')} | {e.get('type')} | {e.get('total_usd')} $ | {e.get('model') or '-'} "
             f"{e.get('quantity') or ''} {e.get('billing_unit') or ''} | solde {e.get('balance_after')} $")
    if not entrees:
        dire("Aucune opération.")
    return OK


# ---------------------------------------------------------------------------
# Personnages
# ---------------------------------------------------------------------------

def cmd_personnages(args):
    dire("Fournis à tous les comptes : " + ", ".join(f"{n} ({i})" for n, i in PERSONNAGES_FOURNIS.items()))
    persos = _api(args).graphql("query { characters { id name created } }").get("characters") or []
    for p in persos:
        dire(f"{p.get('id')} | {p.get('name')} | {p.get('created')}")
    if not persos:
        dire("Aucun personnage importé dans ce compte.")
    return OK


def cmd_importer(args):
    fichier = _fichier_entree(args.fichier, EXTENSIONS_PERSONNAGE, TAILLE_MAX_PERSONNAGE)
    if args.sortie:
        _verifier_sortie(args.sortie, args.ecraser, FORMATS_PERSONNAGE)
    variables = _sans_vides({
        "name": args.nom or os.path.splitext(os.path.basename(fichier))[0],
        "auto_rig": False if args.sans_rig else None,
        "auto_rig_front_facing": False if args.sans_face_avant else None,
        "auto_rig_feet_on_floor": True if args.pieds_au_sol else None,
        "auto_rig_strip_namespace": True if args.sans_prefixe else None,
        "include_fingers": False if args.sans_doigts else None,
        "rerig_target": args.squelette,
    })
    query = ("mutation ($file: Upload!, $name: String!, $auto_rig: Boolean, $auto_rig_front_facing: Boolean, "
             "$auto_rig_feet_on_floor: Boolean, $auto_rig_strip_namespace: Boolean, $include_fingers: Boolean, "
             "$rerig_target: String) { create_character(file: $file, name: $name, auto_rig: $auto_rig, "
             "auto_rig_front_facing: $auto_rig_front_facing, auto_rig_feet_on_floor: $auto_rig_feet_on_floor, "
             "auto_rig_strip_namespace: $auto_rig_strip_namespace, include_fingers: $include_fingers, "
             "rerig_target: $rerig_target) { character { id name } auto_rig_confidence message } }")
    estimation = (f"0 $ si le personnage a déjà un squelette, {PRIX['rig']:.2f} $ s'il faut le rigger"
                  if not args.sans_rig else "0 $ (sans rigging automatique)")
    if args.a_blanc:
        return _a_blanc(query, variables, estimation, fichier)
    signaler(f"Coût estimé : {estimation}")
    api = _api(args)
    avant = solde(api)
    data = api.graphql(query, variables, fichier=fichier, delai=args.delai, payant=True).get("create_character") or {}
    perso = data.get("character") or {}
    dire(f"✓ Personnage importé : {perso.get('id')} ({perso.get('name')})")
    if data.get("auto_rig_confidence") is not None:
        confiance = float(data["auto_rig_confidence"])
        dire(f"  Confiance du rigging automatique : {confiance:.2f}"
             + (" ⚠ faible : vérifie le squelette avant d'animer" if confiance < 0.5 else ""))
    if data.get("message"):
        dire(f"  Message d'Uthana : {data['message']}")
    apres = solde(api) if avant is not None else None
    if apres is not None:
        dire(f"  Solde : {avant:.2f} $ → {apres:.2f} $")
    if args.sortie:
        ext = os.path.splitext(args.sortie)[1].lower().lstrip(".")
        octets, _ = api.telecharger(f"{api.base}/motion/bundle/{perso.get('id')}/character.{ext}", delai=args.delai)
        _ecrire_binaire(args.sortie, octets)
        fiche = {"outil": "uthana", "operation": "create_character", "date": maintenant(),
                 "character_id": perso.get("id"), "nom": perso.get("name"),
                 "entree": entree_pour_fiche(fichier, args.sortie), "parametres": variables,
                 "auto_rig_confidence": data.get("auto_rig_confidence"),
                 "sorties": [os.path.basename(args.sortie)],
                 "controle": inspecter_glb(args.sortie) if ext == "glb" else {"taille_octets": len(octets)}}
        dire(f"✓ {args.sortie} — {resume_controle(fiche['controle']) if ext == 'glb' else _taille_lisible(len(octets))}")
        dire(f"  Fiche : {ecrire_fiche(args.sortie, fiche)}")
    dire("  Note ce character_id dans les conventions du projet.")
    return OK


def cmd_telecharger_personnage(args):
    _verifier_sortie(args.sortie, args.ecraser, FORMATS_PERSONNAGE)
    api = _api(args)
    cid = personnage(args.personnage)
    ext = os.path.splitext(args.sortie)[1].lower().lstrip(".")
    octets, _ = api.telecharger(f"{api.base}/motion/bundle/{cid}/character.{ext}", delai=args.delai)
    _ecrire_binaire(args.sortie, octets)
    controle = inspecter_glb(args.sortie) if ext == "glb" else {"taille_octets": len(octets)}
    fiche = {"outil": "uthana", "operation": "character_bundle", "date": maintenant(), "character_id": cid,
             "sorties": [os.path.basename(args.sortie)], "controle": controle}
    dire(f"✓ {args.sortie} — {resume_controle(controle) if ext == 'glb' else _taille_lisible(len(octets))}")
    dire(f"  Fiche : {ecrire_fiche(args.sortie, fiche)}")
    return OK


# ---------------------------------------------------------------------------
# Animations
# ---------------------------------------------------------------------------

def _prevoir(args, extensions=FORMATS_ANIMATION):
    _verifier_sortie(args.sortie, args.ecraser, extensions)
    _verifier_options_telechargement(args)


def cmd_texte(args):
    _prevoir(args)
    modele = args.modele
    cid = personnage(args.personnage)
    if modele in MODELES_TEXTE_TACHE:
        mini, maxi, defaut = DUREES_TEXTE[modele]
        duree = args.duree if args.duree is not None else defaut
        if not mini <= duree <= maxi:
            raise ErreurUthana(USAGE, f"--duree doit être entre {mini} et {maxi} s pour le modèle {modele}.")
        variables = _sans_vides({"prompt": args.prompt, "model": MODELES_TEXTE[modele], "character_id": cid,
                                 "length": float(duree), "rewrite_prompt": False if args.sans_reecriture else None,
                                 "fast": True if args.rapide else None})
        query = ("mutation ($prompt: String!, $model: String!, $character_id: String, $length: Float, "
                 "$rewrite_prompt: Boolean, $fast: Boolean) { create_text_to_motion_job(prompt: $prompt, "
                 "model: $model, character_id: $character_id, length: $length, rewrite_prompt: $rewrite_prompt, "
                 "fast: $fast) { job { id status } } }")
    else:
        duree = args.duree if args.duree is not None else 10.0
        if not 0.25 <= duree <= 10:
            raise ErreurUthana(USAGE, "--duree doit être entre 0,25 et 10 s pour les modèles 1.0 et 2.0.")
        variables = _sans_vides({"prompt": args.prompt, "model": MODELES_TEXTE[modele], "character_id": cid,
                                 "length": float(duree) if modele == "2.0" else None, "seed": args.graine,
                                 "foot_ik": True if args.ik_pieds else None})
        query = ("mutation ($prompt: String!, $model: String, $character_id: String, $length: Float, $seed: Int, "
                 "$foot_ik: Boolean) { create_text_to_motion(prompt: $prompt, model: $model, character_id: "
                 "$character_id, length: $length, seed: $seed, foot_ik: $foot_ik) { motion { id name } } }")
    estimation = f"≈ {PRIX[modele] * duree:.2f} $ ({duree:g} s × {PRIX[modele]:g} $/s, modèle {modele})"
    if args.a_blanc:
        return _a_blanc(query, variables, estimation)
    signaler(f"Coût estimé : {estimation}")
    api = _api(args)
    avant = solde(api)
    fiche = {"outil": "uthana", "operation": "texte", "date": maintenant(), "prompt": args.prompt,
             "modele": MODELES_TEXTE[modele], "parametres": {k: v for k, v in variables.items() if k != "prompt"},
             "estimation_usd": round(PRIX[modele] * duree, 4)}
    if modele in MODELES_TEXTE_TACHE:
        job = (api.graphql(query, variables, delai=args.delai, payant=True)
               .get("create_text_to_motion_job") or {}).get("job") or {}
        fiche["job_id"] = job.get("id")
        signaler(f"Tâche créée : {job.get('id')}")
        if args.sans_attendre:
            dire(f"Tâche {job.get('id')} créée. Reprise : uthana.py statut {job.get('id')} --sortie {shlex.quote(args.sortie)}")
            return OK
        tache = attendre_tache(api, job.get("id"), args.attente)
        motion_id = motion_id_de_tache(tache)
    else:
        motion = (api.graphql(query, variables, delai=args.delai, payant=True)
                  .get("create_text_to_motion") or {}).get("motion") or {}
        motion_id = motion.get("id")
    return telecharger_animation(args, api, cid, motion_id, fiche, avant)


def cmd_video(args):
    _prevoir(args)
    fichier = _fichier_entree(args.fichier, EXTENSIONS_VIDEO, TAILLE_MAX_VIDEO)
    cid = personnage(args.personnage)
    variables = _sans_vides({"motion_name": args.nom or os.path.splitext(os.path.basename(fichier))[0],
                             "model": args.modele, "character_id": cid,
                             "high_quality_hands": True if args.mains else None})
    query = ("mutation ($file: Upload!, $motion_name: String!, $model: String, $character_id: String, "
             "$high_quality_hands: Boolean) { create_video_to_motion(file: $file, motion_name: $motion_name, "
             "model: $model, character_id: $character_id, high_quality_hands: $high_quality_hands) "
             "{ job { id status } } }")
    estimation = f"{PRIX[args.modele]:g} $ par seconde d'animation produite (vidéo de 2 à 60 s)"
    if args.a_blanc:
        return _a_blanc(query, variables, estimation, fichier)
    signaler(f"Coût estimé : {estimation}")
    api = _api(args)
    avant = solde(api)
    job = (api.graphql(query, variables, fichier=fichier, delai=args.delai, payant=True)
           .get("create_video_to_motion") or {}).get("job") or {}
    signaler(f"Tâche créée : {job.get('id')}")
    fiche = {"outil": "uthana", "operation": "video", "date": maintenant(), "modele": args.modele,
             "entree": entree_pour_fiche(fichier, args.sortie), "job_id": job.get("id"),
             "parametres": {k: v for k, v in variables.items()}}
    if args.sans_attendre:
        dire(f"Tâche {job.get('id')} créée. Reprise : uthana.py statut {job.get('id')} --sortie {shlex.quote(args.sortie)}")
        return OK
    tache = attendre_tache(api, job.get("id"), args.attente)
    return telecharger_animation(args, api, cid, motion_id_de_tache(tache), fiche, avant)


def cmd_locomotion(args):
    _prevoir(args)
    if not 1 <= args.foulees <= 5:
        raise ErreurUthana(USAGE, "--foulees doit être entre 1 et 5.")
    if not 0.25 <= args.vitesse <= 8.0:
        raise ErreurUthana(USAGE, "--vitesse doit être entre 0,25 et 8 m/s.")
    cid = personnage(args.personnage)
    variables = {"character_id": cid, "strides": args.foulees, "move_speed": args.vitesse,
                 "style_id": args.style, "travel_angle": args.angle}
    query = ("mutation ($character_id: String!, $strides: Int, $move_speed: Float, $style_id: String, "
             "$travel_angle: Float) { create_locomotion(character_id: $character_id, strides: $strides, "
             "move_speed: $move_speed, style_id: $style_id, travel_angle: $travel_angle) { motion { id name } } }")
    estimation = f"{PRIX['locomotion']:g} $ par seconde produite (quelques secondes pour {args.foulees} foulée(s))"
    if args.a_blanc:
        return _a_blanc(query, variables, estimation)
    signaler(f"Coût estimé : {estimation}")
    api = _api(args)
    avant = solde(api)
    motion = (api.graphql(query, variables, delai=args.delai, payant=True).get("create_locomotion") or {}).get("motion") or {}
    fiche = {"outil": "uthana", "operation": "locomotion", "date": maintenant(), "parametres": variables}
    return telecharger_animation(args, api, cid, motion.get("id"), fiche, avant)


def cmd_styles(args):
    styles = _api(args).graphql("query { locomotion_styles }").get("locomotion_styles") or []
    dire(", ".join(styles) if styles else "Aucun style renvoyé.")
    return OK


def cmd_boucler(args):
    _prevoir(args)
    cid = personnage(args.personnage)
    for nom, valeur in (("--debut", args.debut), ("--fin", args.fin)):
        if valeur is not None and not 0 <= valeur <= 1:
            raise ErreurUthana(USAGE, f"{nom} est une fraction entre 0 et 1.")
    variables = _sans_vides({"character_id": cid, "motion_id": args.motion_id, "loop_mode": args.mode,
                             "trim_start_pct": args.debut, "trim_end_pct": args.fin,
                             "zone_duration": args.zone, "zone_mode": args.zone_mode})
    query = ("mutation ($character_id: String!, $motion_id: String!, $loop_mode: String!, $trim_start_pct: Float, "
             "$trim_end_pct: Float, $zone_duration: Float, $zone_mode: String) { create_looped_motion("
             "character_id: $character_id, motion_id: $motion_id, loop_mode: $loop_mode, trim_start_pct: "
             "$trim_start_pct, trim_end_pct: $trim_end_pct, zone_duration: $zone_duration, zone_mode: $zone_mode) "
             "{ motion { id name } } }")
    estimation = f"{PRIX['boucle']:g} $ par seconde produite"
    if args.a_blanc:
        return _a_blanc(query, variables, estimation)
    signaler(f"Coût estimé : {estimation}")
    api = _api(args)
    avant = solde(api)
    motion = (api.graphql(query, variables, delai=args.delai, payant=True).get("create_looped_motion") or {}).get("motion") or {}
    fiche = {"outil": "uthana", "operation": "boucler", "date": maintenant(), "source_motion_id": args.motion_id,
             "parametres": variables}
    return telecharger_animation(args, api, cid, motion.get("id"), fiche, avant)


def cmd_enchainer(args):
    _prevoir(args)
    cid = personnage(args.personnage)
    premier = _sans_vides({"motion_id": args.premier, "transition_duration_seconds": args.transition})
    if args.transition is not None and not 0.1 <= args.transition <= 3:
        raise ErreurUthana(USAGE, "--transition doit être entre 0,1 et 3 s.")
    entree = {"character_id": cid, "steps": [premier, {"motion_id": args.second}]}
    query = "mutation ($input: StitchInput!) { stitch(input: $input) { motion { id name } resolved_steps } }"
    estimation = f"{PRIX['boucle']:g} $ par seconde produite"
    if args.a_blanc:
        return _a_blanc(query, {"input": entree}, estimation)
    signaler(f"Coût estimé : {estimation}")
    api = _api(args)
    avant = solde(api)
    data = api.graphql(query, {"input": entree}, delai=args.delai, payant=True).get("stitch") or {}
    fiche = {"outil": "uthana", "operation": "enchainer", "date": maintenant(),
             "sources": [args.premier, args.second], "parametres": entree,
             "etapes_resolues": data.get("resolved_steps")}
    return telecharger_animation(args, api, cid, (data.get("motion") or {}).get("id"), fiche, avant)


# ---------------------------------------------------------------------------
# Reprise et liste
# ---------------------------------------------------------------------------

def cmd_telecharger(args):
    _prevoir(args)
    api = _api(args)
    fiche = {"outil": "uthana", "operation": "telecharger", "date": maintenant()}
    return telecharger_animation(args, api, personnage(args.personnage), args.motion_id, fiche)


def cmd_statut(args):
    api = _api(args)
    tache = api.graphql("query ($job_id: String!) { job(job_id: $job_id) { id status method model result "
                        "est_processing_time } }", {"job_id": args.job_id}).get("job")
    if not tache:
        raise ErreurUthana(USAGE, f"Tâche {args.job_id} introuvable.")
    dire(json.dumps(tache, ensure_ascii=False, indent=2))
    if args.sortie and tache.get("status") == "FINISHED":
        _prevoir(args)
        fiche = {"outil": "uthana", "operation": "reprise", "date": maintenant(), "job_id": args.job_id,
                 "methode": tache.get("method"), "modele": tache.get("model")}
        return telecharger_animation(args, api, personnage(args.personnage), motion_id_de_tache(tache), fiche)
    return OK


def cmd_taches(args):
    taches = _api(args).graphql("query ($method: String) { jobs(method: $method) { id status method model "
                                "created_at } }", _sans_vides({"method": args.methode})).get("jobs") or []
    for t in taches[:args.limite]:
        dire(f"{t.get('id')} | {t.get('status')} | {t.get('method')} | {t.get('model')} | {t.get('created_at')}")
    if not taches:
        dire("Aucune tâche.")
    return OK


def cmd_animations(args):
    page = _api(args).graphql(
        "query ($query: String, $limit: Int, $source: String) { motions_paged(query: $query, limit: $limit, "
        "source: $source) { items { id name created tags } next_cursor } }",
        {"query": args.recherche or "", "limit": args.limite, "source": args.source}).get("motions_paged") or {}
    for m in page.get("items") or []:
        methode = (m.get("tags") or {}).get("Method") if isinstance(m.get("tags"), dict) else None
        dire(f"{m.get('id')} | {m.get('name')} | {methode or '-'} | {m.get('created')}")
    if not page.get("items"):
        dire("Aucune animation.")
    return OK


# ---------------------------------------------------------------------------
# Divers
# ---------------------------------------------------------------------------

def cmd_brut(args):
    query = args.query
    if query.startswith("@"):
        with open(query[1:], encoding="utf-8") as f:
            query = f.read()
    try:
        variables = json.loads(args.variables) if args.variables else {}
    except json.JSONDecodeError as exc:
        raise ErreurUthana(USAGE, f"--variables n'est pas un JSON valide : {exc}") from None
    if args.a_blanc:
        return _a_blanc(query, variables)
    mutation = query.lstrip().startswith("mutation")
    data = _api(args).graphql(query, variables, delai=args.delai, payant=mutation)
    dire(json.dumps(data, ensure_ascii=False, indent=2))
    return OK


def cmd_inspecter(args):
    if not os.path.isfile(args.fichier):
        raise ErreurUthana(USAGE, f"Fichier introuvable : {args.fichier}")
    controle = inspecter_glb(args.fichier)
    dire(resume_controle(controle))
    dire(json.dumps(controle, ensure_ascii=False, indent=2))
    return OK


# ---------------------------------------------------------------------------
# Ligne de commande
# ---------------------------------------------------------------------------

def analyseur():
    p = argparse.ArgumentParser(prog="uthana.py", description="Client de l'API Uthana (voir SKILL.md).")
    p.add_argument("--api", help="URL de base (défaut : UTHANA_API_BASE ou https://uthana.com)")
    sous = p.add_subparsers(dest="commande", required=True, metavar="commande")

    def commande(nom, fonction, aide):
        sp = sous.add_parser(nom, help=aide, description=aide)
        sp.set_defaults(fonction=fonction)
        sp.add_argument("--api", help=argparse.SUPPRESS, default=argparse.SUPPRESS)
        sp.add_argument("--delai", type=float, default=300, help="délai de réponse HTTP en secondes (300)")
        return sp

    def generation(sp):
        sp.add_argument("--a-blanc", action="store_true", help="afficher la requête sans l'envoyer")

    def sortie_animation(sp, requise=True):
        sp.add_argument("--sortie", required=requise, help="fichier à écrire : .glb (conseillé), .fbx ou .bvh")
        sp.add_argument("--ecraser", action="store_true")
        sp.add_argument("--personnage", help="character_id, ou tar, ava, manny, quinn (défaut : tar)")
        sp.add_argument("--fps", type=int, default=30, help="24, 30 (défaut) ou 60")
        sp.add_argument("--sans-maillage", action="store_true", help="squelette et animation seulement")
        sp.add_argument("--sur-place", action="store_true", help="sans déplacement horizontal de la racine")
        sp.add_argument("--torse", action="store_true", help="bas du corps immobile")
        sp.add_argument("--vitesse-lecture", type=float, help="multiplicateur de vitesse, 0 à 2")

    commande("verifier", cmd_verifier, "vérifier la clé, l'accès réseau et le solde")
    commande("prix", cmd_prix, "barème actuel par modèle")
    sp = commande("depenses", cmd_depenses, "dernières opérations du portefeuille")
    sp.add_argument("--limite", type=int, default=20)

    commande("personnages", cmd_personnages, "personnages fournis et personnages du compte")
    sp = commande("importer", cmd_importer, "envoyer un personnage FBX ou GLB, avec rigging automatique")
    sp.add_argument("fichier")
    sp.add_argument("--nom")
    sp.add_argument("--sans-rig", action="store_true", help="ne pas rigger (le fichier a déjà un squelette)")
    sp.add_argument("--squelette", choices=("ue5", "r15"), help="refaire le squelette en UE5 ou Roblox R15")
    sp.add_argument("--sans-doigts", action="store_true")
    sp.add_argument("--pieds-au-sol", action="store_true", help="pieds au sol dans la pose de repos")
    sp.add_argument("--sans-prefixe", action="store_true", help="retirer le préfixe « mixamorig: » des os")
    sp.add_argument("--sans-face-avant", action="store_true", help="ne pas tourner le personnage vers l'avant")
    sp.add_argument("--sortie", help="télécharger aussi le personnage rigué (.glb ou .fbx)")
    sp.add_argument("--ecraser", action="store_true")
    generation(sp)
    sp = commande("telecharger-personnage", cmd_telecharger_personnage, "télécharger un personnage (gratuit)")
    sp.add_argument("personnage")
    sp.add_argument("--sortie", required=True)
    sp.add_argument("--ecraser", action="store_true")

    sp = commande("texte", cmd_texte, "animation depuis une description")
    sp.add_argument("prompt")
    sp.add_argument("--modele", choices=tuple(MODELES_TEXTE), default=MODELE_TEXTE_DEFAUT)
    sp.add_argument("--duree", type=float, help="secondes : 4–10 (3.0), 5–10 (3.0-lite, 3.0-mini)")
    sp.add_argument("--sans-reecriture", action="store_true", help="ne pas réécrire le prompt (modèles 3.0)")
    sp.add_argument("--rapide", action="store_true", help="variante rapide (modèles 3.0)")
    sp.add_argument("--graine", type=int, help="modèle 2.0")
    sp.add_argument("--ik-pieds", action="store_true", help="modèles 1.0 et 2.0")
    sp.add_argument("--sans-attendre", action="store_true")
    sp.add_argument("--attente", type=float, default=600, help="attente maximale de la tâche (600 s)")
    sortie_animation(sp)
    generation(sp)

    sp = commande("video", cmd_video, "animation depuis une vidéo d'une personne")
    sp.add_argument("fichier")
    sp.add_argument("--nom")
    sp.add_argument("--modele", choices=MODELES_VIDEO, default=MODELES_VIDEO[0])
    sp.add_argument("--mains", action="store_true", help="mains de meilleure qualité (plus long)")
    sp.add_argument("--sans-attendre", action="store_true")
    sp.add_argument("--attente", type=float, default=900)
    sortie_animation(sp)
    generation(sp)

    sp = commande("locomotion", cmd_locomotion, "marche ou course dans une direction, faite pour boucler")
    sp.add_argument("--foulees", type=int, default=4, help="paires de pas, 1 à 5 (4)")
    sp.add_argument("--vitesse", type=float, default=1.2, help="m/s, 0,25 à 8 (1,2)")
    sp.add_argument("--style", default="neutral_male_a", help="voir `styles`")
    sp.add_argument("--angle", type=float, default=0, help="degrés : 0 avant, 90 droite, -90 gauche, 180 arrière")
    sortie_animation(sp)
    generation(sp)
    commande("styles", cmd_styles, "styles de locomotion disponibles")

    sp = commande("boucler", cmd_boucler, "rendre une animation bouclable")
    sp.add_argument("motion_id")
    sp.add_argument("--mode", choices=("closed", "open"), default="closed",
                    help="closed : revient au point de départ ; open : avance à chaque cycle")
    sp.add_argument("--debut", type=float, help="début, fraction 0–1")
    sp.add_argument("--fin", type=float, help="fin, fraction 0–1")
    sp.add_argument("--zone", type=float, help="durée de la zone de raccord en s (2)")
    sp.add_argument("--zone-mode", choices=("modify", "extend"))
    sortie_animation(sp)
    generation(sp)

    sp = commande("enchainer", cmd_enchainer, "enchaîner deux animations avec une transition")
    sp.add_argument("premier")
    sp.add_argument("second")
    sp.add_argument("--transition", type=float, help="durée de transition, 0,1 à 3 s (1)")
    sortie_animation(sp)
    generation(sp)

    sp = commande("telecharger", cmd_telecharger, "retélécharger une animation existante (gratuit)")
    sp.add_argument("motion_id")
    sortie_animation(sp)
    sp = commande("statut", cmd_statut, "état d'une tâche ; avec --sortie, télécharge si elle est finie")
    sp.add_argument("job_id")
    sortie_animation(sp, requise=False)
    sp = commande("taches", cmd_taches, "tâches du compte")
    sp.add_argument("--methode", help="TextToMotion, VideoToMotion…")
    sp.add_argument("--limite", type=int, default=20)
    sp = commande("animations", cmd_animations, "animations du compte")
    sp.add_argument("--recherche")
    sp.add_argument("--source", choices=("mine", "uthana", "all"), default="mine")
    sp.add_argument("--limite", type=int, default=20)

    sp = commande("brut", cmd_brut, "opération GraphQL que le script ne connaît pas")
    sp.add_argument("query", help="texte GraphQL, ou @fichier.graphql")
    sp.add_argument("--variables", help="JSON")
    generation(sp)
    sp = commande("inspecter", cmd_inspecter, "contrôler un GLB local (animations, os, maillages)")
    sp.add_argument("fichier")
    return p


def main(argv=None):
    args = analyseur().parse_args(sys.argv[1:] if argv is None else argv)
    try:
        return args.fonction(args)
    except ErreurUthana as exc:
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
