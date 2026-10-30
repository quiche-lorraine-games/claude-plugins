"""Tests de scripts/elevenlabs.py contre un faux serveur HTTP local qui imite l'API ElevenLabs.

Lancer depuis la racine du repo :
    python3 -m unittest discover -s plugins/elevenlabs/tests -v
"""

import base64
import importlib.util
import io
import json
import os
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.parse
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ICI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(ICI, "..", "skills", "audio", "scripts", "elevenlabs.py")
CLE = "sk_cle-de-test-ultra-secrete-0123456789"
VOIX_GEORGE = "JBFqnCBsd6RMkjVDRZzb"
VOIX_ALICE = "Xb7hH8MSUJpSbSDYk0k2"

_spec = importlib.util.spec_from_file_location("elevenlabs", SCRIPT)
eleven = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eleven)


def mp3_factice(trames=10):
    """Trames MPEG-1 Layer III à 128 kb/s, 44,1 kHz, stéréo joint : 417 octets et 1 152 échantillons l'une."""
    trame = b"\xff\xfb\x90\x64" + b"\x00" * 413
    return b"ID3\x03\x00\x00\x00\x00\x00\x00" + trame * trames


def pcm_factice(secondes=0.5, frequence=44100, amplitude=16384):
    n = int(secondes * frequence)
    return struct.pack(f"<{n}h", *([amplitude, -amplitude] * (n // 2) + [0] * (n % 2)))


def zip_pistes():
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, "w") as z:
        z.writestr("stems/vocals.mp3", mp3_factice(5))
        z.writestr("stems/drums.mp3", mp3_factice(5))
        z.writestr("__MACOSX/.cache", b"")
    return tampon.getvalue()


def alignement(texte):
    return {"characters": list(texte),
            "character_start_times_seconds": [i * 0.1 for i in range(len(texte))],
            "character_end_times_seconds": [i * 0.1 + 0.1 for i in range(len(texte))]}


class FauxEleven(BaseHTTPRequestHandler):
    """Rejoue le scénario de la classe de test : self.server.scenario."""

    def log_message(self, *args):
        pass

    def _envoyer(self, statut, corps, type_contenu, entetes=None):
        self.send_response(statut)
        self.send_header("Content-Type", type_contenu)
        self.send_header("Content-Length", str(len(corps)))
        self.send_header("request-id", "req-test")
        for nom, valeur in (entetes or {}).items():
            self.send_header(nom, valeur)
        self.end_headers()
        try:
            self.wfile.write(corps)
        except (BrokenPipeError, ConnectionResetError):
            pass  # le client a abandonné (test du délai dépassé)

    def _json(self, statut, charge, entetes=None):
        self._envoyer(statut, json.dumps(charge).encode("utf-8"), "application/json", entetes)

    def _detail(self, statut, etat, message):
        self._json(statut, {"detail": {"type": "x", "code": etat, "status": etat, "message": message,
                                       "request_id": "req-erreur"}})

    def _lire(self):
        longueur = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(longueur) if longueur else b""

    def _noter(self, corps=b""):
        chemin = urllib.parse.urlsplit(self.path)
        self.server.requetes.append({
            "methode": self.command, "chemin": chemin.path,
            "requete": urllib.parse.parse_qs(chemin.query),
            "cle": self.headers.get("xi-api-key"), "type": self.headers.get("Content-Type"), "corps": corps,
        })

    def _scenario_erreur(self):
        sc = self.server.scenario
        if sc.get("cle_refusee"):
            self._detail(401, "invalid_api_key", f"Invalid API key ({self.headers.get('xi-api-key')})")
            return True
        if sc.get("permission"):
            self._detail(401, "missing_permissions",
                         f"The API key you used is missing the permission {sc['permission']} to execute this operation.")
            return True
        if sc.get("limite", 0) > 0:
            sc["limite"] -= 1
            self._detail(429, "too_many_concurrent_requests", "Too many concurrent requests")
            return True
        erreur = sc.get("erreur")
        if erreur:
            statut, etat, message = erreur
            if statut == 422 and etat == "validation":
                self._json(422, {"detail": [{"type": "missing", "loc": ["body", "text"], "msg": "Field required"}]})
            else:
                self._detail(statut, etat, message)
            return True
        if sc.get("lent"):
            time.sleep(sc["lent"])
        return False

    def do_GET(self):
        self._noter()
        sc = self.server.scenario
        chemin = urllib.parse.urlsplit(self.path).path
        if chemin == "/":
            return self._json(404, {"detail": "Not Found"})
        if sc.get("sans_permission_lecture") and chemin in ("/v1/models", "/v1/history", "/v1/audio-effects/catalog"):
            return self._detail(401, "missing_permissions",
                                "The API key you used is missing the permission models_read to execute this operation.")
        if self._scenario_erreur():
            return
        if chemin == "/v1/user/subscription":
            return self._json(200, {"tier": sc.get("offre", "creator"), "status": "active", "character_count": 1200,
                                    "character_limit": 100000, "next_character_count_reset_unix": 1793404800})
        if chemin == "/v1/audio-effects/catalog":
            return self._json(200, {"filters": [], "environments": []})
        if chemin == "/v2/voices":
            return self._json(200, {"voices": [
                {"voice_id": VOIX_GEORGE, "name": "George - Warm Storyteller", "category": "premade",
                 "labels": {"gender": "male", "accent": "british"}},
                {"voice_id": VOIX_ALICE, "name": "Alice", "category": "premade", "labels": {"gender": "female"}},
            ], "has_more": False, "total_count": 2})
        if chemin.startswith("/v1/voices/"):
            return self._json(200, {"voice_id": chemin.rsplit("/", 1)[1], "name": "George", "category": "premade",
                                    "settings": {"stability": 0.5}})
        if chemin == "/v1/models":
            return self._json(200, [{"model_id": "eleven_multilingual_v2", "name": "Multilingual v2",
                                     "can_do_text_to_speech": True, "token_cost_factor": 1.0,
                                     "max_characters_request_subscribed_user": 10000, "languages": [{}, {}]}])
        if chemin == "/v1/history":
            return self._json(200, {"history": [{"history_item_id": "hist1", "date_unix": 1793404800,
                                                 "voice_name": "George", "model_id": "eleven_multilingual_v2",
                                                 "character_count_change_from": 100,
                                                 "character_count_change_to": 118, "text": "Bonjour, voyageur."}]})
        if chemin == "/v1/history/hist1":
            return self._json(200, {"history_item_id": "hist1", "request_id": "req-ancienne",
                                    "voice_id": VOIX_GEORGE, "voice_name": "George",
                                    "model_id": "eleven_multilingual_v2", "text": "Bonjour, voyageur."})
        if chemin == "/v1/history/hist1/audio":
            return self._envoyer(200, mp3_factice(), "audio/mpeg")
        if chemin == "/v1/usage/character-stats":
            return self._json(200, {"time": [1793318400000, 1793404800000], "usage": {"All": [0, 118]}})
        if chemin == "/v1/voices/settings/default":
            return self._json(200, {"stability": 0.5})
        self._json(404, {"detail": "Not Found"})

    def do_POST(self):
        corps = self._lire()
        self._noter(corps)
        if self._scenario_erreur():
            return
        chemin = urllib.parse.urlsplit(self.path).path
        requete = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
        fmt = requete.get("output_format", ["mp3_44100_128"])[0]

        def audio():
            return pcm_factice() if fmt.startswith("pcm") else mp3_factice()

        type_audio = "audio/mpeg" if fmt.startswith("mp3") else "application/octet-stream"
        cout = {"character-cost": "18"}
        if chemin.endswith("/with-timestamps"):
            texte = json.loads(corps).get("text") or " ".join(i["text"] for i in json.loads(corps)["inputs"])
            return self._json(200, {"audio_base64": base64.b64encode(audio()).decode(),
                                    "alignment": alignement(texte), "normalized_alignment": alignement(texte)},
                              cout)
        if chemin.startswith("/v1/text-to-speech/") or chemin in ("/v1/text-to-dialogue", "/v1/sound-generation"):
            return self._envoyer(200, audio(), type_audio, {**cout, "history-item-id": "hist-nouveau"})
        if chemin == "/v1/music":
            return self._envoyer(200, audio(), type_audio, {"song-id": "chanson1"})
        if chemin == "/v1/music/plan":
            return self._json(200, {"positive_global_styles": ["orchestral"], "negative_global_styles": [],
                                    "sections": [{"section_name": "Intro", "duration_ms": 10000,
                                                  "positive_local_styles": ["calme"], "negative_local_styles": [],
                                                  "lines": []}]})
        if chemin in ("/v1/text-to-voice/design",) or chemin.endswith("/remix"):
            apercu = base64.b64encode(mp3_factice()).decode()
            return self._json(200, {"text": "Texte lu par la voix.", "previews": [
                {"audio_base_64": apercu, "generated_voice_id": "gen1", "media_type": "audio/mpeg",
                 "duration_secs": 0.26, "language": "fr"},
                {"audio_base_64": apercu, "generated_voice_id": "gen2", "media_type": "audio/mpeg",
                 "duration_secs": 0.26, "language": "fr"}]})
        if chemin == "/v1/text-to-voice":
            return self._json(200, {"voice_id": "nouvellevoix00000001", "name": json.loads(corps)["voice_name"]})
        if chemin == "/v1/voices/add":
            return self._json(200, {"voice_id": "voixclonee0000000001", "requires_verification": False})
        if chemin.startswith("/v1/voices/add/"):
            return self._json(200, {"voice_id": "voixpartagee00000001"})
        if chemin.startswith("/v1/voice-changer/") or chemin == "/v1/audio-isolation":
            return self._envoyer(200, audio(), type_audio)
        if chemin == "/v1/music/stem-separation":
            return self._envoyer(200, zip_pistes(), "application/zip")
        if chemin == "/v1/speech-to-text":
            return self._json(200, {"language_code": "fr", "language_probability": 0.99, "text": "Bonjour voyageur.",
                                    "words": [{"text": "Bonjour", "start": 0.0, "end": 0.4, "type": "word"}],
                                    "audio_duration_secs": 1.2,
                                    "additional_formats": [{"requested_format": "srt", "file_extension": "srt",
                                                            "content_type": "text/srt", "is_base64_encoded": False,
                                                            "content": "1\n00:00:00,000 --> 00:00:00,400\nBonjour\n"}]})
        if chemin == "/v1/forced-alignment":
            return self._json(200, {"characters": [], "loss": 0.1,
                                    "words": [{"text": "Bonjour", "start": 0.0, "end": 0.4, "loss": 0.1}]})
        self._json(404, {"detail": "Not Found"})


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
        cls.serveur = demarrer(FauxEleven)
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
               if k.upper() not in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "ELEVENLABS_API_KEY")}
        env["NO_PROXY"] = "127.0.0.1,localhost"
        env["ELEVENLABS_API_BASE"] = self.serveur.base
        env["ELEVENLABS_PAUSE_REESSAI"] = "0"
        if cle:
            env["ELEVENLABS_API_KEY"] = cle
        env.update(env_extra or {})
        res = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True,
                             env=env, timeout=60, cwd=self.dossier)
        self.sorties.append(res.stdout + res.stderr)
        return res

    def tearDown(self):
        for racine, _, fichiers in os.walk(self.dossier):
            for nom in fichiers:
                if nom.endswith((".json", ".srt")):
                    with open(os.path.join(racine, nom), encoding="utf-8") as f:
                        self.sorties.append(f.read())
        for texte in self.sorties:
            self.assertNotIn(CLE, texte, "la clé apparaît dans une sortie ou un fichier")

    def chemin(self, nom):
        return os.path.join(self.dossier, nom)

    def fiche(self, nom):
        with open(self.chemin(nom), encoding="utf-8") as f:
            return json.load(f)

    def derniere(self, methode="POST"):
        return [r for r in self.serveur.requetes if r["methode"] == methode][-1]

    def ok(self, res):
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        return res


class TestParole(BaseTest):
    def test_parole_mp3_et_fiche(self):
        res = self.ok(self.lancer("parole", VOIX_GEORGE, "Bonjour, voyageur.", "--sortie", "voix/pnj_01.mp3",
                                  "--stabilite", "0.4", "--langue", "fr"))
        req = self.derniere()
        self.assertEqual(req["chemin"], f"/v1/text-to-speech/{VOIX_GEORGE}")
        self.assertEqual(req["cle"], CLE)
        self.assertEqual(req["requete"]["output_format"], ["mp3_44100_128"])
        corps = json.loads(req["corps"])
        self.assertEqual(corps, {"text": "Bonjour, voyageur.", "model_id": "eleven_multilingual_v2",
                                 "language_code": "fr", "voice_settings": {"stability": 0.4}})
        self.assertIn("≈ 18 crédits", res.stderr)
        fiche = self.fiche("voix/pnj_01.elevenlabs.json")
        self.assertEqual(fiche["operation"], f"POST /v1/text-to-speech/{VOIX_GEORGE}")
        self.assertEqual(fiche["texte"], "Bonjour, voyageur.")
        self.assertEqual(fiche["credits"], 18)
        self.assertEqual(fiche["request_id"], "req-test")
        self.assertEqual(fiche["history_item_id"], "hist-nouveau")
        self.assertEqual(fiche["sorties"], ["pnj_01.mp3"])
        self.assertEqual(fiche["controle"]["format"], "mp3")
        self.assertAlmostEqual(fiche["controle"]["duree_s"], 0.261, places=3)
        self.assertEqual(fiche["controle"]["debit_kbps"], 128)

    def test_wav_demande_du_pcm_et_l_enveloppe(self):
        self.ok(self.lancer("parole", VOIX_GEORGE, "Salut.", "--sortie", "salut.wav"))
        self.assertEqual(self.derniere()["requete"]["output_format"], ["pcm_44100"])
        with open(self.chemin("salut.wav"), "rb") as f:
            self.assertEqual(f.read(4), b"RIFF")
        controle = self.fiche("salut.elevenlabs.json")["controle"]
        self.assertEqual((controle["format"], controle["frequence_hz"], controle["canaux"]), ("wav", 44100, 1))
        self.assertAlmostEqual(controle["duree_s"], 0.5, places=2)
        self.assertEqual(controle["crete_dbfs"], -6.0)

    def test_voix_par_nom(self):
        self.ok(self.lancer("parole", "george", "Salut.", "--sortie", "a.mp3"))
        self.assertEqual(self.derniere()["chemin"], f"/v1/text-to-speech/{VOIX_GEORGE}")
        self.assertEqual(self.fiche("a.elevenlabs.json")["voix"]["nom"], "George - Warm Storyteller")

    def test_voix_inconnue(self):
        res = self.lancer("parole", "Personne", "Salut.", "--sortie", "a.mp3")
        self.assertEqual(res.returncode, 2)
        self.assertIn("Aucune voix du compte", res.stderr)

    def test_horodatage_ecrit_l_alignement(self):
        self.ok(self.lancer("parole", VOIX_GEORGE, "Bonjour voyageur", "--sortie", "b.mp3", "--horodatage"))
        self.assertTrue(self.derniere()["chemin"].endswith("/with-timestamps"))
        with open(self.chemin("b.alignement.json"), encoding="utf-8") as f:
            mots = json.load(f)["mots"]
        self.assertEqual([m["mot"] for m in mots], ["Bonjour", "voyageur"])
        self.assertAlmostEqual(mots[1]["debut"], 0.8)
        fiche = self.fiche("b.elevenlabs.json")
        self.assertEqual(fiche["sorties"], ["b.mp3", "b.alignement.json"])
        self.assertEqual(fiche["credits"], 18)

    def test_texte_trop_long(self):
        res = self.lancer("parole", VOIX_GEORGE, "a" * 5001, "--modele", "eleven_v3", "--sortie", "a.mp3")
        self.assertEqual(res.returncode, 2)
        self.assertEqual(self.serveur.requetes, [])

    def test_format_incoherent_avec_l_extension(self):
        res = self.lancer("parole", VOIX_GEORGE, "x", "--sortie", "a.wav", "--format", "mp3_44100_128")
        self.assertEqual(res.returncode, 2)
        res = self.lancer("parole", VOIX_GEORGE, "x", "--sortie", "a.ogg")
        self.assertEqual(res.returncode, 2)

    def test_a_blanc_n_envoie_rien(self):
        res = self.ok(self.lancer("parole", "Alice", "Salut.", "--sortie", "a.mp3", "--a-blanc", cle=None))
        self.assertIn("Aucune requête envoyée", res.stdout)
        self.assertEqual(self.serveur.requetes, [])
        self.assertFalse(os.path.exists(self.chemin("a.mp3")))

    def test_refuse_d_ecraser(self):
        open(self.chemin("a.mp3"), "wb").close()
        res = self.lancer("parole", VOIX_GEORGE, "x", "--sortie", "a.mp3")
        self.assertEqual(res.returncode, 2)
        self.ok(self.lancer("parole", VOIX_GEORGE, "x", "--sortie", "a.mp3", "--ecraser"))

    def test_param_supplementaire_et_conflit(self):
        self.ok(self.lancer("parole", VOIX_GEORGE, "x", "--sortie", "a.mp3", "--param", "seed=42"))
        self.assertEqual(json.loads(self.derniere()["corps"])["seed"], 42)
        res = self.lancer("parole", VOIX_GEORGE, "x", "--sortie", "b.mp3", "--param", "text=y")
        self.assertEqual(res.returncode, 2)

    def test_flash_coute_moitie(self):
        res = self.ok(self.lancer("parole", VOIX_GEORGE, "x" * 10, "--modele", "eleven_flash_v2_5",
                                  "--sortie", "a.mp3", "--a-blanc"))
        self.assertIn("≈ 5 crédits", res.stdout)


class TestDialogueEtSons(BaseTest):
    def test_dialogue_repliques_et_script(self):
        script = self.chemin("scene.json")
        with open(script, "w", encoding="utf-8") as f:
            json.dump([{"voix": "Alice", "texte": "Qui va là ?"}], f)
        self.ok(self.lancer("dialogue", "--replique", f"{VOIX_GEORGE}=[whispers] Chut.", "--script", "scene.json",
                            "--sortie", "scene.mp3"))
        corps = json.loads(self.derniere()["corps"])
        self.assertEqual(corps["inputs"], [{"text": "[whispers] Chut.", "voice_id": VOIX_GEORGE},
                                           {"text": "Qui va là ?", "voice_id": VOIX_ALICE}])
        self.assertEqual(corps["model_id"], "eleven_v3")
        self.assertEqual(len(self.fiche("scene.elevenlabs.json")["voix"]), 2)

    def test_dialogue_trop_de_voix(self):
        repliques = []
        for i in range(11):
            repliques += ["--replique", f"{'A' * 19}{i % 10 if i < 10 else 'B'}=salut"]
        res = self.lancer("dialogue", *repliques, "--sortie", "a.mp3")
        self.assertEqual(res.returncode, 2)

    def test_bruitage(self):
        self.ok(self.lancer("bruitage", "wooden door creak", "--duree", "2", "--boucle", "--sortie", "porte.wav"))
        req = self.derniere()
        self.assertEqual(req["chemin"], "/v1/sound-generation")
        self.assertEqual(json.loads(req["corps"]), {"text": "wooden door creak", "model_id": "eleven_text_to_sound_v2",
                                                    "duration_seconds": 2.0, "loop": True})
        self.assertEqual(req["requete"]["output_format"], ["pcm_44100"])
        res = self.lancer("bruitage", "x", "--duree", "31", "--sortie", "b.mp3")
        self.assertEqual(res.returncode, 2)

    def test_bruitage_signale_une_duree_differente(self):
        res = self.ok(self.lancer("bruitage", "x", "--duree", "2", "--sortie", "b.mp3"))
        self.assertIn("Durée obtenue 0.26 s pour 2 s", res.stdout)

    def test_musique_prompt_puis_plan(self):
        self.ok(self.lancer("musique", "calm medieval tavern loop", "--duree", "30", "--instrumental",
                            "--sortie", "taverne.wav"))
        req = self.derniere()
        self.assertEqual(req["requete"]["output_format"], ["pcm_44100"])
        self.assertEqual(json.loads(req["corps"])["music_length_ms"], 30000)
        self.assertEqual(self.fiche("taverne.elevenlabs.json")["song_id"], "chanson1")

        self.ok(self.lancer("plan-musique", "epic boss fight", "--sortie", "plan.json"))
        self.ok(self.lancer("musique", "--plan", "plan.json", "--sortie", "boss.mp3"))
        corps = json.loads(self.derniere()["corps"])
        self.assertEqual(corps["composition_plan"]["sections"][0]["section_name"], "Intro")
        self.assertNotIn("prompt", corps)

    def test_musique_refuse_prompt_et_plan_et_wav_natif(self):
        self.assertEqual(self.lancer("musique", "x", "--plan", "p.json", "--sortie", "a.mp3").returncode, 2)
        res = self.lancer("musique", "x", "--format", "wav_44100", "--sortie", "a.wav")
        self.assertEqual(res.returncode, 2)
        self.assertIn("pcm_44100", res.stderr)
        self.assertEqual(self.serveur.requetes, [])


class TestVoix(BaseTest):
    def test_lister_et_info(self):
        res = self.ok(self.lancer("voix", "--recherche", "george"))
        self.assertIn(VOIX_GEORGE, res.stdout)
        res = self.ok(self.lancer("voix-info", "Alice"))
        self.assertIn('"voice_id": "' + VOIX_ALICE, res.stdout)

    def test_concevoir_puis_creer(self):
        res = self.ok(self.lancer("concevoir-voix", "Vieux forgeron bourru, voix grave et rocailleuse",
                                  "--sortie", "apercus/forgeron.mp3"))
        self.assertTrue(os.path.exists(self.chemin("apercus/forgeron_1.mp3")))
        self.assertTrue(os.path.exists(self.chemin("apercus/forgeron_2.mp3")))
        corps = json.loads(self.derniere()["corps"])
        self.assertTrue(corps["auto_generate_text"])
        fiche = self.fiche("apercus/forgeron.elevenlabs.json")
        self.assertEqual([a["generated_voice_id"] for a in fiche["apercus"]], ["gen1", "gen2"])
        self.assertEqual(fiche["apercus"][0]["fichier"], "forgeron_1.mp3")
        self.assertIn("creer-voix", res.stdout)

        res = self.ok(self.lancer("creer-voix", "gen2", "--nom", "Forgeron", "--description",
                                  "Vieux forgeron bourru, voix grave", "--etiquette", "language=fr"))
        self.assertIn("nouvellevoix00000001", res.stdout)
        self.assertEqual(json.loads(self.derniere()["corps"])["labels"], {"language": "fr"})

    def test_description_trop_courte(self):
        self.assertEqual(self.lancer("concevoir-voix", "court", "--sortie", "a.mp3").returncode, 2)

    def test_cloner_exige_le_consentement(self):
        with open(self.chemin("echantillon.mp3"), "wb") as f:
            f.write(mp3_factice())
        res = self.lancer("cloner", "echantillon.mp3", "--nom", "Narratrice")
        self.assertEqual(res.returncode, 2)
        self.assertIn("--consentement", res.stderr)
        self.assertEqual(self.serveur.requetes, [])
        self.ok(self.lancer("cloner", "echantillon.mp3", "--nom", "Narratrice", "--consentement"))
        req = self.derniere()
        self.assertTrue(req["type"].startswith("multipart/form-data"))
        self.assertIn(b'name="files"; filename="echantillon.mp3"', req["corps"])

    def test_ajouter_voix_de_la_bibliotheque(self):
        self.ok(self.lancer("ajouter-voix", "proprio", "voixpub", "--nom", "Garde"))
        self.assertEqual(self.derniere()["chemin"], "/v1/voices/add/proprio/voixpub")


class TestTraitement(BaseTest):
    def setUp(self):
        super().setUp()
        with open(self.chemin("prise.mp3"), "wb") as f:
            f.write(mp3_factice())

    def test_changer_voix(self):
        self.ok(self.lancer("changer-voix", "prise.mp3", VOIX_ALICE, "--debruiter", "--sortie", "alice.mp3"))
        req = self.derniere()
        self.assertEqual(req["chemin"], f"/v1/voice-changer/{VOIX_ALICE}")
        self.assertIn(b'name="remove_background_noise"\r\n\r\ntrue', req["corps"])
        self.assertIn(b"eleven_multilingual_sts_v2", req["corps"])
        entree = self.fiche("alice.elevenlabs.json")["entree"]
        self.assertEqual(entree["fichier"], "prise.mp3")
        self.assertEqual(len(entree["sha256"]), 64)

    def test_isoler(self):
        self.ok(self.lancer("isoler", "prise.mp3", "--sortie", "propre.mp3"))
        self.assertEqual(self.lancer("isoler", "prise.mp3", "--sortie", "propre.wav").returncode, 2)

    def test_separer_pistes(self):
        self.ok(self.lancer("separer-pistes", "prise.mp3", "--sortie", "pistes"))
        self.assertEqual(sorted(os.listdir(self.chemin("pistes"))), ["drums.mp3", "vocals.mp3"])
        fiche = self.fiche("pistes.elevenlabs.json")
        self.assertEqual(sorted(p["fichier"] for p in fiche["pistes"]), ["pistes/drums.mp3", "pistes/vocals.mp3"])

    def test_transcrire_avec_srt(self):
        self.ok(self.lancer("transcrire", "prise.mp3", "--srt", "--langue", "fr", "--sortie", "prise.json"))
        req = self.derniere()
        self.assertIn(b'"format": "srt"', req["corps"])
        with open(self.chemin("prise.srt"), encoding="utf-8") as f:
            self.assertIn("Bonjour", f.read())
        self.assertEqual(self.fiche("prise.elevenlabs.json")["sorties"], ["prise.json", "prise.srt"])

    def test_aligner(self):
        res = self.ok(self.lancer("aligner", "prise.mp3", "Bonjour", "--sortie", "align.json"))
        self.assertIn("1 mots alignés", res.stdout)

    def test_inspecter(self):
        res = self.ok(self.lancer("inspecter", "prise.mp3"))
        self.assertIn("MP3", res.stdout)
        self.assertIn("0.26 s", res.stdout)


class TestCompte(BaseTest):
    def test_verifier_tout_va_bien(self):
        res = self.ok(self.lancer("verifier"))
        self.assertIn("✓ ELEVENLABS_API_KEY est définie", res.stdout)
        self.assertIn("reste 98800", res.stdout)
        self.assertNotIn("Permissions absentes", res.stdout)

    def test_verifier_liste_les_permissions_absentes(self):
        self.serveur.scenario = {"sans_permission_lecture": True}
        res = self.ok(self.lancer("verifier"))
        self.assertIn("- models_read", res.stdout)
        self.assertIn("- text_to_speech", res.stdout)

    def test_verifier_offre_gratuite(self):
        self.serveur.scenario = {"offre": "free"}
        self.assertIn("pas utilisable commercialement", self.ok(self.lancer("verifier")).stdout)

    def test_verifier_sans_cle(self):
        res = self.lancer("verifier", cle=None)
        self.assertEqual(res.returncode, 3)

    def test_historique_et_recuperer(self):
        res = self.ok(self.lancer("historique"))
        self.assertIn("hist1", res.stdout)
        self.assertIn("18 crédits", res.stdout)
        self.ok(self.lancer("recuperer", "hist1", "--sortie", "repris.mp3"))
        fiche = self.fiche("repris.elevenlabs.json")
        self.assertEqual((fiche["origine"], fiche["texte"]), ("historique", "Bonjour, voyageur."))

    def test_modeles_et_consommation(self):
        self.assertIn("eleven_multilingual_v2", self.ok(self.lancer("modeles")).stdout)
        self.assertIn("118 crédits", self.ok(self.lancer("consommation", "--jours", "2")).stdout)

    def test_brut(self):
        res = self.ok(self.lancer("brut", "GET", "/v1/voices/settings/default"))
        self.assertIn('"stability": 0.5', res.stdout)
        res = self.lancer("brut", "POST", f"/v1/text-to-speech/{VOIX_GEORGE}", "--corps", '{"text": "x"}')
        self.assertEqual(res.returncode, 2)
        self.ok(self.lancer("brut", "POST", f"/v1/text-to-speech/{VOIX_GEORGE}", "--corps", '{"text": "x"}',
                            "--sortie", "brut.mp3"))


class TestErreurs(BaseTest):
    def generer(self):
        return self.lancer("parole", VOIX_GEORGE, "Salut.", "--sortie", "a.mp3")

    def test_cle_absente(self):
        res = self.lancer("parole", VOIX_GEORGE, "Salut.", "--sortie", "a.mp3", cle=None)
        self.assertEqual(res.returncode, 3)
        self.assertIn("ELEVENLABS_API_KEY n'est pas définie", res.stderr)

    def test_cle_refusee_et_masquee(self):
        self.serveur.scenario = {"cle_refusee": True}
        res = self.generer()
        self.assertEqual(res.returncode, 3)

    def test_permission_manquante(self):
        self.serveur.scenario = {"permission": "sound_generation"}
        res = self.lancer("bruitage", "x", "--sortie", "a.mp3")
        self.assertEqual(res.returncode, 6)
        self.assertIn("permission sound_generation", res.stderr)

    def test_credits_epuises(self):
        self.serveur.scenario = {"erreur": (401, "quota_exceeded", "This request exceeds your quota.")}
        self.assertEqual(self.generer().returncode, 4)

    def test_moderation(self):
        self.serveur.scenario = {"erreur": (400, "content_against_policy", "This text violates our terms.")}
        self.assertEqual(self.generer().returncode, 8)

    def test_validation_de_l_api(self):
        self.serveur.scenario = {"erreur": (422, "validation", "")}
        res = self.generer()
        self.assertEqual(res.returncode, 2)
        self.assertIn("text : Field required", res.stderr)

    def test_voix_introuvable(self):
        self.serveur.scenario = {"erreur": (404, "voice_not_found", "A voice with that ID does not exist.")}
        res = self.generer()
        self.assertEqual(res.returncode, 1)
        self.assertIn("Voix introuvable", res.stderr)

    def test_limite_puis_succes(self):
        self.serveur.scenario = {"limite": 2}
        self.ok(self.generer())
        self.assertEqual(len([r for r in self.serveur.requetes if r["methode"] == "POST"]), 3)

    def test_limite_persistante(self):
        self.serveur.scenario = {"limite": 100}
        res = self.generer()
        self.assertEqual(res.returncode, 9)
        self.assertIn("Rien n'a été facturé", res.stderr)

    def test_erreur_serveur_sans_nouvel_essai_pour_une_generation(self):
        self.serveur.scenario = {"erreur": (500, "internal_error", "boom")}
        res = self.generer()
        self.assertEqual(res.returncode, 1)
        self.assertEqual(len(self.serveur.requetes), 1)
        self.assertIn("historique", res.stderr)

    def test_delai_depasse(self):
        self.serveur.scenario = {"lent": 2}
        res = self.lancer("parole", VOIX_GEORGE, "Salut.", "--sortie", "a.mp3", "--delai", "0.5")
        self.assertEqual(res.returncode, 7)
        self.assertIn("historique", res.stderr)
        self.assertFalse(os.path.exists(self.chemin("a.mp3")))


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

    def env_bloque(self):
        return {"HTTPS_PROXY": self.url_proxy, "https_proxy": self.url_proxy,
                "ELEVENLABS_API_BASE": "https://api.elevenlabs.invalid"}

    def test_api_bloquee_par_le_proxy(self):
        res = self.lancer("parole", VOIX_GEORGE, "x", "--sortie", "a.mp3", env_extra=self.env_bloque())
        self.assertEqual(res.returncode, 5)
        self.assertIn("api.elevenlabs.invalid est bloqué par la politique réseau", res.stderr)

    def test_verifier_nomme_l_hote_bloque(self):
        res = self.lancer("verifier", env_extra=self.env_bloque())
        self.assertEqual(res.returncode, 5)
        self.assertIn("✗ api.elevenlabs.invalid", res.stdout)


class TestUnitaire(unittest.TestCase):
    def test_envelopper_pcm(self):
        wav = eleven.envelopper_pcm(pcm_factice(1.0, 22050), 22050)
        info = eleven.analyser_wav(wav)
        self.assertEqual((info["frequence_hz"], info["bits"], info["duree_s"]), (22050, 16, 1.0))

    def test_analyser_mp3_ignore_les_octets_parasites(self):
        info = eleven.analyser_mp3(b"\x00\x01" + mp3_factice(4)[10:])
        self.assertEqual(info["frequence_hz"], 44100)
        self.assertAlmostEqual(info["duree_s"], 4 * 1152 / 44100, places=3)

    def test_format_sortie(self):
        self.assertEqual(eleven.format_sortie("a.mp3", None), ("mp3_44100_128", None))
        self.assertEqual(eleven.format_sortie("a.wav", None), ("pcm_44100", 44100))
        self.assertEqual(eleven.format_sortie("a.wav", "pcm_22050"), ("pcm_22050", 22050))
        self.assertEqual(eleven.format_sortie("a.wav", "wav_48000"), ("wav_48000", None))

    def test_masquer(self):
        os.environ["ELEVENLABS_API_KEY"] = CLE
        try:
            self.assertEqual(eleven.masquer(f"clé {CLE} !"), "clé *** !")
        finally:
            del os.environ["ELEVENLABS_API_KEY"]


class TestHook(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ICI, "..", "hooks", "hooks.json"), encoding="utf-8") as f:
            hooks = json.load(f)["hooks"]["SessionStart"]
        self.commande = hooks[0]["hooks"][0]["command"]

    def lancer(self, cle):
        env = {k: v for k, v in os.environ.items() if k != "ELEVENLABS_API_KEY"}
        if cle:
            env["ELEVENLABS_API_KEY"] = cle
        return subprocess.run(["sh", "-c", self.commande], capture_output=True, text=True, env=env, timeout=10)

    def test_silencieux_si_cle_definie(self):
        res = self.lancer(CLE)
        self.assertEqual(res.returncode, 0)
        self.assertEqual(res.stdout, "")

    def test_une_ligne_si_cle_absente(self):
        res = self.lancer(None)
        self.assertEqual(res.returncode, 0)
        self.assertEqual(len(res.stdout.strip().splitlines()), 1)
        self.assertIn("ELEVENLABS_API_KEY", res.stdout)


if __name__ == "__main__":
    unittest.main()
