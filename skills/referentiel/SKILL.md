---
name: referentiel
description: Référentiel de game design général en français (boucles de jeu, game feel, contrôles, caméra, combat, IA ennemie, progression, économie, équilibrage, aléatoire et procédural, multijoueur, level design, narration, onboarding, UI/UX, audio, accessibilité, profils de joueurs, fiches par genre, prototypage, playtest, gabarits de GDD). À charger dès qu'on conçoit, implémente, règle ou critique une mécanique, un système, un niveau ou une interface de jeu vidéo, qu'on prépare ou analyse un playtest, ou qu'on rédige un GDD, une fiche mécanique, un persona ou un rapport de playtest.
---

# Référentiel game design

Base de connaissances de game design, indépendante de tout projet, pour servir de référence pendant le développement d'un jeu. Les fiches sont dans le même dossier que ce fichier.

## Comment s'en servir

1. **Le projet prime.** Si le projet de jeu a son propre GDD, ses piliers ou des décisions déjà prises, ils l'emportent sur ce référentiel. Ici, ce sont des conseils par défaut, pas des règles imposées.
2. **Lis la fiche avant d'agir.** Avant de concevoir ou d'implémenter une mécanique, repère la fiche pertinente dans la table ci-dessous et lis-la (au minimum « Quand consulter », les règles concrètes et la checklist). Inutile de tout lire : une à trois fiches suffisent en général.
3. **Valeurs chiffrées = points de départ.** Les valeurs données (durées, ratios, courbes) servent à amorcer un réglage. Expose-les comme paramètres modifiables (data asset, fichier de config, variables exportées), jamais en dur.
4. **Gameplay ou présentation ?** Les fiches distinguent ce qui change la logique de jeu (gameplay) de ce qui n'est que du retour visuel ou sonore (présentation, *juice*). Ne laisse jamais un effet de présentation modifier la logique.
5. **Cite tes sources.** Quand une proposition s'appuie sur une fiche, mentionne-la (ex. « cf. référentiel game design, `ressenti/controles-et-mouvement.md`, coyote time »), pour que l'humain puisse vérifier.
6. **Déroule la checklist.** Chaque fiche se termine par une checklist : utilise-la pour auditer une fonctionnalité ou préparer une revue.
7. **Les gabarits se copient dans le projet.** Les fichiers de `production/templates/` se remplissent dans le repo du jeu (ex. `docs/`), jamais ici.

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
| Savoir si un build peut partir en playtest : le minimum à avoir | [production/rendre-un-jeu-playtestable.md](production/rendre-un-jeu-playtestable.md) |
| Organiser ou analyser un playtest, télémétrie | [production/playtest-et-metriques.md](production/playtest-et-metriques.md) |
| Rédiger un GDD | [production/templates/gdd-une-page.md](production/templates/gdd-une-page.md) |
| Spécifier une mécanique | [production/templates/fiche-mecanique.md](production/templates/fiche-mecanique.md) |
| Décrire un joueur type | [production/templates/persona-joueur.md](production/templates/persona-joueur.md) |
| Préparer une session de playtest | [production/templates/plan-playtest.md](production/templates/plan-playtest.md) |
| Rendre compte d'un playtest | [production/templates/rapport-playtest.md](production/templates/rapport-playtest.md) |
| Un vocabulaire précis | [glossaire.md](glossaire.md) |
| Approfondir un sujet (livres, talks, articles) | [sources.md](sources.md) |

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
