"""Tests de scripts/uthana.py contre un faux serveur HTTP local qui imite l'API GraphQL d'Uthana.

Lancer depuis la racine du repo :
    python3 -m unittest discover -s plugins/uthana/tests -v
"""

import base64
import importlib.util
import json
import os
import struct
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ICI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(ICI, "..", "skills", "animer", "scripts", "uthana.py")
CLE = "uth_cle-de-test-ultra-secrete-0123456789"
AUTH = "Basic " + base64.b64encode(f"{CLE}:".encode()).decode()

_spec = importlib.util.spec_from_file_location("uthana", SCRIPT)
uthana = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uthana)


def glb_anime(duree=2.0, images=61, os_=3):
    """GLB minimal : un squelette de `os_` os et une animation de `duree` secondes."""
    temps = struct.pack(f"<{images}f", *[duree * i / (images - 1) for i in range(images)])
    gltf = {
        "asset": {"version": "2.0"},
        "nodes": [{"name": f"os{i}"} for i in range(os_)],
        "skins": [{"joints": list(range(os_))}],
        "meshes": [{"primitives": []}],
        "accessors": [{"bufferView": 0, "componentType": 5126, "count": images, "type": "SCALAR",
                       "min": [0.0], "max": [duree]}],
        "bufferViews": [{"buffer": 0, "byteLength": len(temps)}],
        "buffers": [{"byteLength": len(temps)}],
        "animations": [{"name": "Take 001", "samplers": [{"input": 0, "output": 0}],
                        "channels": [{"sampler": 0, "target": {"node": 0, "path": "rotation"}}]}],
    }
    bloc = json.dumps(gltf).encode()
    bloc += b" " * (-len(bloc) % 4)
    total = 12 + 8 + len(bloc) + 8 + len(temps)
    return (struct.pack("<4sII", b"glTF", 2, total) + struct.pack("<II", len(bloc), 0x4E4F534A) + bloc
            + struct.pack("<II", len(temps), 0x004E4942) + temps)


def multipart_operations(corps, type_contenu):
    frontiere = type_contenu.split("boundary=")[1].encode()
    for partie in corps.split(b"--" + frontiere):
        if b'name="operations"' in partie:
            return json.loads(partie.split(b"\r\n\r\n", 1)[1].rsplit(b"\r\n", 1)[0])
    return {}


class FauxUthana(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _envoyer(self, statut, corps, type_contenu="application/json"):
        self.send_response(statut)
        self.send_header("Content-Type", type_contenu)
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        try:
            self.wfile.write(corps)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, statut, charge):
        self._envoyer(statut, json.dumps(charge).encode())

    def _noter(self, corps=b"", operation=None):
        self.server.requetes.append({"methode": self.command, "chemin": self.path,
                                     "auth": self.headers.get("Authorization"),
                                     "type": self.headers.get("Content-Type"),
                                     "corps": corps, "operation": operation})

    def do_GET(self):
        self._noter()
        sc = self.server.scenario
        chemin = urllib.parse.urlsplit(self.path).path
        if chemin == "/graphql":
            return self._json(400, {"errors": [{"message": "Must provide query string."}]})
        if self.headers.get("Authorization") != AUTH:
            return self._json(401, {"error": "invalid_token"})
        if chemin.startswith("/motion/file/") or chemin.startswith("/motion/bundle/"):
            if sc.get("telechargement_refuse"):
                return self._envoyer(403, b"quota exceeded", "text/plain")
            return self._envoyer(200, glb_anime(), "model/gltf-binary")
        self._envoyer(404, b"not found", "text/plain")

    def do_POST(self):
        longueur = int(self.headers.get("Content-Length") or 0)
        corps = self.rfile.read(longueur) if longueur else b""
        type_contenu = self.headers.get("Content-Type") or ""
        if type_contenu.startswith("multipart/"):
            operation = multipart_operations(corps, type_contenu)
        else:
            operation = json.loads(corps or b"{}")
        self._noter(corps, operation)
        sc = self.server.scenario
        if self.headers.get("Authorization") != AUTH:
            return self._json(401, {"error": "invalid_token", "error_description": "Authorization expired"})
        query = operation.get("query", "")
        variables = operation.get("variables") or {}
        if "mutation" in query:
            sc["mutation_vue"] = True
        if sc.get("limite", 0) > 0 and "mutation" in query:
            sc["limite"] -= 1
            return self._json(429, {"errors": [{"message": "Too many jobs", "extensions": {
                "type": "JobLimitExceeded", "code": "job_limit_exceeded"}}]})
        if sc.get("erreur") and "mutation" in query:
            statut, message = sc["erreur"]
            return self._json(statut, {"errors": [{"message": message}], "data": None})
        if "payg_total_usd" in query:
            sc["solde"] = sc.get("solde", 5.0)
            if sc.get("mutation_vue") and sc.get("debits"):
                sc["solde"] = round(sc["solde"] - sc["debits"].pop(0), 4)
            return self._json(200, {"data": {"org": {"name": "studio", "payg_enabled": sc.get("payg", True),
                                                     "payg_total_usd": str(sc["solde"]),
                                                     "motion_download_secs_per_month_remaining": None,
                                                     "characters_allowed_remaining": None}}})
        if "payg_prices" in query:
            return self._json(200, {"data": {"payg_prices": [
                {"model_key": "text-to-motion-3.0", "billing_unit": "second", "unit_price": "0.10"}]}})
        if "payg_ledger" in query:
            return self._json(200, {"data": {"payg_ledger": [
                {"created": "2026-11-23T10:00:00Z", "type": "debit", "total_usd": "-0.40", "balance_after": "4.60",
                 "model": "text-to-motion-3.0", "quantity": 4, "billing_unit": "second", "job_id": "j1"}]}})
        if "characters {" in query:
            return self._json(200, {"data": {"characters": [{"id": "cPerso00001", "name": "Garde",
                                                             "created": "2026-11-23"}]}})
        if "locomotion_styles" in query:
            return self._json(200, {"data": {"locomotion_styles": ["neutral_male_a", "aeroplane"]}})
        if "create_text_to_motion_job" in query:
            return self._json(200, {"data": {"create_text_to_motion_job": {"job": {"id": "job1", "status": "RESERVED"}}}})
        if "create_text_to_motion(" in query:
            return self._json(200, {"data": {"create_text_to_motion": {"motion": {"id": "mSync0001", "name": "x"}}}})
        if "create_video_to_motion" in query:
            return self._json(200, {"data": {"create_video_to_motion": {"job": {"id": "job2", "status": "RESERVED"}}}})
        if "job(job_id" in query:
            etats = sc.setdefault("etats", ["RESERVED", "READY", "FINISHED"])
            statut = etats.pop(0) if len(etats) > 1 else etats[0]
            resultat = {"result": {"id": "mJob00001"}} if statut == "FINISHED" else (
                {"error": "GPU out of memory"} if statut == "FAILED" else None)
            return self._json(200, {"data": {"job": {"id": variables.get("job_id"), "status": statut,
                                                     "method": "TextToMotion", "model": "text-to-motion-3.0",
                                                     "result": resultat, "est_processing_time": 30}}})
        if "jobs(" in query:
            return self._json(200, {"data": {"jobs": [{"id": "job1", "status": "FINISHED", "method": "TextToMotion",
                                                       "model": "text-to-motion-3.0", "created_at": "2026-11-23"}]}})
        if "create_locomotion" in query:
            return self._json(200, {"data": {"create_locomotion": {"motion": {"id": "mLoco0001", "name": "loco"}}}})
        if "create_looped_motion" in query:
            return self._json(200, {"data": {"create_looped_motion": {"motion": {"id": "mBoucle01", "name": "loop"}}}})
        if "stitch(" in query:
            return self._json(200, {"data": {"stitch": {"motion": {"id": "mStitch01", "name": "s"},
                                                        "resolved_steps": [{"motion_id": "a"}, {"motion_id": "b"}]}}})
        if "create_character" in query:
            return self._json(200, {"data": {"create_character": {"character": {"id": "cNouveau01", "name": variables.get("name")},
                                                                  "auto_rig_confidence": sc.get("confiance", 0.92),
                                                                  "message": None}}})
        if "motions_paged" in query:
            return self._json(200, {"data": {"motions_paged": {"items": [
                {"id": "mJob00001", "name": "garde salue", "created": "2026-11-23", "tags": {"Method": "TextToMotion"}}],
                "next_cursor": None}}})
        if "__typename" in query:
            return self._json(200, {"data": {"__typename": "Query"}})
        self._json(400, {"errors": [{"message": "Cannot query field"}]})


class FauxProxyBloquant(BaseHTTPRequestHandler):
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
        cls.serveur = demarrer(FauxUthana)
        cls.serveur.base = f"http://127.0.0.1:{cls.serveur.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.serveur.shutdown()
        cls.serveur.server_close()

    def setUp(self):
        self.serveur.scenario = {}
        self.serveur.requetes = []
        self.dossier = tempfile.mkdtemp()
        self.sorties = []

    def lancer(self, *args, cle=CLE, env_extra=None):
        env = {k: v for k, v in os.environ.items()
               if k.upper() not in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "UTHANA_API_KEY")}
        env.update({"NO_PROXY": "127.0.0.1,localhost", "UTHANA_API_BASE": self.serveur.base, "UTHANA_PAUSE": "0"})
        if cle:
            env["UTHANA_API_KEY"] = cle
        env.update(env_extra or {})
        res = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True,
                             env=env, timeout=60, cwd=self.dossier)
        self.sorties.append(res.stdout + res.stderr)
        return res

    def tearDown(self):
        for racine, _, fichiers in os.walk(self.dossier):
            for nom in fichiers:
                if nom.endswith(".json"):
                    with open(os.path.join(racine, nom), encoding="utf-8") as f:
                        self.sorties.append(f.read())
        jeton = base64.b64encode(f"{CLE}:".encode()).decode()
        for texte in self.sorties:
            self.assertNotIn(CLE, texte, "la clé apparaît dans une sortie ou un fichier")
            self.assertNotIn(jeton, texte, "la clé encodée apparaît dans une sortie ou un fichier")

    def chemin(self, nom):
        return os.path.join(self.dossier, nom)

    def fiche(self, nom):
        with open(self.chemin(nom), encoding="utf-8") as f:
            return json.load(f)

    def mutations(self):
        return [r for r in self.serveur.requetes if r["operation"] and "mutation" in r["operation"].get("query", "")]

    def ok(self, res):
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        return res


class TestTexte(BaseTest):
    def test_texte_3_0_tache_suivie_puis_telechargee(self):
        self.serveur.scenario = {"debits": [0.4]}
        res = self.ok(self.lancer("texte", "a guard salutes", "--sortie", "anims/garde_salut.glb",
                                  "--personnage", "manny", "--duree", "4"))
        mutation = self.mutations()[0]
        self.assertEqual(mutation["auth"], AUTH)
        self.assertIn("create_text_to_motion_job", mutation["operation"]["query"])
        self.assertEqual(mutation["operation"]["variables"],
                         {"prompt": "a guard salutes", "model": "text-to-motion-3.0",
                          "character_id": "c43tbGks3crJ", "length": 4.0})
        self.assertIn("≈ 0.40 $", res.stderr)
        telechargement = [r for r in self.serveur.requetes if r["chemin"].startswith("/motion/file/")][0]
        self.assertIn("/c43tbGks3crJ/mJob00001/glb/", telechargement["chemin"])
        self.assertIn("fps=30", telechargement["chemin"])
        fiche = self.fiche("anims/garde_salut.uthana.json")
        self.assertEqual((fiche["job_id"], fiche["motion_id"]), ("job1", "mJob00001"))
        self.assertEqual(fiche["debit_usd"], 0.4)
        self.assertEqual(fiche["controle"]["animations"][0]["duree_s"], 2.0)
        self.assertEqual(fiche["controle"]["images_par_seconde"], 30)
        self.assertEqual(fiche["controle"]["os"], 3)

    def test_duree_hors_bornes(self):
        res = self.lancer("texte", "x", "--modele", "3.0-mini", "--duree", "4", "--sortie", "a.glb")
        self.assertEqual(res.returncode, 2)
        self.assertEqual(self.serveur.requetes, [])

    def test_modele_2_0_synchrone(self):
        self.ok(self.lancer("texte", "confident stride", "--modele", "2.0", "--graine", "7", "--sortie", "a.glb"))
        variables = self.mutations()[0]["operation"]["variables"]
        self.assertEqual(variables["model"], "text-to-motion-bucmd")
        self.assertEqual(variables["seed"], 7)
        self.assertEqual(self.fiche("a.uthana.json")["motion_id"], "mSync0001")

    def test_options_de_telechargement(self):
        self.ok(self.lancer("texte", "run", "--sortie", "a.fbx", "--fps", "60", "--sans-maillage",
                            "--sur-place", "--vitesse-lecture", "0.5"))
        chemin = [r for r in self.serveur.requetes if r["chemin"].startswith("/motion/file/")][0]["chemin"]
        self.assertIn("/fbx/", chemin)
        for option in ("fps=60", "no_mesh=true", "in_place=true", "speed_multiplier=0.5"):
            self.assertIn(option, chemin)

    def test_fps_invalide_et_extension(self):
        self.assertEqual(self.lancer("texte", "x", "--sortie", "a.glb", "--fps", "25").returncode, 2)
        self.assertEqual(self.lancer("texte", "x", "--sortie", "a.obj").returncode, 2)

    def test_tache_echouee(self):
        self.serveur.scenario = {"etats": ["READY", "FAILED"]}
        res = self.lancer("texte", "x", "--sortie", "a.glb")
        self.assertEqual(res.returncode, 6)
        self.assertIn("GPU out of memory", res.stderr)

    def test_delai_depasse(self):
        self.serveur.scenario = {"etats": ["READY"]}
        res = self.lancer("texte", "x", "--sortie", "a.glb", "--attente", "0")
        self.assertEqual(res.returncode, 7)
        self.assertIn("statut job1", res.stderr)

    def test_sans_attendre_puis_statut(self):
        res = self.ok(self.lancer("texte", "x", "--sortie", "a.glb", "--sans-attendre"))
        self.assertIn("statut job1", res.stdout)
        self.serveur.scenario = {"etats": ["FINISHED"]}
        self.ok(self.lancer("statut", "job1", "--sortie", "a.glb"))
        self.assertEqual(self.fiche("a.uthana.json")["motion_id"], "mJob00001")

    def test_a_blanc(self):
        res = self.ok(self.lancer("texte", "x", "--sortie", "a.glb", "--a-blanc", cle=None))
        self.assertIn("Aucune requête envoyée", res.stdout)
        self.assertEqual(self.serveur.requetes, [])


class TestAutres(BaseTest):
    def setUp(self):
        super().setUp()
        with open(self.chemin("perso.glb"), "wb") as f:
            f.write(glb_anime())
        with open(self.chemin("prise.mp4"), "wb") as f:
            f.write(b"\x00" * 100)

    def test_video(self):
        self.ok(self.lancer("video", "prise.mp4", "--mains", "--sortie", "v.glb"))
        mutation = self.mutations()[0]
        self.assertTrue(mutation["type"].startswith("multipart/form-data"))
        self.assertEqual(mutation["operation"]["variables"]["model"], "video-to-motion-3.0")
        self.assertTrue(mutation["operation"]["variables"]["high_quality_hands"])
        self.assertIsNone(mutation["operation"]["variables"]["file"])
        self.assertIn(b'filename="prise.mp4"', mutation["corps"])
        self.assertEqual(self.fiche("v.uthana.json")["entree"]["fichier"], "prise.mp4")

    def test_locomotion(self):
        self.ok(self.lancer("locomotion", "--personnage", "cPerso00001", "--angle", "90", "--foulees", "2",
                            "--sur-place", "--sortie", "marche_droite.glb"))
        variables = self.mutations()[0]["operation"]["variables"]
        self.assertEqual(variables, {"character_id": "cPerso00001", "strides": 2, "move_speed": 1.2,
                                     "style_id": "neutral_male_a", "travel_angle": 90.0})
        self.assertEqual(self.lancer("locomotion", "--foulees", "6", "--sortie", "b.glb").returncode, 2)

    def test_boucler_et_enchainer(self):
        self.ok(self.lancer("boucler", "mSource01", "--mode", "open", "--sortie", "boucle.glb"))
        self.assertEqual(self.mutations()[-1]["operation"]["variables"]["loop_mode"], "open")
        self.ok(self.lancer("enchainer", "mA", "mB", "--transition", "1.5", "--sortie", "suite.glb"))
        entree = self.mutations()[-1]["operation"]["variables"]["input"]
        self.assertEqual(entree["steps"], [{"motion_id": "mA", "transition_duration_seconds": 1.5},
                                           {"motion_id": "mB"}])
        self.assertEqual(self.lancer("enchainer", "a", "b", "--transition", "5", "--sortie", "c.glb").returncode, 2)

    def test_importer_avec_rig_et_sortie(self):
        res = self.ok(self.lancer("importer", "perso.glb", "--nom", "Garde", "--squelette", "ue5",
                                  "--pieds-au-sol", "--sortie", "garde_rig.glb"))
        variables = self.mutations()[0]["operation"]["variables"]
        self.assertEqual(variables["rerig_target"], "ue5")
        self.assertTrue(variables["auto_rig_feet_on_floor"])
        self.assertIn("cNouveau01", res.stdout)
        self.assertIn("0.92", res.stdout)
        self.assertTrue(os.path.exists(self.chemin("garde_rig.glb")))
        self.assertEqual(self.fiche("garde_rig.uthana.json")["character_id"], "cNouveau01")

    def test_importer_confiance_faible(self):
        self.serveur.scenario = {"confiance": 0.2}
        self.assertIn("faible", self.ok(self.lancer("importer", "perso.glb")).stdout)

    def test_importer_refuse_un_obj(self):
        open(self.chemin("perso.obj"), "w").close()
        self.assertEqual(self.lancer("importer", "perso.obj").returncode, 2)

    def test_telecharger_et_personnage(self):
        self.ok(self.lancer("telecharger", "mX", "--personnage", "ava", "--sortie", "a.glb"))
        self.assertIn("/cmEE2fT4aSaC/mX/", self.serveur.requetes[-1]["chemin"])
        self.ok(self.lancer("telecharger-personnage", "cPerso00001", "--sortie", "p.fbx"))
        self.assertEqual(self.serveur.requetes[-1]["chemin"], "/motion/bundle/cPerso00001/character.fbx")

    def test_inspecter(self):
        res = self.ok(self.lancer("inspecter", "perso.glb"))
        self.assertIn("2.00 s", res.stdout)


class TestCompteEtErreurs(BaseTest):
    def test_verifier(self):
        res = self.ok(self.lancer("verifier"))
        self.assertIn("solde : 5.0 $", res.stdout)

    def test_verifier_sans_paiement_a_l_usage(self):
        self.serveur.scenario = {"payg": False}
        self.assertIn("non activé", self.ok(self.lancer("verifier")).stdout)

    def test_listes(self):
        self.assertIn("text-to-motion-3.0", self.ok(self.lancer("prix")).stdout)
        self.assertIn("-0.40", self.ok(self.lancer("depenses")).stdout)
        res = self.ok(self.lancer("personnages"))
        self.assertIn("cPerso00001", res.stdout)
        self.assertIn("tar (cXi2eAP19XwQ)", res.stdout)
        self.assertIn("aeroplane", self.ok(self.lancer("styles")).stdout)
        self.assertIn("job1", self.ok(self.lancer("taches")).stdout)
        self.assertIn("garde salue", self.ok(self.lancer("animations")).stdout)
        self.assertIn("__typename", self.ok(self.lancer("brut", "{ __typename }")).stdout)

    def test_cle_absente_et_refusee(self):
        self.assertEqual(self.lancer("verifier", cle=None).returncode, 3)
        self.assertEqual(self.lancer("texte", "x", "--sortie", "a.glb", cle="mauvaise").returncode, 3)

    def test_limite_puis_succes(self):
        self.serveur.scenario = {"limite": 2}
        self.ok(self.lancer("locomotion", "--sortie", "a.glb"))
        self.assertEqual(len(self.mutations()), 3)

    def test_limite_persistante(self):
        self.serveur.scenario = {"limite": 100}
        res = self.lancer("locomotion", "--sortie", "a.glb")
        self.assertEqual(res.returncode, 9)
        self.assertIn("Rien n'a été accepté", res.stderr)

    def test_solde_insuffisant(self):
        self.serveur.scenario = {"erreur": (402, "Insufficient balance")}
        self.assertEqual(self.lancer("locomotion", "--sortie", "a.glb").returncode, 4)

    def test_erreur_serveur_incertaine(self):
        self.serveur.scenario = {"erreur": (500, "boom")}
        res = self.lancer("locomotion", "--sortie", "a.glb")
        self.assertEqual(res.returncode, 7)
        self.assertEqual(len(self.mutations()), 1)

    def test_telechargement_refuse_donne_la_reprise(self):
        self.serveur.scenario = {"telechargement_refuse": True}
        res = self.lancer("locomotion", "--sortie", "a.glb")
        self.assertEqual(res.returncode, 4)
        self.assertIn("uthana.py telecharger mLoco0001", res.stderr)
        self.assertEqual(self.fiche("a.uthana.json")["etat"], "a_telecharger")


class TestProxy(BaseTest):
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

    def test_api_bloquee(self):
        res = self.lancer("locomotion", "--sortie", "a.glb", env_extra={
            "HTTPS_PROXY": self.url_proxy, "https_proxy": self.url_proxy,
            "UTHANA_API_BASE": "https://uthana.invalid"})
        self.assertEqual(res.returncode, 5)
        self.assertIn("uthana.invalid est bloqué", res.stderr)


class TestUnitaire(unittest.TestCase):
    def test_personnage(self):
        self.assertEqual(uthana.personnage(None), "cXi2eAP19XwQ")
        self.assertEqual(uthana.personnage("Manny"), "c43tbGks3crJ")
        self.assertEqual(uthana.personnage("cAutre"), "cAutre")

    def test_motion_id_de_tache(self):
        self.assertEqual(uthana.motion_id_de_tache({"result": {"result": {"id": "m1"}}}), "m1")
        self.assertEqual(uthana.motion_id_de_tache({"result": {"result": {"ids": ["m2", "m3"]}}}), "m2")

    def test_masquer_la_cle_encodee(self):
        os.environ["UTHANA_API_KEY"] = CLE
        try:
            jeton = base64.b64encode(f"{CLE}:".encode()).decode()
            self.assertEqual(uthana.masquer(f"{CLE} {jeton}"), "*** ***")
        finally:
            del os.environ["UTHANA_API_KEY"]


class TestHook(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ICI, "..", "hooks", "hooks.json"), encoding="utf-8") as f:
            self.commande = json.load(f)["hooks"]["SessionStart"][0]["hooks"][0]["command"]

    def lancer(self, cle):
        env = {k: v for k, v in os.environ.items() if k != "UTHANA_API_KEY"}
        if cle:
            env["UTHANA_API_KEY"] = cle
        return subprocess.run(["sh", "-c", self.commande], capture_output=True, text=True, env=env, timeout=10)

    def test_silencieux_si_cle_definie(self):
        self.assertEqual(self.lancer(CLE).stdout, "")

    def test_une_ligne_si_cle_absente(self):
        res = self.lancer(None)
        self.assertEqual(len(res.stdout.strip().splitlines()), 1)
        self.assertIn("UTHANA_API_KEY", res.stdout)


if __name__ == "__main__":
    unittest.main()
