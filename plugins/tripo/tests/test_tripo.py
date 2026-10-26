"""Tests de scripts/tripo.py contre un faux serveur HTTP local qui imite l'API Tripo (apiv3).

Lancer depuis la racine du repo :
    python3 -m unittest discover -s plugins/tripo/tests -v
"""

import importlib.util
import json
import os
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ICI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(ICI, "..", "skills", "generer", "scripts", "tripo.py")
CLE = "tsk_cle-de-test-ultra-secrete-0123456789"

_spec = importlib.util.spec_from_file_location("tripo", SCRIPT)
tripo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tripo)


def glb_triangle(echelle=2.0, normales=False, **extra):
    """GLB minimal : un triangle de 1 m × 1 m sous un nœud mis à l'échelle."""
    positions = struct.pack("<9f", 0, 0, 0, 1, 0, 0, 0, 1, 0)
    gltf = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "scale": [echelle, echelle, echelle]}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}}]}],
        "accessors": [{"bufferView": 0, "componentType": 5126, "count": 3, "type": "VEC3",
                       "min": [0, 0, 0], "max": [1, 1, 0]}],
        "bufferViews": [{"buffer": 0, "byteOffset": 0, "byteLength": len(positions)}],
        "buffers": [{"byteLength": len(positions)}],
        **extra,
    }
    if normales:
        # Normale du triangle (+Z), dans une vue entrelacée après les positions.
        gltf["meshes"][0]["primitives"][0]["attributes"]["NORMAL"] = 1
        gltf["accessors"].append({"bufferView": 1, "componentType": 5126, "count": 3, "type": "VEC3"})
        gltf["bufferViews"].append({"buffer": 0, "byteOffset": len(positions), "byteLength": 36})
        positions += struct.pack("<9f", 0, 0, 1, 0, 0, 1, 0, 0, 1)
        gltf["buffers"][0]["byteLength"] = len(positions)
    bloc_json = json.dumps(gltf).encode("utf-8")
    bloc_json += b" " * (-len(bloc_json) % 4)
    total = 12 + 8 + len(bloc_json) + 8 + len(positions)
    return (struct.pack("<4sII", b"glTF", 2, total)
            + struct.pack("<II", len(bloc_json), 0x4E4F534A) + bloc_json
            + struct.pack("<II", len(positions), 0x004E4942) + positions)


def sortie_selon_operation(base, task_id, operation, corps):
    """Sortie d'une tâche réussie, selon l'endpoint qui l'a créée (formes tirées du SDK officiel)."""
    f = f"{base}/fichiers/{task_id}"
    if operation in ("/v3/generation/text-to-image", "/v3/generation/image-to-image"):
        return {"generated_image_url": f"{f}.png?s=1"}
    if operation in ("/v3/generation/image-to-multiview", "/v3/generation/edit-multiview"):
        return {"generate_multiview_image": {v + "_view_url": f"{f}_{v}.png?s=1"
                                             for v in ("front", "left", "back", "right")}}
    if operation == "/v3/generation/image-to-depth":
        return {"depth_image_url": f"{f}_depth.png?s=1"}
    if operation == "/v3/generation/image-to-splat":
        return {"model_url": f"{f}.ply?s=1"}
    if operation == "/v3/animations/rig-check":
        return {"riggable": not corps.get("_non_riggable"), "rig_type": "biped"}
    if operation == "/v3/animations/retarget":
        return {"model_urls": [f"{f}_1.glb?s=1", f"{f}_2.glb?s=1"]}
    if operation == "/v3/models/import":
        return {}
    if operation == "/v3/models/convert" or corps.get("quad"):
        return {"model_url": f"{f}.fbx?s=1"}
    sortie = {"model_url": f"{f}.glb?auth_key=xyz", "rendered_image_url": f"{f}_rendu.webp?s=1"}
    if operation == "/v3/mesh/uv":
        sortie["uv_render_url"] = f"{f}_uv.png?s=1"
    return sortie


class FauxTripo(BaseHTTPRequestHandler):
    """Rejoue le scénario de la classe de test : self.server.scenario."""

    def log_message(self, *args):
        pass

    def _json(self, statut, charge, entetes=None):
        corps = json.dumps(charge).encode("utf-8")
        self.send_response(statut)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corps)))
        self.send_header("X-Tripo-Trace-ID", "trace-test")
        for nom, valeur in (entetes or {}).items():
            self.send_header(nom, valeur)
        self.end_headers()
        self.wfile.write(corps)

    def _noter(self, corps=b""):
        self.server.requetes.append({
            "methode": self.command,
            "chemin": self.path,
            "auth": self.headers.get("Authorization"),
            "type": self.headers.get("Content-Type"),
            "corps": corps,
        })

    def _tache(self, task_id, avancer=True):
        sc = self.server.scenario
        etats = sc["etats"].setdefault(task_id, list(sc.get("suite", ["queued", "running", "success"])))
        statut = (etats.pop(0) if len(etats) > 1 else etats[0]) if avancer else etats[-1]
        operation = self.server.operations.get(task_id, "/v3/generation/text-to-model")
        data = {"task_id": task_id, "type": "text_to_model", "status": statut,
                "progress": 100 if statut == "success" else 40,
                "input": {"prompt": "caisse en bois", "model": "v3.1-20260211"}}
        if statut == "success":
            corps = dict(self.server.corps.get(task_id, {}), _non_riggable=sc.get("non_riggable"))
            base = sc.get("base_fichiers", self.server.base)
            data["output"] = sortie_selon_operation(base, task_id, operation, corps)
            data["credits_consumed"] = 20
        if statut == "failed":
            data.update({"error_code": 5000, "error_msg": "generation failed"})
        return data

    def do_GET(self):
        self._noter()
        sc = self.server.scenario
        if self.path == "/v3/account/balance":
            if sc.get("cle_refusee"):
                return self._refus_cle()
            return self._json(200, {"code": 0, "data": {"balance": 1234.0, "frozen": 20.0}})
        if self.path.startswith("/v3/account/usage"):
            return self._json(200, {"code": 0, "data": {"items": [
                {"task_id": "a", "type": "text_to_model", "status": "success",
                 "created_at": "2026-10-22T10:00:00Z", "credits_consumed": 20},
                {"task_id": "b", "type": "texture_model", "status": "failed",
                 "created_at": "2026-10-22T10:05:00Z", "credits_consumed": 0}]}})
        if self.path.startswith("/v3/tasks/"):
            if sc.get("pannes", 0) > 0:
                sc["pannes"] -= 1
                return self._json(500, {"code": 500, "status": "error", "message": "internal"})
            return self._json(200, {"code": 0, "data": self._tache(self.path.rsplit("/", 1)[1])})
        if self.path.startswith("/fichiers/"):
            if sc.get("coupures", 0) > 0:
                # Coupure brutale (RST) avant toute réponse, comme le proxy d'un environnement cloud.
                sc["coupures"] -= 1
                self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
                self.connection.close()
                self.close_connection = True
                return
            if sc.get("partiels", 0) > 0:
                # Réponse tronquée : la connexion se ferme avant la longueur annoncée.
                sc["partiels"] -= 1
                self.send_response(200)
                self.send_header("Content-Length", "1000")
                self.end_headers()
                self.wfile.write(b"glTF")
                self.close_connection = True
                return
            if sc.get("fichier_expire"):
                self.send_response(403)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            chemin = self.path.split("?")[0]
            if chemin.endswith(".glb"):
                corps = glb_triangle()
            elif chemin.endswith(".fbx"):
                corps = b"Kaydara FBX Binary  \x00"
            else:
                corps = b"\x89PNG\r\n\x1a\n" + chemin.encode()
            self.send_response(200)
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
            return
        self._json(404, {"code": 404, "status": "error", "message": "not found"})

    def do_PUT(self):
        longueur = int(self.headers.get("Content-Length") or 0)
        self.rfile.read(longueur)
        self._noter(b"<%d octets>" % longueur)
        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        longueur = int(self.headers.get("Content-Length") or 0)
        corps = self.rfile.read(longueur)
        self._noter(corps)
        sc = self.server.scenario
        if sc.get("cle_refusee"):
            return self._refus_cle()
        if sc.get("limites", 0) > 0 and self.path.startswith("/v3/generation/"):
            sc["limites"] -= 1
            return self._json(429, {"code": 2000, "status": "error", "message": "concurrency limit"})
        erreur = sc.get("erreur_creation")
        if erreur and self.path.startswith("/v3/generation/"):
            statut, code, message = erreur
            entetes = {"Retry-After": "1"} if statut == 429 else None
            return self._json(statut, {"code": code, "status": "error", "message": message,
                                       "suggestion": "test"}, entetes)
        if self.path == "/v3/files":
            return self._json(200, {"code": 0, "data": {"file_token": "file_test_123"}})
        if self.path == "/v3/files/presign":
            return self._json(200, {"code": 0, "data": {"presigned_url": f"{self.server.base}/depot/gros?sig=1",
                                                        "file_token": "file_gros_456", "expires_in": 3600}})
        if self.path == "/v3/tasks/list":
            ids = json.loads(corps)["task_ids"]
            connus = [i for i in ids if not i.startswith("inconnu")]
            return self._json(200, {"code": 0, "data": {
                "tasks": {i: self._tache(i, avancer=False) for i in connus},
                "missed": [i for i in ids if i.startswith("inconnu")]}})
        if self.path.startswith("/v3/"):
            self.server.compteur += 1
            task_id = f"tache-{self.server.compteur}"
            self.server.operations[task_id] = self.path
            self.server.corps[task_id] = json.loads(corps or b"{}")
            return self._json(200, {"code": 0, "data": {"task_id": task_id}})
        self._json(404, {"code": 404, "status": "error", "message": "not found"})

    def _refus_cle(self):
        # Le vrai serveur renvoie HTTP 401 et code 2 ; ici on renvoie aussi l'en-tête reçu
        # pour vérifier que le script masque la clé même si l'API la recopiait.
        self._json(401, {"code": 2, "status": "error",
                         "message": f"Invalid API key ({self.headers.get('Authorization')})",
                         "suggestion": "Check if your credentials is valid"})


class FauxProxyBloquant(BaseHTTPRequestHandler):
    """Proxy qui refuse tout CONNECT par un 403, comme celui d'un environnement à accès limité."""

    def log_message(self, *args):
        pass

    def do_CONNECT(self):
        self.send_response(403, "Forbidden")
        self.send_header("Content-Length", "0")
        self.end_headers()


def demarrer(handler):
    serveur = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    return serveur


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.serveur = demarrer(FauxTripo)
        cls.serveur.base = f"http://127.0.0.1:{cls.serveur.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.serveur.shutdown()
        cls.serveur.server_close()

    def setUp(self):
        self.serveur.scenario = {"etats": {}}
        self.serveur.requetes = []
        self.serveur.compteur = 0
        self.serveur.operations = {}
        self.serveur.corps = {}
        self.dossier = tempfile.mkdtemp()
        self.sorties = []

    def lancer(self, *args, cle=CLE, env_extra=None):
        env = {k: v for k, v in os.environ.items()
               if k.upper() not in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "TRIPO_API_KEY")}
        env["NO_PROXY"] = "127.0.0.1,localhost"
        env["TRIPO_API_BASE"] = self.serveur.base
        env["TRIPO_HOTES_FICHIERS"] = self.serveur.base
        env["TRIPO_PAUSE_REESSAI"] = "0"
        if cle:
            env["TRIPO_API_KEY"] = cle
        env.update(env_extra or {})
        res = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True,
                             env=env, timeout=60, cwd=self.dossier)
        self.sorties.append(res.stdout + res.stderr)
        return res

    def tearDown(self):
        for nom in os.listdir(self.dossier):
            if nom.endswith(".json"):
                with open(os.path.join(self.dossier, nom), encoding="utf-8") as f:
                    self.sorties.append(f.read())
        for texte in self.sorties:
            self.assertNotIn(CLE, texte, "la clé apparaît dans une sortie ou un fichier")

    def chemin(self, nom):
        return os.path.join(self.dossier, nom)


class TestGeneration(BaseTest):
    def test_texte_cree_attend_telecharge_et_ecrit_la_fiche(self):
        sortie = self.chemin("caisse.glb")
        res = self.lancer("texte", "caisse en bois", "--sortie", sortie, "--faces", "3000",
                          "--intervalle", "0.01", "--graine", "7")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Tâche créée : tache-1", res.stdout)
        self.assertIn("Modèle écrit", res.stdout)

        creation = self.serveur.requetes[0]
        self.assertEqual(creation["chemin"], "/v3/generation/text-to-model")
        self.assertEqual(creation["auth"], f"Bearer {CLE}")
        corps = json.loads(creation["corps"])
        self.assertEqual(corps["prompt"], "caisse en bois")
        self.assertEqual(corps["model"], "v3.1-20260211")
        self.assertEqual(corps["face_limit"], 3000)
        self.assertTrue(corps["texture"])
        self.assertTrue(corps["pbr"])
        self.assertEqual(corps["model_seed"], 7)

        suivis = [r for r in self.serveur.requetes if r["chemin"].startswith("/v3/tasks/")]
        self.assertEqual(len(suivis), 3, "queued, running puis success")

        telechargement = [r for r in self.serveur.requetes if r["chemin"].startswith("/fichiers/")]
        self.assertEqual(len(telechargement), 2, "le modèle et son rendu")
        for r in telechargement:
            self.assertIsNone(r["auth"], "la clé ne doit pas partir vers l'hôte des fichiers")
        self.assertTrue(os.path.exists(self.chemin("caisse_rendered_image.webp")))

        with open(sortie, "rb") as f:
            self.assertEqual(f.read(4), b"glTF")
        with open(self.chemin("caisse.tripo.json"), encoding="utf-8") as f:
            fiche = json.load(f)
        self.assertEqual(fiche["task_id"], "tache-1")
        self.assertEqual(fiche["prompt"], "caisse en bois")
        self.assertEqual(fiche["modele_tripo"], "v3.1-20260211")
        self.assertEqual(fiche["parametres"]["face_limit"], 3000)
        self.assertEqual(fiche["type"], "text_to_model")
        self.assertEqual(fiche["etat"], "telecharge")
        self.assertEqual(fiche["credits"], 20)
        self.assertIn("date", fiche)
        self.assertEqual(fiche["controle"]["triangles"], 1)
        self.assertEqual(fiche["controle"]["dimensions_m"], [2.0, 2.0, 0.0])
        self.assertEqual(sorted(f["fichier"] for f in fiche["sorties"]),
                         ["caisse.glb", "caisse_rendered_image.webp"], "pas de chemin absolu dans la fiche")
        self.assertNotIn(self.dossier, json.dumps(fiche))

    def test_fiche_chemins_relatifs_et_entree_hors_projet(self):
        os.makedirs(self.chemin("concepts"))
        os.makedirs(self.chemin("assets"))
        dedans = self.chemin("concepts/ref.png")
        with open(dedans, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\0" * 32)
        res = self.lancer("image", dedans, "--sortie", self.chemin("assets/a.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        with open(self.chemin("assets/a.tripo.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["entrees"][0]["fichier"], os.path.join("..", "concepts", "ref.png"))

        ailleurs = tempfile.mkdtemp()
        dehors = os.path.join(ailleurs, "hors_projet.png")
        with open(dehors, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\1" * 32)
        res = self.lancer("image", dehors, "--sortie", self.chemin("assets/b.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        with open(self.chemin("assets/b.tripo.json"), encoding="utf-8") as f:
            fiche = json.load(f)
        entree = fiche["entrees"][0]
        self.assertNotIn("fichier", entree)
        self.assertEqual(entree["nom"], "hors_projet.png")
        self.assertEqual(len(entree["sha256"]), 64)
        self.assertNotIn(ailleurs, json.dumps(fiche))

    def test_negatif_trop_long(self):
        res = self.lancer("texte", "caisse", "--negatif", "x" * 256, "--sortie", self.chemin("c.glb"))
        self.assertEqual(res.returncode, 2)
        self.assertIn("255", res.stderr)
        self.assertIn("(256)", res.stderr)
        self.assertEqual(self.serveur.requetes, [])
        res = self.lancer("texte", "caisse", "--negatif", "x" * 255, "--sortie", self.chemin("c.glb"), "--a-blanc")
        self.assertEqual(res.returncode, 0, res.stderr)

    def test_telechargement_coupe_puis_repris(self):
        self.serveur.scenario["coupures"] = 2
        self.serveur.scenario["partiels"] = 1
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("coupée en cours de transfert", res.stderr)
        self.assertIn("Nouvel essai", res.stderr)
        with open(self.chemin("x.glb"), "rb") as f:
            self.assertEqual(f.read(4), b"glTF")

    def test_telechargement_toujours_coupe(self):
        self.serveur.scenario["coupures"] = 99
        res = self.lancer("texte", "lampe", "--sortie", self.chemin("lampe.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 1, "une coupure n'est pas un hôte bloqué (code 5)")
        self.assertIn("abandonné après 4 essais", res.stderr)
        self.assertIn(f"tripo.py telecharger tache-1 --sortie {self.chemin('lampe.glb')}", res.stderr)
        self.assertIn("ne la relance pas", res.stderr)
        modeles = [r for r in self.serveur.requetes if r["chemin"].startswith("/fichiers/tache-1.glb")]
        self.assertEqual(len(modeles), 4)
        with open(self.chemin("lampe.tripo.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["etat"], "a_telecharger", "la tâche payée garde une trace")

        self.serveur.scenario["coupures"] = 0
        res = self.lancer("telecharger", "tache-1", "--sortie", self.chemin("lampe.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        with open(self.chemin("lampe.tripo.json"), encoding="utf-8") as f:
            fiche = json.load(f)
        self.assertEqual((fiche["etat"], fiche["prompt"]), ("telecharge", "lampe"))

    def test_sans_texture_desactive_aussi_pbr(self):
        res = self.lancer("texte", "rocher", "--sortie", self.chemin("rocher.glb"),
                          "--sans-texture", "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        corps = json.loads(self.serveur.requetes[0]["corps"])
        self.assertFalse(corps["texture"])
        self.assertFalse(corps["pbr"])
        self.assertNotIn("texture_seed", corps)

    def test_image_envoie_le_fichier_puis_cree_la_tache(self):
        image = self.chemin("ref.png")
        with open(image, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\0" * 32)
        res = self.lancer("image", image, "--sortie", self.chemin("ref.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        envoi, creation = self.serveur.requetes[0], self.serveur.requetes[1]
        self.assertEqual(envoi["chemin"], "/v3/files")
        self.assertTrue(envoi["type"].startswith("multipart/form-data"))
        self.assertIn(b'name="file"; filename="ref.png"', envoi["corps"])
        self.assertEqual(creation["chemin"], "/v3/generation/image-to-model")
        self.assertEqual(json.loads(creation["corps"])["input"], "file_test_123")
        with open(self.chemin("ref.tripo.json"), encoding="utf-8") as f:
            fiche = json.load(f)
        self.assertEqual(fiche["entrees"][0]["fichier"], "ref.png", "chemin relatif au dossier de la fiche")
        self.assertEqual(len(fiche["entrees"][0]["sha256"]), 64)
        self.assertEqual(fiche["parametres"]["input"], "<fichier envoyé : image>",
                         "le file_token éphémère n'est pas gardé dans la fiche")

    def test_format_fbx_passe_par_une_conversion(self):
        res = self.lancer("texte", "tonneau", "--sortie", self.chemin("tonneau.fbx"),
                          "--format", "fbx", "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        conversion = [r for r in self.serveur.requetes if r["chemin"] == "/v3/models/convert"]
        self.assertEqual(len(conversion), 1)
        self.assertEqual(json.loads(conversion[0]["corps"]), {"input": "tache-1", "format": "FBX"})
        with open(self.chemin("tonneau.tripo.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["conversion"]["task_id"], "tache-2")

    def test_sans_attendre_puis_telecharger(self):
        sortie = self.chemin("lampe.glb")
        res = self.lancer("texte", "lampe", "--sortie", sortie, "--sans-attendre")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertFalse(os.path.exists(sortie))
        with open(self.chemin("lampe.tripo.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["etat"], "en_cours")

        res = self.lancer("telecharger", "tache-1", "--sortie", sortie, "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        with open(self.chemin("lampe.tripo.json"), encoding="utf-8") as f:
            fiche = json.load(f)
        self.assertEqual(fiche["etat"], "telecharge")
        self.assertEqual(fiche["prompt"], "lampe", "la fiche d'origine est conservée")

    def test_telecharger_sans_fiche_la_reconstitue(self):
        res = self.lancer("telecharger", "tache-42", "--sortie", self.chemin("x.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        with open(self.chemin("x.tripo.json"), encoding="utf-8") as f:
            fiche = json.load(f)
        self.assertEqual(fiche["task_id"], "tache-42")
        self.assertEqual(fiche["prompt"], "caisse en bois")
        self.assertEqual(fiche["modele_tripo"], "v3.1-20260211")

    def test_panne_passagere_pendant_le_suivi(self):
        self.serveur.scenario["pannes"] = 2
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("nouvel essai", res.stderr)
        self.assertEqual(len([r for r in self.serveur.requetes if r["methode"] == "POST"]), 1)

    def test_telecharger_ne_convertit_pas(self):
        res = self.lancer("telecharger", "tache-5", "--sortie", self.chemin("x.fbx"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 2)
        self.assertIn("task_id de la conversion", res.stderr)
        self.assertEqual([r for r in self.serveur.requetes if r["methode"] == "POST"], [], "aucune tâche payante")
        self.assertFalse(os.path.exists(self.chemin("x.fbx")))

    def test_statut(self):
        self.serveur.scenario["suite"] = ["running"]
        res = self.lancer("statut", "tache-9")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("tache-9 : running (40 %)", res.stdout)

    def test_a_blanc_n_envoie_rien(self):
        res = self.lancer("texte", "banc", "--sortie", self.chemin("banc.glb"), "--a-blanc")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(self.serveur.requetes, [])
        self.assertIn('"prompt": "banc"', res.stdout)

    def test_refuse_d_ecraser(self):
        sortie = self.chemin("deja.glb")
        open(sortie, "wb").close()
        res = self.lancer("texte", "x", "--sortie", sortie)
        self.assertEqual(res.returncode, 2)
        self.assertEqual(self.serveur.requetes, [])

    def test_inspecter(self):
        chemin = self.chemin("t.glb")
        with open(chemin, "wb") as f:
            f.write(glb_triangle(echelle=0.5))
        res = self.lancer("inspecter", chemin, cle=None)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("1 triangles", res.stdout)
        self.assertIn("0.5 × 0.5 × 0 m", res.stdout)

    def test_verifier_tout_va_bien(self):
        res = self.lancer("verifier")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("Crédits disponibles : 1234.0", res.stdout)
        self.assertIn("valeur masquée", res.stdout)


class TestCapacites(BaseTest):
    """Une commande par endpoint de l'apiv3 : chemin, corps envoyé, fichiers écrits."""

    def creation(self):
        creations = [r for r in self.serveur.requetes
                     if r["methode"] == "POST" and r["chemin"] not in ("/v3/files", "/v3/files/presign", "/v3/tasks/list")]
        self.assertTrue(creations, "aucune tâche créée")
        return creations[0]["chemin"], json.loads(creations[0]["corps"])

    def fiche(self, nom):
        with open(self.chemin(nom), encoding="utf-8") as f:
            return json.load(f)

    def image(self, nom="vue.png"):
        chemin = self.chemin(nom)
        with open(chemin, "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n" + b"\0" * 32)
        return chemin

    def ok(self, *args):
        res = self.lancer(*args, "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        return res

    def test_multivue_depuis_fichiers(self):
        self.ok("multivue", "--face", self.image("f.png"), "--dos", "https://exemple.test/dos.png",
                "--sortie", self.chemin("m.glb"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/generation/multiview-to-model")
        self.assertEqual(corps["inputs"], ["file_test_123", None, "https://exemple.test/dos.png", None])
        self.assertEqual([e["role"] for e in self.fiche("m.tripo.json")["entrees"]], ["face", "dos"])

    def test_multivue_depuis_tache(self):
        self.ok("multivue", "--depuis-tache", "tache-mv", "--sortie", self.chemin("m.glb"))
        self.assertEqual(self.creation()[1]["inputs"], [{"task_id": "tache-mv"}])

    def test_image_par_multivue(self):
        res = self.ok("image", self.image("concept.png"), "--multivue", "--faces", "1500",
                      "--sortie", self.chemin("baril.glb"))
        creations = [(r["chemin"], json.loads(r["corps"])) for r in self.serveur.requetes
                     if r["methode"] == "POST" and r["chemin"].startswith("/v3/generation/")]
        self.assertEqual(creations[0], ("/v3/generation/image-to-multiview", {"input": "file_test_123"}))
        chemin, corps = creations[1]
        self.assertEqual(chemin, "/v3/generation/multiview-to-model")
        self.assertEqual(corps["inputs"], [{"task_id": "tache-1"}], "les vues passent par leur task_id")
        self.assertEqual(corps["face_limit"], 1500)
        self.assertEqual(len(creations), 2, "pas de génération image → modèle directe")
        for vue in ("front", "left", "back", "right"):
            self.assertTrue(os.path.exists(self.chemin(f"baril_{vue}_view.png")), vue)
        self.assertIn("Vue écrite", res.stdout)
        with open(self.chemin("baril.glb"), "rb") as f:
            self.assertEqual(f.read(4), b"glTF")
        fiche = self.fiche("baril.tripo.json")
        self.assertEqual(fiche["type"], "image_to_multiview_to_model")
        self.assertEqual(fiche["multivue"]["task_id"], "tache-1")
        self.assertIn("baril_front_view.png", fiche["multivue"]["vues"])
        self.assertEqual([e["role"] for e in fiche["entrees"]], ["image", "vues"])

    def test_image_par_multivue_a_blanc_et_refus(self):
        res = self.lancer("image", self.image(), "--multivue", "--sortie", self.chemin("m.glb"), "--a-blanc", cle=None)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("image-to-multiview", res.stdout)
        self.assertIn("multiview-to-model", res.stdout)
        self.assertEqual(self.serveur.requetes, [])
        res = self.lancer("image", self.image(), "--multivue", "--autofix", "--sortie", self.chemin("m.glb"),
                          "--a-blanc", cle=None)
        self.assertEqual(res.returncode, 2)

    def test_multivue_sans_face(self):
        res = self.lancer("multivue", "--dos", self.image(), "--sortie", self.chemin("m.glb"))
        self.assertEqual(res.returncode, 2)

    def test_options_de_generation(self):
        self.ok("texte", "statue", "--sortie", self.chemin("s.glb"), "--qualite-texture", "detailed",
                "--version-texture", "v3.5-20260815", "--qualite-geometrie", "detailed", "--taille-auto",
                "--low-poly", "--param", "export_uv=false", "--param", 'export_orientation="+x"')
        corps = self.creation()[1]
        for cle, valeur in (("texture_quality", "detailed"), ("texture_version", "v3.5-20260815"),
                            ("geometry_quality", "detailed"), ("auto_size", True), ("smart_low_poly", True),
                            ("export_uv", False), ("export_orientation", "+x")):
            self.assertEqual(corps[cle], valeur, cle)

    def test_quad_donne_un_fbx_sans_conversion(self):
        self.ok("texte", "chaise", "--quad", "--format", "fbx", "--sortie", self.chemin("c.fbx"))
        self.assertTrue(self.creation()[1]["quad"])
        self.assertFalse([r for r in self.serveur.requetes if r["chemin"] == "/v3/models/convert"])
        self.assertTrue(os.path.exists(self.chemin("c.fbx")))

    def test_quad_exige_fbx(self):
        res = self.lancer("texte", "chaise", "--quad", "--sortie", self.chemin("c.glb"))
        self.assertEqual(res.returncode, 2)

    def test_parties_exige_sans_texture(self):
        res = self.lancer("texte", "robot", "--parties", "--sortie", self.chemin("r.glb"))
        self.assertEqual(res.returncode, 2)
        self.ok("texte", "robot", "--parties", "--sans-texture", "--sortie", self.chemin("r.glb"))
        self.assertTrue(self.creation()[1]["generate_parts"])

    def test_param_ne_remplace_pas_une_option(self):
        res = self.lancer("texte", "x", "--faces", "100", "--param", "face_limit=200", "--sortie", self.chemin("x.glb"))
        self.assertEqual(res.returncode, 2)

    def test_image_texte(self):
        res = self.ok("image-texte", "concept de caisse", "--modele", "seedream_v5", "--taille", "2048x2048",
                      "--sortie", self.chemin("concept.png"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/generation/text-to-image")
        self.assertEqual(corps, {"prompt": "concept de caisse", "model": "seedream_v5", "size": "2048x2048"})
        self.assertIn("Image écrite :", res.stdout)
        self.assertTrue(os.path.exists(self.chemin("concept.png")))

    def test_image_texte_combinaisons_selon_le_modele(self):
        def a_blanc(*options):
            return self.lancer("image-texte", "caisse", *options, "--sortie", self.chemin("c.png"), "--a-blanc",
                               cle=None)
        res = a_blanc("--ratio", "1:1")
        self.assertEqual(res.returncode, 2, "le modèle par défaut (seedream) refuse aspect_ratio")
        self.assertIn("banana", res.stderr)
        self.assertEqual(a_blanc("--modele", "chat_image", "--ratio", "16:9").returncode, 2)
        self.assertEqual(a_blanc("--modele", "nano_banana", "--ratio", "1:1").returncode, 0)
        res = a_blanc("--taille", "1024x1024")
        self.assertEqual(res.returncode, 2, "seedream refuse 1024x1024 (pixels sous le minimum)")
        self.assertIn("2048x2048", res.stderr)
        self.assertEqual(a_blanc("--modele", "seedream_v4", "--taille", "2048x2048").returncode, 0)
        self.assertEqual(a_blanc("--taille", "2560x1440").returncode, 0)
        self.assertEqual(a_blanc("--taille", "8192x8192").returncode, 2)
        self.assertEqual(a_blanc("--modele", "chat_image", "--taille", "1024x1024").returncode, 0)
        self.assertEqual(a_blanc("--taille", "grand").returncode, 2)
        res = a_blanc("--negatif", "y" * 300)
        self.assertEqual(res.returncode, 2)
        self.assertIn("(300)", res.stderr)

    def test_image_image_plusieurs_references(self):
        self.ok("image-image", self.image("a.png"), "https://exemple.test/b.png", "--prompt", "même objet, rouillé",
                "--t-pose", "--sortie", self.chemin("r.png"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/generation/image-to-image")
        self.assertEqual(corps["inputs"], ["file_test_123", "https://exemple.test/b.png"])
        self.assertTrue(corps["t_pose"])

    def test_image_image_sans_consigne(self):
        res = self.lancer("image-image", self.image(), "--sortie", self.chemin("r.png"))
        self.assertEqual(res.returncode, 2)

    def test_image_multivue_ecrit_quatre_vues(self):
        self.ok("image-multivue", self.image(), "--sortie", self.chemin("caisse.png"))
        self.assertEqual(self.creation()[0], "/v3/generation/image-to-multiview")
        for vue in ("front", "left", "back", "right"):
            self.assertTrue(os.path.exists(self.chemin(f"caisse_{vue}_view.png")), vue)
        self.assertEqual(len(self.fiche("caisse.tripo.json")["sorties"]), 4)

    def test_editer_multivue(self):
        self.ok("editer-multivue", "tache-mv", "--vue", "front=porte ouverte", "--vue", "back=rouille",
                "--sortie", self.chemin("e.png"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/generation/edit-multiview")
        self.assertEqual(corps, {"input": "tache-mv", "prompts": [{"view": "front", "prompt": "porte ouverte"},
                                                                   {"view": "back", "prompt": "rouille"}]})
        res = self.lancer("editer-multivue", "t", "--vue", "dessus=x", "--sortie", self.chemin("e2.png"))
        self.assertEqual(res.returncode, 2)

    def test_splat(self):
        self.ok("splat", self.image(), "--graine", "3", "--sortie", self.chemin("s.ply"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/generation/image-to-splat")
        self.assertEqual(corps["model_seed"], 3)
        self.assertTrue(os.path.exists(self.chemin("s.ply")))

    def test_profondeur(self):
        self.ok("profondeur", self.image(), "--type", "color", "--resolution", "504", "--sortie", self.chemin("p.png"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/generation/image-to-depth")
        self.assertEqual((corps["kind"], corps["process_res"]), ("color", 504))
        self.assertTrue(os.path.exists(self.chemin("p.png")))
        res = self.lancer("profondeur", self.image(), "--resolution", "5000", "--sortie", self.chemin("p2.png"))
        self.assertEqual(res.returncode, 2)

    def test_retexturer(self):
        self.ok("retexturer", "tache-modele", "--prompt-texture", "bois peint en vert", "--image-style", self.image(),
                "--modele", "v3.5-20260815", "--pieces", "couvercle, corps", "--sortie", self.chemin("t.glb"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/models/texture")
        self.assertEqual(corps["input"], "tache-modele")
        self.assertEqual(corps["texture_prompt"], {"text": "bois peint en vert", "style_image": "file_test_123"})
        self.assertEqual(corps["part_names"], ["couvercle", "corps"])
        fiche = self.fiche("t.tripo.json")
        self.assertEqual(fiche["parametres"]["texture_prompt"]["style_image"], "<fichier envoyé : image_style>")
        self.assertEqual(fiche["entrees"][0], {"role": "modele", "task_id": "tache-modele"})

    def test_convertir(self):
        self.ok("convertir", "tache-modele", "--format", "fbx", "--echelle", "0.01", "--pivot-bas",
                "--taille-texture", "2048", "--sortie", self.chemin("c.fbx"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/models/convert")
        self.assertEqual(corps, {"input": "tache-modele", "format": "FBX", "texture_size": 2048,
                                 "scale_factor": 0.01, "pivot_to_center_bottom": True})

    def test_importer_gros_fichier_par_url_presignee(self):
        gros = self.chemin("gros.glb")
        with open(gros, "wb") as f:
            f.truncate(51 * 1024 * 1024)
        res = self.ok("importer", gros, "--sortie", self.chemin("i.glb"))
        chemins = [r["chemin"] for r in self.serveur.requetes]
        self.assertIn("/v3/files/presign", chemins)
        self.assertIn("/depot/gros?sig=1", chemins)
        depot = [r for r in self.serveur.requetes if r["chemin"].startswith("/depot/")][0]
        self.assertIsNone(depot["auth"], "la clé ne part pas vers l'URL pré-signée")
        self.assertEqual(self.creation(), ("/v3/models/import", {"input": "file_gros_456"}))
        self.assertIn("sans fichier à télécharger", res.stdout)

    def test_importer_refuse_un_format_inconnu(self):
        mauvais = self.chemin("m.blend")
        open(mauvais, "wb").close()
        res = self.lancer("importer", mauvais, "--sortie", self.chemin("i.glb"))
        self.assertEqual(res.returncode, 2)

    def test_decimer(self):
        self.ok("decimer", "tache-modele", "--faces", "1500", "--modele", "v3.0", "--uv-intelligentes",
                "--sortie", self.chemin("d.glb"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/mesh/decimate")
        self.assertEqual(corps, {"input": "tache-modele", "model": "v3.0", "face_limit": 1500, "smart_uv": True})
        res = self.lancer("decimer", "t", "--uv-intelligentes", "--sortie", self.chemin("d2.glb"))
        self.assertEqual(res.returncode, 2)

    def test_uv_telecharge_le_rendu_uv(self):
        self.ok("uv", "tache-modele", "--sortie", self.chemin("u.glb"))
        self.assertEqual(self.creation()[0], "/v3/mesh/uv")
        self.assertTrue(os.path.exists(self.chemin("u_uv_render.png")))

    def test_segmenter_et_completer(self):
        self.ok("segmenter", "tache-modele", "--modele", "v2.0-20260430", "--par-connexite",
                "--sortie", self.chemin("s.glb"))
        self.assertEqual(self.creation(), ("/v3/mesh/segment", {
            "input": "tache-modele", "model": "v2.0-20260430", "split_by_connectivity": True}))
        self.serveur.requetes.clear()
        self.ok("completer", "tache-seg", "--mode", "quick_cap", "--pieces", "roue", "--sortie", self.chemin("c.glb"))
        self.assertEqual(self.creation(), ("/v3/mesh/complete", {
            "input": "tache-seg", "completion_mode": "quick_cap", "part_names": ["roue"]}))

    def test_segmenter_intelligent(self):
        glb = self.chemin("source.glb")
        with open(glb, "wb") as f:
            f.write(glb_triangle())
        self.ok("segmenter-intelligent", glb, "--granularite", "fine", "--indice", "roues",
                "--sortie", self.chemin("si.glb"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/mesh/smartsegment")
        self.assertEqual(corps["seg_type"], "model")
        self.assertEqual(len(corps["transform"]), 16)
        self.assertEqual((corps["granularity"], corps["hint"]), ("fine", "roues"))
        res = self.lancer("segmenter-intelligent", "tache-modele", "--sortie", self.chemin("si2.glb"))
        self.assertEqual(res.returncode, 2, "smartsegment n'accepte pas de task_id")

    def test_riggable(self):
        res = self.ok("riggable", "tache-modele")
        self.assertEqual(self.creation(), ("/v3/animations/rig-check", {"input": "tache-modele"}))
        self.assertIn("Riggable : oui (squelette détecté : biped)", res.stdout)

    def test_riggable_non_explique_l_orientation(self):
        self.serveur.scenario["non_riggable"] = True
        res = self.ok("riggable", "tache-modele")
        self.assertIn("Riggable : non", res.stdout)
        self.assertIn("l'avant vers +X", res.stdout)
        self.assertIn("--avant -z", res.stdout)

    def test_rigger(self):
        self.ok("rigger", "tache-modele", "--type", "quadruped", "--spec", "mixamo", "--sortie", self.chemin("r.glb"))
        self.assertEqual(self.creation(), ("/v3/animations/rig", {
            "input": "tache-modele", "model": "v3.0-20260909", "rig_type": "quadruped", "spec": "mixamo",
            "out_format": "glb"}), "sans --modele, un modèle de rig valide (le défaut de l'API est refusé)")
        res = self.lancer("rigger", "t", "--modele", "v1.0-20240301", "--spec", "unity",
                          "--sortie", self.chemin("r2.glb"))
        self.assertEqual(res.returncode, 2, "unity exige un modèle de rig récent")

    def test_rigger_modele_par_defaut_a_blanc(self):
        res = self.lancer("rigger", "t", "--sortie", self.chemin("r.glb"), "--a-blanc", cle=None)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn('"model": "v3.0-20260909"', res.stdout)
        res = self.lancer("rigger", "t", "--modele", "v2.5-20260210", "--sortie", self.chemin("r.glb"), "--a-blanc",
                          cle=None)
        self.assertIn('"model": "v2.5-20260210"', res.stdout)
        aide = self.lancer("rigger", "--help", cle=None).stdout
        self.assertIn("v3.0-20260909", aide)

    def test_rigger_avant_moins_z_tourne_le_glb(self):
        glb = self.chemin("perso.glb")
        with open(glb, "wb") as f:
            f.write(glb_triangle(echelle=1.0))
        res = self.ok("rigger", glb, "--avant", "-z", "--sortie", self.chemin("perso_rig.glb"))
        self.assertIn("réorienté", res.stderr)
        self.assertIn("+90°", res.stdout)
        envoi = [r for r in self.serveur.requetes if r["chemin"] == "/v3/files"][0]["corps"]
        debut = envoi.index(b"glTF")
        envoye = envoi[debut:envoi.rindex(b"\r\n--")]
        _, gltf, binaire = tripo.lire_glb(envoye, "envoi")
        self.assertEqual(struct.unpack_from("<9f", binaire),
                         (0, 0, 0, 0, 0, 1, 0, 1, 0), "x devient z : l'avant -z passe sur +x")
        with open(glb, "rb") as f:
            self.assertEqual(f.read(), glb_triangle(echelle=1.0), "le fichier d'origine n'est pas modifié")
        fiche = self.fiche("perso_rig.tripo.json")
        self.assertEqual(fiche["entrees"][0]["fichier"], "perso.glb")
        self.assertIn("reorientation", fiche["entrees"][0])
        self.assertEqual(fiche["avant_origine"], "-z")

    def test_riggable_avant(self):
        glb = self.chemin("perso.glb")
        with open(glb, "wb") as f:
            f.write(glb_triangle())
        res = self.lancer("riggable", glb, "--avant", "+z", "--a-blanc", cle=None)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("réorienté", res.stderr)
        res = self.lancer("riggable", "tache-modele", "--avant", "-z", "--a-blanc", cle=None)
        self.assertEqual(res.returncode, 2, "un task_id Tripo est déjà orienté vers +X")
        rigge = self.chemin("rigge.glb")
        with open(rigge, "wb") as f:
            f.write(glb_triangle(skins=[{"joints": [0]}]))
        res = self.lancer("riggable", rigge, "--avant", "-z", "--a-blanc", cle=None)
        self.assertEqual(res.returncode, 2)
        self.assertIn("réorientation impossible", res.stderr)
        aide = self.lancer("riggable", "--help", cle=None).stdout
        self.assertNotIn("--sortie", aide, "riggable n'écrit pas de fichier")

    def test_animer_plusieurs_animations(self):
        self.ok("animer", "tache-rig", "--animation", "walk", "--animation", "preset:run", "--sur-place",
                "--sortie", self.chemin("perso.glb"))
        chemin, corps = self.creation()
        self.assertEqual(chemin, "/v3/animations/retarget")
        self.assertEqual(corps["animations"], ["preset:walk", "preset:run"])
        self.assertTrue(corps["animate_in_place"])
        self.assertTrue(os.path.exists(self.chemin("perso_model_1.glb")))
        self.assertTrue(os.path.exists(self.chemin("perso_model_2.glb")))
        res = self.lancer("animer", "t", *sum((["--animation", "walk"] for _ in range(6)), []),
                          "--sortie", self.chemin("x.glb"))
        self.assertEqual(res.returncode, 2)

    def test_taches(self):
        res = self.lancer("taches", "tache-1", "inconnu-2")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Tâche tache-1 : success", res.stdout)
        self.assertIn("inconnu-2 : introuvable", res.stdout)

    def test_consommation(self):
        res = self.lancer("consommation", "--limite", "2")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Total sur ces 2 tâches : 20 crédits", res.stdout)
        self.assertIn("limit=2", [r["chemin"] for r in self.serveur.requetes][0])

    def test_envoyer(self):
        res = self.lancer("envoyer", self.image())
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("file_token : file_test_123", res.stdout)

    def test_brut(self):
        self.ok("brut", "/v3/mesh/nouveau", "--corps", '{"input": "tache-modele", "option": 1}',
                "--sortie", self.chemin("b.glb"))
        self.assertEqual(self.creation(), ("/v3/mesh/nouveau", {"input": "tache-modele", "option": 1}))
        res = self.lancer("brut", "/v2/openapi/task", "--corps", "{}", "--sortie", self.chemin("b2.glb"))
        self.assertEqual(res.returncode, 2)

    def test_telecharger_devine_la_nature(self):
        self.serveur.operations["tache-img"] = "/v3/generation/text-to-image"
        self.ok("telecharger", "tache-img", "--sortie", self.chemin("i.png"))
        self.assertTrue(os.path.exists(self.chemin("i.png")))

    def test_a_blanc_sans_cle_ni_reseau(self):
        res = self.lancer("multivue", "--face", self.image(), "--sortie", self.chemin("m.glb"), "--a-blanc", cle=None)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(self.serveur.requetes, [])
        self.assertIn("<file_token de vue.png>", res.stdout)


class TestErreurs(BaseTest):
    def test_cle_absente(self):
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), cle=None)
        self.assertEqual(res.returncode, 3)
        self.assertIn("TRIPO_API_KEY n'est pas définie", res.stderr)
        self.assertEqual(self.serveur.requetes, [], "aucun appel réseau sans clé")

    def test_verifier_cle_absente(self):
        res = self.lancer("verifier", cle=None)
        self.assertEqual(res.returncode, 3)
        self.assertIn("joignable", res.stdout, "les hôtes sont quand même testés")

    def test_cle_refusee_401(self):
        self.serveur.scenario["cle_refusee"] = True
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"))
        self.assertEqual(res.returncode, 3)
        self.assertIn("refuse la clé", res.stderr)

    def test_verifier_cle_refusee(self):
        self.serveur.scenario["cle_refusee"] = True
        res = self.lancer("verifier")
        self.assertEqual(res.returncode, 3)

    def test_credits_epuises(self):
        self.serveur.scenario["erreur_creation"] = (403, 2010, "You don't have enough credit")
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"))
        self.assertEqual(res.returncode, 4)
        self.assertIn("Crédits Tripo insuffisants", res.stderr)

    def test_contenu_refuse(self):
        self.serveur.scenario["erreur_creation"] = (400, 2008, "content policy")
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"))
        self.assertEqual(res.returncode, 8)

    def test_tache_bannie(self):
        self.serveur.scenario["suite"] = ["queued", "banned"]
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 8)

    def test_limite_de_debit(self):
        self.serveur.scenario["erreur_creation"] = (429, 2000, "concurrency limit")
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"))
        self.assertEqual(res.returncode, 9)
        self.assertIn("une seule tâche à la fois", res.stderr)
        creations = [r for r in self.serveur.requetes if r["methode"] == "POST"]
        self.assertEqual(len(creations), len(tripo.ATTENTES_LIMITE) + 1, "quelques essais, puis abandon")

    def test_limite_passagere_puis_creation(self):
        self.serveur.scenario["limites"] = 2
        res = self.lancer("image-texte", "caisse", "--sortie", self.chemin("c.png"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("tâches simultanées", res.stderr)
        creations = [r for r in self.serveur.requetes if r["chemin"] == "/v3/generation/text-to-image"]
        self.assertEqual(len(creations), 3)

    def test_erreur_serveur_a_la_creation_non_rejouee(self):
        self.serveur.scenario["erreur_creation"] = (500, 500, "internal")
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"))
        self.assertEqual(res.returncode, 1)
        creations = [r for r in self.serveur.requetes if r["methode"] == "POST"]
        self.assertEqual(len(creations), 1, "une création qui a pu aboutir n'est jamais rejouée")

    def test_tache_echouee(self):
        self.serveur.scenario["suite"] = ["running", "failed"]
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 6)
        self.assertIn("a échoué", res.stderr)
        self.assertIn("generation failed", res.stderr)
        self.assertFalse(os.path.exists(self.chemin("x.glb")))

    def test_statut_tache_echouee(self):
        self.serveur.scenario["suite"] = ["failed"]
        res = self.lancer("statut", "tache-3")
        self.assertEqual(res.returncode, 6)

    def test_delai_depasse(self):
        self.serveur.scenario["suite"] = ["running"]
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), "--delai", "0.3", "--intervalle", "0.05")
        self.assertEqual(res.returncode, 7)
        self.assertIn("telecharger tache-1", res.stderr)

    def test_url_expiree(self):
        self.serveur.scenario["fichier_expire"] = True
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), "--intervalle", "0.01")
        self.assertEqual(res.returncode, 1)
        self.assertIn("telecharger tache-1", res.stderr)

    def test_argument_invalide(self):
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.obj"))
        self.assertEqual(res.returncode, 2)
        res = self.lancer("texte")
        self.assertEqual(res.returncode, 2)


class TestReseauBloque(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.proxy = demarrer(FauxProxyBloquant)
        cls.url_proxy = f"http://127.0.0.1:{cls.proxy.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.proxy.shutdown()
        cls.proxy.server_close()
        super().tearDownClass()

    def env_bloque(self, **extra):
        return {"HTTPS_PROXY": self.url_proxy, "https_proxy": self.url_proxy,
                "TRIPO_API_BASE": "https://openapi.tripo3d.invalid", **extra}

    def test_api_bloquee_par_le_proxy(self):
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), env_extra=self.env_bloque())
        self.assertEqual(res.returncode, 5)
        self.assertIn("openapi.tripo3d.invalid est bloqué par la politique réseau", res.stderr)

    def test_verifier_nomme_chaque_hote_bloque(self):
        res = self.lancer("verifier", env_extra=self.env_bloque(
            TRIPO_HOTES_FICHIERS="https://cdn.tripo3d.invalid"))
        self.assertEqual(res.returncode, 5)
        self.assertIn("✗ openapi.tripo3d.invalid (API)", res.stdout)
        self.assertIn("✗ cdn.tripo3d.invalid (fichiers)", res.stdout)

    def test_telechargement_bloque_par_le_proxy(self):
        # API joignable, fichiers sur un hôte refusé : code 5 tout de suite, avec la commande de reprise.
        self.serveur.scenario["base_fichiers"] = "https://fichiers.tripo3d.invalid"
        res = self.lancer("texte", "x", "--sortie", self.chemin("x.glb"), "--intervalle", "0.01",
                          env_extra={"HTTPS_PROXY": self.url_proxy, "https_proxy": self.url_proxy})
        self.assertEqual(res.returncode, 5)
        self.assertIn("fichiers.tripo3d.invalid est bloqué", res.stderr)
        self.assertNotIn("Nouvel essai", res.stderr, "un hôte refusé n'est pas réessayé")
        self.assertIn("tripo.py telecharger tache-1 --sortie", res.stderr)

    def test_hote_des_fichiers_bloque(self):
        # API joignable, mais l'URL du modèle vise un hôte que le proxy refuse.
        res = self.lancer("verifier", env_extra={
            "HTTPS_PROXY": self.url_proxy, "https_proxy": self.url_proxy,
            "TRIPO_HOTES_FICHIERS": "https://fichiers.tripo3d.invalid"})
        self.assertEqual(res.returncode, 5)
        self.assertIn("✓ 127.0.0.1 (API)", res.stdout)
        self.assertIn("fichiers.tripo3d.invalid est bloqué", res.stdout)
        self.assertIn("Crédits disponibles", res.stdout)


class TestReorientation(unittest.TestCase):
    def test_avant_moins_z_vers_plus_x_avec_echelle_et_normales(self):
        source = glb_triangle(echelle=2.0, normales=True)
        tourne = tripo.reorienter_glb(source, "-z", "t.glb")
        _, gltf, binaire = tripo.lire_glb(tourne, "t.glb")
        self.assertNotIn("scale", gltf["nodes"][0], "la transformation du nœud est appliquée aux sommets")
        self.assertEqual(struct.unpack_from("<9f", binaire), (0, 0, 0, 0, 0, 2, 0, 2, 0))
        self.assertEqual(struct.unpack_from("<3f", binaire, 36), (-1, 0, 0), "le dos (+Z) passe sur -X")
        self.assertEqual((gltf["accessors"][0]["min"], gltf["accessors"][0]["max"]), ([0, 0, 0], [0, 2, 2]))

    def test_les_quatre_orientations(self):
        attendu = {"+x": (1, 0, 0), "-z": (0, 0, 1), "+z": (0, 0, -1), "-x": (-1, 0, 0)}
        for avant, sommet in attendu.items():
            _, _, binaire = tripo.lire_glb(tripo.reorienter_glb(glb_triangle(echelle=1.0), avant, "t.glb"), "t")
            self.assertEqual(struct.unpack_from("<3f", binaire, 12), sommet, avant)
        # Inverse : l'avant indiqué arrive bien sur +X.
        for avant, rotation in tripo.ROTATIONS_VERS_X.items():
            axe = {"+x": (1, 0, 0), "-x": (-1, 0, 0), "+z": (0, 0, 1), "-z": (0, 0, -1)}[avant]
            self.assertEqual(tripo._appliquer3(rotation, axe), [1, 0, 0], avant)

    def test_refus(self):
        for extra in ({"skins": [{"joints": [0]}]},
                      {"extensionsUsed": ["KHR_draco_mesh_compression"]}):
            with self.assertRaises(tripo.ErreurTripo) as ctx:
                tripo.reorienter_glb(glb_triangle(**extra), "-z", "t.glb")
            self.assertEqual(ctx.exception.code, tripo.USAGE)


class TestHook(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ICI, "..", "hooks", "hooks.json"), encoding="utf-8") as f:
            hooks = json.load(f)["hooks"]["SessionStart"]
        self.commande = hooks[0]["hooks"][0]["command"]

    def lancer(self, cle):
        env = {k: v for k, v in os.environ.items() if k != "TRIPO_API_KEY"}
        if cle:
            env["TRIPO_API_KEY"] = cle
        return subprocess.run(["sh", "-c", self.commande], capture_output=True, text=True, env=env, timeout=10)

    def test_silencieux_si_cle_definie(self):
        res = self.lancer(CLE)
        self.assertEqual(res.returncode, 0)
        self.assertEqual(res.stdout, "")

    def test_une_ligne_si_cle_absente(self):
        res = self.lancer(None)
        self.assertEqual(res.returncode, 0)
        self.assertEqual(len(res.stdout.strip().splitlines()), 1)
        self.assertIn("TRIPO_API_KEY", res.stdout)


if __name__ == "__main__":
    unittest.main()
