---
name: animer
description: Pilote l'API Uthana (animation 3D par IA) et range les animations dans un projet Godot. À charger quand on veut animer un personnage humanoïde - animation depuis une description (text-to-motion 3.0, Lite, Mini), depuis une vidéo d'une personne (video-to-motion), marche ou course dans une direction et à une vitesse données (locomotion, faite pour boucler), boucler ou enchaîner des animations ; importer un personnage FBX ou GLB (par exemple fait avec Tripo) avec rigging automatique, ou changer son squelette (Mixamo, UE5, Roblox R15) ; télécharger des animations retargetées sur ce personnage en GLB, FBX ou BVH (sur place, sans maillage, 24 à 60 i/s) ; puis contrôler durée, os et animations, importer dans Godot (AnimationPlayer, bibliothèque d'animations, boucle, root motion) et vérifier l'import en headless. Couvre aussi les crédits et le solde, la clé UTHANA_API_KEY, la reprise d'une tâche, et les erreurs (réseau bloqué, clé refusée, solde insuffisant, tâche échouée, trop de tâches simultanées, réponse incertaine). Ne convient pas aux créatures non humanoïdes (quadrupèdes, oiseaux), aux animations faciales, ni à l'animation en temps réel pendant la partie.
---

# Animer un personnage avec Uthana

Ce skill pilote l'API GraphQL d'Uthana (`https://uthana.com/graphql`) avec le script `scripts/uthana.py`, rangé dans le même dossier que ce fichier. Le script n'utilise que la bibliothèque standard de Python 3. Il lit la clé dans `UTHANA_API_KEY` et l'envoie en authentification Basic (clé en nom d'utilisateur, mot de passe vide).

```bash
UTHANA="${CLAUDE_PLUGIN_ROOT}/skills/animer/scripts/uthana.py"
python3 "$UTHANA" --help
```

Toutes les commandes sont décrites dans [commandes.md](commandes.md). Ce fichier-ci donne les règles communes et le déroulé.

Le projet prime : ses conventions (dossier, nommage, personnages, images par seconde, root motion) l'emportent sur les valeurs par défaut de ce skill.

## Quand s'en servir

**Oui** :
- animations de personnages humanoïdes bipèdes : gestes, réactions, attaques, danses, idles, emotes, cinématiques courtes ;
- cycles de déplacement (marche, course, pas de côté, recul) pour un contrôleur de personnage : `locomotion` ;
- animer un personnage généré avec Tripo ou fait main : `importer` (rigging automatique), puis les animations retargetées sur lui ;
- reproduire un mouvement filmé (une personne, plan fixe) : `video` ;
- premier jet d'animation pour valider un rythme ou une mise en scène.

**Non**, propose une autre voie :
- créatures non humanoïdes (quadrupèdes, oiseaux, araignées), objets mécaniques ;
- expressions faciales, lip sync ;
- animation générée pendant la partie, en temps réel ;
- animation qui doit tomber à l'image près sur un événement de gameplay (frame data d'un jeu de combat) : génère, puis retouche à la main.

## Avant tout : vérifier l'accès

```bash
python3 "$UTHANA" verifier
```

Le script vérifie que la clé est présente sans l'afficher, teste l'accès réseau, puis lit l'organisation et le solde. Il signale si le paiement à l'usage n'est pas activé : sans lui, l'API ne génère rien. S'il échoue, consulte la section « Erreurs » et arrête-toi : ne contourne rien.

## Conventions du projet

Avant la première génération, cherche les conventions d'animation du projet :
1. `.claude/uthana.md`, le fichier dédié s'il existe ([gabarit](conventions-exemple.md)) ;
2. le `CLAUDE.md` du projet, puis le GDD (section animation, personnages) ;
3. les animations déjà présentes : dossier, nommage, `.uthana.json`.

Il te faut au minimum :
- le dossier de destination et la règle de nommage ;
- le **personnage** cible : son `character_id` Uthana (importé une fois, puis noté), ou un personnage fourni (`tar`, `ava`, `manny`, `quinn`) ;
- le format (`.glb` pour Godot) et les images par seconde (30 par défaut) ;
- **root motion ou sur place** : le déplacement vient-il de l'animation ou du code (`CharacterBody3D`) ?
- avec ou sans maillage : le GLB complet (personnage et animation) ou l'animation seule, pour une bibliothèque d'animations.

**S'il manque une de ces informations, demande-la à l'utilisateur au lieu de deviner.** Propose-lui ensuite de les écrire dans `.claude/uthana.md`.

## Choisir la commande

| Besoin | Commande |
|---|---|
| Un geste, une action, une réaction décrits en mots | `texte` (modèle 3.0 par défaut) |
| Un premier jet bon marché | `texte --modele 3.0-mini` |
| Marche, course, pas de côté pour un contrôleur | `locomotion` (une par direction et vitesse) |
| Un mouvement filmé | `video` |
| Une animation qui doit boucler sans à-coup | `boucler` (ou `locomotion`, déjà faite pour) |
| Deux animations à la suite | `enchainer` |
| Animer son propre personnage | `importer` une fois, puis `--personnage <character_id>` partout |
| Changer de squelette (UE5, Roblox) | `importer --squelette ue5` |
| Retélécharger, autre format ou autres options | `telecharger` (gratuit) |
| Reprendre une tâche | `statut <job_id> --sortie …` |
| Opération que le script ne connaît pas | `brut` |

**Retargeting automatique** : une animation se télécharge pour un personnage donné (`--personnage`), et Uthana l'adapte à son squelette. Une même animation peut être téléchargée pour plusieurs personnages, gratuitement. Le script passe le même `--personnage` à la génération et au téléchargement.

## Coût

Uthana fonctionne en paiement à l'usage : un solde en dollars, sans abonnement, partagé entre l'application web et l'API. Les nouveaux comptes reçoivent 5 $ de crédit. Les crédits achetés n'expirent pas.

Barème relevé le 23/11/2026 sur [uthana.com/pricing](https://uthana.com/pricing) (`prix` donne le barème actuel) :

| Opération | Prix |
|---|---|
| `texte`, modèles 3.0 et 3.0-lite | 0,10 $ par seconde générée (3.0 : 4 à 10 s ; Lite : 5 à 10 s) |
| `texte --modele 3.0-mini` | 0,075 $ par seconde (5 à 10 s) |
| `texte --modele 2.0` / `1.0` | 0,03 / 0,02 $ par seconde |
| `video` (3.0) | 0,06 $ par seconde d'animation produite (2.0, 2.1 : 0,05 $) |
| `locomotion` | 0,02 $ par seconde |
| `boucler`, `enchainer` | 0,01 $ par seconde produite |
| `importer` avec rigging automatique | 0,15 $ ; gratuit si le personnage a déjà un squelette |
| Téléchargements, listes, statut, `prix`, `verifier` | gratuit |

Exemples : une animation de 4 s en 3.0 coûte 0,40 $ ; cinq directions de locomotion, quelques centimes.

Le script annonce l'estimation avant l'envoi, puis le débit réel (solde avant et après) dans la fiche. `depenses` liste les opérations du portefeuille. Une tâche échouée n'est pas facturée.

Règles :
- **Une génération demandée explicitement** : annonce son coût en une ligne, puis lance-la, sauf si les conventions exigent un accord à chaque fois.
- **Avant une série** (2 générations payantes ou plus : un jeu de locomotion complet, plusieurs variantes d'un geste), un rigging, ou une variante non demandée : annonce le nombre d'opérations et le total estimé. **Attends l'accord.**
- **Ne relance jamais en boucle pour « améliorer ».** Après un résultat décevant, décris-le, propose un prompt corrigé et son coût, et laisse l'utilisateur décider.
- Pour voir la requête sans rien dépenser : `--a-blanc`.

**Une opération à la fois.** Sans moyen de paiement enregistré, un compte a 4 tâches simultanées au plus par type. Le script réessaie environ 5 minutes un refus pour cette raison (rien n'est alors accepté ni facturé), puis sort en code 9.

**Jamais de nouvel essai d'une opération payante incertaine.** Après un délai dépassé, une erreur 5xx ou un 429 sans code connu (code 7), l'opération a pu être acceptée et facturée : regarde `taches` et `animations`, récupère le résultat avec `statut` ou `telecharger`, et ne relance qu'après avoir vérifié qu'il n'existe pas.

## Déroulé

### 1. Brief

Établis avec l'utilisateur, ou à partir du GDD :
- **quoi** : l'action, son contexte de jeu (combat, dialogue, exploration), son début et sa fin (part-elle d'un idle ? y revient-elle ?) ;
- **durée** voulue, et si elle **boucle** ;
- **déplacement** : sur place, ou avec déplacement de la racine ;
- **personnage** cible et nom de fichier.

### 2. Prompt (pour `texte`)

- Décris **un seul mouvement**, physiquement, en anglais de préférence : posture, membres, rythme, intensité, émotion visible. Ex. « a tired soldier slowly sits down on the ground, leaning back on his hands ».
- Indique le début et la fin si l'animation doit s'enchaîner : « starts from a neutral standing pose and returns to it ».
- Pas de décor, de caméra ni d'objet tenu : Uthana ne génère que le corps. Pour une arme, décris le geste (« two-handed overhead sword swing ») ; l'objet s'attache dans Godot.
- Les modèles 3.0 réécrivent le prompt en direction physique (désactivable : `--sans-reecriture`).
- Guide de prompts d'Uthana : [Text-to-3D animation prompts](https://uthana.com/resources/text-to-3d-animation-prompts).

Pour une **vidéo** : une seule personne, plan fixe, corps entier visible, 2 à 60 s, commençant debout, MP4, MOV, AVI ou WebM de 128 Mo au plus.

### 3. Génération

```bash
python3 "$UTHANA" texte "a guard raises his hand to stop someone, firm and calm" \
  --personnage cAbc123def45 --duree 4 --sortie assets/anims/garde/garde_halte.glb

python3 "$UTHANA" locomotion --personnage cAbc123def45 --angle 0 --vitesse 1.4 --sur-place \
  --sortie assets/anims/garde/garde_marche_avant.glb
```

Le script crée l'opération, suit la tâche si besoin (modèles 3.0, vidéo), télécharge l'animation retargetée sur le personnage, écrit la fiche `.uthana.json` à côté, et affiche le contrôle et le débit.

Options de téléchargement communes : `--fps 24|30|60` (30 par défaut), `--sans-maillage`, `--sur-place`, `--torse` (bas du corps immobile), `--vitesse-lecture 0–2`. Elles se changent ensuite gratuitement avec `telecharger`.

### 4. Contrôle du résultat

Le script affiche, et range dans le champ `controle` de la fiche, pour un GLB :
- animations (nom, durée), images par seconde ;
- nombre d'os et de maillages ;
- taille du fichier.

Pour un GLB existant : `python3 "$UTHANA" inspecter <fichier>`.

Vérifie :
- **durée** : proche de la demande ; une animation 3.0 courte demandée en 4 s peut sortir un peu différente ;
- **os** : le même nombre que le personnage cible (sinon, mauvais `--personnage`) ;
- **maillage** : présent ou absent selon l'option voulue ;
- **mouvement** : tu ne peux pas le voir. Demande à l'utilisateur de le regarder (dans Godot ou sur la page de l'animation dans l'application Uthana, `https://uthana.com/app/<character_id>/<motion_id>`), en particulier les pieds qui glissent, les mains, les traversées du corps.

Ne présente jamais une animation comme validée sur la seule foi du contrôle.

### 5. Import dans Godot

- Range le GLB sous la racine du projet Godot, dans le dossier des conventions. Garde la fiche `.uthana.json` à côté et commite les deux, avec le `.import`. Ne commite jamais `.godot/`.
- **GLB complet** (personnage et animation) : Godot crée une scène avec `Skeleton3D` et `AnimationPlayer`. Pratique pour un personnage dont toutes les animations viennent d'Uthana.
- **Animation seule** (`--sans-maillage`) : dans le dock *Import*, choisis *Import As: Animation Library*, puis ajoute la bibliothèque à l'`AnimationPlayer` du personnage. Le squelette doit être le même : télécharge toujours pour le `character_id` de ce personnage.
- **Boucle** : dans les réglages d'import avancés (*Advanced Import Settings*), sélectionne l'animation et règle *Loop Mode* sur *Linear*. Godot passe aussi en boucle les animations dont le nom finit par `-loop` ou `-cycle` ; Uthana choisit le nom, donc règle-le dans l'import.
- **Root motion** : avec un déplacement dans l'animation, utilise un `AnimationTree` avec `root_motion_track` pointant l'os racine, et applique `get_root_motion_position()` au `CharacterBody3D`. Sinon, télécharge avec `--sur-place` et déplace le personnage en code, dans la direction de la `locomotion` jouée (`--angle` : 0 avant, 90 droite, −90 gauche, 180 arrière).
- **Échelle et orientation** : glTF est en mètres, Y vers le haut. Vérifie dans Godot que le personnage fait face à la bonne direction et a la bonne taille ; corrige à l'import, ne régénère pas.

### 6. Vérification de l'import en headless

```bash
godot --headless --path <racine_du_projet> --import 2>&1 | tee /tmp/import-godot.log
```

Puis vérifie que le log ne cite pas le fichier en `ERROR`, que le `.import` existe sans `valid=false`, et que l'importé existe dans `.godot/imported/`. Sans Godot dans l'environnement, dis que l'import n'a pas été vérifié.

## Personnages faits avec Tripo

Un personnage humanoïde généré avec le plugin `tripo` s'anime ainsi :
1. modèle **non riggé** (sortie de `tripo image` ou `tripo texte`) : `importer perso.glb --pieds-au-sol --sortie perso_rig.glb` (rigging automatique, 0,15 $). Vérifie la confiance affichée : sous 0,5, le rig risque d'être mauvais ;
2. modèle **déjà riggé** par `tripo rigger` : `importer perso_rig.glb --sans-rig` (gratuit), à condition que le squelette ait les os essentiels (bassin, épaules, hanches) ;
3. note le `character_id` dans les conventions, puis génère les animations avec `--personnage <character_id>`.

Uthana rigge les bipèdes humanoïdes ; le personnage doit être en pose neutre, debout, bras écartés de préférence. Fichiers FBX ou GLB de 30 Mo au plus.

## Fiche `.uthana.json`

Chaque animation téléchargée a une fiche (`garde_halte.glb` → `garde_halte.uthana.json`), avec : l'opération, le prompt ou l'entrée (fichier relatif ou nom, SHA-256), le modèle, les paramètres, le `job_id`, le `motion_id` et le `character_id`, les options de téléchargement, l'estimation et le débit réel, la date, le contrôle. Ne la modifie pas à la main : avec le `motion_id`, `telecharger` refait le fichier gratuitement, pour n'importe quel personnage.

## Erreurs et ce qu'il faut dire

| Code | Cas | Ce que tu dis à l'utilisateur |
|---|---|---|
| 0 | succès | résumé du contrôle et chemin du fichier |
| 1 | erreur API inattendue, réponse illisible | le message du script |
| 2 | argument invalide (refusé par le script ou par l'API) | corrige l'appel toi-même |
| 3 | clé absente ou refusée (401) | « La clé Uthana manque ou est refusée. Ajoute ou corrige `UTHANA_API_KEY` dans l'environnement, puis ouvre une nouvelle session. » Jamais de clé dans le chat |
| 4 | solde insuffisant, limite de personnages, ou quota d'un ancien abonnement | « Le solde Uthana ne suffit pas ; rien n'a été généré. Ajoute du crédit sur uthana.com/app/account. » |
| 5 | domaine bloqué par la politique réseau | « Le domaine `<hôte>` est bloqué. Ajoute-le aux domaines autorisés de l'environnement. » |
| 6 | tâche échouée | « La génération a échoué ; elle n'est pas facturée. » Propose une autre entrée (prompt, vidéo plus courte ou plus nette), sans relancer d'office. Une vidéo qui a fait échouer la tâche est bloquée par Uthana jusqu'à vérification |
| 7 | délai dépassé, erreur 5xx ou 429 inconnu sur une opération payante | « L'opération a pu être acceptée et facturée. » Regarde `taches` et `animations`, reprends avec `statut` ou `telecharger`, ne relance pas |
| 9 | trop de tâches simultanées, malgré environ 5 minutes d'essais | rien n'a été accepté ; attends la fin des tâches en cours |

Si le téléchargement échoue après une génération réussie, le script écrit la fiche (`"etat": "a_telecharger"`) et affiche la commande `telecharger` exacte, gratuite.

## Droits et confidentialité

- **Licence** (conditions d'utilisation v2.0.0 du 09/11/2026) : dès le premier achat de crédit, les animations sont utilisables commercialement dans un jeu, sans mention d'Uthana, y compris celles faites avant avec les crédits gratuits. Sans achat, l'usage commercial est permis avec la mention « Animation generated with Uthana (uthana.com) » dans les crédits du jeu. Voir le README.
- **Entraînement** : interdit d'utiliser les animations pour entraîner un modèle de génération ou d'extraction de mouvement concurrent d'Uthana, ou de les vendre comme jeu de données.
- **Ce qu'Uthana garde** : par défaut, Uthana peut utiliser les personnages et vidéos envoyés et les animations produites pour entraîner ses modèles, et inclure les animations générées depuis un texte dans des jeux de données qu'il vend. Avant d'envoyer un personnage ou une vidéo confidentiels (jeu non annoncé), préviens l'utilisateur.
- **Clé** : ne demande **jamais** la clé dans le chat ; ne l'affiche pas (pas de `echo`, `env` non filtré, `set -x`) ; ne la mets dans aucun fichier, log ou commit. Le script la masque partout, et ne suit aucune redirection. Pour tester sa présence : `python3 "$UTHANA" verifier`.
