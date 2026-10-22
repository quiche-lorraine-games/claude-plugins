# tripo

Plugin Claude Code qui donne à un agent **toute l'API de [Tripo 3D](https://developers.tripo3d.ai/en)** (apiv3), puis lui fait ranger les résultats dans un projet Godot : brief, prompt, génération, contrôle du résultat (poids, nombre de faces, échelle), import dans Godot et vérification de l'import en headless.

Ce que l'agent peut faire :
- **générer un modèle** depuis un prompt, une image ou plusieurs vues ;
- **retravailler un modèle** Tripo ou importé : retexturer, réduire les faces, déplier les UV, convertir (GLTF, USDZ, FBX, OBJ, STL, 3MF), découper en pièces et compléter ces pièces ;
- **produire des images** : concept depuis un prompt, retouche d'image, quatre vues d'un objet et retouche de ces vues, carte de profondeur, splat gaussien ;
- **animer** : vérifier qu'un modèle peut être riggé, le rigger, lui appliquer des animations prédéfinies ;
- **suivre le compte** : solde, historique de consommation, statut d'une ou plusieurs tâches.

Le plugin contient :
- **le skill `tripo:generer`** : quand utiliser Tripo et quand l'éviter, le déroulé en six étapes, où trouver les conventions du projet, les règles de coût, les erreurs et ce qu'il faut en dire, la sécurité de la clé ;
- **le script `skills/generer/scripts/tripo.py`** : client de l'API REST Tripo (apiv3) en Python 3, bibliothèque standard uniquement. Il a une sous-commande par endpoint, listées dans [`skills/generer/commandes.md`](skills/generer/commandes.md), et une commande `brut` pour un endpoint qu'il ne connaît pas encore. Chaque résultat téléchargé reçoit une fiche `.tripo.json` qui permet de le retrouver, de retracer sa chaîne de fabrication et de le refaire ;
- **un hook de démarrage**, sans appel réseau, qui ne dit rien si `TRIPO_API_KEY` est définie, et signale en une ligne son absence ;
- **un gabarit de conventions** ([`skills/generer/conventions-exemple.md`](skills/generer/conventions-exemple.md)) à copier dans le projet du jeu, en `.claude/tripo.md`.

Le plugin est générique : le dossier de destination, le nommage, le budget de faces, le style et les textures viennent du projet, jamais du plugin.

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
    "tripo@quiche-lorraine-games": true
  }
}
```

Ce que ce réglage fait, et ne fait pas :
- **En local**, il est appliqué une fois que le dossier est approuvé (dialogue de confiance de l'espace de travail). La marketplace est alors ajoutée, mais le plugin n'est pas installé pour autant : chaque personne le fait une fois, avec `claude plugin install tripo@quiche-lorraine-games --scope project`. Tant que ce n'est pas fait, `/plugin` affiche dans l'onglet *Errors* que le plugin est activé mais pas installé.
- **Dans le cloud** (Claude Code sur le web), il est ignoré : une session cloud n'installe pas les plugins listés dans `enabledPlugins` d'un repo, ni les marketplaces de `extraKnownMarketplaces`. Il faut activer le plugin dans les réglages du Project (rubrique Plugins) ou dans les réglages gérés de l'organisation. Voir le [README de la marketplace](../../README.md) et la [documentation des environnements cloud](https://code.claude.com/docs/en/cloud-environments).

Pour l'installer sur une machine, une fois pour tous les projets :

```bash
claude plugin marketplace add quiche-lorraine-games/claude-plugins
claude plugin install tripo@quiche-lorraine-games
```

Ensuite, écrire les conventions d'assets du jeu dans `.claude/tripo.md` à partir du [gabarit](skills/generer/conventions-exemple.md). Sans elles, l'agent pose les questions avant de générer.

## Prérequis de l'environnement cloud

Pour une session Claude Code dans le cloud, régler l'environnement (menu de l'environnement dans la barre de titre de la session, puis *Edit*) :

1. **Accès réseau**, dans *Allowed domains* (niveau *Limited*), ajouter :

   | Domaine | Rôle | Certitude |
   |---|---|---|
   | `openapi.tripo3d.ai` | API v3 : création et suivi des tâches, envoi d'images, solde | documenté ; testé le 21/10/2026 (répond 401 sans clé) |
   | `tripo-data.rg1.data.tripo3d.com` | hôte des fichiers de modèles (URL signées) | **non documenté** ; signalé par un projet tiers, à confirmer à la première génération |

   - `api.tripo3d.ai` est l'hôte de l'**ancienne API v2**, qui n'accepte plus de requêtes à partir du 31/10/2026 à 16:00 UTC. Le plugin ne s'en sert pas.
   - Les exemples de la documentation montrent des URL de modèles sur `cdn.tripo3d.ai`, mais ce domaine ne résolvait pas au 21/10/2026 : c'est un exemple, pas l'hôte réel.
   - L'hôte réel de chaque fichier est écrit dans le champ `hote_fichier` du `.tripo.json`. Si le téléchargement est bloqué, le script cite le domaine à ajouter.
   - Les fichiers de plus de 50 Mo (modèles à `importer`, jusqu'à 150 Mo) sont envoyés sur une URL pré-signée. Son hôte n'est pas documenté. S'il est bloqué, le script le cite aussi.

2. **Secret** : enregistrer la clé API Tripo (créée dans la console Tripo, page *API Keys*) en variable d'environnement **`TRIPO_API_KEY`** dans les réglages de l'environnement. Ne jamais la coller dans le chat ni la commiter. Une clé ajoutée en *Network secret* (injectée par le proxy dans les requêtes) ne suffit pas : le script et le hook lisent la variable d'environnement.

3. **Ouvrir une nouvelle session** : les variables de l'environnement ne sont lues qu'au démarrage d'une session.

4. Vérifier, dans la nouvelle session :

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/generer/scripts/tripo.py" verifier
   ```

   ou, depuis une copie de ce repo, `python3 plugins/tripo/skills/generer/scripts/tripo.py verifier`.

Pour la vérification de l'import (étape 6 du skill), Godot doit être installé dans l'environnement, par exemple par son script d'installation. Sans Godot, l'agent livre le modèle mais signale que l'import n'a pas été vérifié.

## Coût en crédits

L'API est pré-payée : 1 crédit = 0,01 $. Le paiement se fait à l'usage, par recharge depuis 1 $ ([prix](https://developers.tripo3d.ai/en/pricing), [facturation](https://developers.tripo3d.ai/en/docs/billing)).

Barème publié au 22/10/2026 (pages [prix](https://developers.tripo3d.ai/en/pricing) et [H3.1](https://developers.tripo3d.ai/en/models/v3-1)). Générations avec le modèle par défaut du script, `v3.1-20260211` :

| Tâche | Sans texture | Texture standard | Texture detailed |
|---|---|---|---|
| Texte → modèle | 10 | 20 | 30 |
| Image ou vues multiples → modèle | 20 | 30 | 40 |

Suppléments : géométrie detailed +20, quads +5, low-poly +10, pièces séparées +20, texture 8K +20. Modèles [P1](https://developers.tripo3d.ai/en/models/p1) : 30 à 60 ; [P2](https://developers.tripo3d.ai/en/models/p2) : 100 à 130.

| Autres tâches | Crédits |
|---|---|
| Retexture | 10 à 30 |
| Conversion de format | 5 à 10 |
| Réduction des faces | 10 à 40 |
| UV automatiques | 20 |
| Segmentation | 40 ; intelligente : 85 (image) ou 55 (modèle) |
| Complétion des pièces | 50, ou 30 en `quick_cap` |
| Vérification de rig | gratuite |
| Rig | 25 ([page Rigging](https://developers.tripo3d.ai/en/models/rig)) |
| Animation | 10 par animation |
| Image depuis un prompt ou une image | 5 à 20 selon le modèle d'image |
| Quatre vues depuis une image | 10 ; retouche : 5 par vue |
| Import, splat, profondeur | non publié |

Les crédits sont gelés à la création de la tâche, débités si elle réussit, et rendus si elle échoue ou est annulée. Le solde s'affiche avec `tripo.py verifier`.

Le skill impose à l'agent d'annoncer le coût d'une génération. Avant une série ou une option payante, il attend l'accord. Il ne relance jamais en boucle pour « améliorer ».

## Licence des modèles générés : à vérifier avant tout usage commercial

**Point bloquant pour un jeu commercial.** D'après les [conditions d'utilisation de Tripo](https://www.tripo3d.ai/terms), reprises sur le [portail développeurs](https://developers.tripo3d.ai/en/terms) :

- **§ 5.2.1, utilisateurs gratuits** (*Free Users*) : Tripo conserve tous les droits sur leurs entrées et leurs sorties (*« Tripo retains all rights over their Inputs and Outputs »*). Un modèle produit sans offre payante n'appartient donc pas au studio.
- **§ 5.2.2, utilisateurs payants** (*Paid Users*) : ils ont en général tous les droits sur leurs entrées et leurs sorties. Tripo garde une licence non exclusive, gratuite, pour fournir le service, et s'engage à ne pas s'en servir pour entraîner ses modèles.
- **§ 3.2** : les sorties peuvent servir à des fins commerciales ou non. Ce passage ne distingue pas gratuit et payant ; un article de Tripo y voit une tension avec le § 5.2.1 et conseille de traiter les sorties gratuites comme non commerciales.
- La page d'aide [How to Use Tripo Models Commercially](https://www.tripo3d.ai/help/privacy-policy/how-to-use-tripo-models-commercially) le confirme : seuls les utilisateurs payants peuvent exploiter commercialement leurs modèles (jeux, packs d'assets, travail client).

À faire avant de mettre un asset Tripo dans le jeu :
1. **Lire la version en vigueur** des conditions (§ 3.2 et § 5.2). Elles n'ont pas pu être ouvertes directement pendant l'écriture de ce plugin : les citations ci-dessus viennent d'extraits de recherche.
2. **Confirmer que le compte API compte comme « payant »**. Les crédits API sont pré-payés, mais les nouveaux comptes reçoivent des crédits gratuits : rien ne dit si un modèle généré avec ces crédits relève du § 5.2.1. Le demander par écrit au support Tripo.
3. **Traiter tout modèle généré avant le premier paiement comme un prototype**, à régénérer ou à remplacer avant la sortie.
4. **Garder les `.tripo.json`** (date, `task_id`) pour prouver quand et avec quel compte chaque asset a été produit.
5. **Vérifier les droits de l'image source** pour `image` : l'image d'entrée a ses propres droits, distincts de ceux du modèle.

## Alternative : un serveur MCP

Tripo n'a ni connecteur officiel ni serveur MCP distant. Il existe des serveurs MCP qui tournent en local :
- [VAST-AI-Research/tripo-mcp](https://github.com/VAST-AI-Research/tripo-mcp), présenté comme officiel, lancé par `uvx tripo-mcp` et pensé pour Blender ;
- des serveurs communautaires récents, comme [ebrob/tripo3d-mcp-server](https://github.com/ebrob/tripo3d-mcp-server) ou [pasie15/tripo-ai-mcp-server](https://github.com/pasie15/tripo-ai-mcp-server).

Ce plugin n'en déclare aucun, pour trois raisons :
- ces serveurs sont jeunes, et il faudrait les installer et les lancer dans chaque environnement ;
- plusieurs visaient encore l'API v2, qui ferme ;
- un script lisible sans dépendance est plus simple à auditer : on voit ce qui part vers l'API et où va la clé.

On peut en ajouter un soi-même dans le `.mcp.json` d'un projet. Les règles de coût et de sécurité du skill restent alors valables.

## Tests

```bash
python3 -m unittest discover -s plugins/tripo/tests -v
```

Les tests lancent le script contre un faux serveur HTTP local (`http.server`) qui imite l'API, et contre un faux proxy qui refuse les connexions. L'URL de base se règle par `--api` ou `TRIPO_API_BASE`, et les hôtes de fichiers testés par `TRIPO_HOTES_FICHIERS`.

Les tests couvrent :
- la création de tâche, le suivi jusqu'au succès, le téléchargement de toutes les sorties et le `.tripo.json` ;
- chaque sous-commande : endpoint appelé, corps envoyé, fichiers écrits, validations locales ;
- l'envoi de fichiers, y compris par URL pré-signée au-delà de 50 Mo ;
- la conversion de format et la reprise d'une tâche (`telecharger`) ;
- chaque cas d'erreur et son code de sortie ;
- l'absence de la clé dans toutes les sorties et tous les fichiers ;
- le hook de démarrage.

## Documentation de l'API utilisée

Le script vise l'**apiv3** (`https://openapi.tripo3d.ai/v3`, en-tête `Authorization: Bearer <clé>`). Il s'appuie sur la documentation officielle de Tripo :

- [Quick Start](https://developers.tripo3d.ai/en/docs/quick-start) : flux création, suivi puis téléchargement ; `output.model_url` ; URL à télécharger aussitôt (la page indique une expiration après 5 minutes).
- [Migration v2 → v3](https://developers.tripo3d.ai/en/docs/migration-v2-to-v3) : nouvel hôte, un endpoint par capacité, fin de la v2.
- [Authentication](https://developers.tripo3d.ai/en/docs/authentication) : en-tête `Authorization: Bearer`.
- [Text to 3D Model](https://developers.tripo3d.ai/en/docs/generation-text-to-model/standard) : `POST /v3/generation/text-to-model`, avec les champs `prompt` (1 024 caractères au maximum), `model`, `negative_prompt`, `face_limit`, `texture`, `pbr`, `texture_quality`, `auto_size`, `smart_low_poly` et les graines.
- [File Upload](https://developers.tripo3d.ai/en/docs/files) : `POST /v3/files` en multipart, champ `file`, réponse `file_token` ; images JPEG ou PNG de 20 Mo au maximum. Le `file_token` est ensuite le champ `input` de `POST /v3/generation/image-to-model`.
- [Convert Format](https://developers.tripo3d.ai/en/docs/models-convert) : `POST /v3/models/convert`, formats cibles GLTF, USDZ, FBX, OBJ, STL et 3MF.
- [Billing](https://developers.tripo3d.ai/en/docs/billing) : `GET /v3/account/balance` → `balance`, `frozen` ; gel, débit et remboursement des crédits.
- [Rate Limits & Concurrency](https://developers.tripo3d.ai/en/docs/rate-limits) : HTTP 429 avec le code 1007 (débit) ou 2000 (tâches simultanées), en-tête `Retry-After`.
- [Errors](https://docs.tripo3d.ai/get-started/errors-and-error-handling.html) : 401/1002 authentification, 400/2008 politique de contenu, 403/2010 crédits insuffisants ; en-tête `X-Tripo-Trace-ID`.
- [Models & Versions](https://developers.tripo3d.ai/en/docs/models-and-versions) et [Tripo H3.1](https://developers.tripo3d.ai/en/models/v3-1) : `v3.1-20260211` est le modèle par défaut ; `seedream_v4` est le modèle d'image par défaut.
- [Multiview to 3D Model](https://developers.tripo3d.ai/en/docs/generation-multiview-to-model/p) et [Image to Multiview](https://developers.tripo3d.ai/en/docs/generation-image-to-multiview) : vues multiples.
- [Mesh Segmentation](https://developers.tripo3d.ai/en/docs/mesh-segment) et [Smart Segmentation](https://developers.tripo3d.ai/en/docs/mesh-smartsegment) : `POST /v3/mesh/segment` ; `POST /v3/mesh/smartsegment` avec `seg_type`, `input`, `granularity`, `hint` et `transform`.
- [Auto Rig](https://developers.tripo3d.ai/en/docs/animations-rig) et [Animation Retarget](https://developers.tripo3d.ai/en/docs/animations-retarget) : `out_format` glb ou fbx, `animation` ou `animations` (5 au maximum), sortie `output.model_urls`.
- [Batch Task Query](https://developers.tripo3d.ai/en/docs/task-batch-query) : `POST /v3/tasks/list`, réponse `tasks` et `missed`.
- [Webhooks](https://developers.tripo3d.ai/en/docs/webhooks) : configurés dans la console, avec un serveur HTTPS public. Non utilisés : le script suit les tâches en interrogeant l'API.
- Le SDK Python officiel [tripo3d 1.0.0](https://pypi.org/project/tripo3d/1.0.0/) a servi à recouper les chemins, les statuts de tâche (`queued`, `running`, `success`, `failed`, `cancelled`, `banned`, `expired`, `unknown`) et l'enveloppe `{code, data}`.

Ce qui reste incertain, et comment le script le gère :
- **Pages lues de façon indirecte.** Elles n'ont pas pu être ouvertes directement depuis l'environnement d'écriture (domaines bloqués). Leur contenu a été lu par extraits de recherche, puis recoupé avec le code source du SDK officiel et avec de vraies réponses de l'API sans clé ou avec une clé invalide.
- **Clé invalide.** Elle renvoie HTTP 401 avec `{"code": 2, "message": "Invalid API key"}` (observé le 21/10/2026), et non le code 1002 de la documentation. Le script traite donc tout 401 comme une clé refusée.
- **Hôte des fichiers et durée de vie des URL.** Ils ne sont pas documentés de façon fiable : 5 minutes selon le Quick Start, plus longtemps selon des projets tiers. Le script télécharge aussitôt la tâche réussie. `telecharger <task_id>` relit la tâche pour obtenir une URL neuve.
- **`face_limit` sans valeur.** La documentation dit que Tripo choisit une topologie adaptative ; une autre page parle de 10 000 faces. Mieux vaut toujours passer `--faces`.
- **Options de `texture_quality`.** `fast` et `extreme` dépendent de la version de texture (`--version-texture`). La documentation ne dit pas exactement lesquelles les acceptent : l'API renvoie l'erreur 1004 sinon.
- **Endpoints décrits seulement par le SDK.** Pour `image-to-image`, `edit-multiview`, `image-to-splat`, `image-to-depth`, `models/import`, `mesh/uv`, `mesh/complete` et `files/presign`, les champs viennent du SDK officiel. Les pages de doc correspondantes n'ont pas été trouvées ou lues en entier. La forme exacte de certaines sorties (format du splat, `model_urls` d'une animation) n'est pas documentée : le script télécharge toutes les URL qu'il trouve dans la sortie.
- **Champ `credits_consumed` de la tâche.** Il est recopié dans le `.tripo.json` s'il est présent ; sa présence n'est pas garantie par la documentation.
- **Appel réel.** Aucune de ces commandes n'a encore été validée par un appel réel payant : voir les PR qui les ont introduites.
