# elevenlabs

Plugin Claude Code qui donne à un agent **l'API d'[ElevenLabs](https://elevenlabs.io/docs/api-reference)** pour produire l'audio d'un jeu, puis lui fait ranger les sons dans un projet Godot : brief, texte ou prompt, génération, contrôle du résultat (durée, format, niveaux), import dans Godot et vérification de l'import en headless.

Ce que l'agent peut faire :
- **faire parler les personnages** : répliques en synthèse vocale (`eleven_multilingual_v2`, `eleven_v3` expressif, `eleven_flash_v2_5` à moitié prix), dialogues à plusieurs voix, horodatage de chaque mot pour les sous-titres ou le lip sync ;
- **caster les voix** : chercher dans les voix du compte et dans la bibliothèque partagée, concevoir une voix depuis une description, la remixer, cloner une voix avec l'accord écrit de la personne ;
- **produire des bruitages** (bouclables ou non) et **de la musique**, depuis un prompt ou un plan de composition relu avant de payer ;
- **retravailler un enregistrement** : le rejouer avec une autre voix, isoler la voix du bruit, séparer un morceau en pistes ;
- **transcrire** un audio ou une vidéo, avec sous-titres SRT, et **aligner** un texte sur un audio ;
- **suivre le compte** : offre, solde, consommation par jour, historique, et récupération gratuite d'un audio de parole déjà payé.

Le plugin contient :
- **le skill `elevenlabs:audio`** : quand utiliser ElevenLabs et quand l'éviter, le casting des voix, le déroulé en six étapes, les conventions du projet, les règles de coût, les erreurs et ce qu'il faut en dire, les droits et la sécurité de la clé ;
- **le script `skills/audio/scripts/elevenlabs.py`** : client de l'API REST ElevenLabs en Python 3, bibliothèque standard uniquement. Il a une sous-commande par capacité, listées dans [`skills/audio/commandes.md`](skills/audio/commandes.md), et une commande `brut` pour tout autre endpoint. Chaque son reçoit une fiche `.elevenlabs.json` qui permet de le retrouver et de le refaire ;
- **un hook de démarrage**, sans appel réseau, qui ne dit rien si `ELEVENLABS_API_KEY` est définie, et signale en une ligne son absence ;
- **un gabarit de conventions** ([`skills/audio/conventions-exemple.md`](skills/audio/conventions-exemple.md)) à copier dans le projet du jeu, en `.claude/elevenlabs.md`, avec le casting des voix.

Le plugin est générique : le dossier de destination, le nommage, le format, la langue, le casting et le style viennent du projet, jamais du plugin.

Hors du champ du plugin : les agents conversationnels (ElevenAgents), le streaming en temps réel, le doublage de vidéos, Studio et les projets longs. On peut les atteindre avec `brut`, sans l'accompagnement du skill.

## Activer le plugin dans un projet

Dans le `.claude/settings.json` du projet, commité dans son repo :

```json
{
  "extraKnownMarketplaces": {
    "quiche-lorraine-games": {
      "source": {
        "source": "github",
        "repo": "quiche-lorraine-games/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "elevenlabs@quiche-lorraine-games": true
  }
}
```

Ce que ce réglage fait, et ne fait pas :
- **En local**, il est appliqué une fois que le dossier est approuvé. La marketplace est alors ajoutée, mais le plugin n'est pas installé pour autant : chaque personne le fait une fois, avec `claude plugin install elevenlabs@quiche-lorraine-games --scope project`.
- **Dans le cloud** (Claude Code sur le web), il est ignoré : il faut activer le plugin dans les réglages du Project (rubrique Plugins) ou dans les réglages gérés de l'organisation. Voir le [README de la marketplace](../../README.md).

Pour l'installer sur une machine, une fois pour tous les projets :

```bash
claude plugin marketplace add quiche-lorraine-games/claude-plugins
claude plugin install elevenlabs@quiche-lorraine-games
```

Ensuite, écrire les conventions audio du jeu, et son casting, dans `.claude/elevenlabs.md` à partir du [gabarit](skills/audio/conventions-exemple.md). Sans elles, l'agent pose les questions avant de générer.

## Prérequis de l'environnement cloud

Pour une session Claude Code dans le cloud, régler l'environnement (menu de l'environnement dans la barre de titre de la session, puis *Edit*) :

1. **Accès réseau**, dans *Allowed domains* (niveau *Limited*), ajouter **`api.elevenlabs.io`**. C'est le seul hôte utilisé : l'audio revient dans la réponse de l'API, il n'y a pas d'hôte de fichiers à part. Testé le 30/10/2026 : l'API répond (401 sans clé), alors que le site de documentation `elevenlabs.io` était bloqué par le proxy de l'environnement.
   - Les comptes à résidence de données utilisent un autre hôte (par exemple `api.eu.residency.elevenlabs.io`) : l'ajouter, et le passer au script par `ELEVENLABS_API_BASE=https://<hôte>`.

2. **Secret** : créer une clé API dans les réglages ElevenLabs (*Developers*, *API Keys*), puis l'enregistrer en variable d'environnement **`ELEVENLABS_API_KEY`** dans les réglages de l'environnement. Ne jamais la coller dans le chat ni la commiter. Une clé ajoutée en *Network secret* (injectée par le proxy) ne suffit pas : le script et le hook lisent la variable d'environnement.

3. **Permissions de la clé** : une clé ElevenLabs peut être restreinte endpoint par endpoint. Pour tout le plugin, cocher au moins :

   | Permission | Commandes |
   |---|---|
   | Text to Speech | `parole`, `dialogue` |
   | Sound Effects | `bruitage` |
   | Music Generation | `musique`, `plan-musique`, `separer-pistes` |
   | Voice Changer, Audio Isolation | `changer-voix`, `isoler` |
   | Speech to Text, Forced Alignment | `transcrire`, `aligner` |
   | Voices : lecture et écriture | `voix`, `voix-info`, `bibliotheque`, voix par nom ; `ajouter-voix`, `concevoir-voix`, `creer-voix`, `cloner` |
   | User : lecture | solde dans `verifier`, `consommation` |
   | Models : lecture | `modeles` |
   | History : lecture | `historique`, `recuperer` |

   Les noms exacts des cases changent selon l'interface ; les noms techniques (`text_to_speech`, `voices_read`, `user_read`, `models_read`, `speech_history_read`…) sont ceux que l'API cite quand une permission manque. Une permission manquante fait sortir le script en code 6 avec son nom. Modifier les permissions ne change pas la valeur de la clé : inutile de toucher au secret.

   Une limite de crédits par clé peut aussi être réglée au même endroit : c'est un bon garde-fou pour un agent.

4. **Ouvrir une nouvelle session** : les variables de l'environnement ne sont lues qu'au démarrage d'une session.

5. Vérifier, dans la nouvelle session :

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/audio/scripts/elevenlabs.py" verifier
   ```

   ou, depuis une copie de ce repo, `python3 plugins/elevenlabs/skills/audio/scripts/elevenlabs.py verifier`. Le script affiche l'offre, le solde et les permissions de lecture absentes. Les permissions de génération ne se testent pas sans payer.

Pour la vérification de l'import (étape 6 du skill), Godot doit être installé dans l'environnement. Sans Godot, l'agent livre le son mais signale que l'import n'a pas été vérifié.

## Coût en crédits

ElevenLabs décompte des crédits, inclus chaque mois dans l'abonnement (offres Free, Starter, Creator, Pro, Scale, Business), avec un dépassement facturé à l'usage sur certaines offres ([prix de l'API](https://elevenlabs.io/pricing/api), [prix des offres](https://elevenlabs.io/pricing)).

Barème indicatif relevé le 30/10/2026, **à vérifier** sur ces pages : les sources secondaires se contredisent, et la page officielle n'a pas pu être ouverte depuis l'environnement d'écriture.

| Usage | Crédits | Source |
|---|---|---|
| Parole et dialogue, `eleven_multilingual_v2` et `eleven_v3` | 1 par caractère | documentation des modèles, recoupée par plusieurs guides |
| Parole, `eleven_flash_v2_5` et `eleven_turbo_v2_5` | 0,5 par caractère | idem |
| Bruitage | environ 200 par génération | guides tiers |
| Musique | environ 900 par minute | guides tiers |
| Transcription, changement de voix, isolation, séparation, alignement, conception de voix | non relevé | — |

Le coût réel de chaque génération est recopié dans la fiche (`credits`) quand l'API le donne, par l'en-tête `character-cost`. `verifier` affiche le solde ; `consommation` les crédits consommés par jour.

Le skill impose à l'agent d'annoncer le coût d'une génération. Avant une série ou une musique, il attend l'accord. Il ne relance jamais en boucle pour « améliorer ».

## Droits sur l'audio généré : à vérifier avant tout usage commercial

**Point bloquant pour un jeu commercial.** D'après l'aide d'ElevenLabs ([Can I publish the content I generate on the platform?](https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform)) et sa documentation de facturation :

- **Offre payante** : l'audio généré pendant un abonnement payant peut être utilisé commercialement, sans limite de durée, même après la fin de l'abonnement. Les conditions propres à chaque service (*Service-Specific Terms*) s'appliquent en plus.
- **Offre gratuite** : usage non commercial seulement, avec attribution. Les conditions d'Eleven Music interdisent expressément l'usage commercial des musiques générées en offre gratuite.
- **Après un passage à l'offre gratuite**, l'audio produit pendant la période payante reste utilisable commercialement ; l'audio produit ensuite ne l'est pas.

À faire avant de mettre un son ElevenLabs dans le jeu :
1. **Lire la version en vigueur** des [conditions d'utilisation](https://elevenlabs.io/terms-of-use), des conditions propres aux services, et des [conditions d'Eleven Music](https://elevenlabs.io/eleven-music-v1-terms). Les points ci-dessus viennent d'extraits de recherche : les pages n'ont pas pu être ouvertes directement.
2. **Vérifier l'offre du compte** au moment de la génération : `verifier` l'affiche, et signale l'offre gratuite. Traiter tout son généré en offre gratuite comme un prototype, à régénérer avant la sortie.
3. **Voix de la bibliothèque** : leur auteur peut fixer des conditions (tarif propre, préavis de retrait). Lire la fiche de la voix avant de l'utiliser pour un personnage durable.
4. **Voix clonées** : garder l'accord écrit de la personne enregistrée, qui couvre l'usage dans le jeu.
5. **Garder les `.elevenlabs.json`** (date, `request_id`) pour prouver quand et avec quel compte chaque son a été produit.

## Alternative : le serveur MCP officiel

ElevenLabs publie un serveur MCP officiel, [elevenlabs/elevenlabs-mcp](https://github.com/elevenlabs/elevenlabs-mcp), lancé en local par `uvx elevenlabs-mcp`. Ce plugin ne le déclare pas :
- il faudrait installer `uv` et lancer le serveur dans chaque environnement ;
- ses outils écrivent les fichiers où il l'entend, sans la fiche de traçabilité ni le contrôle du résultat ;
- un script lisible sans dépendance est plus simple à auditer : on voit ce qui part vers l'API et où va la clé.

On peut l'ajouter soi-même dans le `.mcp.json` d'un projet. Les règles de coût, de droits et de sécurité du skill restent alors valables.

## Tests

```bash
python3 -m unittest discover -s plugins/elevenlabs/tests -v
```

Les tests lancent le script contre un faux serveur HTTP local (`http.server`) qui imite l'API, et contre un faux proxy qui refuse les connexions. L'URL de base se règle par `--api` ou `ELEVENLABS_API_BASE`.

Les tests couvrent :
- chaque sous-commande : endpoint appelé, corps ou formulaire envoyé, paramètres d'URL, fichiers écrits, fiche, validations locales ;
- le choix du format selon l'extension, et l'enveloppe WAV autour du PCM ;
- l'analyse des MP3 et des WAV (durée, fréquence, débit, niveaux) ;
- la résolution d'une voix par son nom ;
- chaque cas d'erreur et son code de sortie, les nouveaux essais sur 429 et l'absence de nouvel essai sur une génération payante en erreur 5xx ;
- l'absence de la clé dans toutes les sorties et tous les fichiers ;
- le hook de démarrage.

## Documentation de l'API utilisée

Le script vise `https://api.elevenlabs.io`, avec l'en-tête `xi-api-key: <clé>`. Il s'appuie sur la **spécification OpenAPI officielle**, servie par l'API elle-même ([`/openapi.json`](https://api.elevenlabs.io/openapi.json), lue le 30/10/2026) : chemins, champs, bornes (durées, longueurs de description), formats de sortie par endpoint, forme des réponses (`audio_base64` et `alignment` des endpoints horodatés, `previews` de la conception de voix, `additional_formats` de la transcription), en-têtes `character-cost` et `song-id`.

Observé sur l'API réelle le 30/10/2026, sans rien dépenser :
- erreurs de clé : HTTP 401 avec `detail.status` à `invalid_api_key` (clé fausse), `needs_authorization` (clé absente) ou `missing_permissions` (permission absente, citée dans `detail.message`) ;
- erreurs de validation : HTTP 422 avec une liste `detail` de champs (`loc`, `msg`), ou un `detail` objet `unprocessable_entity` ;
- la validation du corps passe avant le contrôle des permissions.

Recoupé par recherche (pages de documentation bloquées depuis l'environnement d'écriture) :
- [erreur 429](https://elevenlabs.io/docs/help-center/technical/api-error-code-429) : `too_many_concurrent_requests` (limite de l'offre : 2 en gratuit, 3 Starter, 5 Creator, 10 Pro, 15 Scale et Business) et `system_busy`, à réessayer ;
- longueurs maximales par requête selon le modèle : 5 000 caractères (`eleven_v3`), 10 000 (`eleven_multilingual_v2`), 40 000 (`eleven_flash_v2_5`, `eleven_turbo_v2_5`).

Ce qui reste incertain, et comment le script le gère :
- **Appels payants.** Aucune commande de génération n'a encore été validée par un appel réel : la clé de l'environnement d'écriture n'avait aucune permission de génération. Les formes de réponse viennent de la spécification OpenAPI.
- **Erreurs non observées** : `quota_exceeded` (crédits épuisés) et la modération n'ont pas de forme documentée fiable. Le script les reconnaît par mots-clés dans `detail.status` et `detail.message` ; un cas mal reconnu sort en code 1 avec le message de l'API.
- **En-têtes de coût.** `character-cost` n'est documenté que pour les bruitages ; le script le lit sur toutes les réponses, et la fiche n'a pas de champ `credits` quand il manque. `request-id` et `history-item-id` sont lus de la même façon.
- **Formats réservés aux offres supérieures** (`pcm_44100`, `mp3_44100_192`…) : la liste exacte par offre n'est pas dans la spécification. Le script laisse l'API refuser et suggère un autre `--format`.
- **`additional_formats` de la transcription** est envoyé en JSON dans le formulaire, comme le font les SDK ; non validé par un appel réel.
- **Bibliothèque de voix** : certains champs d'une voix partagée (`public_owner_id`, `use_case`) viennent de la spécification et n'ont pas été vus dans une vraie réponse.
