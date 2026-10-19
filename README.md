# game-design

Plugin Claude Code qui fournit un référentiel de **game design général**, en français, pour que les agents s'en servent comme référence quand ils conçoivent, implémentent ou critiquent une mécanique, un système, un niveau, une interface ou un playtest.

Le plugin contient :
- **le skill `game-design:referentiel`** : une table de routage « tâche → fiche » et une quarantaine de fiches, dont 8 fiches genres, 5 gabarits, un glossaire et une bibliographie ;
- **un hook de démarrage** qui rappelle à l'agent, en une phrase, que le référentiel existe et quand le charger.

Chaque fiche suit le même format : résumé, situations où la consulter, règles concrètes et valeurs de départ, pièges, checklist, pistes d'implémentation, liens et sources.

## Installation

Le repo sert aussi de marketplace (`quiche-lorraine-games`).

**Claude Code en ligne de commande** (une fois par machine, valable pour tous les projets) :

```bash
claude plugin marketplace add quiche-lorraine-games/game-design
claude plugin install game-design@quiche-lorraine-games
```

Ou depuis une session : `/plugin marketplace add quiche-lorraine-games/game-design`, puis `/plugin install game-design@quiche-lorraine-games`.

Si le repo est privé, la machine doit pouvoir le cloner avec tes identifiants git habituels.

**Sessions Claude Code dans le cloud** : les plugins activés seulement dans tes réglages locaux ne sont pas chargés dans le cloud. Deux possibilités :
- dans un Project, l'ajouter dans les réglages du Project, rubrique Plugins ;
- pour toute une organisation, l'activer dans les réglages gérés (*managed settings*) de l'organisation sur claude.ai, avec `extraKnownMarketplaces` et `enabledPlugins`.

**Mise à jour** : le plugin n'a pas de numéro de version, l'installation suit donc les commits de la branche par défaut. Pour récupérer les nouveautés :

```bash
claude plugin marketplace update quiche-lorraine-games
claude plugin update game-design@quiche-lorraine-games
```

En session : `/plugin marketplace update quiche-lorraine-games`, puis `/reload-plugins`. On peut aussi activer la mise à jour automatique de la marketplace dans `/plugin`, rubrique Marketplaces.

## Utilisation

Une fois le plugin installé, rien à faire : le hook de démarrage signale le référentiel à l'agent, qui charge le skill quand la tâche porte sur le jeu. On peut aussi le demander explicitement avec `/game-design:referentiel`.

Pour un projet où le référentiel doit être systématiquement consulté, ajouter au `CLAUDE.md` du jeu :

```markdown
## Référentiel game design
Avant de concevoir ou d'implémenter une mécanique, un système, un niveau ou une
interface, charge le skill `game-design:referentiel` et applique la fiche
pertinente. Les décisions de ce projet (GDD, piliers, code existant) priment
sur le référentiel.
```

## Contenu

```
skills/referentiel/
  SKILL.md        règles d'usage et table de routage
  fondamentaux/   boucles de gameplay, cadres théoriques (MDA, flow, SDT…), principes de conception,
                  profils de joueurs
  ressenti/       game feel et juice, contrôles et mouvement, caméra
  systemes/       combat, IA ennemie, progression, économie, équilibrage et difficulté,
                  aléatoire et génération procédurale, multijoueur
  contenu/        level design, narration, onboarding et tutoriels
  interface/      UI/UX et HUD, audio, accessibilité
  genres/         plateforme, shooter, roguelike, puzzle, RPG, stratégie, survie-crafting, deckbuilder
  production/     processus et prototypage, rendre un jeu playtestable, playtest et métriques,
                  gabarits (GDD, fiche mécanique, persona, plan et rapport de playtest)
  glossaire.md    vocabulaire du game design
  sources.md      livres, talks et articles de référence
```

La fiche [game feel et juice](skills/referentiel/ressenti/game-feel-juice.md) contient des pistes d'implémentation spécifiques à Unreal Engine 5 ; les autres fiches sont agnostiques du moteur, avec des notes UE5, Godot ou Unity quand c'est utile.

## Contribuer

Voir [CONTRIBUER.md](CONTRIBUER.md).
