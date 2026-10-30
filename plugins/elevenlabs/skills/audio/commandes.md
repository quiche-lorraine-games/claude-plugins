# Référence des commandes de `elevenlabs.py`

Les capacités de l'API ElevenLabs utiles à un jeu, une sous-commande par endpoint. Ce fichier complète [SKILL.md](SKILL.md) : les règles de coût, de conventions, de droits et de sécurité y restent valables pour chaque commande. `python3 "$ELEVEN" <commande> --help` donne toutes les options.

## Entrées, sorties et options communes

**Voix.** Partout où une commande attend une voix, on peut passer son `voice_id` (20 caractères) ou le nom exact d'une voix du compte. Les voix par défaut s'appellent par exemple « George - Warm Storyteller » : « George » suffit. Un nom demande la permission `voices_read` ; un `voice_id` ne demande rien.

**Entrées audio.** Fichiers locaux : MP3, WAV, Ogg, FLAC, M4A, AAC, Opus, WebM, et pour `transcrire` des vidéos (MP4, MOV, MKV). `transcrire` accepte aussi une URL.

**Format de sortie.** Par défaut, l'extension de `--sortie` choisit le format :

| Extension | `output_format` demandé | Remarque |
|---|---|---|
| `.mp3` | `mp3_44100_128` | toutes les offres |
| `.wav` | `pcm_44100`, enveloppé en WAV par le script | PCM 16 bits mono. `pcm_44100` peut demander une offre supérieure : passe `--format pcm_22050` ou `pcm_24000` |
| `.opus`, `.pcm` | `opus_48000_96`, `pcm_44100` | Godot ne les importe pas |

`--format` impose un autre format (`mp3_44100_192`, `pcm_48000`, `wav_44100`…), à condition qu'il corresponde à l'extension. La musique et la séparation de pistes n'ont pas de format `wav_*` : avec une sortie `.wav`, le script demande du PCM et l'enveloppe.

**Fichiers écrits.** `--sortie` désigne le fichier principal ; le dossier est créé au besoin. La fiche `<nom>.elevenlabs.json` est écrite à côté. Les autres fichiers (`<nom>.alignement.json`, `<nom>.srt`, aperçus `<nom>_1.mp3`…) sont listés dans le champ `sorties` de la fiche, par des chemins relatifs à son dossier.

**Options de toutes les commandes payantes** :

| Option | Effet |
|---|---|
| `--sortie F` | fichier principal (obligatoire) ; refuse d'écraser sans `--ecraser` |
| `--a-blanc` | affiche la requête sans l'envoyer : ni clé, ni réseau, ni crédit |
| `--param CLE=VALEUR` | ajoute un champ de l'API tel quel (valeur JSON, sinon texte) ; répétable. Il ne peut pas remplacer un champ déjà fixé par une option |
| `--delai S` | délai de réponse maximal, de 120 à 600 s selon la commande |

## Compte

| Commande | Endpoint | Permission de la clé |
|---|---|---|
| `verifier` | `GET /v1/user/subscription`, et sondes de permissions | `user_read` pour le solde |
| `modeles` | `GET /v1/models` | `models_read` |
| `consommation [--jours N]` | `GET /v1/usage/character-stats` | non vérifiée |
| `historique [--limite N] [--voix ID] [--recherche T]` | `GET /v1/history` | `speech_history_read` |
| `recuperer HISTORY_ID --sortie F.mp3` | `GET /v1/history/{id}` et `/audio` | `speech_history_read` |

Tout est gratuit. `historique` ne liste que la parole, le dialogue et le changement de voix : l'API ne garde ni les bruitages ni la musique. `recuperer` sert après un délai dépassé ou une erreur, pour ne pas payer deux fois.

## Voix

| Commande | Endpoint |
|---|---|
| `voix [--recherche T] [--type T] [--categorie C] [--limite N]` | `GET /v2/voices` |
| `voix-info VOIX` | `GET /v1/voices/{voice_id}` |
| `bibliotheque [--recherche] [--genre] [--age] [--accent] [--langue] [--usage] [--categorie]` | `GET /v1/shared-voices` |
| `ajouter-voix PUBLIC_OWNER_ID VOICE_ID --nom N` | `POST /v1/voices/add/{public_owner_id}/{voice_id}` |
| `concevoir-voix "description" --sortie base.mp3` | `POST /v1/text-to-voice/design` |
| `remixer-voix VOIX "changements" --sortie base.mp3` | `POST /v1/text-to-voice/{voice_id}/remix` |
| `creer-voix GENERATED_VOICE_ID --nom N --description D` | `POST /v1/text-to-voice` |
| `cloner FICHIERS… --nom N --consentement` | `POST /v1/voices/add` |

`concevoir-voix` :
- description de 20 à 1 000 caractères : âge, genre, timbre, accent, débit, attitude, contexte (« vieille aubergiste chaleureuse, voix éraillée, accent du sud, parle vite ») ;
- `--texte` : texte lu par les aperçus, 100 à 1 000 caractères. Sans lui, l'API en écrit un adapté à la description. Pour juger une voix de personnage, donne plutôt une vraie réplique du jeu ;
- `--modele eleven_ttv_v3` (plus expressif) ou `eleven_multilingual_ttv_v2` (défaut) ; `--ameliorer` laisse l'IA enrichir la description ; `--volume` (−1 à 1), `--guidage`, `--graine` ;
- écrit les aperçus en `base_1.mp3`, `base_2.mp3`… et la fiche `base.elevenlabs.json` avec le `generated_voice_id` de chacun. Un aperçu n'est pas une voix : il faut `creer-voix` pour le garder.

`remixer-voix` prend les mêmes options, avec une description des changements (5 caractères au moins) : « plus âgée, plus fatiguée ».

`creer-voix` occupe un emplacement de voix du compte (nombre limité selon l'offre). `--etiquette language=fr` (répétable) ajoute des étiquettes.

`cloner` fait un clonage instantané depuis un ou plusieurs enregistrements propres de la même personne (quelques minutes au total suffisent). `--debruiter` retire le bruit de fond des échantillons. **`--consentement` est obligatoire** et engage : l'accord écrit de la personne existe.

## Générer

### `parole VOIX "texte" --sortie F`

`POST /v1/text-to-speech/{voice_id}`, ou `/with-timestamps` avec `--horodatage`.

| Option | Champ de l'API | Effet |
|---|---|---|
| `--fichier-texte F` | `text` | texte lu dans un fichier, au lieu de l'argument |
| `--modele` | `model_id` | `eleven_multilingual_v2` (défaut, stable), `eleven_v3` (le plus expressif, balises `[whispers]`…), `eleven_flash_v2_5` (rapide, moitié prix) |
| `--langue fr` | `language_code` | impose la langue |
| `--stabilite 0–1` | `voice_settings.stability` | bas : plus expressif et variable ; haut : plus régulier. Avec `eleven_v3`, préfère 0, 0,5 ou 1 |
| `--similarite 0–1` | `voice_settings.similarity_boost` | fidélité à la voix d'origine |
| `--style 0–1` | `voice_settings.style` | exagère le style ; à garder bas |
| `--vitesse 0,7–1,2` | `voice_settings.speed` | débit |
| `--sans-boost` | `voice_settings.use_speaker_boost` | désactive le renfort de ressemblance |
| `--graine N` | `seed` | meilleur effort de reproductibilité |
| `--texte-avant`, `--texte-apres` | `previous_text`, `next_text` | continuité d'un texte découpé |
| `--normalisation auto\|on\|off` | `apply_text_normalization` | lecture des nombres, dates, sigles |
| `--horodatage` | endpoint `/with-timestamps` | écrit `<nom>.alignement.json` : temps de début et de fin de chaque caractère et de chaque mot |

Les réglages non passés gardent ceux de la voix (`voix-info`).

### `dialogue --replique VOIX=TEXTE … --sortie F`

`POST /v1/text-to-dialogue` (`/with-timestamps` avec `--horodatage`). Les répliques s'enchaînent dans l'ordre, dans un seul fichier, avec des transitions naturelles.
- `--replique` est répétable ; `--script scene.json` lit une liste `[{"voix": "…", "texte": "…"}, …]` (ajoutée après les `--replique`) ;
- 10 voix différentes au plus ; au-delà de 2 000 caractères en tout, l'API peut couper ou refuser : découpe en scènes ;
- modèle `eleven_v3` par défaut, avec ses balises (`[laughs]`, `[interrupting]`…) ; `--stabilite`, `--langue`, `--graine`.

Pour des répliques à déclencher séparément dans le jeu, préfère une `parole` par réplique : un dialogue sort en un seul fichier.

### `bruitage "prompt" --sortie F`

`POST /v1/sound-generation`.
- `--duree S` : de 0,5 à 30 s ; sans elle, le modèle choisit. Le script signale une durée obtenue très différente ;
- `--boucle` : son qui boucle sans raccord audible (à déclarer aussi à l'import Godot) ;
- `--influence 0–1` : fidélité au prompt (0,3 par défaut côté API) ; plus haut, moins de variété ;
- `--modele eleven_text_to_sound_v2` (défaut) ou `eleven_text_to_sound_v3`.

Pour plusieurs variantes d'un même son (pas, impacts), c'est une série : annonce le total et attends l'accord.

### `musique "prompt" --sortie F` ou `musique --plan plan.json --sortie F`

`POST /v1/music`.
- `--duree S` : de 3 à 600 s, avec un prompt ;
- `--instrumental` : garantit l'absence de voix ;
- `--modele music_v1` (défaut), `music_v2`, `music_v2_5` ; `--graine` ;
- `--plan` : plan de composition JSON, sortie de `plan-musique`, éventuellement retouché. Les sections fixent alors la durée.

L'en-tête `song-id` est recopié dans la fiche (`song_id`).

### `plan-musique "prompt" --sortie plan.json`

`POST /v1/music/plan`. Écrit un plan : styles globaux (positifs et négatifs) et sections (nom, durée, styles locaux, paroles). Le script affiche les sections. Relis-le avec l'utilisateur, ajuste-le au besoin (durées, styles, `lines` vides pour un instrumental), puis passe-le à `musique --plan`. Coût non publié : vérifie la page de prix.

## Traitement

| Commande | Endpoint | Sortie |
|---|---|---|
| `changer-voix ENTREE VOIX --sortie F` | `POST /v1/voice-changer/{voice_id}` | la prise rejouée par la voix cible, mêmes intonations et timing |
| `isoler ENTREE --sortie F.mp3` | `POST /v1/audio-isolation` | la voix seule, sans bruit ni musique (MP3) |
| `separer-pistes ENTREE --sortie DOSSIER` | `POST /v1/music/stem-separation` | une piste par instrument dans le dossier, et `DOSSIER.elevenlabs.json` à côté |
| `transcrire ENTREE --sortie F.json` | `POST /v1/speech-to-text` | transcription JSON (mots, temps, locuteurs) |
| `aligner AUDIO "texte" --sortie F.json` | `POST /v1/forced-alignment` | temps de chaque mot et caractère du texte |

`changer-voix` : `--modele eleven_multilingual_sts_v2` (défaut) ou `eleven_english_sts_v2` ; `--debruiter` ; mêmes réglages de voix que `parole`. Utile pour garder le jeu d'une prise enregistrée par l'équipe, avec la voix d'un personnage.

`separer-pistes` : six pistes par défaut (voix, batterie, basse, guitare, piano, autres), `--deux-pistes` pour voix et accompagnement. `--format pcm_44100` écrit les pistes en WAV.

`transcrire` :
- `--modele scribe_v2` (défaut) ; `--langue` (ISO 639-1 ou 639-3) ;
- `--locuteurs N` : active la diarisation, N locuteurs au plus ;
- `--sans-evenements` : ne note pas « (rires) », « (pas) » ;
- `--srt` : écrit aussi `<nom>.srt`, prêt pour des sous-titres ;
- `--terme MOT` (répétable) : noms propres du jeu à reconnaître.

`aligner` prend le texte en argument ou par `--fichier-texte`. Pour une réplique générée par `parole`, `--horodatage` donne le même résultat sans seconde requête.

## Divers

**`brut METHODE CHEMIN [--corps JSON|@fichier.json] [--requete CLE=VALEUR]… [--sortie F]`** appelle un endpoint que le script ne connaît pas (la liste complète est dans la [référence de l'API](https://elevenlabs.io/docs/api-reference)). Une réponse JSON est affichée ; une réponse binaire exige `--sortie`. Les règles de coût valent aussi : un `POST` est en général payant.

```bash
python3 "$ELEVEN" brut GET /v1/voices/settings/default
python3 "$ELEVEN" brut GET /v1/audio-effects/catalog
```

**`inspecter FICHIER`** : contrôle local d'un audio (format, durée, fréquence, canaux, débit, niveaux d'un WAV 16 bits), gratuit.

## Enchaînements utiles

**Voix d'un nouveau personnage :**
```bash
python3 "$ELEVEN" concevoir-voix "vieux forgeron bourru, voix grave et rocailleuse, parle lentement" \
  --texte "<une vraie réplique du personnage, 100 caractères au moins>" --sortie /tmp/forgeron.mp3
# l'utilisateur écoute /tmp/forgeron_1.mp3, _2, _3 et choisit
python3 "$ELEVEN" creer-voix <generated_voice_id> --nom "Forgeron" --description "vieux forgeron bourru, voix grave"
# noter le voice_id dans le casting du projet
```

**Scène de dialogue à déclencher réplique par réplique :** une `parole` par réplique, avec `--texte-avant` (réplique précédente) pour garder le ton, et la même voix et les mêmes réglages que le casting pour chaque personnage.

**Musique de niveau :**
```bash
python3 "$ELEVEN" plan-musique "dark ambient dungeon exploration, low strings, distant drums, loopable" \
  --duree 90 --sortie musique/donjon.plan.json
# relire le plan avec l'utilisateur, l'ajuster
python3 "$ELEVEN" musique --plan musique/donjon.plan.json --sortie assets/audio/musique/donjon_01.mp3
```

**Sous-titres d'une cinématique enregistrée :** `transcrire cinematique.wav --srt --langue fr --terme <nom propre> --sortie sous-titres/intro.json`, puis relire le `.srt`.
