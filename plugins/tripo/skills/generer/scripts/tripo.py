#!/usr/bin/env python3
"""Client en ligne de commande de l'API Tripo 3D (apiv3), bibliothèque standard uniquement.

Sous-commandes : verifier, texte, image, statut, telecharger, inspecter.
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
EXTENSIONS_IMAGE = (".png", ".jpg", ".jpeg")
TAILLE_MAX_IMAGE = 20 * 1024 * 1024
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
    type_fichier = "image/png" if nom.lower().endswith(".png") else "image/jpeg"
    with open(chemin, "rb") as f:
        contenu = f.read()
    corps = (
        f"--{frontiere}\r\n"
        f'Content-Disposition: form-data; name="{champ}"; filename="{nom}"\r\n'
        f"Content-Type: {type_fichier}\r\n\r\n"
    ).encode("utf-8") + contenu + f"\r\n--{frontiere}--\r\n".encode("utf-8")
    return corps, f"multipart/form-data; boundary={frontiere}"


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


def url_modele(tache):
    sortie = tache.get("output") or {}
    for cle in ("model_url", "pbr_model_url", "model", "pbr_model", "base_model_url", "base_model"):
        valeur = sortie.get(cle)
        if isinstance(valeur, str) and valeur:
            return valeur
    raise ErreurTripo(ERREUR, f"La tâche {tache.get('task_id', '?')} est terminée mais ne donne pas d'URL de modèle.")


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
# Sous-commandes
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


def _parametres_communs(args):
    corps = {"model": args.modele}
    texture = not args.sans_texture
    corps["texture"] = texture
    corps["pbr"] = texture and not args.sans_pbr
    if texture and args.qualite_texture:
        corps["texture_quality"] = args.qualite_texture
    if args.faces is not None:
        if args.faces <= 0:
            raise ErreurTripo(USAGE, "--faces doit être un entier positif.")
        corps["face_limit"] = args.faces
    if args.taille_auto:
        corps["auto_size"] = True
    if args.low_poly:
        corps["smart_low_poly"] = True
    if args.graine is not None:
        corps["model_seed"] = args.graine
        if texture:
            corps["texture_seed"] = args.graine
    return corps


def _verifier_sortie(args):
    sortie = args.sortie
    attendu = "." + args.format
    if not sortie.lower().endswith(attendu):
        raise ErreurTripo(USAGE, f"--sortie doit finir par {attendu} (format choisi : {args.format}).")
    if os.path.exists(sortie) and not args.ecraser:
        raise ErreurTripo(USAGE, f"{sortie} existe déjà. Choisis un autre nom ou ajoute --ecraser.")


def cmd_texte(args):
    prompt = args.prompt.strip()
    if not prompt:
        raise ErreurTripo(USAGE, "Le prompt est vide.")
    if len(prompt) > LONGUEUR_MAX_PROMPT:
        raise ErreurTripo(USAGE, f"Le prompt dépasse {LONGUEUR_MAX_PROMPT} caractères ({len(prompt)}).")
    _verifier_sortie(args)
    corps = {"prompt": prompt}
    if args.negatif:
        corps["negative_prompt"] = args.negatif
    corps.update(_parametres_communs(args))
    if args.graine is not None:
        corps["image_seed"] = args.graine
    source = {"type": "text_to_model", "prompt": prompt}
    if args.negatif:
        source["negatif"] = args.negatif
    return _generer(args, "/v3/generation/text-to-model", corps, source)


def cmd_image(args):
    chemin = args.chemin
    if not os.path.isfile(chemin):
        raise ErreurTripo(USAGE, f"Image introuvable : {chemin}")
    if not chemin.lower().endswith(EXTENSIONS_IMAGE):
        raise ErreurTripo(USAGE, "L'image doit être en PNG ou JPEG.")
    taille = os.path.getsize(chemin)
    if taille > TAILLE_MAX_IMAGE:
        raise ErreurTripo(USAGE, "L'image dépasse 20 Mo, la limite de Tripo.")
    _verifier_sortie(args)
    with open(chemin, "rb") as f:
        empreinte = hashlib.sha256(f.read()).hexdigest()
    corps = _parametres_communs(args)
    source = {
        "type": "image_to_model",
        "image": {"chemin": chemin, "octets": taille, "sha256": empreinte},
    }
    if args.a_blanc:
        corps = {"input": "<file_token après envoi de l'image>", **corps}
        return _a_blanc("/v3/generation/image-to-model", corps)
    api = Api(base_api(args), lire_cle())
    envoi = api.appel("POST", "/v3/files", multipart=_multipart("file", chemin))
    jeton = envoi.get("file_token") if isinstance(envoi, dict) else None
    if not jeton:
        raise ErreurTripo(ERREUR, "Envoi de l'image : réponse sans file_token.")
    corps = {"input": jeton, **corps}
    return _generer(args, "/v3/generation/image-to-model", corps, source, api=api)


def _a_blanc(chemin, corps):
    dire(f"À blanc : POST {chemin}")
    dire(json.dumps(corps, ensure_ascii=False, indent=2))
    dire("Aucune requête envoyée, aucun crédit consommé.")
    return OK


def _generer(args, chemin, corps, source, api=None):
    if args.a_blanc:
        return _a_blanc(chemin, corps)
    api = api or Api(base_api(args), lire_cle())
    parametres = {k: v for k, v in corps.items() if k not in ("prompt", "negative_prompt", "input")}
    task_id = creer_tache(api, chemin, corps)
    dire(f"Tâche créée : {task_id}")
    fiche = {
        "outil": "plugin tripo (quiche-lorraine-games), scripts/tripo.py",
        "date": maintenant(),
        "api": api.base,
        "task_id": task_id,
        "modele_tripo": corps.get("model"),
        **source,
        "parametres": parametres,
        "format": args.format,
        "fichier": os.path.basename(args.sortie),
        "etat": "en_cours",
    }
    if args.sans_attendre:
        ecrire_fiche(args.sortie, fiche)
        dire(f"Sans attente. Récupère le modèle avec : tripo.py telecharger {task_id} --sortie {args.sortie}")
        return OK
    tache = attendre(api, task_id, args.delai, args.intervalle)
    verifier_succes(tache)
    return _finaliser(args, api, tache, fiche)


def _finaliser(args, api, tache, fiche, convertir=True):
    task_id = tache["task_id"] if tache.get("task_id") else fiche["task_id"]
    tache_fichier = tache
    if args.format != "glb" and convertir:
        conversion_id = creer_tache(api, "/v3/models/convert", {"input": task_id, "format": args.format.upper()})
        dire(f"Conversion en {args.format.upper()} : tâche {conversion_id}")
        tache_fichier = attendre(api, conversion_id, args.delai, args.intervalle)
        verifier_succes(tache_fichier)
        fiche["conversion"] = {"task_id": conversion_id, "format": args.format,
                               "credits": tache_fichier.get("credits_consumed")}
    hote_fichier, octets = telecharger_fichier(url_modele(tache_fichier), args.sortie, task_id)
    with open(args.sortie, "rb") as f:
        est_glb = f.read(4) == b"glTF"
    if est_glb != (args.format == "glb"):
        os.remove(args.sortie)
        raise ErreurTripo(USAGE, (
            f"Le fichier de la tâche {task_id} n'est pas au format {args.format}. Pour un FBX ou un OBJ, "
            "passe à `telecharger` le task_id de la tâche de conversion (champ conversion du .tripo.json)."))
    fiche.update({
        "etat": "telecharge",
        "date_telechargement": maintenant(),
        "hote_fichier": hote_fichier,
        "credits": tache.get("credits_consumed"),
        "fichier": os.path.basename(args.sortie),
        "format": args.format,
    })
    if not fiche.get("modele_tripo"):
        fiche["modele_tripo"] = (tache.get("input") or {}).get("model") or tache.get("model_version")
    resume = f"{_taille_lisible(octets)}"
    if args.format == "glb":
        controle = inspecter_glb(args.sortie)
        fiche["controle"] = controle
        resume = resume_controle(controle)
        limite = (fiche.get("parametres") or {}).get("face_limit")
        if limite and controle["triangles"] > limite * 1.05:
            signaler(f"Attention : {controle['triangles']} triangles pour une limite demandée de {limite}.")
    chemin = ecrire_fiche(args.sortie, fiche)
    dire(f"Modèle écrit : {args.sortie} ({resume})")
    dire(f"Fiche de traçabilité : {chemin}")
    return OK


def cmd_statut(args):
    api = Api(base_api(args), lire_cle())
    tache = lire_tache(api, args.task_id)
    statut = str(tache.get("status") or "unknown").lower()
    ligne = f"Tâche {args.task_id} : {statut}"
    if tache.get("progress") is not None:
        ligne += f" ({tache['progress']} %)"
    if tache.get("type"):
        ligne += f", type {tache['type']}"
    dire(ligne)
    if statut in ("failed", "cancelled", "expired", "banned"):
        verifier_succes(tache)
    return OK


def cmd_telecharger(args):
    _verifier_sortie(args)
    api = Api(base_api(args), lire_cle())
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
    return _finaliser(args, api, tache, fiche, convertir=False)


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


def analyseur():
    p = _Analyseur(prog="tripo.py", description="Génère des modèles 3D avec l'API Tripo (apiv3).")
    p.add_argument("--api", help=f"URL de base de l'API (défaut : TRIPO_API_BASE ou {API_BASE_DEFAUT})")
    sous = p.add_subparsers(dest="commande", required=True, parser_class=_Analyseur)

    v = sous.add_parser("verifier", help="clé, accès réseau à chaque hôte, solde de crédits")
    v.add_argument("--hote-fichiers", action="append",
                   help="hôte des fichiers à tester (répétable ; défaut : TRIPO_HOTES_FICHIERS ou tripo-data.rg1.data.tripo3d.com)")
    v.set_defaults(fonction=cmd_verifier)

    def options_generation(sp):
        sp.add_argument("--sortie", required=True, help="fichier à écrire (ex. assets/props/caisse.glb)")
        sp.add_argument("--format", choices=FORMATS, default="glb",
                        help="glb par défaut ; fbx et obj passent par une tâche de conversion payante")
        sp.add_argument("--modele", default=MODELE_DEFAUT, help=f"version du modèle Tripo (défaut : {MODELE_DEFAUT})")
        sp.add_argument("--faces", type=int, help="nombre maximal de faces (face_limit)")
        sp.add_argument("--sans-texture", action="store_true", help="géométrie seule (moins chère)")
        sp.add_argument("--sans-pbr", action="store_true", help="texture sans cartes PBR")
        sp.add_argument("--qualite-texture", choices=("standard", "detailed"),
                        help="qualité de texture ; detailed coûte plus cher")
        sp.add_argument("--taille-auto", action="store_true", help="mise à l'échelle réelle en mètres (auto_size)")
        sp.add_argument("--low-poly", action="store_true", help="smart_low_poly (surcoût)")
        sp.add_argument("--graine", type=int, help="graine pour refaire un résultat proche")
        sp.add_argument("--delai", type=float, default=600, help="attente maximale en secondes (défaut : 600)")
        sp.add_argument("--intervalle", type=float, default=3, help="premier intervalle de suivi en secondes")
        sp.add_argument("--sans-attendre", action="store_true", help="crée la tâche et rend la main")
        sp.add_argument("--a-blanc", action="store_true", help="affiche la requête sans l'envoyer")
        sp.add_argument("--ecraser", action="store_true", help="autorise à remplacer --sortie")

    t = sous.add_parser("texte", help="génère un modèle depuis un prompt")
    t.add_argument("prompt")
    t.add_argument("--negatif", help="ce qu'il faut éviter (negative_prompt)")
    options_generation(t)
    t.set_defaults(fonction=cmd_texte)

    i = sous.add_parser("image", help="génère un modèle depuis une image locale (PNG ou JPEG)")
    i.add_argument("chemin")
    options_generation(i)
    i.set_defaults(fonction=cmd_image)

    s = sous.add_parser("statut", help="affiche le statut d'une tâche")
    s.add_argument("task_id")
    s.set_defaults(fonction=cmd_statut)

    d = sous.add_parser("telecharger", help="attend si besoin, puis télécharge le modèle d'une tâche")
    d.add_argument("task_id")
    d.add_argument("--sortie", required=True)
    d.add_argument("--format", choices=FORMATS, default="glb")
    d.add_argument("--delai", type=float, default=600)
    d.add_argument("--intervalle", type=float, default=3)
    d.add_argument("--ecraser", action="store_true")
    d.set_defaults(fonction=cmd_telecharger)

    n = sous.add_parser("inspecter", help="poids, triangles, dimensions et textures d'un GLB local")
    n.add_argument("chemin")
    n.set_defaults(fonction=cmd_inspecter)
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
