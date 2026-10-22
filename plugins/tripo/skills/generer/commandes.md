# Référence des commandes de `tripo.py`

Toutes les capacités de l'apiv3 de Tripo, une sous-commande par endpoint. Ce fichier complète [SKILL.md](SKILL.md) : les règles de coût, de conventions et de sécurité y restent valables pour chaque commande. `python3 "$TRIPO" <commande> --help` donne toutes les options.

## Entrées, sorties et options communes

**Entrées.** Partout où une commande attend une image ou un modèle, on peut passer :
- un **fichier local** : il est envoyé d'abord. Jusqu'à 50 Mo par `POST /v3/files`, au-delà par une URL pré-signée (`POST /v3/files/presign`), dans la limite de 150 Mo pour un modèle. Images : PNG, JPEG ou WebP, 20 Mo au maximum. Modèles : GLB, GLTF, FBX, OBJ ou STL ;
- une **URL publique** ;
- un **`file_token`** obtenu avec `envoyer` (il commence par `file_`) ;
- le **`task_id`** d'une tâche précédente, pour enchaîner sans retélécharger.

**Sorties.** `--sortie` désigne le fichier principal. Les autres fichiers de la tâche sont écrits à côté, sous la forme `<nom>_<sortie>.<ext>`. Ce sont l'aperçu `_rendered_image`, le rendu UV `_uv_render`, les vues `_front_view`, `_left_view`, etc. La fiche `.tripo.json` les liste tous dans `sorties`, par des chemins relatifs à son dossier.

**Téléchargement.** Une connexion coupée en cours de transfert (`Connection reset by peer`, réponse tronquée, erreur 5xx de l'hôte des fichiers) est réessayée 4 fois, après 2, 4 puis 8 s. Un hôte refusé par le proxy (403, code 5) ne l'est pas. Si le téléchargement échoue quand même, la tâche a réussi et elle est payée : le script écrit la fiche (`"etat": "a_telecharger"`) et affiche la commande `telecharger <task_id> --sortie …` exacte, gratuite, à relancer.

**Tâches simultanées.** Le compte peut n'accepter qu'une tâche à la fois. Une création refusée pour cette raison (HTTP 429) ne crée ni ne débite rien : le script attend et réessaie pendant environ 5 minutes, puis sort en code 9. Lance les tâches l'une après l'autre.

**Options de toutes les commandes qui créent une tâche**, sauf `riggable`, qui n'écrit aucun fichier et n'accepte que `--delai`, `--intervalle`, `--a-blanc` et `--avant` :

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
| `texte "prompt" [--negatif "..."]` | `POST /v3/generation/text-to-model` ; prompt de 1 024 caractères au maximum, `--negatif` de 255 |
| `image ENTREE [--autofix]` | `POST /v3/generation/image-to-model` |
| `multivue --face F [--gauche G] [--dos D] [--droite R]` ou `multivue --depuis-tache ID` | `POST /v3/generation/multiview-to-model` |

Options communes aux trois :
- `--modele` : `v3.1-20260211` par défaut. Autres valeurs : `v3.0-20250812`, `v2.5-20250123`, `P1-20260311` (low-poly), `P2-20260801` (aperçu, cher) ;
- `--faces N` : un nombre de **faces**, souvent des quads, pas de triangles. Avec `--low-poly`, on a mesuré 1 641 triangles pour 1 500 faces, 3 614 et 2 854 pour 2 000, 5 473 pour 3 600. Pour un budget en triangles, passe environ la moitié ;
- `--sans-texture` et `--sans-pbr` ;
- `--qualite-texture standard|detailed|fast|extreme` (`fast` et `extreme` exigent `--version-texture v3.5-20260815`) et `--version-texture` ;
- `--qualite-geometrie standard|detailed` ;
- `--taille-auto` (`auto_size`) : n'a changé l'échelle d'aucun modèle essayé, qui sortent tous dans une boîte d'environ 1 m. Mets à l'échelle à l'import dans Godot ;
- `--low-poly` ;
- `--quad`, qui produit un FBX : à combiner avec `--format fbx` ;
- `--parties`, qui exige `--sans-texture`, sans `--quad` ni `--low-poly` ;
- `--graine N` ;
- `--format glb|fbx|obj`, où `fbx` et `obj` ajoutent une conversion payante, sauf avec `--quad`.

Pour `image` et `multivue` seulement :
- `--orientation default|align_image` ;
- `--alignement-texture original_image|geometry`.

Pour `multivue`, la vue de face est obligatoire et les autres sont facultatives. `--depuis-tache` prend le `task_id` d'un `image-multivue` ou d'un `editer-multivue`.

Pour un objet, `image` donne des formes bien plus fidèles et nettes que `texte`, qui produit des surfaces bosselées et ajoute des pièces malgré `--negatif`. Voir la chaîne conseillée dans « Enchaînements utiles ».

Les GLB `--low-poly` ont un jeu de sommets par facette (arêtes vives). Dans Blender, ils arrivent en centaines de morceaux : *Merge Vertices* à l'import, ou *Merge by Distance* en mode édition. glTF stocke une normale par sommet : un GLB ne peut pas être à la fois soudé et en facettes.

## Images

| Commande | Endpoint | Sortie |
|---|---|---|
| `image-texte "prompt" [--negatif] [--modele seedream_v4\|seedream_v5\|chat_image\|<banana>] [--taille 2048x2048] [--ratio 1:1] [--format-image png]` | `POST /v3/generation/text-to-image` | l'image, dans `--sortie` ; voir les combinaisons ci-dessous |
| `image-image ENTREE… --prompt "…" [--modele] [--gabarit t-pose] [--t-pose] [--croquis]` | `POST /v3/generation/image-to-image` | l'image ; plusieurs entrées = plusieurs références |
| `image-multivue ENTREE` | `POST /v3/generation/image-to-multiview` | 4 vues : `<nom>_front_view.png`, etc. |
| `editer-multivue ID --vue "front=consigne" [--vue "back=…"]` | `POST /v3/generation/edit-multiview` | 4 vues |
| `splat ENTREE [--graine N]` | `POST /v3/generation/image-to-splat` | splat gaussien (format choisi par Tripo) |
| `profondeur ENTREE [--type gray\|color] [--resolution 126–2016]` | `POST /v3/generation/image-to-depth` | carte de profondeur |

`--taille` et `--ratio` dépendent du modèle d'image. Le script refuse localement les combinaisons que l'API rejette :

| Modèle (`--modele`) | `--taille` | `--ratio` |
|---|---|---|
| seedream (défaut de Tripo : sans `--modele`, ou `seedream_v4`, `seedream_v5`…) | de 2560×1440 à 4096×4096 pixels au total : `2048x2048`, `2560x1440`, `1440x2560` ; `1024x1024` est refusé | refusé |
| `chat_image` | accepté | refusé |
| modèles banana | non vérifié | accepté (`1:1`, `16:9`…) |

Sans `--taille` ni `--ratio`, Tripo choisit. Le minimum de seedream vient des bornes publiées pour Seedream 4.5 et 5 ; s'il change, `--param size=LARGEURxHAUTEUR` envoie une taille sans contrôle local. `--negatif` : 255 caractères au maximum.

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
| `riggable ENTREE` | `POST /v3/animations/rig-check` | gratuit, sans `--sortie` ni fichier écrit ; dit si le modèle peut être riggé et quel squelette Tripo détecte. `--avant`, `--a-blanc` |
| `rigger ENTREE` | `POST /v3/animations/rig` | `--modele v1.0-20240301\|v2.5-20260210\|v3.0-20260909` (`v3.0-20260909` par défaut), `--type biped\|quadruped\|hexapod\|octopod\|avian\|serpentine\|aquatic\|others`, `--spec tripo\|mixamo\|actorcore\|unity\|unreal\|vrm` (les trois dernières refusent `v1.0-20240301`), `--avant`, `--format glb\|fbx` |
| `animer ID_RIG --animation walk [--animation run …]` | `POST /v3/animations/retarget` | 1 à 5 préréglages (`idle`, `walk`, `run`, `jump`, `climb`, `dive`, `slash`, `shoot`, `hurt`, `fall`, `turn`, `quadruped:walk`…), `--format glb\|fbx`, `--avec-geometrie` ou `--sans-geometrie`, `--sur-place`, `--sans-cuisson` |

`rigger` envoie toujours un modèle de rig : sans ce champ, l'API a pris `v2.5-20250123` (constaté le 22/10/2026), une valeur qu'elle refuse elle-même (HTTP 400, code 1004).

**Orientation.** Tripo ne reconnaît un squelette que sur un modèle debout sur +Y, l'avant vers +X, l'orientation de ses propres modèles. Tourné de 90° autour de Y (avant vers −Z), le même maillage est jugé non riggable, quelle que soit son échelle. Pour un GLB local, `--avant -z|+z|-x` (sur `riggable` et `rigger`) tourne une copie du modèle vers +X avant l'envoi. Le fichier d'origine n'est pas modifié, et la fiche note la réorientation. Cela ne marche pas pour un GLB compressé (Draco, meshopt), déjà riggé, avec des morph targets ou en miroir : tourne-le alors dans un éditeur 3D. Un `task_id` Tripo est déjà orienté vers +X. Le GLB riggé sort avant vers +X : dans Godot, tourne son nœud autour de Y de +90° (avant d'origine −Z), −90° (+Z) ou 180° (−X).

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
# Objet : variantes d'image, choix de l'utilisateur, puis image → modèle (le plus fidèle)
python3 "$TRIPO" image-texte "rusty fuel barrel, game asset, plain background" --taille 2048x2048 --sortie concepts/baril_a.png
python3 "$TRIPO" image-texte "rusty fuel barrel, game asset, plain background" --taille 2048x2048 --sortie concepts/baril_b.png
python3 "$TRIPO" image concepts/baril_b.png --low-poly --faces 1500 --sortie assets/props/baril_01.glb

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
# GLB local qui regarde vers -Z (exporté de Godot ou de Blender)
python3 "$TRIPO" riggable assets/persos/garde.glb --avant -z
python3 "$TRIPO" rigger assets/persos/garde.glb --avant -z --sortie assets/persos/garde_rig.glb
python3 "$TRIPO" animer <id rig> --animation quadruped:walk --sortie assets/creatures/chien_marche.glb
```

## Non couvert

**Les webhooks.** Ils se configurent dans la console Tripo et exigent un serveur HTTPS public pour recevoir les événements. Une session d'agent n'en a pas : le script suit donc les tâches en interrogeant l'API.
