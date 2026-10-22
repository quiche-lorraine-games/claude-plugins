---
name: generer
description: Pilote toute l'API Tripo 3D (apiv3) et range les résultats dans un projet Godot. À charger quand on veut créer un prop ou un asset 3D plein et non interactif (caisse, rocher, mobilier, débris, objet de décor, arme posée) depuis un prompt, une image ou plusieurs vues ; retravailler un modèle existant ou importé (retexturer, réduire les faces, déplier les UV, convertir en FBX/OBJ/USDZ/STL, découper en pièces) ; produire des images de concept ou des vues multiples ; rigger et animer une créature de prototype ; puis contrôler le poids, le nombre de faces et l'échelle, importer dans Godot et vérifier l'import en headless. Couvre aussi la reprise d'une tâche Tripo, les crédits, la clé TRIPO_API_KEY et les erreurs (réseau bloqué, clé refusée, crédits épuisés, tâche échouée, délai dépassé). Ne convient pas aux pièces de kit modulaire qui doivent s'emboîter au millimètre, ni aux personnages à animer finement.
---

# Générer un modèle 3D avec Tripo

Ce skill pilote l'API REST de Tripo 3D (apiv3, `https://openapi.tripo3d.ai/v3`) avec le script `scripts/tripo.py`, rangé dans le même dossier que ce fichier. Le script n'utilise que la bibliothèque standard de Python 3. Il lit la clé dans `TRIPO_API_KEY`.

```bash
TRIPO="${CLAUDE_PLUGIN_ROOT}/skills/generer/scripts/tripo.py"
python3 "$TRIPO" --help
```

Le script a une sous-commande par capacité de l'API. Toutes sont décrites dans [commandes.md](commandes.md) : options, endpoints, enchaînements. Ce fichier-ci donne les règles communes et le déroulé.

Le projet prime : ses conventions (dossier, nommage, budget, style) l'emportent sur les valeurs par défaut de ce skill.

## Quand s'en servir

**Oui** : props et assets pleins, non interactifs, vus à distance de jeu.
- Objets de décor : caisses, tonneaux, rochers, mobilier, débris, végétation isolée, machines.
- Objets posés ou ramassables sans mécanisme : munitions, outils, nourriture, armes au sol.
- Premier jet pour valider une silhouette ou une échelle avant de commander un asset fait main.
- Retravailler un modèle Tripo ou importé : l'alléger, le retexturer, lui faire des UV, le convertir.
- Créatures et PNJ **de prototype**, riggés et animés avec les préréglages de Tripo.

**Non**, propose une autre voie (modélisation, kit existant, primitive) :
- pièces de kit modulaire (murs, sols, coins, portes de niveau) : elles doivent s'emboîter au millimètre sur une grille, ce que Tripo ne garantit pas ;
- objets à pièces mobiles ou articulées (porte qui s'ouvre, levier, véhicule) ;
- personnages et créatures du jeu final à animer finement, visages ;
- tout ce qui sert de collision précise ou de repère de gameplay ;
- logos, textes lisibles, marques.

## Avant tout : vérifier l'accès

```bash
python3 "$TRIPO" verifier
```

Le script vérifie que la clé est présente, sans l'afficher. Il teste ensuite l'accès réseau à l'API et à l'hôte des fichiers, puis lit le solde de crédits. S'il échoue, consulte la section « Erreurs » et arrête-toi là : ne contourne rien.

## Conventions du projet

Avant la première génération, cherche les conventions d'assets du projet :
1. `.claude/tripo.md`, le fichier dédié s'il existe ([gabarit](conventions-exemple.md)) ;
2. le `CLAUDE.md` du projet, puis le GDD (section art, assets ou budget technique) ;
3. les assets déjà présents : dossier, nommage, présence de `.tripo.json`.

Il te faut au minimum :
- le dossier de destination ;
- la règle de nommage ;
- la limite de faces ;
- le style visuel ;
- avec ou sans textures, et PBR ou non.

**S'il manque une de ces informations, demande-la à l'utilisateur au lieu de deviner.** Propose-lui ensuite d'écrire ses réponses dans `.claude/tripo.md` à partir du gabarit, pour ne pas reposer la question.

## Choisir la commande

| Besoin | Commande |
|---|---|
| Un prop depuis une description | `image-texte` (3 ou 4 variantes), choix de l'utilisateur, puis `image --low-poly` ; `texte` pour un premier jet |
| Un prop depuis un concept (une image) | `image` |
| Un prop fidèle à plusieurs vues | `multivue`, éventuellement après `image-multivue` |
| Une image de concept, ou la retoucher | `image-texte`, `image-image` |
| Modèle trop lourd | `decimer` (pas une nouvelle génération) |
| Changer matériaux ou couleurs | `retexturer` (pas une nouvelle génération) |
| UV propres pour texturer à la main | `uv` |
| Un autre format que GLB | `convertir` |
| Retravailler un modèle qui ne vient pas de Tripo | `importer`, puis la commande voulue |
| Séparer les pièces d'un modèle | `segmenter`, `segmenter-intelligent`, puis `completer` |
| Animer une créature de prototype | `riggable` (gratuit), `rigger`, `animer` |
| Carte de profondeur, splat | `profondeur`, `splat` |
| Endpoint récent que le script ne connaît pas | `brut` |

Retravailler coûte moins cher que régénérer. Corriger le poids ou la texture d'un modèle presque bon ne doit jamais passer par une nouvelle génération sans l'accord de l'utilisateur.

**Pour un objet, préfère image → modèle à texte → modèle.** `texte` donne des surfaces bosselées et ajoute des pièces malgré le prompt négatif. `image` donne des formes bien plus fidèles et plus nettes. La chaîne conseillée :
1. `image-texte` : 3 ou 4 variantes du concept, environ 5 crédits l'une (c'est une série : annonce le total et attends l'accord) ;
2. l'utilisateur choisit une image ;
3. `image <image choisie> --low-poly` (ou sans `--low-poly`, selon le style).

## Coût

Chaque génération consomme des crédits Tripo. Le compte est pré-payé : 1 crédit = 0,01 $.

Barème publié au 22/10/2026, à vérifier sur la [page de prix](https://developers.tripo3d.ai/en/pricing). Générations avec le modèle par défaut `v3.1-20260211` (H3.1) :

| Tâche | Sans texture | Texture standard | Texture detailed |
|---|---|---|---|
| `texte` | 10 | 20 | 30 |
| `image`, `multivue` | 20 | 30 | 40 |

Suppléments de génération :
- `--qualite-geometrie detailed` : +20 ;
- `--quad` : +5 ;
- `--low-poly` : +10 ;
- `--parties` : +20 ;
- texture 8K (`extreme`) : +20.

Les modèles P1 coûtent de 30 à 60 crédits, les modèles P2 de 100 à 130.

| Autres tâches | Crédits |
|---|---|
| `retexturer` | 10 (standard) à 30 (8K) |
| `convertir`, ou `--format fbx\|obj` | 5 (options par défaut) à 10 |
| `decimer` | 10 à 40 |
| `uv` | 20 |
| `segmenter` | 40 |
| `segmenter-intelligent` | 85 depuis une image, 55 depuis un modèle |
| `completer` | 50 (`ai_completion`), 30 (`quick_cap`) |
| `riggable` | gratuit |
| `rigger` | 25 |
| `animer` | 10 par animation |
| `image-texte`, `image-image` | 5 à 20 selon le modèle d'image |
| `image-multivue` | 10 |
| `editer-multivue` | 5 par vue modifiée |
| `importer`, `splat`, `profondeur`, `brut` | non publié : vérifie la page de prix, puis le champ `credits` du `.tripo.json` après coup |

`verifier`, `consommation`, `envoyer`, `statut`, `taches`, `telecharger` et `inspecter` sont gratuits. Une tâche échouée ou annulée n'est pas débitée. `consommation` liste les crédits réellement débités.

Règles :
- **Une génération demandée explicitement** par l'utilisateur : annonce son coût en une ligne (ex. « texte → modèle, texture standard : 20 crédits »), puis lance-la. Fais-le sauf si les conventions du projet exigent un accord à chaque fois.
- **Avant une série** (2 tâches payantes ou plus, y compris un enchaînement comme `rigger` puis `animer`), une option payante (`detailed`, `--low-poly`, `--quad`, `--parties`, conversion, modèle P1 ou P2) ou une variante non demandée : annonce combien de tâches tu vas lancer et le total estimé de crédits. **Attends l'accord.**
- **Ne relance jamais en boucle pour « améliorer ».** Après un résultat décevant, montre-le, dis ce qui ne va pas, propose un prompt corrigé et son coût, et laisse l'utilisateur décider.
- Pour montrer la requête sans rien dépenser, ajoute `--a-blanc`.

**Une tâche à la fois.** Le compte Tripo peut n'accepter qu'une tâche à la fois : lancées en parallèle, les tâches en trop sont refusées (HTTP 429, code 9). Lance les tâches d'une série l'une après l'autre, jamais en arrière-plan en parallèle. Sur un 429, le script attend et réessaie pendant environ 5 minutes avant d'abandonner ; un refus pour limite ne crée ni ne débite aucune tâche.

## Déroulé

### 1. Brief

Avant d'écrire le prompt, établis avec l'utilisateur, ou à partir du GDD :
- **quoi** : l'objet, son usage dans le jeu, la distance de vue (vue de dessus, premier plan, décor lointain) ;
- **taille réelle** en mètres ;
- **style** : celui du projet ;
- **budget** : faces, textures ou non ;
- **nom et dossier** de destination, selon les conventions.

Si le brief couvre plusieurs objets, c'est une série : applique la règle de coût.

### 2. Prompt

- Un seul objet par prompt, décrit concrètement : forme, matériaux, état (neuf, rouillé, cabossé), couleurs dominantes.
- Ajoute les mots de style imposés par les conventions du projet.
- Évite les décors, les socles, le texte et les personnages autour de l'objet. Mets-les plutôt dans `--negatif`.
- En anglais de préférence. 1 024 caractères au maximum, et 255 pour `--negatif` : le script refuse au-delà, avant tout envoi.
- Pour partir d'un concept existant, utilise `image` avec une image nette de l'objet seul, sur fond uni, en PNG, JPEG ou WebP de 20 Mo au maximum. Avec plusieurs vues du même objet, utilise `multivue`.

Montre le prompt à l'utilisateur avant une série.

### 3. Génération

```bash
python3 "$TRIPO" texte "weathered wooden supply crate, metal corners, stenciled paint" \
  --negatif "text, logo, pedestal" \
  --sortie assets/props/caisses/caisse_bois_01.glb --faces 3000

python3 "$TRIPO" image concepts/caisse.png --sortie assets/props/caisses/caisse_bois_02.glb --faces 3000
```

Le script crée la tâche, suit son avancement (intervalle croissant de 3 à 15 s) et télécharge le modèle, avec ses autres sorties (aperçu `caisse_bois_01_rendered_image.*`). Il écrit ensuite la fiche `caisse_bois_01.tripo.json` à côté du fichier, puis affiche le contrôle du résultat. Il affiche aussi le `task_id`, à réutiliser pour retravailler le modèle (voir [commandes.md](commandes.md)).

Options principales (liste complète dans [commandes.md](commandes.md)) :

| Option | Effet |
|---|---|
| `--sortie` | fichier à écrire (obligatoire) ; refuse d'écraser sans `--ecraser` |
| `--format glb\|fbx\|obj` | `glb` par défaut, à garder pour Godot ; `fbx` et `obj` passent par une conversion payante |
| `--faces N` | limite de faces (`face_limit`) ; sans elle, Tripo choisit. Ce sont des faces, souvent des quads, pas des triangles : pour un budget en triangles, passe environ la moitié |
| `--sans-texture` | géométrie seule, moins chère |
| `--sans-pbr` | texture sans cartes PBR |
| `--qualite-texture detailed` | texture plus fine, plus chère |
| `--taille-auto` | `auto_size` ; sans effet constaté sur l'échelle (voir « Contrôle du résultat ») |
| `--low-poly` | topologie low-poly (`smart_low_poly`), avec supplément |
| `--modele` | version du modèle Tripo, `v3.1-20260211` par défaut |
| `--graine N` | graine, pour refaire un résultat proche |
| `--param CLE=VALEUR` | champ de l'API sans option dédiée, envoyé tel quel |
| `--delai S` | attente maximale, 600 s par défaut |
| `--sans-attendre` | crée la tâche et rend la main ; reprise avec `telecharger` |
| `--a-blanc` | affiche la requête sans l'envoyer |

Pour reprendre une tâche :

```bash
python3 "$TRIPO" statut <task_id>
python3 "$TRIPO" telecharger <task_id> --sortie assets/props/caisses/caisse_bois_01.glb
```

`telecharger` ne relance pas de génération et ne coûte rien. Si la tâche est encore en cours, il l'attend. Il ne convertit pas : pour un FBX ou un OBJ, passe-lui le `task_id` de la conversion (champ `conversion` du `.tripo.json`), avec une `--sortie` en `.fbx` ou en `.obj`.

### 4. Contrôle du résultat

Le script affiche, et range dans le champ `controle` du `.tripo.json`, les valeurs suivantes :
- poids du fichier ;
- nombre de triangles et de sommets ;
- dimensions en mètres (x × y × z) ;
- textures et leur résolution ;
- extensions glTF requises.

Si Tripo a fourni un aperçu (`<nom>_rendered_image.*`), regarde-le avant de présenter le résultat.

Pour un GLB déjà présent :

```bash
python3 "$TRIPO" inspecter assets/props/caisses/caisse_bois_01.glb
```

Compare ces valeurs aux conventions et au brief :
- **faces** : `--faces` compte des faces, souvent des quads, et le contrôle compte des triangles. Avec `--low-poly`, on a mesuré 1 641 triangles pour `--faces 1500`, 3 614 et 2 854 pour 2 000, 5 473 pour 3 600 : jusqu'à 2 triangles par face demandée. Pour un budget de N triangles, passe environ N/2 à `--faces`. Au-delà de 2 triangles par face, le script avertit : signale-le, sans relancer d'office.
- **poids** : au-dessus du budget, ce sont souvent les textures. Propose `--sans-pbr`, une texture standard, `decimer` pour la géométrie, ou une réduction dans Godot.
- **échelle** : Tripo rend l'objet dans une boîte d'environ 1 m. `--taille-auto` (`auto_size`) n'a changé l'échelle d'aucun des modèles essayés (une dizaine, octobre 2026) : ne compte pas dessus. Corrige l'échelle à l'import dans Godot (option `nodes/root_scale` du `.import`, ou échelle de la scène qui l'instancie, selon les conventions), à partir de la taille réelle du brief. Ne régénère pas pour une question d'échelle.
- **orientation et pivot** : vérifie que l'avant et le sol sont corrects une fois dans Godot. Les modèles de Tripo sortent debout sur +Y, l'avant vers +X.
- **low poly en facettes** : un GLB low poly de Tripo a un jeu de sommets par facette, pour garder des arêtes vives. Godot l'affiche correctement. Dans Blender, le modèle arrive en centaines de morceaux : coche *Merge Vertices* à l'import glTF, ou sélectionne tout en mode édition puis *Mesh > Clean Up > Merge by Distance*. Ce n'est pas un défaut à corriger dans le fichier : glTF stocke une normale par sommet, donc un GLB ne peut pas être à la fois soudé et en facettes, et Blender redécoupe le maillage à l'export.

Décris le résultat à l'utilisateur en une ou deux lignes (valeurs et écarts). Ne présente jamais un asset comme validé sans ce contrôle.

### Cas du rig : l'orientation compte

`riggable` et `rigger` ne reconnaissent un squelette que sur un modèle debout sur +Y, l'avant vers +X, comme Tripo rend ses propres modèles. Le même personnage tourné de 90° autour de Y (avant vers −Z, après un passage par Godot ou Blender) est jugé non riggable, quelle que soit son échelle.
- Un `task_id` Tripo est déjà dans la bonne orientation.
- Pour un GLB local qui regarde ailleurs, ajoute `--avant -z` (ou `+z`, `-x`) à `riggable` et à `rigger` : le script tourne une copie du modèle vers +X avant l'envoi, sans toucher au fichier d'origine, et le note dans la fiche.
- Le GLB riggé sort dans l'orientation de Tripo (avant vers +X). Le script dit de combien tourner son nœud autour de Y dans Godot pour retrouver l'orientation d'origine : +90° pour un avant −Z, −90° pour +Z, 180° pour −X.

### 5. Import dans Godot

- Le fichier doit être sous la racine du projet Godot (celle qui contient `project.godot`), dans le dossier prévu par les conventions. Passe directement le bon chemin à `--sortie`.
- Garde le `.tripo.json` à côté du modèle et commite les deux, avec le `.glb.import` que Godot va créer. Ne commite jamais `.godot/`.
- Si le projet utilise Git LFS pour les `.glb`, vérifie que le fichier est bien suivi par LFS (`git lfs status`).
- Les réglages d'import propres au projet (collisions, LOD, matériaux, échelle) se règlent dans le `.glb.import` ou par un script d'import du projet, selon ses conventions.

### 6. Vérification de l'import en headless

Lance l'import sans éditeur graphique. Le binaire vient des conventions du projet : `godot`, `godot4` ou la variable `$GODOT`.

```bash
godot --headless --path <racine_du_projet> --import 2>&1 | tee /tmp/import-godot.log
```

`--import` existe depuis Godot 4.3. Sur une version plus ancienne : `godot --headless --path <racine> --editor --quit`.

Puis vérifie :
1. `grep -n "ERROR" /tmp/import-godot.log` ne cite pas le nouveau fichier ;
2. le fichier `<modèle>.glb.import` existe et ne contient pas `valid=false` ;
3. le fichier importé existe dans `.godot/imported/` (`ls .godot/imported/ | grep <nom du modèle>`).

Si Godot n'est pas installé dans l'environnement, dis-le clairement : le modèle est livré, mais l'import n'a pas été vérifié. Ne le présente pas comme validé.

## Fiche `.tripo.json`

Chaque résultat a une fiche, à côté de lui (`caisse_bois_01.glb` → `caisse_bois_01.tripo.json`). Elle permet de retrouver et de refaire l'asset. Elle contient :
- l'opération (endpoint) et le prompt ;
- les entrées : fichiers (chemin relatif au dossier de la fiche, taille, empreinte SHA-256), URL ou `task_id` des tâches précédentes, ce qui retrace la chaîne de fabrication. Un fichier pris hors du projet (dossier temporaire, par exemple) ne garde que son nom et son empreinte ;
- le `task_id` ;
- les paramètres envoyés ;
- la version du modèle Tripo ;
- la date ;
- les crédits débités, si l'API les donne ;
- la liste des fichiers écrits, relatifs au dossier de la fiche, et l'hôte d'où ils viennent ;
- le contrôle.

Ne la modifie pas à la main. Pour refaire un asset, relis-la et relance avec les mêmes prompt, paramètres et graine, après accord sur le coût.

## Erreurs et ce qu'il faut dire

Le script écrit sur la sortie d'erreur un message court qui donne l'action à faire. Il sort avec un code distinct selon le cas. Transmets l'essentiel à l'utilisateur et arrête-toi : ne contourne jamais une erreur de réseau ou de clé.

| Code | Cas | Ce que tu dis à l'utilisateur |
|---|---|---|
| 0 | succès | résumé du contrôle et chemin du fichier |
| 1 | erreur API inattendue, téléchargement refusé ou coupé | le message du script. Si la tâche a réussi, le script a déjà réessayé 4 fois ; il affiche son `task_id` et la commande `telecharger` exacte, gratuite, à relancer après une pause. Ne relance jamais la génération |
| 2 | argument invalide | corrige l'appel toi-même, sans rien demander |
| 3 | clé absente ou refusée (401) | « La clé Tripo manque ou est refusée. Ajoute ou corrige `TRIPO_API_KEY` dans les secrets de l'environnement, puis ouvre une nouvelle session. » Ne demande jamais la clé dans le chat. |
| 4 | crédits épuisés (code 2010) | « Le compte Tripo n'a plus assez de crédits ; rien n'a été débité. Recharge-le dans la console Tripo. » |
| 5 | domaine bloqué par la politique réseau (403 du proxy) ou injoignable | « Le domaine `<hôte>` est bloqué. Ajoute-le aux domaines autorisés de l'environnement. » Donne l'hôte exact cité par le script. Si la tâche avait réussi, donne aussi la commande `telecharger` qu'il affiche. Une connexion coupée en cours de transfert n'est pas un blocage : le script la réessaie |
| 6 | tâche échouée, annulée ou expirée | « La génération a échoué ; Tripo ne débite pas les tâches échouées. » Propose un prompt ou une image modifiés, avec leur coût, sans relancer d'office. |
| 7 | délai dépassé | « La tâche `<task_id>` tourne encore côté Tripo. » Reprends plus tard avec `telecharger <task_id>` : ne relance pas de génération, ce qui paierait deux fois. |
| 8 | contenu refusé par la modération (code 2008, statut `banned`) | dis-le, et propose une reformulation |
| 9 | trop de tâches simultanées (429), malgré environ 5 minutes de nouveaux essais | rien n'a été créé ni débité. Attends la fin des tâches en cours, puis relance une seule tâche à la fois |

## Sécurité de la clé

- Ne demande **jamais** la clé dans le chat. Si l'utilisateur la colle quand même, ne la réutilise pas, ne la recopie nulle part, et conseille-lui de la révoquer dans la console Tripo et d'en créer une autre, à mettre en secret de l'environnement.
- Ne l'affiche pas : pas de `echo $TRIPO_API_KEY`, pas de `env` ni de `printenv` non filtrés, pas de `set -x` autour des appels.
- Ne la mets dans aucun fichier, log, commit, `.tripo.json` ou message de PR. Le script masque la clé dans tout ce qu'il écrit et ne l'envoie qu'à l'API, jamais à l'hôte des fichiers.
- Pour tester sa présence : `python3 "$TRIPO" verifier`, jamais un affichage de la variable.
