---
name: generer
description: Génère des modèles 3D avec l'API Tripo 3D (apiv3) puis les range dans un projet Godot. À charger quand on veut créer un prop ou un asset 3D plein et non interactif (caisse, rocher, mobilier, débris, objet de décor, arme posée) depuis un prompt ou une image, le télécharger en GLB, contrôler son poids, son nombre de faces et son échelle, l'importer dans Godot et vérifier l'import en headless. Couvre aussi la reprise d'une tâche Tripo (statut, téléchargement), les crédits, la clé TRIPO_API_KEY et les erreurs (réseau bloqué, clé refusée, crédits épuisés, tâche échouée, délai dépassé). Ne convient pas aux pièces de kit modulaire qui doivent s'emboîter au millimètre, ni aux personnages à animer finement.
---

# Générer un modèle 3D avec Tripo

Ce skill pilote l'API REST de Tripo 3D (apiv3, `https://openapi.tripo3d.ai/v3`) avec le script `scripts/tripo.py`, rangé dans le même dossier que ce fichier. Le script n'utilise que la bibliothèque standard de Python 3. Il lit la clé dans `TRIPO_API_KEY`.

```bash
TRIPO="${CLAUDE_PLUGIN_ROOT}/skills/generer/scripts/tripo.py"
python3 "$TRIPO" --help
```

Le projet prime : ses conventions (dossier, nommage, budget, style) l'emportent sur les valeurs par défaut de ce skill.

## Quand s'en servir

**Oui** : props et assets pleins, non interactifs, vus à distance de jeu.
- Objets de décor : caisses, tonneaux, rochers, mobilier, débris, végétation isolée, machines.
- Objets posés ou ramassables sans mécanisme : munitions, outils, nourriture, armes au sol.
- Premier jet pour valider une silhouette ou une échelle avant de commander un asset fait main.

**Non**, propose une autre voie (modélisation, kit existant, primitive) :
- pièces de kit modulaire (murs, sols, coins, portes de niveau) : elles doivent s'emboîter au millimètre sur une grille, ce que Tripo ne garantit pas ;
- objets à pièces mobiles ou articulées (porte qui s'ouvre, levier, véhicule) ;
- personnages et créatures à animer finement, visages ;
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

## Coût

Chaque génération consomme des crédits Tripo. Le compte est pré-payé : 1 crédit = 0,01 $.

Barème publié pour le modèle par défaut `v3.1-20260211` (H3.1), à vérifier sur la [page de prix](https://developers.tripo3d.ai/en/pricing) :

| Tâche | Sans texture | Texture standard | Texture detailed |
|---|---|---|---|
| Texte → modèle (`texte`) | 10 | 20 | 30 |
| Image → modèle (`image`) | 20 | 30 | 40 |

Suppléments :
- `--low-poly` : +10 ;
- conversion `--format fbx|obj` : 5 à 10 par conversion ;
- modèles P1 : 30 à 60 ; modèles P2 : 100 à 130.

Une tâche échouée ou annulée n'est pas débitée.

Règles :
- **Une génération demandée explicitement** par l'utilisateur : annonce son coût en une ligne (ex. « texte → modèle, texture standard : 20 crédits »), puis lance-la. Fais-le sauf si les conventions du projet exigent un accord à chaque fois.
- **Avant une série** (2 générations ou plus), une option payante (`detailed`, `--low-poly`, conversion, modèle P1 ou P2) ou une variante non demandée : annonce combien de générations tu vas lancer et le total estimé de crédits. **Attends l'accord.**
- **Ne relance jamais en boucle pour « améliorer ».** Après un résultat décevant, montre-le, dis ce qui ne va pas, propose un prompt corrigé et son coût, et laisse l'utilisateur décider.
- Pour montrer la requête sans rien dépenser, ajoute `--a-blanc`.

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
- En anglais de préférence. 1 024 caractères au maximum.
- Pour partir d'un concept existant, utilise `image` avec une image nette de l'objet seul, sur fond uni, en PNG ou JPEG de 20 Mo au maximum.

Montre le prompt à l'utilisateur avant une série.

### 3. Génération

```bash
python3 "$TRIPO" texte "weathered wooden supply crate, metal corners, stenciled paint" \
  --negatif "text, logo, pedestal" \
  --sortie assets/props/caisses/caisse_bois_01.glb --faces 3000

python3 "$TRIPO" image concepts/caisse.png --sortie assets/props/caisses/caisse_bois_02.glb --faces 3000
```

Le script crée la tâche, suit son avancement (intervalle croissant de 3 à 15 s) et télécharge le modèle. Il écrit ensuite la fiche `caisse_bois_01.tripo.json` à côté du fichier, puis affiche le contrôle du résultat.

Options :

| Option | Effet |
|---|---|
| `--sortie` | fichier à écrire (obligatoire) ; refuse d'écraser sans `--ecraser` |
| `--format glb\|fbx\|obj` | `glb` par défaut, à garder pour Godot ; `fbx` et `obj` passent par une conversion payante |
| `--faces N` | limite de faces (`face_limit`) ; sans elle, Tripo choisit |
| `--sans-texture` | géométrie seule, moins chère |
| `--sans-pbr` | texture sans cartes PBR |
| `--qualite-texture detailed` | texture plus fine, plus chère |
| `--taille-auto` | Tripo met l'objet à l'échelle réelle en mètres (`auto_size`) |
| `--low-poly` | topologie low-poly (`smart_low_poly`), avec supplément |
| `--modele` | version du modèle Tripo, `v3.1-20260211` par défaut |
| `--graine N` | graine, pour refaire un résultat proche |
| `--delai S` | attente maximale, 600 s par défaut |
| `--sans-attendre` | crée la tâche et rend la main ; reprise avec `telecharger` |
| `--a-blanc` | affiche la requête sans l'envoyer |

Pour reprendre une tâche :

```bash
python3 "$TRIPO" statut <task_id>
python3 "$TRIPO" telecharger <task_id> --sortie assets/props/caisses/caisse_bois_01.glb
```

`telecharger` ne relance pas de génération et ne coûte rien. Si la tâche est encore en cours, il l'attend. Il ne convertit pas : pour un FBX ou un OBJ, passe-lui le `task_id` de la conversion (champ `conversion` du `.tripo.json`), avec `--format fbx` ou `--format obj`.

### 4. Contrôle du résultat

Le script affiche, et range dans le champ `controle` du `.tripo.json`, les valeurs suivantes :
- poids du fichier ;
- nombre de triangles et de sommets ;
- dimensions en mètres (x × y × z) ;
- textures et leur résolution ;
- extensions glTF requises.

Pour un GLB déjà présent :

```bash
python3 "$TRIPO" inspecter assets/props/caisses/caisse_bois_01.glb
```

Compare ces valeurs aux conventions et au brief :
- **faces** au-dessus de la limite : le script avertit. Signale-le, sans relancer d'office.
- **poids** : au-dessus du budget, ce sont souvent les textures. Propose `--sans-pbr`, une texture standard ou une réduction dans Godot.
- **échelle** : Tripo rend souvent l'objet dans une boîte d'environ 1 unité. Corrige l'échelle à l'import dans Godot (option `nodes/root_scale` du `.import`, ou échelle de la scène qui l'instancie, selon les conventions). Ne régénère pas pour une question d'échelle. `--taille-auto` aide pour les prochaines générations.
- **orientation et pivot** : vérifie que l'avant et le sol sont corrects une fois dans Godot.

Décris le résultat à l'utilisateur en une ou deux lignes (valeurs et écarts). Ne présente jamais un asset comme validé sans ce contrôle.

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

Chaque modèle a une fiche, à côté de lui (`caisse_bois_01.glb` → `caisse_bois_01.tripo.json`). Elle permet de retrouver et de refaire l'asset. Elle contient :
- le prompt, ou l'image source (chemin, taille, empreinte SHA-256) ;
- le `task_id` ;
- les paramètres envoyés ;
- la version du modèle Tripo ;
- la date ;
- les crédits débités, si l'API les donne ;
- l'hôte d'où vient le fichier ;
- le contrôle.

Ne la modifie pas à la main. Pour refaire un asset, relis-la et relance avec les mêmes prompt, paramètres et graine, après accord sur le coût.

## Erreurs et ce qu'il faut dire

Le script écrit sur la sortie d'erreur un message court qui donne l'action à faire. Il sort avec un code distinct selon le cas. Transmets l'essentiel à l'utilisateur et arrête-toi : ne contourne jamais une erreur de réseau ou de clé.

| Code | Cas | Ce que tu dis à l'utilisateur |
|---|---|---|
| 0 | succès | résumé du contrôle et chemin du fichier |
| 1 | erreur API inattendue, téléchargement refusé | le message du script ; pour une URL expirée, relance `telecharger <task_id>` (gratuit) |
| 2 | argument invalide | corrige l'appel toi-même, sans rien demander |
| 3 | clé absente ou refusée (401) | « La clé Tripo manque ou est refusée. Ajoute ou corrige `TRIPO_API_KEY` dans les secrets de l'environnement, puis ouvre une nouvelle session. » Ne demande jamais la clé dans le chat. |
| 4 | crédits épuisés (code 2010) | « Le compte Tripo n'a plus assez de crédits ; rien n'a été débité. Recharge-le dans la console Tripo. » |
| 5 | domaine bloqué par la politique réseau (403 du proxy) ou injoignable | « Le domaine `<hôte>` est bloqué. Ajoute-le aux domaines autorisés de l'environnement. » Donne l'hôte exact cité par le script. |
| 6 | tâche échouée, annulée ou expirée | « La génération a échoué ; Tripo ne débite pas les tâches échouées. » Propose un prompt ou une image modifiés, avec leur coût, sans relancer d'office. |
| 7 | délai dépassé | « La tâche `<task_id>` tourne encore côté Tripo. » Reprends plus tard avec `telecharger <task_id>` : ne relance pas de génération, ce qui paierait deux fois. |
| 8 | contenu refusé par la modération (code 2008, statut `banned`) | dis-le, et propose une reformulation |
| 9 | trop de requêtes ou de tâches simultanées (429) | attends la fin des tâches en cours avant d'en créer d'autres |

## Sécurité de la clé

- Ne demande **jamais** la clé dans le chat. Si l'utilisateur la colle quand même, ne la réutilise pas, ne la recopie nulle part, et conseille-lui de la révoquer dans la console Tripo et d'en créer une autre, à mettre en secret de l'environnement.
- Ne l'affiche pas : pas de `echo $TRIPO_API_KEY`, pas de `env` ni de `printenv` non filtrés, pas de `set -x` autour des appels.
- Ne la mets dans aucun fichier, log, commit, `.tripo.json` ou message de PR. Le script masque la clé dans tout ce qu'il écrit et ne l'envoie qu'à l'API, jamais à l'hôte des fichiers.
- Pour tester sa présence : `python3 "$TRIPO" verifier`, jamais un affichage de la variable.
