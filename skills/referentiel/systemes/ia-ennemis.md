# IA et design d'ennemis

> **En bref** : comment concevoir des ennemis qui créent des situations intéressantes, comment les combiner en rencontres, et quelle architecture d'IA choisir (FSM, behavior tree, utility, GOAP). Principe directeur : une IA de jeu doit être **amusante et lisible**, pas intelligente.

## Quand consulter cette fiche

- Tu crées un nouveau type d'ennemi ou tu dois varier un bestiaire.
- Tu construis une rencontre, une vague, une arène.
- Tu choisis une architecture d'IA ou ton IA devient impossible à maintenir.
- Les joueurs trouvent les ennemis « bêtes », « tricheurs » ou « imprévisibles ».
- Tu conçois un boss.

---

## 1. Principe : fun avant intelligence

- Le but de l'IA est de **donner au joueur des occasions de briller**. Un ennemi optimal (visée parfaite, coordination totale) est frustrant.
- **Lisibilité > réalisme** : le joueur doit comprendre ce que l'ennemi fait et va faire. Une intention invisible équivaut à de l'aléatoire.
- **Montrer que l'IA réfléchit** : un ennemi qui crie « Grenade ! » ou « Il est derrière le mur ! » paraît plus intelligent qu'un algorithme sophistiqué silencieux. Les « barks » (répliques contextuelles) sont un outil majeur.
- **Rater exprès** : les premiers tirs ennemis peuvent manquer volontairement, surtout hors champ de vision du joueur, pour signaler la menace avant de toucher.
- **Prévisible localement, varié globalement** : un ennemi donné doit être apprenable ; c'est la composition qui crée la variété.

## 2. Rôles d'ennemis

Concevoir chaque ennemi par **la question qu'il pose au joueur** et la réponse qu'il exige.

| Rôle | Ce qu'il fait | Ce qu'il exige du joueur | Exemple de réglage |
|---|---|---|---|
| **Fodder** (chair à canon) | Faible, nombreux | Gestion de foule, satisfaction | Meurt en 1–2 coups |
| **Rusher** | Fonce sur le joueur | Réaction, recul, priorisation | Rapide, peu de PV |
| **Tank** / brute | Absorbe, bloque l'espace | Contournement, point faible, patience | Lent, beaucoup de PV, attaques lourdes télégraphiées |
| **Sniper** / artilleur | Attaque à distance, reste loin | Mouvement, couverture, rapprochement | Visée annoncée (laser), fragile au contact |
| **Support** / soigneur / buffer | Renforce les autres | Priorisation de cible | Fragile, reconnaissable |
| **Contrôleur de zone** | Interdit des zones (pièges, flammes, mines) | Repositionnement | Zones clairement visibles |
| **Invocateur** | Crée d'autres ennemis | Agression, priorisation | Limite de créatures actives |
| **Flanqueur** / assassin | Attaque par derrière ou par surprise | Vigilance, conscience de l'espace | Signal audio obligatoire |
| **Bouclier** / défenseur | Protège frontalement | Angle d'attaque, outil spécifique | Faiblesse dos ou côté |

Règles :
- Un ennemi = **un rôle principal**. Les hybrides brouillent la lecture.
- Différencier par la **silhouette**, la couleur et le son avant les stats.
- Les **variantes** (version élite, version élémentaire) réutilisent un rôle connu en ajoutant une seule règle.

## 3. Composition de rencontres

Une rencontre est une **phrase** composée de rôles. Le même bestiaire produit des dizaines de situations différentes.

- **Combiner des rôles qui se complètent** : tank devant + sniper derrière force le joueur à contourner ; rusher + contrôleur de zone pousse le joueur dans les zones interdites.
- **Introduire un ennemi seul** d'abord, dans un contexte sûr, puis le combiner (voir [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md) et [Level design](../contenu/level-design.md)).
- **Vagues** : varier l'intensité (montée, pic, relâchement). Laisser un temps de respiration entre deux vagues.
- **Budget de menace** : attribuer un coût à chaque ennemi et composer les rencontres avec un budget qui augmente au fil du jeu. Utile pour la génération procédurale.
- **L'arène fait partie de la rencontre** : couverture, hauteur, obstacles, chemins de fuite changent tout.

```text
budget = base + progression * k
while budget > 0:
    role = pick_role_weighted(contraintes_de_rencontre)  # ex. max 1 support
    enemy = pick_enemy(role, budget)
    spawn(enemy); budget -= enemy.cost
```

## 4. Choisir une architecture d'IA

| Architecture | Principe | Idéal pour | Limites |
|---|---|---|---|
| **FSM** (machine à états finis) | États (Patrouille, Poursuite, Attaque) et transitions | Ennemis simples, boss à phases, peu de comportements | Explosion des transitions au-delà d'une dizaine d'états |
| **HFSM** (FSM hiérarchique) | États imbriqués | Ennemis moyens avec sous-comportements | Reste rigide |
| **Behavior Tree** (arbre de comportement) | Arbre de sélecteurs/séquences évalué en priorité | La majorité des ennemis de jeux d'action ; standard industriel (popularisé par Halo 2) | Mal adapté aux arbitrages fins entre options proches |
| **Utility AI** | Chaque action a un score calculé à partir de courbes ; on choisit le meilleur | Choix nuancés (quand se soigner, fuir, viser qui), simulation, PNJ de jeux de survie/gestion | Difficile à déboguer, réglage des courbes |
| **GOAP** (planification orientée but) | L'agent planifie une suite d'actions pour atteindre un but (popularisé par F.E.A.R.) | Comportements émergents, tactiques multi-étapes | Coût CPU, imprévisibilité, réglage complexe |
| **HTN** (réseau de tâches hiérarchiques) | Décomposition de tâches en sous-tâches planifiées | Tactique de groupe structurée | Complexité de mise en œuvre |

Arbre de décision simple :
1. Moins de ~6 comportements, transitions évidentes → **FSM**.
2. Ennemi d'action standard, priorités claires (réagir au danger > attaquer > se positionner > patrouiller) → **Behavior Tree**.
3. Beaucoup d'options concurrentes à arbitrer selon le contexte → **Utility** (éventuellement comme nœud d'un BT).
4. Besoin de plans multi-étapes émergents et prêt à payer le coût de réglage → **GOAP / HTN**.

Les combinaisons sont fréquentes : BT pour la structure, scores d'utilité pour choisir une cible ou une action dans un nœud.

## 5. Perception

- **Vue** : cône de vision (angle, distance) + test de ligne de vue (raycast). Ajouter une **jauge de détection** progressive plutôt qu'un passage instantané à « alerte ».
- **Ouïe** : les actions du joueur émettent des événements sonores avec un rayon ; les ennemis réagissent selon la distance.
- **Mémoire** : dernière position connue du joueur. Un ennemi qui oublie instantanément paraît stupide ; un ennemi omniscient paraît tricheur.
- **États d'alerte lisibles** : inactif → suspicieux → recherche → combat → retour au calme. Chaque transition signalée (icône, réplique, posture). Indispensable en jeu d'infiltration.
- La perception est le premier endroit où **tricher en faveur du joueur** : détection plus lente que réaliste, angle de vue réduit à faible difficulté.

## 6. Déplacement : pathfinding et steering

- **Pathfinding** : A* sur grille ou *navmesh* pour trouver un chemin. Utiliser le système du moteur plutôt que réimplémenter.
- **Steering** (comportements de pilotage, Craig Reynolds) : *seek*, *flee*, *arrive*, *pursue*, *evade*, *wander*, séparation, alignement, cohésion. Pour un mouvement fluide et des groupes qui ne se superposent pas.
- **Évitement local** entre agents (RVO/ORCA ou séparation simple) pour éviter les embouteillages.
- **Points tactiques** (*cover points*, *smart objects*) : pré-annoter le niveau avec des positions intéressantes (couverture, flanc, hauteur) plutôt que les calculer à la volée.
- **Ne pas recalculer un chemin chaque frame** : à intervalle ou quand la cible a bougé significativement.

## 7. Triche acceptable

Tricher est normal tant que **le joueur ne s'en rend pas compte ou que c'est à son avantage**.

| Triche | Acceptable ? |
|---|---|
| Rater exprès les premiers tirs, réduire la précision quand le joueur est faible | Oui, recommandé |
| Limiter le nombre d'attaquants simultanés (jetons d'attaque) | Oui, recommandé (voir [Combat](combat.md)) |
| Ralentir la détection, oublier le joueur plus vite | Oui |
| L'ennemi « sait » où est le joueur pour se rapprocher (sans l'attaquer) | Oui, avec parcimonie |
| Viser parfaitement à travers les murs, voir sans ligne de vue | Non : ressenti comme injuste |
| Bonus de ressources à l'IA en stratégie | Acceptable si annoncé (niveaux de difficulté) |
| Apparition d'ennemis dans le champ de vision du joueur | Non : casse l'immersion |

## 8. Lisibilité des intentions

- **Télégraphier chaque attaque** (voir [Combat](combat.md), section télégraphie).
- **Exposer l'état** : posture d'alerte, icône au-dessus de la tête, couleur d'œil, barks.
- **Faire durer les décisions** : un ennemi qui change d'avis toutes les 0,1 s paraît erratique. Ajouter une **inertie** (durée minimale par action, hystérésis sur les scores d'utilité).
- **Patterns** : les ennemis répètent des schémas reconnaissables. La répétition permet l'apprentissage.
- **Feedback de mort et de dégât** : réaction visible à chaque coup (flinch, recul) pour confirmer au joueur que son action a porté.

## 9. Boss design

Un boss est un **examen** des compétences apprises jusque-là, avec une identité forte.

- **Phases** : 2–4 phases, chacune ajoutant ou combinant des attaques. Annoncer clairement la transition (animation, musique, changement d'arène). Une FSM par phase est souvent suffisante.
- **Moveset limité et lisible** : chaque attaque a une télégraphie unique et une réponse claire.
- **Fenêtres de punition** : après certaines attaques, le boss est vulnérable. C'est là que le joueur doit infliger ses dégâts.
- **Apprentissage par l'échec** : le joueur doit pouvoir comprendre **pourquoi** il est mort. Relance rapide (point de sauvegarde proche, pas de longue cinématique non-skippable).
- **Escalade** : la dernière phase reprend les attaques connues en plus rapide ou combinées, plutôt que d'en introduire beaucoup de nouvelles.
- **Éviter** : les boss « sacs à PV », les attaques imparables, les ajouts de sbires interminables, les instakills non télégraphiés.
- Prévoir des **mécaniques d'indulgence** discrètes (dernier coup qui tue même si le joueur meurt en même temps, attaques ralenties aux faibles difficultés).

---

## Anti-patterns et pièges

- **IA trop forte** : visée parfaite, réaction instantanée.
- **IA indécise** : oscillation entre deux comportements (absence d'hystérésis).
- **Ennemis indistincts** : rôles et silhouettes trop proches.
- **Spawn visible** ou derrière le joueur sans signal.
- **FSM monolithique** de 30 états maintenue à la main.
- **Comportements non testables** : pas d'outil de debug pour voir l'état, la cible et la décision de chaque ennemi.
- **Ennemis qui restent coincés** : navmesh incomplet, pas de comportement de secours.

## Checklist

- [ ] Chaque ennemi a un rôle unique et une question claire posée au joueur.
- [ ] Silhouette, couleur et son distinguent chaque rôle.
- [ ] Chaque ennemi est introduit seul avant d'être combiné.
- [ ] Les rencontres combinent des rôles complémentaires et respectent un budget de menace.
- [ ] L'architecture d'IA est choisie selon la complexité réelle des comportements.
- [ ] La perception a des états d'alerte progressifs et lisibles.
- [ ] Les décisions ont une durée minimale / une hystérésis.
- [ ] Les attaques simultanées sont limitées.
- [ ] Les triches éventuelles sont invisibles ou à l'avantage du joueur.
- [ ] Un affichage debug montre état, cible et décision de chaque agent.
- [ ] Les boss ont des phases annoncées, des fenêtres de punition et une relance rapide.

## Pistes d'implémentation

- Séparer **décision** (FSM/BT/utility), **perception** et **action** (locomotion, animation, attaque) en modules distincts.
- Paramètres en **données** par type d'ennemi : PV, vitesses, distances de perception, attaques, coût de menace, rôle.
- Mettre à jour l'IA à fréquence réduite (ex. 5–10 Hz) pour la décision, chaque frame pour le mouvement.
- **UE5** : Behavior Tree + Blackboard, AI Perception (vue, ouïe), Environment Query System (EQS) pour choisir positions et cibles, StateTree comme alternative plus récente, Smart Objects pour les points d'interaction.
- **Godot** : `NavigationAgent2D/3D` et `NavigationRegion` ; FSM en nœuds ou scripts ; plugins de BT communautaires (ex. LimboAI, Beehave).
- **Unity** : NavMesh (AI Navigation package) ; FSM via scripts ou Animator ; BT via assets tiers ou Unity Behavior.

## Voir aussi

- [Combat](combat.md)
- [Équilibrage et difficulté](equilibrage-et-difficulte.md)
- [Aléatoire et procédural](aleatoire-et-procedural.md)
- [Level design](../contenu/level-design.md)
- [Audio](../interface/audio.md)

## Sources

- Damian Isla, « Handling Complexity in the Halo 2 AI », GDC 2005.
- Jeff Orkin, « Three States and a Plan: The A.I. of F.E.A.R. », GDC 2006.
- Dave Mark, *Behavioral Mathematics for Game AI*, Course Technology, 2009.
- Steve Rabin (dir.), série *Game AI Pro* (vol. 1–3, 2013–2017), CRC Press — http://www.gameaipro.com/
- Craig Reynolds, « Steering Behaviors For Autonomous Characters », GDC 1999 — https://www.red3d.com/cwr/steer/
- Ian Millington, *AI for Games* (3e éd.), CRC Press, 2019.
- Amit Patel, *Red Blob Games* (A*, pathfinding) — https://www.redblobgames.com/
