"""Tests de scripts/tripo.py contre un faux serveur HTTP local qui imite l'API Tripo (apiv3).

Lancer depuis la racine du repo :
    python3 -m unittest discover -s plugins/tripo/tests -v
"""

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


def glb_triangle(echelle=2.0):
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
    }
    bloc_json = json.dumps(gltf).encode("utf-8")
    bloc_json += b" " * (-len(bloc_json) % 4)
    total = 12 + 8 + len(bloc_json) + 8 + len(positions)
    return (struct.pack("<4sII", b"glTF", 2, total)
            + struct.pack("<II", len(bloc_json), 0x4E4F534A) + bloc_json
            + struct.pack("<II", len(positions), 0x004E4942) + positions)


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

    def do_GET(self):
        self._noter()
        sc = self.server.scenario
        if self.path == "/v3/account/balance":
            if sc.get("cle_refusee"):
                return self._refus_cle()
            return self._json(200, {"code": 0, "data": {"balance": 1234.0, "frozen": 20.0}})
        if self.path.startswith("/v3/tasks/"):
            if sc.get("pannes", 0) > 0:
                sc["pannes"] -= 1
                return self._json(500, {"code": 500, "status": "error", "message": "internal"})
            task_id = self.path.rsplit("/", 1)[1]
            etats = sc["etats"].setdefault(task_id, list(sc.get("suite", ["queued", "running", "success"])))
            statut = etats.pop(0) if len(etats) > 1 else etats[0]
            data = {"task_id": task_id, "type": "text_to_model", "status": statut,
                    "progress": 100 if statut == "success" else 40,
                    "input": {"prompt": "caisse en bois", "model": "v3.1-20260211"}}
            if statut == "success":
                ext = "fbx" if task_id in self.server.conversions else "glb"
                data["output"] = {"model_url": f"{self.server.base}/fichiers/{task_id}.{ext}?auth_key=xyz"}
                data["credits_consumed"] = 20
            if statut == "failed":
                data.update({"error_code": 5000, "error_msg": "generation failed"})
            return self._json(200, {"code": 0, "data": data})
        if self.path.startswith("/fichiers/"):
            if sc.get("fichier_expire"):
                self.send_response(403)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            corps = b"Kaydara FBX Binary  \x00" if ".fbx" in self.path else glb_triangle()
            self.send_response(200)
            self.send_header("Content-Type", "model/gltf-binary")
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
            return
        self._json(404, {"code": 404, "status": "error", "message": "not found"})

    def do_POST(self):
        longueur = int(self.headers.get("Content-Length") or 0)
        corps = self.rfile.read(longueur)
        self._noter(corps)
        sc = self.server.scenario
        if sc.get("cle_refusee"):
            return self._refus_cle()
        erreur = sc.get("erreur_creation")
        if erreur and self.path.startswith("/v3/generation/"):
            statut, code, message = erreur
            entetes = {"Retry-After": "1"} if statut == 429 else None
            return self._json(statut, {"code": code, "status": "error", "message": message,
                                       "suggestion": "test"}, entetes)
        if self.path == "/v3/files":
            return self._json(200, {"code": 0, "data": {"file_token": "file_test_123"}})
        if self.path.startswith("/v3/generation/") or self.path == "/v3/models/convert":
            self.server.compteur += 1
            if self.path == "/v3/models/convert":
                self.server.conversions.add(f"tache-{self.server.compteur}")
            return self._json(200, {"code": 0, "data": {"task_id": f"tache-{self.server.compteur}"}})
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
        self.serveur.conversions = set()
        self.dossier = tempfile.mkdtemp()
        self.sorties = []

    def lancer(self, *args, cle=CLE, env_extra=None):
        env = {k: v for k, v in os.environ.items()
               if k.upper() not in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "TRIPO_API_KEY")}
        env["NO_PROXY"] = "127.0.0.1,localhost"
        env["TRIPO_API_BASE"] = self.serveur.base
        env["TRIPO_HOTES_FICHIERS"] = self.serveur.base
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
        self.assertEqual(len(telechargement), 1)
        self.assertIsNone(telechargement[0]["auth"], "la clé ne doit pas partir vers l'hôte des fichiers")

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
        self.assertEqual(fiche["image"]["chemin"], image)
        self.assertEqual(len(fiche["image"]["sha256"]), 64)
        self.assertNotIn("input", fiche["parametres"])

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
        res = self.lancer("telecharger", "tache-5", "--sortie", self.chemin("x.fbx"), "--format", "fbx",
                          "--intervalle", "0.01")
        self.assertEqual(res.returncode, 2)
        self.assertIn("task_id de la tâche de conversion", res.stderr)
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
        creations = [r for r in self.serveur.requetes if r["methode"] == "POST"]
        self.assertEqual(len(creations), 1, "une création n'est jamais rejouée automatiquement")

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

    def test_hote_des_fichiers_bloque(self):
        # API joignable, mais l'URL du modèle vise un hôte que le proxy refuse.
        res = self.lancer("verifier", env_extra={
            "HTTPS_PROXY": self.url_proxy, "https_proxy": self.url_proxy,
            "TRIPO_HOTES_FICHIERS": "https://fichiers.tripo3d.invalid"})
        self.assertEqual(res.returncode, 5)
        self.assertIn("✓ 127.0.0.1 (API)", res.stdout)
        self.assertIn("fichiers.tripo3d.invalid est bloqué", res.stdout)
        self.assertIn("Crédits disponibles", res.stdout)


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
