#!/usr/bin/env python3
"""Client en ligne de commande de l'API Tripo 3D (apiv3), bibliothèque standard uniquement.

Sous-commandes :
  compte      verifier, consommation, envoyer
  modèles     texte, image, multivue
  images      image-texte, image-image, image-multivue, editer-multivue, splat, profondeur
  traitement  retexturer, convertir, importer, decimer, uv, segmenter, segmenter-intelligent, completer
  animation   riggable, rigger, animer
  tâches      statut, taches, telecharger, brut
  local       inspecter
La clé est lue dans la variable d'environnement TRIPO_API_KEY ; elle n'est jamais affichée.
Lancer `tripo.py <sous-commande> --help` pour les options, et voir ../SKILL.md pour l'usage.
"""

import argparse
import datetime
import hashlib
import json
import math
import os
import socket
import ssl
import struct
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

API_BASE_DEFAUT = "https://openapi.tripo3d.ai"
# Hôte des fichiers signalé pour l'apiv3 (non confirmé par la documentation officielle) :
# l'hôte réel de chaque modèle est noté dans le champ hote_fichier du .tripo.json.
HOTES_FICHIERS_DEFAUT = ["https://tripo-data.rg1.data.tripo3d.com"]
MODELE_DEFAUT = "v3.1-20260211"
FORMATS = ("glb", "fbx", "obj")
FORMATS_CONVERSION = ("gltf", "usdz", "fbx", "obj", "stl", "3mf")
EXTENSIONS_IMAGE = (".png", ".jpg", ".jpeg", ".webp")
EXTENSIONS_MODELE = (".glb", ".gltf", ".fbx", ".obj", ".stl")
TYPES_MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
    ".glb": "model/gltf-binary", ".gltf": "model/gltf+json",
}
TAILLE_MAX_IMAGE = 20 * 1024 * 1024
TAILLE_MAX_MODELE = 150 * 1024 * 1024
TAILLE_MAX_MULTIPART = 50 * 1024 * 1024
LONGUEUR_MAX_PROMPT = 1024
STATUTS_FINAUX = ("success", "failed", "cancelled", "banned", "expired")
AGENT = "tripo-plugin-quiche-lorraine-games/1"

# Codes de sortie (documentés dans SKILL.md).
OK = 0
ERREUR = 1           # erreur API inattendue, téléchargement impossible, fichier invalide
USAGE = 2            # argument invalide (aussi utilisé par argparse)
CLE = 3              # TRIPO_API_KEY absente ou refusée (401)
CREDITS = 4          # crédits insuffisants (code 2010)
RESEAU = 5           # hôte bloqué par la politique réseau ou injoignable
TACHE_ECHOUEE = 6    # tâche failed / cancelled / expired (crédits rendus par Tripo)
DELAI = 7            # délai d'attente dépassé (la tâche continue côté Tripo)
CONTENU_REFUSE = 8   # prompt ou image refusé par la modération (code 2008, statut banned)
LIMITE = 9           # trop de requêtes ou de tâches simultanées (HTTP 429)


class ErreurTripo(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


# ---------------------------------------------------------------------------
# Sortie : tout texte affiché passe par masquer(), pour que la clé n'apparaisse jamais.
# ---------------------------------------------------------------------------

def masquer(texte):
    texte = str(texte)
    cle = os.environ.get("TRIPO_API_KEY", "").strip()
    if cle:
        texte = texte.replace(cle, "***")
    return texte


def dire(texte=""):
    print(masquer(texte), flush=True)


def signaler(texte):
    print(masquer(texte), file=sys.stderr, flush=True)


def lire_cle():
    cle = os.environ.get("TRIPO_API_KEY", "").strip()
    if not cle:
        raise ErreurTripo(CLE, (
            "TRIPO_API_KEY n'est pas définie. Ajoute la clé Tripo en secret de l'environnement "
            "(variable TRIPO_API_KEY), puis ouvre une nouvelle session. Ne la colle pas dans le chat."))
    return cle


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

class _SansRedirection(urllib.request.HTTPRedirectHandler):
    """Les redirections sont suivies à la main : on sait ainsi quel hôte est contacté,
    et l'en-tête Authorization n'est jamais renvoyé vers un autre hôte."""

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
        return ErreurTripo(RESEAU, (
            f"Le domaine {nom} est bloqué par la politique réseau de l'environnement (403 du proxy). "
            f"Ajoute {nom} aux domaines autorisés de l'environnement, puis relance."))
    if "Tunnel connection failed" in texte:
        return ErreurTripo(RESEAU, (
            f"Le proxy n'a pas pu joindre {nom} ({texte}). Vérifie que ce domaine existe et qu'il est "
            "autorisé dans la politique réseau de l'environnement."))
    if isinstance(raison, socket.gaierror):
        return ErreurTripo(RESEAU, f"Hôte {nom} introuvable (DNS). Vérifie l'accès réseau de l'environnement.")
    if isinstance(raison, ssl.SSLError):
        return ErreurTripo(RESEAU, f"Échec TLS avec {nom} ({texte}). Vérifie les certificats de l'environnement.")
    if isinstance(raison, (socket.timeout, TimeoutError)):
        return ErreurTripo(RESEAU, f"{nom} ne répond pas (délai réseau dépassé). Réessaie plus tard.")
    return ErreurTripo(RESEAU, f"Impossible de joindre {nom} : {texte}.")


def requete(methode, url, corps=None, entetes=None, delai=60):
    """Renvoie (statut HTTP, en-têtes, corps en octets) sans lever sur les statuts >= 400."""
    req = urllib.request.Request(url, data=corps, method=methode, headers=dict(entetes or {}))
    req.add_header("User-Agent", AGENT)
    try:
        with _OUVREUR.open(req, timeout=delai) as rep:
            return rep.status, rep.headers, rep.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers, exc.read() or b""
    except (urllib.error.URLError, OSError) as exc:
        raise _erreur_reseau(url, exc) from None


class Api:
    def __init__(self, base, cle):
        self.base = base.rstrip("/")
        self.cle = cle

    def appel(self, methode, chemin, json_corps=None, multipart=None, essais=1):
        entetes = {
            "Authorization": f"Bearer {self.cle}",
            "Accept": "application/json",
        }
        corps = None
        if json_corps is not None:
            corps = json.dumps(json_corps).encode("utf-8")
            entetes["Content-Type"] = "application/json"
        elif multipart is not None:
            corps, type_contenu = multipart
            entetes["Content-Type"] = type_contenu
        url = self.base + chemin
        for essai in range(essais):
            statut, rep_entetes, brut = requete(methode, url, corps, entetes)
            if statut in (429, 502, 503, 504) and essai + 1 < essais:
                time.sleep(_attente_retry(rep_entetes, essai))
                continue
            break
        return _lire_enveloppe(statut, rep_entetes, brut)


def _attente_retry(entetes, essai):
    valeur = entetes.get("Retry-After") if entetes else None
    try:
        return min(max(float(valeur), 0.0), 10.0)
    except (TypeError, ValueError):
        return min(0.5 * (2 ** essai), 10.0)


def _lire_enveloppe(statut, entetes, brut):
    texte = brut.decode("utf-8", errors="replace")
    try:
        charge = json.loads(texte) if texte else {}
    except json.JSONDecodeError:
        charge = None
    trace = (entetes.get("X-Tripo-Trace-ID") if entetes else None) or ""
    if not isinstance(charge, dict):
        if statut == 401:
            raise _erreur_cle()
        raise ErreurTripo(ERREUR, f"Réponse inattendue de l'API Tripo (HTTP {statut}) : {texte[:200]}")
    code = charge.get("code")
    if statut < 400 and code in (0, None) and charge.get("status") != "error":
        return charge.get("data") if "data" in charge else charge
    raise _erreur_api(statut, code, charge.get("message") or "", charge.get("suggestion") or "", trace)


def _erreur_cle():
    return ErreurTripo(CLE, (
        "Tripo refuse la clé TRIPO_API_KEY (401). Vérifie-la dans la console Tripo (API Keys), "
        "mets à jour le secret de l'environnement, puis ouvre une nouvelle session."))


def _erreur_api(statut, code, message, suggestion, trace):
    if statut == 401 or code == 1002:
        return _erreur_cle()
    if code == 2010:
        return ErreurTripo(CREDITS, (
            "Crédits Tripo insuffisants pour cette tâche (code 2010) ; rien n'a été généré ni débité. "
            "Recharge le compte dans la console Tripo, puis relance."))
    if code == 2008:
        return ErreurTripo(CONTENU_REFUSE, (
            "Tripo refuse l'entrée au titre de sa politique de contenu (code 2008). "
            "Reformule le prompt ou change d'image."))
    if statut == 429 or code in (1007, 2000):
        return ErreurTripo(LIMITE, (
            f"Tripo limite les requêtes ou les tâches simultanées (HTTP {statut}, code {code}). "
            "Attends la fin des tâches en cours, puis relance."))
    detail = " ".join(part for part in (message, suggestion) if part)
    suffixe = f" (trace {trace})" if trace else ""
    return ErreurTripo(ERREUR, f"Erreur de l'API Tripo (HTTP {statut}, code {code}) : {detail}{suffixe}")



def _multipart(champ, chemin):
    frontiere = "----tripo" + uuid.uuid4().hex
    nom = os.path.basename(chemin)
    type_fichier = TYPES_MIME.get(os.path.splitext(nom)[1].lower(), "application/octet-stream")
    with open(chemin, "rb") as f:
        contenu = f.read()
    corps = (
        f"--{frontiere}\r\n"
        f'Content-Disposition: form-data; name="{champ}"; filename="{nom}"\r\n'
        f"Content-Type: {type_fichier}\r\n\r\n"
    ).encode("utf-8") + contenu + f"\r\n--{frontiere}--\r\n".encode("utf-8")
    return corps, f"multipart/form-data; boundary={frontiere}"


# ---------------------------------------------------------------------------
# Fichiers d'entrée : envoi et résolution (fichier local, URL, file_token ou task_id)
# ---------------------------------------------------------------------------

def _controler_fichier(chemin, extensions):
    ext = os.path.splitext(chemin)[1].lower()
    if ext not in extensions:
        raise ErreurTripo(USAGE, f"{chemin} : extension {ext or '(aucune)'} non acceptée ici "
                                 f"({', '.join(extensions)}).")
    taille = os.path.getsize(chemin)
    limite = TAILLE_MAX_IMAGE if ext in EXTENSIONS_IMAGE else TAILLE_MAX_MODELE
    if taille > limite:
        raise ErreurTripo(USAGE, f"{chemin} dépasse {limite // (1024 * 1024)} Mo, la limite de Tripo.")
    return taille


def envoyer_fichier(api, chemin):
    """Envoie un fichier local et renvoie son file_token (multipart jusqu'à 50 Mo, URL pré-signée au-delà)."""
    if os.path.getsize(chemin) <= TAILLE_MAX_MULTIPART:
        data = api.appel("POST", "/v3/files", multipart=_multipart("file", chemin))
        jeton = data.get("file_token") if isinstance(data, dict) else None
        if not jeton:
            raise ErreurTripo(ERREUR, f"Envoi de {chemin} : réponse sans file_token.")
        return str(jeton)
    ext = os.path.splitext(chemin)[1].lstrip(".").lower()
    data = api.appel("POST", "/v3/files/presign", json_corps={"format": ext})
    url = (data.get("presigned_url") or data.get("upload_url")) if isinstance(data, dict) else None
    jeton = data.get("file_token") if isinstance(data, dict) else None
    if not url or not jeton:
        raise ErreurTripo(ERREUR, f"Envoi de {chemin} : réponse de pré-signature incomplète.")
    with open(chemin, "rb") as f:
        contenu = f.read()
    statut, _, _ = requete("PUT", url, contenu, {
        "Content-Type": TYPES_MIME.get("." + ext, "application/octet-stream"),
        "Content-Length": str(len(contenu)),
    }, delai=600)
    if statut >= 400:
        raise ErreurTripo(ERREUR, f"Envoi de {chemin} vers {hote(url)} refusé (HTTP {statut}).")
    return str(jeton)


class Entrees:
    """Résout les entrées d'une commande et garde leur description pour le .tripo.json."""

    def __init__(self, api, a_blanc):
        self.api = api
        self.a_blanc = a_blanc
        self.liste = []
        self.jetons = {}

    def resoudre(self, valeur, role, extensions=EXTENSIONS_IMAGE, references=True):
        valeur = str(valeur).strip()
        if not valeur:
            raise ErreurTripo(USAGE, f"Entrée « {role} » vide.")
        if os.path.isfile(valeur):
            taille = _controler_fichier(valeur, extensions)
            with open(valeur, "rb") as f:
                empreinte = hashlib.sha256(f.read()).hexdigest()
            self.liste.append({"role": role, "fichier": valeur, "octets": taille, "sha256": empreinte})
            if self.a_blanc:
                return f"<file_token de {os.path.basename(valeur)}>"
            jeton = envoyer_fichier(self.api, valeur)
            self.jetons[jeton] = f"<fichier envoyé : {role}>"
            signaler(f"Fichier envoyé : {valeur}")
            return jeton
        if valeur.startswith(("http://", "https://")):
            self.liste.append({"role": role, "url": valeur})
            return valeur
        if os.sep in valeur or "/" in valeur or os.path.splitext(valeur)[1] and not valeur.startswith("file_"):
            raise ErreurTripo(USAGE, f"Fichier introuvable : {valeur}")
        if not references:
            raise ErreurTripo(USAGE, f"« {role} » attend un fichier local ou une URL, pas une référence ({valeur}).")
        nature = "file_token" if valeur.startswith("file_") else "task_id"
        self.liste.append({"role": role, nature: valeur})
        return valeur



# ---------------------------------------------------------------------------
# Tâches
# ---------------------------------------------------------------------------

def creer_tache(api, chemin, corps):
    data = api.appel("POST", chemin, json_corps=corps)
    task_id = data.get("task_id") if isinstance(data, dict) else None
    if not task_id:
        raise ErreurTripo(ERREUR, f"Réponse de création sans task_id : {data!r}")
    return str(task_id)


def lire_tache(api, task_id):
    data = api.appel("GET", f"/v3/tasks/{urllib.parse.quote(task_id)}", essais=3)
    if not isinstance(data, dict):
        raise ErreurTripo(ERREUR, f"Réponse de tâche inattendue : {data!r}")
    return data


def attendre(api, task_id, delai, intervalle):
    debut = time.monotonic()
    pause = max(intervalle, 0.01)
    dernier = None
    echecs = 0
    while True:
        try:
            tache = lire_tache(api, task_id)
            echecs = 0
        except ErreurTripo as exc:
            # Une coupure passagère ne doit pas faire perdre le suivi d'une tâche déjà payée.
            echecs += 1
            if exc.code not in (RESEAU, LIMITE, ERREUR) or echecs >= 4:
                raise
            signaler(f"Suivi de {task_id} interrompu ({exc.message}) ; nouvel essai.")
            time.sleep(min(pause, 15.0))
            continue
        statut = str(tache.get("status") or "unknown").lower()
        progression = tache.get("progress")
        etat = (statut, progression)
        if etat != dernier:
            signaler(f"Tâche {task_id} : {statut}" + (f" ({progression} %)" if progression is not None else ""))
            dernier = etat
        if statut in STATUTS_FINAUX:
            return tache
        reste = delai - (time.monotonic() - debut)
        if reste <= 0:
            raise ErreurTripo(DELAI, (
                f"Délai de {delai:g} s dépassé : la tâche {task_id} est encore « {statut} » côté Tripo. "
                f"Ne relance pas de génération : récupère-la plus tard avec "
                f"`tripo.py telecharger {task_id} --sortie <fichier>`."))
        time.sleep(min(pause, reste))
        pause = min(pause * 1.5, 15.0)


def verifier_succes(tache):
    statut = str(tache.get("status") or "").lower()
    if statut == "success":
        return
    task_id = tache.get("task_id", "?")
    detail = tache.get("error_msg") or tache.get("error_message") or ""
    code = tache.get("error_code")
    precision = " : " + " ".join(str(p) for p in (code, detail) if p) if (code or detail) else ""
    if statut == "banned":
        raise ErreurTripo(CONTENU_REFUSE, (
            f"Tâche {task_id} refusée par la modération Tripo{precision}. Reformule le prompt ou change d'image."))
    raise ErreurTripo(TACHE_ECHOUEE, (
        f"La tâche {task_id} a échoué (statut « {statut} »){precision}. Tripo ne débite pas les tâches "
        "échouées. Ajuste le prompt ou l'image avant de proposer une nouvelle tentative."))



def telecharger_fichier(url, destination, task_id):
    for _ in range(5):
        statut, entetes, brut = requete("GET", url, delai=300)
        if statut in (301, 302, 303, 307, 308) and entetes.get("Location"):
            url = urllib.parse.urljoin(url, entetes["Location"])
            continue
        break
    if statut != 200:
        raise ErreurTripo(ERREUR, (
            f"Téléchargement refusé par {hote(url)} (HTTP {statut}). Les URL de Tripo expirent vite : "
            f"relance `tripo.py telecharger {task_id} --sortie {destination}` (pas de nouvelle génération)."))
    dossier = os.path.dirname(os.path.abspath(destination))
    os.makedirs(dossier, exist_ok=True)
    temporaire = destination + ".part"
    with open(temporaire, "wb") as f:
        f.write(brut)
    os.replace(temporaire, destination)
    return hote(url), len(brut)


# ---------------------------------------------------------------------------
# Inspection d'un GLB (poids, triangles, dimensions)
# ---------------------------------------------------------------------------

def _mat_mul(a, b):
    return [sum(a[r + 4 * k] * b[k + 4 * c] for k in range(4)) for c in range(4) for r in range(4)]


def _mat_noeud(noeud):
    if "matrix" in noeud:
        return [float(x) for x in noeud["matrix"]]
    tx, ty, tz = noeud.get("translation", [0, 0, 0])
    qx, qy, qz, qw = noeud.get("rotation", [0, 0, 0, 1])
    sx, sy, sz = noeud.get("scale", [1, 1, 1])
    rot = [
        1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy + qz * qw), 2 * (qx * qz - qy * qw), 0,
        2 * (qx * qy - qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz + qx * qw), 0,
        2 * (qx * qz + qy * qw), 2 * (qy * qz - qx * qw), 1 - 2 * (qx * qx + qy * qy), 0,
        0, 0, 0, 1,
    ]
    echelle = [sx, 0, 0, 0, 0, sy, 0, 0, 0, 0, sz, 0, 0, 0, 0, 1]
    translation = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, tx, ty, tz, 1]
    return _mat_mul(translation, _mat_mul(rot, echelle))


def _dimensions_image(octets):
    if octets[:8] == b"\x89PNG\r\n\x1a\n" and len(octets) >= 24:
        return struct.unpack(">II", octets[16:24])
    if octets[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(octets):
            if octets[i] != 0xFF:
                i += 1
                continue
            marqueur = octets[i + 1]
            if marqueur in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                hauteur, largeur = struct.unpack(">HH", octets[i + 5:i + 9])
                return largeur, hauteur
            if marqueur in (0xD8, 0x01) or 0xD0 <= marqueur <= 0xD7:
                i += 2
                continue
            i += 2 + struct.unpack(">H", octets[i + 2:i + 4])[0]
    return None


def inspecter_glb(chemin):
    with open(chemin, "rb") as f:
        donnees = f.read()
    if len(donnees) < 20 or donnees[:4] != b"glTF":
        raise ErreurTripo(ERREUR, f"{chemin} n'est pas un fichier GLB valide (en-tête « glTF » absent).")
    _, version, _ = struct.unpack("<4sII", donnees[:12])
    longueur, type_bloc = struct.unpack("<II", donnees[12:20])
    if type_bloc != 0x4E4F534A:
        raise ErreurTripo(ERREUR, f"{chemin} : premier bloc GLB non JSON.")
    gltf = json.loads(donnees[20:20 + longueur].decode("utf-8"))
    binaire = b""
    debut_bin = 20 + longueur
    if len(donnees) >= debut_bin + 8:
        lg_bin, type_bin = struct.unpack("<II", donnees[debut_bin:debut_bin + 8])
        if type_bin == 0x004E4942:
            binaire = donnees[debut_bin + 8:debut_bin + 8 + lg_bin]

    accesseurs = gltf.get("accessors", [])
    maillages = gltf.get("meshes", [])
    noeuds = gltf.get("nodes", [])

    def triangles_maillage(maillage):
        total = 0
        for prim in maillage.get("primitives", []):
            mode = prim.get("mode", 4)
            if "indices" in prim:
                n = accesseurs[prim["indices"]].get("count", 0)
            else:
                n = accesseurs[prim.get("attributes", {}).get("POSITION", 0)].get("count", 0) if accesseurs else 0
            total += n // 3 if mode == 4 else max(n - 2, 0) if mode in (5, 6) else 0
        return total

    sommets = sum(
        accesseurs[p["attributes"]["POSITION"]].get("count", 0)
        for m in maillages for p in m.get("primitives", []) if "POSITION" in p.get("attributes", {}))

    triangles = 0
    mini = [math.inf] * 3
    maxi = [-math.inf] * 3
    identite = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    scenes = gltf.get("scenes") or [{"nodes": list(range(len(noeuds)))}]
    racines = scenes[gltf.get("scene", 0)].get("nodes", [])
    pile = [(i, identite) for i in racines]
    while pile:
        index, parent = pile.pop()
        noeud = noeuds[index]
        monde = _mat_mul(parent, _mat_noeud(noeud))
        if "mesh" in noeud:
            maillage = maillages[noeud["mesh"]]
            triangles += triangles_maillage(maillage)
            for prim in maillage.get("primitives", []):
                acc = accesseurs[prim.get("attributes", {}).get("POSITION", -1)] if "POSITION" in prim.get("attributes", {}) else {}
                if "min" not in acc or "max" not in acc:
                    continue
                for coin in [(x, y, z) for x in (acc["min"][0], acc["max"][0])
                             for y in (acc["min"][1], acc["max"][1]) for z in (acc["min"][2], acc["max"][2])]:
                    for axe in range(3):
                        v = sum(monde[axe + 4 * k] * coin[k] for k in range(3)) + monde[axe + 12]
                        mini[axe] = min(mini[axe], v)
                        maxi[axe] = max(maxi[axe], v)
        pile.extend((enfant, monde) for enfant in noeud.get("children", []))

    textures = []
    for image in gltf.get("images", []):
        taille = None
        dims = None
        if "bufferView" in image and binaire:
            vue = gltf["bufferViews"][image["bufferView"]]
            debut = vue.get("byteOffset", 0)
            octets = binaire[debut:debut + vue["byteLength"]]
            taille = len(octets)
            dims = _dimensions_image(octets)
        textures.append({
            "type": image.get("mimeType", "?"),
            "octets": taille,
            "resolution": f"{dims[0]}x{dims[1]}" if dims else None,
        })

    dimensions = None
    if mini[0] != math.inf:
        dimensions = [round(maxi[i] - mini[i], 4) for i in range(3)]
    return {
        "fichier_octets": len(donnees),
        "gltf_version": version,
        "triangles": triangles,
        "sommets": sommets,
        "maillages": len(maillages),
        "materiaux": len(gltf.get("materials", [])),
        "textures": textures,
        "dimensions_m": dimensions,
        "extensions_requises": gltf.get("extensionsRequired", []),
    }


def resume_controle(controle):
    morceaux = [_taille_lisible(controle["fichier_octets"]), f"{controle['triangles']:,} triangles".replace(",", " ")]
    if controle["dimensions_m"]:
        x, y, z = controle["dimensions_m"]
        morceaux.append(f"{x:g} × {y:g} × {z:g} m (x × y × z)")
    else:
        morceaux.append("dimensions inconnues")
    textures = controle["textures"]
    if textures:
        resolutions = sorted({t["resolution"] for t in textures if t["resolution"]})
        morceaux.append(f"{len(textures)} texture(s)" + (f" {', '.join(resolutions)}" if resolutions else ""))
    else:
        morceaux.append("sans texture")
    return ", ".join(morceaux)


def _taille_lisible(octets):
    if octets >= 1024 * 1024:
        return f"{octets / (1024 * 1024):.1f} Mo".replace(".", ",")
    return f"{octets / 1024:.0f} Ko"


# ---------------------------------------------------------------------------
# Fichier .tripo.json
# ---------------------------------------------------------------------------

def chemin_fiche(sortie):
    racine, _ = os.path.splitext(sortie)
    return racine + ".tripo.json"


def ecrire_fiche(sortie, fiche):
    chemin = chemin_fiche(sortie)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(masquer(json.dumps(fiche, ensure_ascii=False, indent=2)) + "\n")
    return chemin


def lire_fiche(sortie):
    try:
        with open(chemin_fiche(sortie), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def maintenant():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()




# ---------------------------------------------------------------------------
# Sorties d'une tâche : collecte des URL, téléchargement, contrôle
# ---------------------------------------------------------------------------

CLES_MODELE = ("model_url", "pbr_model_url", "model", "pbr_model", "base_model_url", "base_model")
CLES_IMAGE = ("generated_image_url", "image_url", "generated_image", "image")
CLES_PROFONDEUR = ("depth_image_url", "depth_image")
EXT_PAR_DEFAUT = {"video": ".mp4", "image": ".png", "render": ".png", "depth": ".png", "view": ".png"}

# Nature de la sortie principale selon le type de tâche renvoyé par l'API.
NATURE_PAR_TYPE = {
    "text_to_image": "image", "generate_image": "image", "image_to_image": "image",
    "generate_multiview_image": "multivue", "image_to_multiview": "multivue",
    "edit_multiview_image": "multivue", "edit_multiview": "multivue",
    "image_to_depth": "profondeur", "image_to_splat": "splat",
}


def _etiquette(texte):
    texte = str(texte).lower().replace("preset:", "")
    return "".join(c if c.isalnum() else "_" for c in texte).strip("_") or "x"


def collecter_urls(sortie):
    """Renvoie [(clé d'origine, nom de fichier court, url)] pour toutes les URL d'une sortie, sans doublon."""
    trouves = []

    def ajouter(cle, nom, url):
        if isinstance(url, str) and url.startswith(("http://", "https://")) and url not in [u for _, _, u in trouves]:
            trouves.append((cle, _etiquette(nom), url))

    def parcourir(objet):
        for cle, valeur in (objet or {}).items():
            nom = cle[:-4] if cle.endswith("_url") else cle[:-5] if cle.endswith("_urls") else cle
            if isinstance(valeur, str):
                ajouter(cle, nom, valeur)
            elif isinstance(valeur, dict):
                parcourir(valeur)
            elif isinstance(valeur, list):
                for i, element in enumerate(valeur, 1):
                    if isinstance(element, str):
                        ajouter(cle, f"{nom}_{i}", element)
                    elif isinstance(element, dict):
                        url = element.get("url") or element.get("model_url")
                        etiquette = element.get("animation") or element.get("name") or i
                        if url:
                            ajouter(cle, f"{nom}_{etiquette}", url)
                        else:
                            parcourir(element)

    parcourir(sortie if isinstance(sortie, dict) else {})
    return trouves


def _principale(urls, nature):
    cles = {"modele": CLES_MODELE, "image": CLES_IMAGE, "profondeur": CLES_PROFONDEUR,
            "splat": CLES_MODELE, "multivue": ()}[nature]
    for cle_voulue in cles:
        for entree in urls:
            if entree[0] == cle_voulue:
                return entree
    if nature == "modele":
        # Sortie sans clé connue (ex. model_urls d'une animation) : seul fichier 3D, s'il est unique.
        modeles = [e for e in urls if not any(m in e[1] for m in ("image", "render", "video", "view", "depth"))]
        if len(modeles) == 1:
            return modeles[0]
    if nature == "splat" and urls:
        return urls[0]
    return None


def deviner_nature(tache):
    nature = NATURE_PAR_TYPE.get(str(tache.get("type") or ""))
    if nature:
        return nature
    urls = collecter_urls(tache.get("output"))
    cles = {c for c, _, _ in urls}
    if cles & set(CLES_MODELE) or any(c.endswith("_urls") for c in cles):
        return "modele"
    if cles & set(CLES_IMAGE):
        return "image"
    if cles & set(CLES_PROFONDEUR):
        return "profondeur"
    return "multivue" if urls else "modele"


def _extension_url(url, nom):
    ext = os.path.splitext(urllib.parse.urlsplit(url).path)[1].lower()
    if ext:
        return ext
    for indice, defaut in EXT_PAR_DEFAUT.items():
        if indice in nom:
            return defaut
    return ".glb"


def telecharger_sorties(tache, sortie, nature, task_id, principale_requise=True):
    """Télécharge la sortie principale dans `sortie` et les autres à côté (<base>_<nom><ext>)."""
    urls = collecter_urls(tache.get("output"))
    principale = _principale(urls, nature)
    if principale is None and principale_requise and nature != "multivue":
        raise ErreurTripo(ERREUR, f"La tâche {task_id} est terminée mais ne donne pas de fichier "
                                  f"de type « {nature} ». Regarde `tripo.py statut {task_id}`.")
    racine = os.path.splitext(sortie)[0]
    fichiers = []
    for cle, nom, url in urls:
        est_principale = principale is not None and url == principale[2]
        destination = sortie if est_principale else f"{racine}_{nom}{_extension_url(url, nom)}"
        if not est_principale and os.path.abspath(destination) == os.path.abspath(sortie):
            destination = f"{racine}_{nom}_2{_extension_url(url, nom)}"
        try:
            hote_fichier, octets = telecharger_fichier(url, destination, task_id)
        except ErreurTripo as exc:
            if est_principale or exc.code == RESEAU:
                raise
            signaler(f"Sortie secondaire « {nom} » non téléchargée : {exc.message}")
            continue
        fichiers.append({"role": "principale" if est_principale else nom, "fichier": destination,
                         "hote": hote_fichier, "octets": octets})
        if est_principale:
            ext_url = os.path.splitext(urllib.parse.urlsplit(url).path)[1].lower()
            ext_sortie = os.path.splitext(sortie)[1].lower()
            if ext_url and ext_url != ext_sortie:
                signaler(f"Attention : Tripo fournit un fichier {ext_url}, écrit sous {sortie}.")
    if principale is not None and nature in ("modele", "splat"):
        with open(sortie, "rb") as f:
            est_glb = f.read(4) == b"glTF"
        if est_glb != sortie.lower().endswith(".glb"):
            os.remove(sortie)
            raise ErreurTripo(USAGE, (
                f"Le fichier principal de la tâche {task_id} {'est' if est_glb else 'n’est pas'} un GLB, "
                f"ce qui ne correspond pas à {sortie}. Change l'extension de --sortie ; pour un autre format, "
                "passe par `convertir`, ou donne à `telecharger` le task_id de la conversion."))
    if not fichiers and principale_requise:
        raise ErreurTripo(ERREUR, f"La tâche {task_id} ne donne aucun fichier à télécharger.")
    return fichiers


# ---------------------------------------------------------------------------
# Exécution commune d'une tâche : création, suivi, téléchargement, fiche
# ---------------------------------------------------------------------------

def base_api(args):
    return (args.api or os.environ.get("TRIPO_API_BASE") or API_BASE_DEFAUT).rstrip("/")


def hotes_fichiers(args):
    if args.hote_fichiers:
        valeurs = args.hote_fichiers
    elif os.environ.get("TRIPO_HOTES_FICHIERS"):
        valeurs = [v.strip() for v in os.environ["TRIPO_HOTES_FICHIERS"].split(",") if v.strip()]
    else:
        valeurs = HOTES_FICHIERS_DEFAUT
    return [v if "://" in v else "https://" + v for v in valeurs]


def _api(args):
    return Api(base_api(args), lire_cle())


def _contexte(args):
    """Api et résolveur d'entrées ; en mode --a-blanc, ni clé ni réseau."""
    a_blanc = getattr(args, "a_blanc", False)
    api = None if a_blanc else _api(args)
    return api, Entrees(api, a_blanc)


def _verifier_sortie(args, extensions=None):
    sortie = args.sortie
    if extensions and not sortie.lower().endswith(tuple(extensions)):
        raise ErreurTripo(USAGE, f"--sortie doit finir par {' ou '.join(extensions)}.")
    if os.path.exists(sortie) and not args.ecraser:
        raise ErreurTripo(USAGE, f"{sortie} existe déjà. Choisis un autre nom ou ajoute --ecraser.")


def _ajouter_params(corps, params):
    for brut in params or []:
        if "=" not in brut:
            raise ErreurTripo(USAGE, f"--param attend CLE=VALEUR, pas « {brut} ».")
        cle, valeur = brut.split("=", 1)
        cle = cle.strip()
        if cle in corps:
            raise ErreurTripo(USAGE, f"Le paramètre « {cle} » est déjà fixé par une option de la commande.")
        try:
            corps[cle] = json.loads(valeur)
        except json.JSONDecodeError:
            corps[cle] = valeur
    return corps


def _anonymiser(valeur, jetons):
    """Remplace dans les paramètres les file_token éphémères par le rôle de l'entrée."""
    if isinstance(valeur, str):
        return jetons.get(valeur, valeur)
    if isinstance(valeur, list):
        return [_anonymiser(v, jetons) for v in valeur]
    if isinstance(valeur, dict):
        return {k: _anonymiser(v, jetons) for k, v in valeur.items()}
    return valeur


def _a_blanc(chemin, corps):
    dire(f"À blanc : POST {chemin}")
    dire(json.dumps(corps, ensure_ascii=False, indent=2))
    dire("Aucune requête envoyée, aucun crédit consommé.")
    return OK


def executer(args, api, entrees, chemin, corps, nature, meta=None, conversion=None, principale_requise=True):
    _ajouter_params(corps, getattr(args, "param", None))
    if args.a_blanc:
        return _a_blanc(chemin, corps)
    task_id = creer_tache(api, chemin, corps)
    dire(f"Tâche créée : {task_id}")
    fiche = {
        "outil": "plugin tripo (quiche-lorraine-games), scripts/tripo.py",
        "date": maintenant(),
        "api": api.base,
        "operation": chemin,
        "task_id": task_id,
        "modele_tripo": corps.get("model"),
        **{k: v for k, v in (meta or {}).items() if v is not None},
        "entrees": entrees.liste,
        "parametres": _anonymiser(corps, entrees.jetons),
        "nature": nature,
        "fichier": os.path.basename(args.sortie),
        "etat": "en_cours",
    }
    if getattr(args, "sans_attendre", False):
        ecrire_fiche(args.sortie, fiche)
        dire(f"Sans attente. Récupère le résultat avec : tripo.py telecharger {task_id} --sortie {args.sortie}")
        return OK
    tache = attendre(api, task_id, args.delai, args.intervalle)
    verifier_succes(tache)
    return finaliser(args, api, tache, fiche, nature, conversion, principale_requise)


def finaliser(args, api, tache, fiche, nature, conversion=None, principale_requise=True):
    task_id = tache.get("task_id") or fiche["task_id"]
    tache_fichiers = tache
    if conversion:
        conversion_id = creer_tache(api, "/v3/models/convert", {"input": task_id, "format": conversion.upper()})
        dire(f"Conversion en {conversion.upper()} : tâche {conversion_id}")
        tache_fichiers = attendre(api, conversion_id, args.delai, args.intervalle)
        verifier_succes(tache_fichiers)
        fiche["conversion"] = {"task_id": conversion_id, "format": conversion,
                               "credits": tache_fichiers.get("credits_consumed")}
    fichiers = telecharger_sorties(tache_fichiers, args.sortie, nature, task_id, principale_requise)
    fiche.update({
        "etat": "telecharge",
        "date_telechargement": maintenant(),
        "credits": tache.get("credits_consumed"),
        "fichier": os.path.basename(args.sortie),
        "sorties": fichiers,
        "hote_fichier": fichiers[0]["hote"] if fichiers else None,
    })
    if not fiche.get("modele_tripo"):
        entree = tache.get("input") if isinstance(tache.get("input"), dict) else {}
        fiche["modele_tripo"] = entree.get("model") or tache.get("model_version")
    resume = None
    if os.path.exists(args.sortie) and args.sortie.lower().endswith(".glb"):
        controle = inspecter_glb(args.sortie)
        fiche["controle"] = controle
        resume = resume_controle(controle)
        limite = (fiche.get("parametres") or {}).get("face_limit")
        if isinstance(limite, int) and limite > 0 and controle["triangles"] > limite * 1.05:
            signaler(f"Attention : {controle['triangles']} triangles pour une limite demandée de {limite}.")
    chemin = ecrire_fiche(args.sortie, fiche)
    libelles = {"modele": "Modèle écrit", "image": "Image écrite", "profondeur": "Carte de profondeur écrite",
                "splat": "Splat écrit"}
    for f in fichiers:
        detail = resume if f["fichier"] == args.sortie and resume else _taille_lisible(f["octets"])
        libelle = libelles.get(nature, "Fichier écrit") if f["role"] == "principale" else f"Fichier écrit ({f['role']})"
        dire(f"{libelle} : {f['fichier']} ({detail})")
    if not fichiers:
        dire(f"Tâche {task_id} réussie, sans fichier à télécharger : réutilise son task_id.")
    dire(f"Fiche de traçabilité : {chemin}")
    return OK


# ---------------------------------------------------------------------------
# Compte
# ---------------------------------------------------------------------------

def cmd_verifier(args):
    premier_echec = None

    def echec(code):
        nonlocal premier_echec
        if premier_echec is None:
            premier_echec = code

    cle = os.environ.get("TRIPO_API_KEY", "").strip()
    if cle:
        dire("✓ TRIPO_API_KEY est définie (valeur masquée).")
    else:
        dire("✗ TRIPO_API_KEY n'est pas définie : ajoute-la en secret de l'environnement, "
             "puis ouvre une nouvelle session.")
        echec(CLE)

    base = base_api(args)
    acces_api = False
    for role, url in [("API", base)] + [("fichiers", u) for u in hotes_fichiers(args)]:
        try:
            statut, _, _ = requete("GET", url.rstrip("/") + "/", delai=15)
            dire(f"✓ {hote(url)} ({role}) est joignable (HTTP {statut}).")
            acces_api = acces_api or role == "API"
        except ErreurTripo as exc:
            dire(f"✗ {hote(url)} ({role}) : {exc.message}")
            echec(exc.code)

    if cle and acces_api:
        try:
            solde = Api(base, cle).appel("GET", "/v3/account/balance", essais=2)
            dire(f"✓ Clé acceptée. Crédits disponibles : {solde.get('balance')}, "
                 f"gelés par des tâches en cours : {solde.get('frozen')}.")
        except ErreurTripo as exc:
            dire(f"✗ {exc.message}")
            echec(exc.code)
    return premier_echec or OK


def cmd_consommation(args):
    api = _api(args)
    chemin = f"/v3/account/usage?limit={args.limite}&offset={args.decalage}"
    data = api.appel("GET", chemin, essais=2)
    lignes = data.get("items") if isinstance(data, dict) else data
    lignes = [l for l in (lignes or []) if isinstance(l, dict)]
    if not lignes:
        dire("Aucune tâche dans l'historique.")
        return OK
    total = 0.0
    for l in lignes:
        credits = l.get("credits_consumed")
        try:
            total += float(credits or 0)
        except (TypeError, ValueError):
            pass
        dire(f"{l.get('created_at', '?')}  {l.get('task_id', '?')}  {l.get('type', '?')}  "
             f"{l.get('status', '?')}  {credits if credits is not None else '?'} crédits")
    dire(f"Total sur ces {len(lignes)} tâches : {total:g} crédits.")
    return OK


def cmd_envoyer(args):
    if not os.path.isfile(args.fichier):
        raise ErreurTripo(USAGE, f"Fichier introuvable : {args.fichier}")
    _controler_fichier(args.fichier, EXTENSIONS_IMAGE + EXTENSIONS_MODELE)
    jeton = envoyer_fichier(_api(args), args.fichier)
    dire(f"file_token : {jeton}")
    dire("Ce jeton remplace le fichier comme entrée d'une autre commande (il n'est pas permanent).")
    return OK


# ---------------------------------------------------------------------------
# Génération de modèles : texte, image, multivue
# ---------------------------------------------------------------------------

def _parametres_generation(args, depuis_image):
    if args.parties and (not args.sans_texture or args.quad or args.low_poly):
        raise ErreurTripo(USAGE, "--parties exige --sans-texture, sans --quad ni --low-poly (règle de Tripo).")
    if args.quad and args.format != "fbx":
        raise ErreurTripo(USAGE, "--quad produit un FBX : ajoute --format fbx et une --sortie en .fbx.")
    corps = {"model": args.modele}
    texture = not args.sans_texture
    corps["texture"] = texture
    corps["pbr"] = texture and not args.sans_pbr
    if texture and args.qualite_texture:
        corps["texture_quality"] = args.qualite_texture
    if texture and args.version_texture:
        corps["texture_version"] = args.version_texture
    if args.qualite_geometrie:
        corps["geometry_quality"] = args.qualite_geometrie
    if args.faces is not None:
        if args.faces <= 0:
            raise ErreurTripo(USAGE, "--faces doit être un entier positif.")
        corps["face_limit"] = args.faces
    for option, champ in (("taille_auto", "auto_size"), ("low_poly", "smart_low_poly"),
                          ("quad", "quad"), ("parties", "generate_parts")):
        if getattr(args, option):
            corps[champ] = True
    if args.graine is not None:
        corps["model_seed"] = args.graine
        if texture:
            corps["texture_seed"] = args.graine
    if depuis_image:
        if args.orientation:
            corps["orientation"] = args.orientation
        if texture and args.alignement_texture:
            corps["texture_alignment"] = args.alignement_texture
    return corps


def _conversion(args):
    return args.format if args.format != "glb" and not args.quad else None


def cmd_texte(args):
    prompt = args.prompt.strip()
    if not prompt:
        raise ErreurTripo(USAGE, "Le prompt est vide.")
    if len(prompt) > LONGUEUR_MAX_PROMPT:
        raise ErreurTripo(USAGE, f"Le prompt dépasse {LONGUEUR_MAX_PROMPT} caractères ({len(prompt)}).")
    _verifier_sortie(args, ["." + args.format])
    corps = {"prompt": prompt}
    if args.negatif:
        corps["negative_prompt"] = args.negatif
    corps.update(_parametres_generation(args, depuis_image=False))
    if args.graine is not None:
        corps["image_seed"] = args.graine
    meta = {"type": "text_to_model", "prompt": prompt}
    if args.negatif:
        meta["negatif"] = args.negatif
    api, entrees = _contexte(args)
    return executer(args, api, entrees, "/v3/generation/text-to-model", corps, "modele", meta, _conversion(args))


def cmd_image(args):
    _verifier_sortie(args, ["." + args.format])
    corps = _parametres_generation(args, depuis_image=True)
    if args.autofix:
        corps["enable_image_autofix"] = True
    api, entrees = _contexte(args)
    corps = {"input": entrees.resoudre(args.chemin, "image"), **corps}
    return executer(args, api, entrees, "/v3/generation/image-to-model", corps, "modele",
                    {"type": "image_to_model"}, _conversion(args))


def cmd_multivue(args):
    _verifier_sortie(args, ["." + args.format])
    corps = _parametres_generation(args, depuis_image=True)
    api, entrees = _contexte(args)
    if args.depuis_tache:
        if any((args.face, args.gauche, args.dos, args.droite)):
            raise ErreurTripo(USAGE, "--depuis-tache remplace --face, --gauche, --dos et --droite.")
        entrees.liste.append({"role": "vues", "task_id": args.depuis_tache})
        vues = [{"task_id": args.depuis_tache}]
    else:
        if not args.face:
            raise ErreurTripo(USAGE, "La vue de face (--face) est obligatoire, ou bien --depuis-tache.")
        vues = [None if v is None else entrees.resoudre(v, nom)
                for v, nom in ((args.face, "face"), (args.gauche, "gauche"), (args.dos, "dos"), (args.droite, "droite"))]
    corps = {"inputs": vues, **corps}
    return executer(args, api, entrees, "/v3/generation/multiview-to-model", corps, "modele",
                    {"type": "multiview_to_model"}, _conversion(args))


# ---------------------------------------------------------------------------
# Images : texte → image, image → image, multivue, splat, profondeur
# ---------------------------------------------------------------------------

def _options(corps, args, correspondance):
    for option, champ in correspondance:
        valeur = getattr(args, option, None)
        if valeur not in (None, False):
            corps[champ] = valeur
    return corps


def cmd_image_texte(args):
    _verifier_sortie(args, EXTENSIONS_IMAGE)
    corps = {"prompt": args.prompt}
    _options(corps, args, (("negatif", "negative_prompt"), ("modele", "model"), ("taille", "size"),
                           ("ratio", "aspect_ratio"), ("format_image", "output_format")))
    api, entrees = _contexte(args)
    return executer(args, api, entrees, "/v3/generation/text-to-image", corps, "image",
                    {"type": "text_to_image", "prompt": args.prompt})


def cmd_image_image(args):
    _verifier_sortie(args, EXTENSIONS_IMAGE)
    api, entrees = _contexte(args)
    references = [entrees.resoudre(v, f"reference_{i}") for i, v in enumerate(args.entrees, 1)]
    corps = {"input": references[0]} if len(references) == 1 else {"inputs": references}
    _options(corps, args, (("prompt", "prompt"), ("modele", "model"), ("gabarit", "template"),
                           ("t_pose", "t_pose"), ("croquis", "sketch_to_render")))
    if "prompt" not in corps and "template" not in corps:
        raise ErreurTripo(USAGE, "image-image demande --prompt ou --gabarit.")
    return executer(args, api, entrees, "/v3/generation/image-to-image", corps, "image",
                    {"type": "image_to_image", "prompt": args.prompt})


def cmd_image_multivue(args):
    _verifier_sortie(args, EXTENSIONS_IMAGE)
    api, entrees = _contexte(args)
    corps = {"input": entrees.resoudre(args.entree, "image")}
    return executer(args, api, entrees, "/v3/generation/image-to-multiview", corps, "multivue",
                    {"type": "image_to_multiview"})


def cmd_editer_multivue(args):
    _verifier_sortie(args, EXTENSIONS_IMAGE)
    prompts = []
    for brut in args.vue:
        vue, _, texte = brut.partition("=")
        if vue not in ("front", "left", "back", "right") or not texte.strip():
            raise ErreurTripo(USAGE, f"--vue attend front|left|back|right=texte, pas « {brut} ».")
        prompts.append({"view": vue, "prompt": texte.strip()})
    api, entrees = _contexte(args)
    entrees.liste.append({"role": "multivue", "task_id": args.task_id})
    corps = {"input": args.task_id, "prompts": prompts}
    return executer(args, api, entrees, "/v3/generation/edit-multiview", corps, "multivue",
                    {"type": "edit_multiview"})


def cmd_splat(args):
    _verifier_sortie(args)
    api, entrees = _contexte(args)
    corps = {"input": entrees.resoudre(args.entree, "image")}
    _options(corps, args, (("graine", "model_seed"),))
    return executer(args, api, entrees, "/v3/generation/image-to-splat", corps, "splat", {"type": "image_to_splat"})


def cmd_profondeur(args):
    _verifier_sortie(args, EXTENSIONS_IMAGE)
    if args.resolution is not None and not 126 <= args.resolution <= 2016:
        raise ErreurTripo(USAGE, "--resolution doit être entre 126 et 2016.")
    api, entrees = _contexte(args)
    corps = {"input": entrees.resoudre(args.entree, "image")}
    _options(corps, args, (("type_profondeur", "kind"), ("resolution", "process_res")))
    return executer(args, api, entrees, "/v3/generation/image-to-depth", corps, "profondeur",
                    {"type": "image_to_depth"})


# ---------------------------------------------------------------------------
# Traitement de modèles
# ---------------------------------------------------------------------------

def _pieces(args):
    return [p.strip() for p in args.pieces.split(",") if p.strip()] if getattr(args, "pieces", None) else None


def _entree_modele(entrees, valeur, role="modele"):
    return entrees.resoudre(valeur, role, extensions=EXTENSIONS_MODELE)


def cmd_retexturer(args):
    _verifier_sortie(args, [".glb"])
    api, entrees = _contexte(args)
    corps = {"input": _entree_modele(entrees, args.entree)}
    _options(corps, args, (("modele", "model"), ("qualite_texture", "texture_quality"),
                           ("alignement_texture", "texture_alignment")))
    corps["texture"] = True
    corps["pbr"] = not args.sans_pbr
    if args.graine is not None:
        corps["texture_seed"] = args.graine
    if _pieces(args):
        corps["part_names"] = _pieces(args)
    if args.sans_cuisson:
        corps["bake"] = False
    guide = {}
    if args.prompt_texture:
        guide["text"] = args.prompt_texture
    if args.image_texture:
        guide["image"] = entrees.resoudre(args.image_texture, "image_texture")
    if args.image_style:
        guide["style_image"] = entrees.resoudre(args.image_style, "image_style")
    if guide:
        corps["texture_prompt"] = guide
    return executer(args, api, entrees, "/v3/models/texture", corps, "modele",
                    {"type": "texture_model", "prompt": args.prompt_texture})


def cmd_convertir(args):
    _verifier_sortie(args, ["." + args.format])
    api, entrees = _contexte(args)
    entrees.liste.append({"role": "modele", "task_id": args.task_id})
    corps = {"input": args.task_id, "format": args.format.upper()}
    if args.faces is not None and args.faces > 0:
        corps["face_limit"] = args.faces
    _options(corps, args, (("quad", "quad"), ("taille_texture", "texture_size"), ("format_texture", "texture_format"),
                           ("echelle", "scale_factor"), ("pivot_bas", "pivot_to_center_bottom"),
                           ("aplatir_base", "flatten_bottom"), ("orientation_export", "export_orientation"),
                           ("preset_fbx", "fbx_preset"), ("sur_place", "animate_in_place")))
    if args.sans_cuisson:
        corps["bake"] = False
    if args.sans_animation:
        corps["with_animation"] = False
    return executer(args, api, entrees, "/v3/models/convert", corps, "modele", {"type": "convert_model"})


def cmd_importer(args):
    _verifier_sortie(args, [".glb"])
    api, entrees = _contexte(args)
    corps = {"input": _entree_modele(entrees, args.entree)}
    return executer(args, api, entrees, "/v3/models/import", corps, "modele", {"type": "import_model"},
                    principale_requise=False)


def cmd_decimer(args):
    _verifier_sortie(args, [".glb", ".fbx"])
    if args.uv_intelligentes and args.modele != "v3.0":
        raise ErreurTripo(USAGE, "--uv-intelligentes exige --modele v3.0.")
    if args.faces is not None and args.faces <= 0:
        raise ErreurTripo(USAGE, "--faces doit être un entier positif.")
    api, entrees = _contexte(args)
    corps = {"input": _entree_modele(entrees, args.entree)}
    _options(corps, args, (("modele", "model"), ("faces", "face_limit"), ("quad", "quad"),
                           ("uv_intelligentes", "smart_uv")))
    if args.sans_cuisson:
        corps["bake"] = False
    if _pieces(args):
        corps["part_names"] = _pieces(args)
    return executer(args, api, entrees, "/v3/mesh/decimate", corps, "modele", {"type": "highpoly_to_lowpoly"})


def cmd_uv(args):
    _verifier_sortie(args, [".glb"])
    api, entrees = _contexte(args)
    corps = {"input": _entree_modele(entrees, args.entree)}
    _options(corps, args, (("modele", "model"),))
    return executer(args, api, entrees, "/v3/mesh/uv", corps, "modele", {"type": "mesh_uv"})


def cmd_segmenter(args):
    _verifier_sortie(args, [".glb"])
    api, entrees = _contexte(args)
    corps = {"input": _entree_modele(entrees, args.entree)}
    _options(corps, args, (("modele", "model"), ("granularite", "segmentation_granularity"),
                           ("par_connexite", "split_by_connectivity")))
    if args.image_ref:
        corps["ref_image"] = entrees.resoudre(args.image_ref, "image_ref")
    return executer(args, api, entrees, "/v3/mesh/segment", corps, "modele", {"type": "mesh_segmentation"})


def cmd_segmenter_intelligent(args):
    _verifier_sortie(args, [".glb"])
    seg_type = args.type_entree
    if seg_type is None:
        seg_type = "model" if args.entree.lower().split("?")[0].endswith(".glb") else "image"
    api, entrees = _contexte(args)
    extensions = (".glb",) if seg_type == "model" else EXTENSIONS_IMAGE
    corps = {"seg_type": seg_type,
             "input": entrees.resoudre(args.entree, "source", extensions=extensions, references=False)}
    _options(corps, args, (("granularite", "granularity"), ("indice", "hint")))
    if seg_type == "model":
        matrice = args.transformation or [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        if len(matrice) != 16:
            raise ErreurTripo(USAGE, "--transformation attend 16 nombres (matrice 4×4 en colonnes).")
        corps["transform"] = matrice
    return executer(args, api, entrees, "/v3/mesh/smartsegment", corps, "modele", {"type": "smart_segmentation"})


def cmd_completer(args):
    _verifier_sortie(args, [".glb"])
    api, entrees = _contexte(args)
    entrees.liste.append({"role": "segmentation", "task_id": args.task_id})
    corps = {"input": args.task_id}
    _options(corps, args, (("modele", "model"), ("mode", "completion_mode")))
    if _pieces(args):
        corps["part_names"] = _pieces(args)
    return executer(args, api, entrees, "/v3/mesh/complete", corps, "modele", {"type": "mesh_completion"})


# ---------------------------------------------------------------------------
# Animation
# ---------------------------------------------------------------------------

def cmd_riggable(args):
    api, entrees = _contexte(args)
    corps = {"input": _entree_modele(entrees, args.entree)}
    if args.a_blanc:
        return _a_blanc("/v3/animations/rig-check", corps)
    task_id = creer_tache(api, "/v3/animations/rig-check", corps)
    tache = attendre(api, task_id, args.delai, args.intervalle)
    verifier_succes(tache)
    sortie = tache.get("output") or {}
    riggable = sortie.get("riggable")
    squelette = sortie.get("rig_type") or sortie.get("topology") or "?"
    if riggable:
        dire(f"Riggable : oui (squelette détecté : {squelette}). Tâche {task_id}.")
    else:
        dire(f"Riggable : non. Tâche {task_id}.")
    return OK


def cmd_rigger(args):
    _verifier_sortie(args, ["." + args.format])
    if args.spec in ("unity", "unreal", "vrm") and args.modele in (None, "v1.0-20240301"):
        raise ErreurTripo(USAGE, "Les specs unity, unreal et vrm exigent --modele v2.5-20260210 ou v3.0-20260909.")
    api, entrees = _contexte(args)
    corps = {"input": _entree_modele(entrees, args.entree)}
    _options(corps, args, (("modele", "model"), ("type_squelette", "rig_type"), ("spec", "spec")))
    corps["out_format"] = args.format
    return executer(args, api, entrees, "/v3/animations/rig", corps, "modele", {"type": "animate_rig"})


def cmd_animer(args):
    _verifier_sortie(args, ["." + args.format])
    if len(args.animation) > 5:
        raise ErreurTripo(USAGE, "5 animations au maximum par tâche.")
    if args.sans_cuisson and args.format != "glb":
        raise ErreurTripo(USAGE, "--sans-cuisson ne s'applique qu'au GLB.")
    api, entrees = _contexte(args)
    entrees.liste.append({"role": "modele_rigge", "task_id": args.task_id})
    animations = [a if a.startswith("preset:") else "preset:" + a for a in args.animation]
    corps = {"input": args.task_id}
    if len(animations) == 1:
        corps["animation"] = animations[0]
    else:
        corps["animations"] = animations
    corps["out_format"] = args.format
    if args.avec_geometrie is not None:
        corps["export_with_geometry"] = args.avec_geometrie
    _options(corps, args, (("sur_place", "animate_in_place"),))
    if args.sans_cuisson:
        corps["bake_animation"] = False
    return executer(args, api, entrees, "/v3/animations/retarget", corps, "modele",
                    {"type": "animate_retarget", "animations": animations},
                    principale_requise=len(animations) == 1)


# ---------------------------------------------------------------------------
# Tâches
# ---------------------------------------------------------------------------

def _ligne_tache(task_id, tache):
    statut = str(tache.get("status") or "unknown").lower()
    ligne = f"Tâche {task_id} : {statut}"
    if tache.get("progress") is not None:
        ligne += f" ({tache['progress']} %)"
    if tache.get("type"):
        ligne += f", type {tache['type']}"
    if statut == "success":
        noms = [nom for _, nom, _ in collecter_urls(tache.get("output"))]
        if noms:
            ligne += f", sorties : {', '.join(noms)}"
    return ligne


def cmd_statut(args):
    tache = lire_tache(_api(args), args.task_id)
    dire(_ligne_tache(args.task_id, tache))
    if str(tache.get("status") or "").lower() in ("failed", "cancelled", "expired", "banned"):
        verifier_succes(tache)
    return OK


def cmd_taches(args):
    data = _api(args).appel("POST", "/v3/tasks/list", json_corps={"task_ids": args.task_ids})
    taches = (data.get("tasks") if isinstance(data, dict) else None) or {}
    for task_id in args.task_ids:
        if task_id in taches:
            dire(_ligne_tache(task_id, taches[task_id]))
    for task_id in (data.get("missed") if isinstance(data, dict) else None) or []:
        dire(f"Tâche {task_id} : introuvable (identifiant faux, autre clé ou tâche expirée).")
    return OK


def cmd_telecharger(args):
    _verifier_sortie(args)
    api = _api(args)
    tache = lire_tache(api, args.task_id)
    if str(tache.get("status") or "").lower() not in STATUTS_FINAUX:
        tache = attendre(api, args.task_id, args.delai, args.intervalle)
    verifier_succes(tache)
    fiche = lire_fiche(args.sortie)
    if fiche.get("task_id") not in (None, args.task_id):
        fiche = {}
    if not fiche:
        entree = tache.get("input") if isinstance(tache.get("input"), dict) else {}
        fiche = {
            "outil": "plugin tripo (quiche-lorraine-games), scripts/tripo.py",
            "date": maintenant(),
            "api": api.base,
            "task_id": args.task_id,
            "type": tache.get("type"),
            "modele_tripo": entree.get("model"),
            "parametres": entree,
            "note": "Fiche reconstituée depuis la tâche : prompt et paramètres tels que renvoyés par l'API.",
        }
        if entree.get("prompt"):
            fiche["prompt"] = entree["prompt"]
    nature = fiche.get("nature") or deviner_nature(tache)
    return finaliser(args, api, tache, fiche, nature)


def cmd_brut(args):
    if not args.chemin.startswith("/v3/"):
        raise ErreurTripo(USAGE, "Le chemin doit commencer par /v3/ (ex. /v3/mesh/smartsegment).")
    _verifier_sortie(args)
    texte = args.corps
    if texte.startswith("@"):
        with open(texte[1:], encoding="utf-8") as f:
            texte = f.read()
    try:
        corps = json.loads(texte)
    except json.JSONDecodeError as exc:
        raise ErreurTripo(USAGE, f"--corps n'est pas du JSON valide : {exc}.") from None
    if not isinstance(corps, dict):
        raise ErreurTripo(USAGE, "--corps doit être un objet JSON.")
    api, entrees = _contexte(args)
    return executer(args, api, entrees, args.chemin, corps, args.nature, {"type": "brut"})


def cmd_inspecter(args):
    controle = inspecter_glb(args.chemin)
    dire(f"{args.chemin} : {resume_controle(controle)}")
    dire(json.dumps(controle, ensure_ascii=False, indent=2))
    return OK


# ---------------------------------------------------------------------------
# Ligne de commande
# ---------------------------------------------------------------------------

class _Analyseur(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        signaler(f"tripo.py : argument invalide : {message}")
        sys.exit(USAGE)


def _commun(sp, sortie=True, attente=True):
    if sortie:
        sp.add_argument("--sortie", required=True, help="fichier principal à écrire ; la fiche .tripo.json va à côté")
        sp.add_argument("--ecraser", action="store_true", help="autorise à remplacer --sortie")
    if attente:
        sp.add_argument("--delai", type=float, default=600, help="attente maximale en secondes (défaut : 600)")
        sp.add_argument("--intervalle", type=float, default=3, help="premier intervalle de suivi en secondes")


def _creation(sp):
    _commun(sp)
    sp.add_argument("--sans-attendre", action="store_true", help="crée la tâche et rend la main")
    sp.add_argument("--a-blanc", action="store_true", help="affiche la requête sans l'envoyer")
    sp.add_argument("--param", action="append", metavar="CLE=VALEUR",
                    help="champ supplémentaire de l'API, envoyé tel quel (valeur JSON ou texte ; répétable)")


def _generation(sp, depuis_image):
    _creation(sp)
    sp.add_argument("--format", choices=FORMATS, default="glb",
                    help="glb par défaut ; fbx et obj passent par une conversion payante (sauf fbx avec --quad)")
    sp.add_argument("--modele", default=MODELE_DEFAUT, help=f"version du modèle Tripo (défaut : {MODELE_DEFAUT})")
    sp.add_argument("--faces", type=int, help="nombre maximal de faces (face_limit)")
    sp.add_argument("--sans-texture", action="store_true", help="géométrie seule (moins chère)")
    sp.add_argument("--sans-pbr", action="store_true", help="texture sans cartes PBR")
    sp.add_argument("--qualite-texture", choices=("standard", "detailed", "fast", "extreme"),
                    help="detailed et extreme coûtent plus ; fast et extreme dépendent de --version-texture")
    sp.add_argument("--version-texture", help="modèle de texture (texture_version), ex. v3.5-20260815")
    sp.add_argument("--qualite-geometrie", choices=("standard", "detailed"), help="detailed : supplément")
    sp.add_argument("--taille-auto", action="store_true", help="mise à l'échelle réelle en mètres (auto_size)")
    sp.add_argument("--low-poly", action="store_true", help="smart_low_poly (supplément)")
    sp.add_argument("--quad", action="store_true", help="maillage en quads, sortie FBX (supplément)")
    sp.add_argument("--parties", action="store_true", help="génère des pièces séparées (generate_parts, supplément)")
    sp.add_argument("--graine", type=int, help="graine, pour refaire un résultat proche")
    if depuis_image:
        sp.add_argument("--orientation", choices=("default", "align_image"), help="orientation du modèle")
        sp.add_argument("--alignement-texture", choices=("original_image", "geometry"),
                        help="priorité de la texture : fidélité à l'image ou à la géométrie")


def analyseur():
    p = _Analyseur(prog="tripo.py", description="Pilote l'API Tripo 3D (apiv3).")
    p.add_argument("--api", help=f"URL de base de l'API (défaut : TRIPO_API_BASE ou {API_BASE_DEFAUT})")
    sous = p.add_subparsers(dest="commande", required=True, parser_class=_Analyseur)

    def commande(nom, fonction, aide):
        sp = sous.add_parser(nom, help=aide, description=aide)
        sp.set_defaults(fonction=fonction)
        return sp

    # Compte
    v = commande("verifier", cmd_verifier, "clé, accès réseau à chaque hôte, solde de crédits")
    v.add_argument("--hote-fichiers", action="append",
                   help="hôte des fichiers à tester (répétable ; défaut : TRIPO_HOTES_FICHIERS ou "
                        "tripo-data.rg1.data.tripo3d.com)")
    c = commande("consommation", cmd_consommation, "historique des tâches et des crédits consommés")
    c.add_argument("--limite", type=int, default=20)
    c.add_argument("--decalage", type=int, default=0)
    e = commande("envoyer", cmd_envoyer, "envoie un fichier local et affiche son file_token")
    e.add_argument("fichier")

    # Modèles
    t = commande("texte", cmd_texte, "modèle 3D depuis un prompt")
    t.add_argument("prompt")
    t.add_argument("--negatif", help="ce qu'il faut éviter (negative_prompt)")
    _generation(t, depuis_image=False)
    i = commande("image", cmd_image, "modèle 3D depuis une image (fichier, URL, file_token ou task_id)")
    i.add_argument("chemin")
    i.add_argument("--autofix", action="store_true", help="correction automatique de l'image (enable_image_autofix)")
    _generation(i, depuis_image=True)
    m = commande("multivue", cmd_multivue, "modèle 3D depuis 1 à 4 vues (face, gauche, dos, droite)")
    m.add_argument("--face")
    m.add_argument("--gauche")
    m.add_argument("--dos")
    m.add_argument("--droite")
    m.add_argument("--depuis-tache", help="task_id d'une tâche image-multivue ou editer-multivue")
    _generation(m, depuis_image=True)

    # Images
    it = commande("image-texte", cmd_image_texte, "image depuis un prompt")
    it.add_argument("prompt")
    it.add_argument("--negatif")
    it.add_argument("--modele", help="modèle d'image, ex. seedream_v4 (défaut de Tripo) ou seedream_v5")
    it.add_argument("--taille", help="taille, ex. 1024x1024")
    it.add_argument("--ratio", help="rapport largeur/hauteur, ex. 1:1")
    it.add_argument("--format-image", help="format de sortie, ex. png")
    _creation(it)
    ii = commande("image-image", cmd_image_image, "transforme une ou plusieurs images de référence")
    ii.add_argument("entrees", nargs="+")
    ii.add_argument("--prompt")
    ii.add_argument("--modele")
    ii.add_argument("--gabarit", help="gabarit d'image Tripo, ex. t-pose")
    ii.add_argument("--t-pose", action="store_true", help="met le sujet en T-pose")
    ii.add_argument("--croquis", action="store_true", help="rend un croquis (sketch_to_render)")
    _creation(ii)
    im = commande("image-multivue", cmd_image_multivue, "vues face, gauche, dos et droite depuis une image")
    im.add_argument("entree")
    _creation(im)
    em = commande("editer-multivue", cmd_editer_multivue, "modifie des vues d'une tâche multivue")
    em.add_argument("task_id")
    em.add_argument("--vue", action="append", required=True, metavar="VUE=TEXTE",
                    help="front, left, back ou right, suivi de la consigne (répétable)")
    _creation(em)
    s = commande("splat", cmd_splat, "splat gaussien depuis une image")
    s.add_argument("entree")
    s.add_argument("--graine", type=int)
    _creation(s)
    pr = commande("profondeur", cmd_profondeur, "carte de profondeur depuis une image")
    pr.add_argument("entree")
    pr.add_argument("--type", dest="type_profondeur", choices=("gray", "color"))
    pr.add_argument("--resolution", type=int, help="résolution de calcul, de 126 à 2016")
    _creation(pr)

    # Traitement
    r = commande("retexturer", cmd_retexturer, "nouvelle texture sur un modèle existant")
    r.add_argument("entree", help="task_id d'un modèle, fichier GLB/FBX/OBJ/STL, URL ou file_token")
    r.add_argument("--prompt-texture", help="consigne de texture en texte")
    r.add_argument("--image-texture", help="image de référence pour la texture")
    r.add_argument("--image-style", help="image de style")
    r.add_argument("--modele", help="modèle de texture : v2.5-20250123, v3.0-20250812 ou v3.5-20260815")
    r.add_argument("--qualite-texture", choices=("standard", "detailed", "fast", "extreme"))
    r.add_argument("--alignement-texture", choices=("original_image", "geometry"))
    r.add_argument("--sans-pbr", action="store_true")
    r.add_argument("--pieces", help="noms de pièces à retexturer, séparés par des virgules")
    r.add_argument("--sans-cuisson", action="store_true", help="bake=false")
    r.add_argument("--graine", type=int)
    _creation(r)
    cv = commande("convertir", cmd_convertir, "convertit le modèle d'une tâche dans un autre format")
    cv.add_argument("task_id")
    cv.add_argument("--format", required=True, choices=FORMATS_CONVERSION)
    cv.add_argument("--faces", type=int)
    cv.add_argument("--quad", action="store_true")
    cv.add_argument("--taille-texture", type=int, help="ex. 2048 (Tripo : 4096 par défaut)")
    cv.add_argument("--format-texture", help="ex. JPEG ou PNG")
    cv.add_argument("--echelle", type=float, help="facteur d'échelle (scale_factor)")
    cv.add_argument("--pivot-bas", action="store_true", help="pivot au centre de la base")
    cv.add_argument("--aplatir-base", action="store_true", help="aplatit le dessous (flatten_bottom)")
    cv.add_argument("--orientation-export", help="ex. +x (export_orientation)")
    cv.add_argument("--preset-fbx", help="ex. blender (fbx_preset)")
    cv.add_argument("--sur-place", action="store_true", help="animation sur place (animate_in_place)")
    cv.add_argument("--sans-cuisson", action="store_true", help="bake=false")
    cv.add_argument("--sans-animation", action="store_true", help="with_animation=false")
    _creation(cv)
    imp = commande("importer", cmd_importer, "importe un modèle externe pour le retravailler avec Tripo")
    imp.add_argument("entree", help="fichier GLB/GLTF/FBX/OBJ/STL (150 Mo max), URL ou file_token")
    _creation(imp)
    d = commande("decimer", cmd_decimer, "réduit le nombre de faces d'un modèle (retopologie)")
    d.add_argument("entree")
    d.add_argument("--faces", type=int)
    d.add_argument("--modele", choices=("v1.0", "v2.0", "v3.0"))
    d.add_argument("--quad", action="store_true")
    d.add_argument("--uv-intelligentes", action="store_true", help="smart_uv (exige --modele v3.0)")
    d.add_argument("--pieces")
    d.add_argument("--sans-cuisson", action="store_true", help="bake=false")
    _creation(d)
    u = commande("uv", cmd_uv, "dépliage UV automatique (Smart UV)")
    u.add_argument("entree")
    u.add_argument("--modele")
    _creation(u)
    sg = commande("segmenter", cmd_segmenter, "découpe un modèle en pièces")
    sg.add_argument("entree")
    sg.add_argument("--modele", help="v1.0-20250506 (défaut de Tripo) ou v2.0-20260430")
    sg.add_argument("--granularite", help="finesse du découpage (modèle v2.0)")
    sg.add_argument("--image-ref", help="image de référence (modèle v2.0)")
    sg.add_argument("--par-connexite", action="store_true", help="split_by_connectivity (modèle v2.0)")
    _creation(sg)
    si = commande("segmenter-intelligent", cmd_segmenter_intelligent,
                  "segmentation intelligente depuis une image ou un GLB (smartsegment)")
    si.add_argument("entree", help="fichier image ou GLB, URL ou file_token (pas de task_id)")
    si.add_argument("--type", dest="type_entree", choices=("image", "model"), help="déduit de l'extension sinon")
    si.add_argument("--granularite", choices=("coarse", "medium", "fine"))
    si.add_argument("--indice", help="texte qui aide à repérer les pièces (hint)")
    si.add_argument("--transformation", type=float, nargs=16, help="matrice 4×4 en colonnes (GLB ; identité sinon)")
    _creation(si)
    cp = commande("completer", cmd_completer, "complète les pièces d'une segmentation")
    cp.add_argument("task_id", help="task_id d'une tâche segmenter")
    cp.add_argument("--pieces")
    cp.add_argument("--mode", choices=("ai_completion", "quick_cap"))
    cp.add_argument("--modele")
    _creation(cp)

    # Animation
    rc = commande("riggable", cmd_riggable, "vérifie qu'un modèle peut être riggé (gratuit)")
    rc.add_argument("entree")
    rc.add_argument("--a-blanc", action="store_true")
    _commun(rc, sortie=False)
    rg = commande("rigger", cmd_rigger, "ajoute un squelette à un modèle")
    rg.add_argument("entree")
    rg.add_argument("--format", choices=("glb", "fbx"), default="glb")
    rg.add_argument("--modele", help="v1.0-20240301 (défaut de Tripo), v2.5-20260210 ou v3.0-20260909")
    rg.add_argument("--type", dest="type_squelette",
                    choices=("biped", "quadruped", "hexapod", "octopod", "avian", "serpentine", "aquatic", "others"))
    rg.add_argument("--spec", choices=("tripo", "mixamo", "actorcore", "unity", "unreal", "vrm"))
    _creation(rg)
    an = commande("animer", cmd_animer, "applique des animations prédéfinies à un modèle riggé")
    an.add_argument("task_id", help="task_id d'une tâche rigger")
    an.add_argument("--animation", action="append", required=True,
                    help="préréglage, ex. walk, run, idle ou preset:walk (1 à 5)")
    an.add_argument("--format", choices=("glb", "fbx"), default="glb")
    geo = an.add_mutually_exclusive_group()
    geo.add_argument("--avec-geometrie", dest="avec_geometrie", action="store_true", default=None)
    geo.add_argument("--sans-geometrie", dest="avec_geometrie", action="store_false")
    an.add_argument("--sur-place", action="store_true", help="animation sur place (animate_in_place)")
    an.add_argument("--sans-cuisson", action="store_true", help="bake_animation=false (GLB)")
    _creation(an)

    # Tâches
    st = commande("statut", cmd_statut, "affiche le statut d'une tâche")
    st.add_argument("task_id")
    ts = commande("taches", cmd_taches, "statut de plusieurs tâches en une requête")
    ts.add_argument("task_ids", nargs="+")
    tl = commande("telecharger", cmd_telecharger, "attend si besoin, puis télécharge les fichiers d'une tâche")
    tl.add_argument("task_id")
    _commun(tl)
    b = commande("brut", cmd_brut, "crée une tâche sur n'importe quel endpoint /v3/ (corps JSON tel quel)")
    b.add_argument("chemin", help="ex. /v3/mesh/smartsegment")
    b.add_argument("--corps", required=True, help="objet JSON, ou @fichier.json")
    b.add_argument("--nature", choices=("modele", "image", "multivue", "profondeur", "splat"), default="modele")
    _creation(b)
    n = commande("inspecter", cmd_inspecter, "poids, triangles, dimensions et textures d'un GLB local")
    n.add_argument("chemin")
    return p


def main(argv=None):
    args = analyseur().parse_args(argv)
    try:
        return args.fonction(args)
    except ErreurTripo as exc:
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
