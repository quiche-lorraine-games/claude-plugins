# Référentiel game design — instructions pour les agents

Ce repo est une **base de connaissances de game design**, indépendante de tout projet. Il est attaché aux sessions où l'on développe un jeu pour servir de référence. Il ne contient pas de code de jeu.

## Comment s'en servir quand tu travailles sur un jeu

1. **Le projet prime.** Si le projet de jeu a son propre GDD, ses piliers ou des décisions déjà prises, ils l'emportent sur ce référentiel. Ici, ce sont des conseils par défaut, pas des règles imposées.
2. **Lis la fiche avant d'agir.** Avant de concevoir ou d'implémenter une mécanique, repère la fiche pertinente dans la table ci-dessous et lis-la (au minimum « Quand consulter », les règles concrètes et la checklist). Inutile de tout lire : une à trois fiches suffisent en général.
3. **Valeurs chiffrées = points de départ.** Les valeurs données (durées, ratios, courbes) servent à amorcer un réglage. Expose-les comme paramètres modifiables (data asset, fichier de config, variables exportées), jamais en dur.
4. **Gameplay ou présentation ?** Les fiches distinguent ce qui change la logique de jeu (gameplay) de ce qui n'est que du retour visuel ou sonore (présentation, *juice*). Ne laisse jamais un effet de présentation modifier la logique.
5. **Cite tes sources.** Quand une proposition s'appuie sur une fiche, mentionne-la (ex. « cf. `ressenti/controles-et-mouvement.md`, coyote time »), pour que l'humain puisse vérifier.
6. **Déroule la checklist.** Chaque fiche se termine par une checklist : utilise-la pour auditer une fonctionnalité ou préparer une revue.

## Table de routage

| Tu travailles sur… | Lis d'abord |
|---|---|
| Définir le concept, la boucle de jeu, ce que fait le joueur | [fondamentaux/boucles-de-gameplay.md](fondamentaux/boucles-de-gameplay.md) |
| Justifier ou critiquer un choix de design (MDA, flow, motivation, types de joueurs) | [fondamentaux/cadres-theoriques.md](fondamentaux/cadres-theoriques.md) |
| Choix intéressants, lisibilité, risque/récompense, profondeur | [fondamentaux/principes-de-conception.md](fondamentaux/principes-de-conception.md) |
| Public cible, profils et motivations de joueurs, personas | [fondamentaux/profils-de-joueurs.md](fondamentaux/profils-de-joueurs.md) |
| Le ressenti d'une action (tir, impact, saut, dash, mort) | [ressenti/game-feel-juice.md](ressenti/game-feel-juice.md) |
| Déplacement, saut, contrôles, réglages manette, assistance de visée | [ressenti/controles-et-mouvement.md](ressenti/controles-et-mouvement.md) |
| Caméra 2D ou 3D, camera shake | [ressenti/camera.md](ressenti/camera.md) |
| Combat, hitbox, frame data, dégâts | [systemes/combat.md](systemes/combat.md) |
| Ennemis, comportements, boss, architecture d'IA | [systemes/ia-ennemis.md](systemes/ia-ennemis.md) |
| XP, niveaux, déblocages, arbres de compétences, méta-progression | [systemes/progression.md](systemes/progression.md) |
| Monnaies, loot, prix, crafting, monétisation | [systemes/economie.md](systemes/economie.md) |
| Courbe de difficulté, équilibrage, stratégies dominantes | [systemes/equilibrage-et-difficulte.md](systemes/equilibrage-et-difficulte.md) |
| Hasard, drops, génération procédurale, seeds | [systemes/aleatoire-et-procedural.md](systemes/aleatoire-et-procedural.md) |
| Coop, PvP, matchmaking, contraintes réseau | [systemes/multijoueur.md](systemes/multijoueur.md) |
| Niveaux, rythme, guidage du joueur, blockout | [contenu/level-design.md](contenu/level-design.md) |
| Histoire, dialogues, choix, narration environnementale | [contenu/narration.md](contenu/narration.md) |
| Tutoriel, premières minutes, apprentissage des mécaniques | [contenu/onboarding-tutoriels.md](contenu/onboarding-tutoriels.md) |
| HUD, menus, feedback, navigation manette | [interface/ui-ux-hud.md](interface/ui-ux-hud.md) |
| Effets sonores, mixage, musique adaptative | [interface/audio.md](interface/audio.md) |
| Options d'accessibilité, sous-titres, daltonisme, remapping | [interface/accessibilite.md](interface/accessibilite.md) |
| Organiser le développement, prototyper, maîtriser le périmètre | [production/processus-et-prototypage.md](production/processus-et-prototypage.md) |
| Préparer un build pour un playtest (stabilité, version, réinitialisation, retours, distribution) | [production/rendre-un-jeu-playtestable.md](production/rendre-un-jeu-playtestable.md) |
| Organiser ou analyser un playtest, télémétrie | [production/playtest-et-metriques.md](production/playtest-et-metriques.md) |
| Rédiger un GDD, une fiche mécanique, un persona, un plan ou un rapport de playtest | [production/templates/](production/templates/) |
| Un vocabulaire précis | [glossaire.md](glossaire.md) |

### Par genre

Les fiches genres servent de point d'entrée : boucle typique, piliers, pièges, jeux de référence, puis renvoi vers les fiches thématiques.

| Genre | Fiche |
|---|---|
| Plateforme | [genres/plateforme.md](genres/plateforme.md) |
| Shooter (top-down, twin-stick, FPS/TPS, shmup) | [genres/shooter.md](genres/shooter.md) |
| Roguelike / roguelite | [genres/roguelike.md](genres/roguelike.md) |
| Puzzle | [genres/puzzle.md](genres/puzzle.md) |
| RPG | [genres/rpg.md](genres/rpg.md) |
| Stratégie (4X, RTS, tactique, tower defense) | [genres/strategie.md](genres/strategie.md) |
| Survie / crafting | [genres/survie-crafting.md](genres/survie-crafting.md) |
| Deckbuilder / jeu de cartes | [genres/deckbuilder-cartes.md](genres/deckbuilder-cartes.md) |

## Structure d'une fiche

`En bref` → `Quand consulter cette fiche` → principes et règles concrètes → anti-patterns → `Checklist` → `Pistes d'implémentation` → `Voir aussi` → `Sources`.

## Modifier ce repo

Si on te demande d'enrichir ce référentiel, suis [CONTRIBUER.md](CONTRIBUER.md) : même format de fiche, pas de statistique ni de source inventée, et mise à jour de cette table de routage, du glossaire et des sources.
