# Référence des commandes de `tripo.py`

Toutes les capacités de l'apiv3 de Tripo, une sous-commande par endpoint. Ce fichier complète [SKILL.md](SKILL.md) : les règles de coût, de conventions et de sécurité y restent valables pour chaque commande. `python3 "$TRIPO" <commande> --help` donne toutes les options.

## Entrées, sorties et options communes

**Entrées.** Partout où une commande attend une image ou un modèle, on peut passer :
- un **fichier local** : il est envoyé d'abord. Jusqu'à 50 Mo par `POST /v3/files`, au-delà par une URL pré-signée (`POST /v3/files/presign`), dans la limite de 150 Mo pour un modèle. Images : PNG, JPEG ou WebP, 20 Mo au maximum. Modèles : GLB, GLTF, FBX, OBJ ou STL ;
- une **URL publique** ;
- un **`file_token`** obtenu avec `envoyer` (il commence par `file_`) ;
- le **`task_id`** d'une tâche précédente, pour enchaîner sans retélécharger.

**Sorties.** `--sortie` désigne le fichier principal. Les autres fichiers de la tâche sont écrits à côté, sous la forme `<nom>_<sortie>.<ext>`. Ce sont l'aperçu `_rendered_image`, le rendu UV `_uv_render`, les vues `_front_view`, `_left_view`, etc. La fiche `.tripo.json` les liste tous dans `sorties`.

**Options de toutes les commandes qui créent une tâche** :

| Option | Effet |
|---|---|
| `--sortie F` | fichier principal (obligatoire) ; refuse d'écraser sans `--ecraser` |
| `--delai S`, `--intervalle S` | attente maximale (600 s) et premier intervalle de suivi (3 s) |
| `--sans-attendre` | crée la tâche et rend la main ; reprise avec `telecharger` |
| `--a-blanc` | affiche la requête sans l'envoyer : ni clé, ni réseau, ni crédit |
| `--param CLE=VALEUR` | ajoute un champ de l'API tel quel (valeur JSON, sinon texte) ; répétable. Il ne peut pas remplacer un champ déjà fixé par une option |

## Compte

| Commande | Endpoint | Coût |
|---|---|---|
| `verifier` | test des hôtes, `GET /v3/account/balance` | gratuit |
| `consommation [--limite N] [--decalage N]` | `GET /v3/account/usage` | gratuit |
| `envoyer FICHIER` | `POST /v3/files` (ou `files/presign`) ; affiche le `file_token` | gratuit |

## Générer un modèle

| Commande | Endpoint |
|---|---|
| `texte "prompt" [--negatif "..."]` | `POST /v3/generation/text-to-model` |
| `image ENTREE [--autofix]` | `POST /v3/generation/image-to-model` |
| `multivue --face F [--gauche G] [--dos D] [--droite R]` ou `multivue --depuis-tache ID` | `POST /v3/generation/multiview-to-model` |

Options communes aux trois :
- `--modele` : `v3.1-20260211` par défaut. Autres valeurs : `v3.0-20250812`, `v2.5-20250123`, `P1-20260311` (low-poly), `P2-20260801` (aperçu, cher) ;
- `--faces N` ;
- `--sans-texture` et `--sans-pbr` ;
- `--qualite-texture standard|detailed|fast|extreme` (`fast` et `extreme` exigent `--version-texture v3.5-20260815`) et `--version-texture` ;
- `--qualite-geometrie standard|detailed` ;
- `--taille-auto` ;
- `--low-poly` ;
- `--quad`, qui produit un FBX : à combiner avec `--format fbx` ;
- `--parties`, qui exige `--sans-texture`, sans `--quad` ni `--low-poly` ;
- `--graine N` ;
- `--format glb|fbx|obj`, où `fbx` et `obj` ajoutent une conversion payante, sauf avec `--quad`.

Pour `image` et `multivue` seulement :
- `--orientation default|align_image` ;
- `--alignement-texture original_image|geometry`.

Pour `multivue`, la vue de face est obligatoire et les autres sont facultatives. `--depuis-tache` prend le `task_id` d'un `image-multivue` ou d'un `editer-multivue`.

## Images

| Commande | Endpoint | Sortie |
|---|---|---|
| `image-texte "prompt" [--negatif] [--modele seedream_v4\|seedream_v5…] [--taille 1024x1024] [--ratio 1:1] [--format-image png]` | `POST /v3/generation/text-to-image` | l'image, dans `--sortie` |
| `image-image ENTREE… --prompt "…" [--modele] [--gabarit t-pose] [--t-pose] [--croquis]` | `POST /v3/generation/image-to-image` | l'image ; plusieurs entrées = plusieurs références |
| `image-multivue ENTREE` | `POST /v3/generation/image-to-multiview` | 4 vues : `<nom>_front_view.png`, etc. |
| `editer-multivue ID --vue "front=consigne" [--vue "back=…"]` | `POST /v3/generation/edit-multiview` | 4 vues |
| `splat ENTREE [--graine N]` | `POST /v3/generation/image-to-splat` | splat gaussien (format choisi par Tripo) |
| `profondeur ENTREE [--type gray\|color] [--resolution 126–2016]` | `POST /v3/generation/image-to-depth` | carte de profondeur |

## Retravailler un modèle

L'entrée est en général le `task_id` d'une tâche qui a produit un modèle. Ce peut aussi être un fichier, une URL ou un `file_token` : un modèle externe passe d'abord par `importer`.

| Commande | Endpoint | Options principales |
|---|---|---|
| `retexturer ENTREE` | `POST /v3/models/texture` | `--prompt-texture "…"`, `--image-texture`, `--image-style`, `--modele v2.5-20250123\|v3.0-20250812\|v3.5-20260815`, `--qualite-texture`, `--alignement-texture`, `--sans-pbr`, `--pieces a,b`, `--sans-cuisson`, `--graine` |
| `convertir ID --format gltf\|usdz\|fbx\|obj\|stl\|3mf` | `POST /v3/models/convert` | `--faces`, `--quad`, `--taille-texture 2048`, `--format-texture JPEG`, `--echelle`, `--pivot-bas`, `--aplatir-base`, `--orientation-export`, `--preset-fbx`, `--sur-place`, `--sans-cuisson`, `--sans-animation` |
| `importer ENTREE` | `POST /v3/models/import` | aucune ; donne un `task_id` à réutiliser, avec un fichier s'il y en a un |
| `decimer ENTREE` | `POST /v3/mesh/decimate` | `--faces N`, `--modele v1.0\|v2.0\|v3.0`, `--quad`, `--uv-intelligentes` (exige v3.0), `--pieces`, `--sans-cuisson` |
| `uv ENTREE` | `POST /v3/mesh/uv` | `--modele` ; écrit aussi `<nom>_uv_render.png` |
| `segmenter ENTREE` | `POST /v3/mesh/segment` | `--modele v1.0-20250506\|v2.0-20260430` ; v2.0 seulement : `--granularite`, `--image-ref`, `--par-connexite` |
| `segmenter-intelligent ENTREE` | `POST /v3/mesh/smartsegment` | `--type image\|model` (déduit de l'extension), `--granularite coarse\|medium\|fine`, `--indice "…"`, `--transformation` (16 nombres, identité par défaut pour un GLB) ; l'entrée est un fichier, une URL ou un `file_token`, jamais un `task_id` |
| `completer ID_SEGMENTATION` | `POST /v3/mesh/complete` | `--mode ai_completion\|quick_cap`, `--pieces`, `--modele` |

## Animer

| Commande | Endpoint | Options |
|---|---|---|
| `riggable ENTREE` | `POST /v3/animations/rig-check` | gratuit ; dit si le modèle peut être riggé et quel squelette Tripo détecte |
| `rigger ENTREE` | `POST /v3/animations/rig` | `--type biped\|quadruped\|hexapod\|octopod\|avian\|serpentine\|aquatic\|others`, `--spec tripo\|mixamo\|actorcore\|unity\|unreal\|vrm` (les trois dernières exigent `--modele v2.5-20260210` ou `v3.0-20260909`), `--format glb\|fbx` |
| `animer ID_RIG --animation walk [--animation run …]` | `POST /v3/animations/retarget` | 1 à 5 préréglages (`idle`, `walk`, `run`, `jump`, `climb`, `dive`, `slash`, `shoot`, `hurt`, `fall`, `turn`, `quadruped:walk`…), `--format glb\|fbx`, `--avec-geometrie` ou `--sans-geometrie`, `--sur-place`, `--sans-cuisson` |

Avec plusieurs animations, chaque fichier est écrit à côté de `--sortie`. Il est nommé d'après l'animation si Tripo la donne, sinon numéroté dans l'ordre de l'API (`<nom>_model_1.glb`, `<nom>_model_2.glb`). La fiche `.tripo.json` liste les animations demandées.

## Tâches

| Commande | Endpoint | Effet |
|---|---|---|
| `statut ID` | `GET /v3/tasks/{id}` | statut, progression et noms des sorties |
| `taches ID…` | `POST /v3/tasks/list` | statut de plusieurs tâches en une requête |
| `telecharger ID --sortie F` | `GET /v3/tasks/{id}` | attend si besoin, puis télécharge toutes les sorties ; gratuit, ne convertit pas |
| `brut /v3/... --corps '{…}' [--nature modele\|image\|multivue\|profondeur\|splat]` | n'importe quel endpoint de création | pour un endpoint que le script ne connaît pas encore ; corps envoyé tel quel, ou lu depuis `@fichier.json` |
| `inspecter FICHIER.glb` | local | poids, triangles, dimensions, textures |

## Enchaînements utiles

Chaque commande affiche le `task_id` de sa tâche, et le `.tripo.json` le garde. On le passe à l'étape suivante :

```bash
# Concept → vues → modèle
python3 "$TRIPO" image-texte "rusty fuel barrel, game asset, neutral background" --sortie concepts/baril.png
python3 "$TRIPO" image-multivue concepts/baril.png --sortie concepts/baril_vues.png
python3 "$TRIPO" multivue --depuis-tache <id image-multivue> --sortie assets/props/baril_01.glb --faces 3000

# Modèle trop lourd ou mal texturé : retravailler sans régénérer
python3 "$TRIPO" decimer <id modèle> --faces 1500 --sortie assets/props/baril_01_lod1.glb
python3 "$TRIPO" retexturer <id modèle> --prompt-texture "blue paint, heavy rust" --sortie assets/props/baril_02.glb

# Créature de prototype animée
python3 "$TRIPO" riggable <id modèle>
python3 "$TRIPO" rigger <id modèle> --type quadruped --sortie assets/creatures/chien_rig.glb
python3 "$TRIPO" animer <id rig> --animation quadruped:walk --sortie assets/creatures/chien_marche.glb
```

## Non couvert

**Les webhooks.** Ils se configurent dans la console Tripo et exigent un serveur HTTPS public pour recevoir les événements. Une session d'agent n'en a pas : le script suit donc les tâches en interrogeant l'API.
