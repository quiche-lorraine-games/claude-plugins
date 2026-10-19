# claude-plugins

Marketplace de plugins Claude Code de Quiche Lorraine Games (`quiche-lorraine-games`).

## Plugins

| Plugin | Contenu |
|---|---|
| [game-design](plugins/game-design/) | Référentiel de game design général en français : fiches thématiques, fiches genres, gabarits, glossaire et sources, consultés par les agents pendant le développement d'un jeu. |

## Installation

**Claude Code en ligne de commande** (une fois par machine, valable pour tous les projets) :

```bash
claude plugin marketplace add quiche-lorraine-games/claude-plugins
claude plugin install <plugin>@quiche-lorraine-games
```

Ou depuis une session : `/plugin marketplace add quiche-lorraine-games/claude-plugins`, puis `/plugin install <plugin>@quiche-lorraine-games`.

Si le repo est privé, la machine doit pouvoir le cloner avec tes identifiants git habituels.

Si la marketplace avait été ajoutée sous l'ancien nom du repo (`game-design`), la remettre sur le nouveau :

```bash
claude plugin marketplace remove quiche-lorraine-games
claude plugin marketplace add quiche-lorraine-games/claude-plugins
claude plugin install game-design@quiche-lorraine-games
```

**Sessions Claude Code dans le cloud** : les plugins activés seulement dans tes réglages locaux ne sont pas chargés dans le cloud. Deux possibilités :
- dans un Project, ajouter le plugin dans les réglages du Project, rubrique Plugins ;
- pour toute une organisation, l'activer dans les réglages gérés (*managed settings*) de l'organisation sur claude.ai, avec `extraKnownMarketplaces` et `enabledPlugins`.

## Mises à jour

Les plugins n'ont pas de numéro de version : une installation suit les commits de la branche par défaut. Pour récupérer les nouveautés :

```bash
claude plugin marketplace update quiche-lorraine-games
claude plugin update <plugin>@quiche-lorraine-games
```

En session : `/plugin marketplace update quiche-lorraine-games`, puis `/reload-plugins`. On peut aussi activer la mise à jour automatique de la marketplace dans `/plugin`, rubrique Marketplaces.

## Ajouter un plugin

Voir [CLAUDE.md](CLAUDE.md).
