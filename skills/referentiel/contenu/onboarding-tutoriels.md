# Onboarding et tutoriels

> **En bref** : comment apprendre au joueur à jouer sans qu'il ait l'impression d'être en classe. Couvre l'apprentissage par la pratique, l'introduction d'une mécanique à la fois, les environnements sûrs, « montrer plutôt que dire », les messages contextuels, les tutoriels qui ne freinent pas les joueurs expérimentés, les rappels après une pause, la courbe d'apprentissage et le premier contact, avec World 1-1 de *Super Mario Bros.* comme étude de cas.

## Quand consulter cette fiche

- Tu conçois les premières minutes du jeu ou l'introduction d'une nouvelle mécanique.
- Les playtesteurs ne comprennent pas une mécanique, ou abandonnent tôt.
- Tu écris des messages d'aide, des pop-ups ou un menu de didacticiel.
- Les joueurs expérimentés se plaignent d'un tutoriel lent ou impossible à passer.
- Le jeu se joue en sessions espacées (le joueur revient après des jours).
- Tu ajoutes une capacité tard dans le jeu et dois l'enseigner.

---

## 1. Principes

- **Apprendre en faisant** : on retient ce qu'on fait, pas ce qu'on lit. Chaque notion est apprise par une action du joueur, dans un contexte qui lui donne du sens (Celia Hodent, *The Gamer's Brain*).
- **Une chose à la fois** : la mémoire de travail est limitée. Introduire une mécanique, la laisser pratiquer, puis la suivante.
- **Le niveau est le tutoriel** : la meilleure leçon est un espace conçu pour que la bonne action soit évidente ou inévitable (voir [Level design](level-design.md)).
- **Montrer plutôt que dire** (*show, don't tell*) : mettre la situation sous les yeux du joueur, le laisser tenter.
- **Le joueur doit réussir vite** : un premier succès dans les premières secondes établit la confiance.
- **Sentiment de compétence** : le joueur doit avoir l'impression d'avoir **compris** lui-même (lien avec la motivation, voir [Cadres théoriques](../fondamentaux/cadres-theoriques.md)).

## 2. Le cycle d'apprentissage d'une mécanique

Pour chaque mécanique, dérouler :

| Étape | Objectif | Comment |
|---|---|---|
| 1. **Exposer** | Le joueur voit que la mécanique existe | Obstacle qui la nécessite, objet visible, PNJ qui l'utilise |
| 2. **Expérimenter en sécurité** | Essayer sans punition | Zone sans danger, chute courte, pas d'ennemi |
| 3. **Confirmer** | Le joueur sait qu'il a réussi | Feedback clair : son, animation, porte qui s'ouvre |
| 4. **Pratiquer** | Ancrer le geste | Quelques répétitions avec un peu de variation |
| 5. **Tester** | Vérifier la maîtrise avec un enjeu | Risque réel, combinaison avec une autre mécanique |
| 6. **Approfondir** | Utilisation avancée ou détournée | Twist (voir kishōtenketsu dans [Level design](level-design.md)) |

C'est la même logique que la structure « introduire → développer → twister → conclure », appliquée à l'enseignement. Daniel Cook décrit chaque unité apprise comme un *skill atom* (action → simulation → feedback → modèle mental) ; si une étape manque, l'apprentissage échoue.

## 3. Environnement sûr

- **L'échec pendant l'apprentissage doit coûter presque rien** : réapparition immédiate, pas de perte de progression.
- **Isoler la variable** : quand on apprend le saut, pas d'ennemi ; quand on apprend le combat, sol plat.
- **Faire monter le risque progressivement** : un trou peu profond avant un vide mortel ; un ennemi lent avant un rapide.
- **Laisser jouer avec la mécanique** sans objectif imposé (bac à sable) quand la mécanique est riche.

## 4. Messages et invites

Hiérarchie, du plus discret au plus intrusif :

1. **Aucun message** : l'espace suffit.
2. **Indice diégétique** : un PNJ, un panneau dans le monde, un personnage qui fait l'action.
3. **Invite contextuelle** (*prompt*) : icône du bouton qui apparaît près de l'objet interactif (« [E] Ouvrir »).
4. **Message court non bloquant** : bandeau quelques secondes, jeu non interrompu.
5. **Pause avec explication** : réservé aux systèmes complexes (menus, économie) ; court, avec image.
6. **Écran de tutoriel long** : à éviter ; rarement lu.

Règles :
- **Afficher l'invite au moment où l'action est utile**, pas au début du niveau.
- **Utiliser l'icône du périphérique actif** (clavier/souris ou manette, et le bon modèle de manette), mis à jour dynamiquement.
- **Retirer l'invite dès que le joueur a réussi l'action** (une ou quelques fois), et ne pas la réafficher sauf s'il bloque.
- **Une ligne, un verbe** : « Maintiens [A] pour sauter plus haut ».
- **Ne jamais afficher une information critique pendant un moment intense** : elle ne sera pas lue.
- **Consultation** : toutes les aides vues doivent être relisibles (menu « Aide » ou codex).

## 5. Ne pas freiner les joueurs expérimentés

- **Détecter la compétence** : si le joueur fait l'action avant l'invite, ne pas afficher l'invite (et valider l'étape).
- **Tutoriel passable** ou désactivable (option « aides : complètes / réduites / aucune »).
- **Tutoriel intégré au premier niveau** plutôt qu'un niveau tutoriel séparé obligatoire.
- **Chemin d'apprentissage optionnel** : une salle d'entraînement à côté du chemin principal, que l'expert ignore.
- **Pas de verrouillage artificiel** (« appuie sur X pour continuer » répété cinq fois).
- **Joueurs qui reviennent** sur un nouveau profil : proposer de passer l'introduction.

## 6. Rappels et retour après une pause

Les joueurs reviennent après des jours ou des semaines et ont oublié contrôles et contexte.

- **Résumé de reprise** : « Précédemment… », objectif courant visible dès le chargement.
- **Journal de quêtes** et objectif actuel toujours accessibles.
- **Liste des contrôles** consultable à tout moment dans le menu pause.
- **Aide adaptative** : si le joueur est bloqué longtemps (aucune progression pendant un temps donné, morts répétées au même endroit), proposer un indice gradué, puis une aide plus forte (le *Super Guide* de Nintendo propose de montrer la solution après plusieurs échecs).
- **Rappel contextuel** d'une mécanique peu utilisée quand la situation l'exige à nouveau (« [B] pour esquiver » réapparaît si le joueur n'a pas esquivé depuis longtemps et prend des coups).
- **Écrans de chargement** : astuces pertinentes pour la progression actuelle, pas aléatoires.

## 7. Courbe d'apprentissage

- **Front d'apprentissage dense au début, puis espacé** : beaucoup de notions dans la première heure, puis une nouvelle mécanique régulièrement pour garder la nouveauté.
- **Ne pas tout débloquer d'emblée** : un menu avec quinze systèmes au départ submerge. Les ouvrir au fil du jeu (voir [Progression](../systemes/progression.md)).
- **Profondeur cachée** : un système simple en surface avec des subtilités découvertes plus tard (combos, annulations, interactions) satisfait débutants et experts.
- **Vérifier la mémorisation** : réutiliser une mécanique ancienne après une période sans elle, dans un contexte facile, avant de la tester sérieusement.
- Lien avec la difficulté : voir [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md) et le flow dans [Cadres théoriques](../fondamentaux/cadres-theoriques.md).

## 8. Premier contact

Les premières minutes décident souvent si le joueur continue.

- **Interaction en quelques secondes** : le joueur contrôle quelque chose tôt, avant les longs logos et menus.
- **Pas de création de compte, de menu complexe ou de paramétrage obligatoire** avant de jouer, quand c'est évitable. Proposer des réglages par défaut sensés et un accès rapide aux options essentielles (sous-titres, taille de texte, sensibilité, inversion d'axes).
- **Le fun central apparaît tôt** : montrer ce qui rend le jeu unique dans les premières minutes.
- **Promesse** : l'ouverture annonce le ton, l'enjeu et le type d'expérience.
- **Premier échec bienveillant** : si le joueur peut échouer tôt, l'échec doit être rapide à réparer et instructif.

## 9. Étude de cas : World 1-1 de *Super Mario Bros.* (1985)

Le premier niveau, décrit par Shigeru Miyamoto et Takashi Tezuka (entretien Eurogamer, 2015), enseigne le jeu sans un mot :

| Moment | Ce que le joueur apprend | Comment |
|---|---|---|
| Départ | Aller à droite | Mario est à gauche de l'écran, l'espace vide est à droite |
| Premier Goomba | Les ennemis font mal ; on les évite ou on saute dessus | Il avance vers le joueur sur un terrain plat ; le contact tue, le saut est la réponse naturelle |
| Blocs « ? » | Les blocs se frappent par-dessous et contiennent des objets | Placés au-dessus du chemin, clignotants, à hauteur de saut |
| Champignon | Les objets qui sortent des blocs sont bénéfiques | Le champignon (qui ressemble à un Goomba) part à droite, rebondit sur un tuyau et revient vers le joueur : difficile de l'éviter, même en essayant |
| Tuyaux de hauteurs croissantes | Le saut est variable (maintenir = plus haut) | Chaque tuyau demande un peu plus de hauteur ; un Goomba entre deux tuyaux ajoute un léger test |
| Trous | Tomber tue | Introduits après que le saut est maîtrisé |
| Bloc caché, tuyau secret | Le monde récompense la curiosité | Bonus optionnels pour ceux qui explorent |
| Escaliers et drapeau | Fin de niveau, plus haut = plus de points | Dernier test de saut, avec une récompense graduée |

Leçons généralisables :
- **Le premier danger arrive vite mais sur un terrain sûr.**
- **L'espace force la découverte** : le champignon est presque inévitable.
- **Progression graduée** : même obstacle, difficulté croissante (tuyaux).
- **Les dangers mortels n'arrivent qu'après les outils pour les surmonter.**
- **Le contenu optionnel récompense l'exploration** sans pénaliser ceux qui l'ignorent.

Autres exemples souvent cités : le premier niveau de *Mega Man X* (analysé par la vidéo *Sequelitis* d'Egoraptor, 2011) et les salles de test de *Portal* (une notion par salle, puis combinaisons).

---

## Anti-patterns et pièges

- **Mur de texte au démarrage** : liste de tous les contrôles avant de jouer.
- **Tutoriel obligatoire et lent** répété à chaque nouvelle partie.
- **Enseigner tout dans le premier niveau**, puis plus rien.
- **Invite affichée hors contexte** (« appuie sur X pour planer » alors qu'il n'y a rien à franchir).
- **Échec punitif pendant l'apprentissage** : retour loin en arrière.
- **Mécanique enseignée une fois puis non utilisée pendant des heures**, puis exigée dans un boss.
- **Icônes de boutons fausses** pour le périphérique utilisé.
- **Aucun moyen de revoir une explication.**

## Checklist

- [ ] Chaque mécanique suit exposer → essayer en sécurité → confirmer → pratiquer → tester.
- [ ] Le joueur contrôle quelque chose dans les premières secondes.
- [ ] Le fun central est visible dans les premières minutes.
- [ ] Une seule nouvelle notion à la fois ; pas de mécanique mortelle avant ses outils.
- [ ] Les invites apparaissent au moment utile, avec l'icône du périphérique actif, et disparaissent après réussite.
- [ ] Le tutoriel est passable ou adapté aux joueurs qui font l'action d'eux-mêmes.
- [ ] Les aides vues sont relisibles dans un menu.
- [ ] Après une pause, l'objectif courant et les contrôles sont immédiatement accessibles.
- [ ] Une aide graduée se déclenche quand le joueur est bloqué longtemps.
- [ ] Les premières minutes ont été testées avec des joueurs n'ayant jamais vu le jeu, sans intervention.

## Pistes d'implémentation

Système de tutoriels piloté par événements, qui s'efface quand le joueur sait faire :

```
tutorial "double_jump":
    trigger: player_enters_zone("tuto_dj") or player_blocked_near(ledge_high, 10s)
    prompt: "TUTO_DOUBLE_JUMP"            // id de texte localisé + icône d'action
    complete_when: event("double_jump_performed") count >= 2
    skip_if: event("double_jump_performed") happened_before_trigger

function onEvent(e):
    for t in activeTutorials:
        if t.complete_when.matches(e): t.complete(); hidePrompt(t)
```

- **Associer les invites à des actions d'entrée**, pas à des touches en dur : l'icône est résolue selon le périphérique actif et les remappages.
- **Persister l'état des tutoriels** (vu, réussi, ignoré) dans le profil, pas seulement dans la sauvegarde de partie.
- **Télémétrie** : temps pour réussir chaque étape, nombre d'échecs, taux d'abandon par étape (voir [Playtest et métriques](../production/playtest-et-metriques.md)).
- **UE5** : *Enhanced Input* pour relier actions et icônes (requête des touches associées à une `UInputAction`) ; *Common UI* pour les icônes selon le périphérique.
- **Godot** : `InputMap` pour retrouver les événements liés à une action ; détecter le dernier périphérique utilisé dans `_input`.
- **Unity** : *Input System* (`InputAction.GetBindingDisplayString`) et détection du changement de périphérique.

## Voir aussi

- [Level design](level-design.md) — kishōtenketsu, guidage.
- [UI, UX et HUD](../interface/ui-ux-hud.md) — invites, icônes.
- [Accessibilité](../interface/accessibilite.md) — remappage, aides, sous-titres.
- [Contrôles et mouvement](../ressenti/controles-et-mouvement.md).
- [Progression](../systemes/progression.md) — déblocages progressifs.
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md).
- [Playtest et métriques](../production/playtest-et-metriques.md).
- [Plateforme](../genres/plateforme.md).

## Sources

- Celia Hodent, *The Gamer's Brain: How Neuroscience and UX Can Impact Video Game Design*, CRC Press, 2017.
- Daniel Cook, « The Chemistry of Game Design », Gamasutra / Lostgarden, 2007 (*skill atoms*).
- Shigeru Miyamoto & Takashi Tezuka, entretien vidéo sur World 1-1, Eurogamer, 2015.
- Egoraptor (Arin Hanson), *Sequelitis: Mega Man Classic vs. Mega Man X*, 2011.
- Koichi Hayashida, entretien sur le kishōtenketsu, Gamasutra, 2012.
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, 3e éd., CRC Press, 2019.
- Mark Brown, Game Maker's Toolkit (analyses de tutoriels) — https://www.youtube.com/@GMTK
