# game-design

Référentiel de **game design général**, en français, pensé pour être attaché aux sessions de développement de jeux afin que les agents (Claude Code) s'en servent comme référence quand ils conçoivent, implémentent ou critiquent une mécanique.

Chaque fiche suit le même format : résumé, situations où la consulter, règles concrètes et valeurs de départ, pièges, checklist, pistes d'implémentation, liens et sources. Le point d'entrée pour un agent est [CLAUDE.md](CLAUDE.md), qui contient la table de routage « tâche → fiche ».

## Utiliser le référentiel dans un projet de jeu

**Session Claude Code dans le cloud** : ajouter ce repo aux sources de la session, à côté du repo du jeu. Le skill `game-design` (dans `.claude/skills/`) devient alors disponible, et l'agent peut lire les fiches directement.

**Claude Code en local** : cloner ce repo à côté du projet, puis l'ajouter au contexte avec `claude --add-dir ../game-design`, ou `/add-dir ../game-design` en cours de session.

**Dans tous les cas**, le plus fiable est d'ajouter ces lignes au `CLAUDE.md` du projet de jeu, pour que l'agent sache que le référentiel existe et quand s'en servir :

```markdown
## Référentiel game design
Un référentiel de game design général est disponible dans le repo `game-design`
(attaché à la session, ou cloné dans `../game-design`). Avant de concevoir ou
d'implémenter une mécanique, un système, un niveau ou une interface, lis son
`CLAUDE.md` pour trouver la fiche pertinente et applique-la. Les décisions de
ce projet (GDD, piliers, code existant) priment sur le référentiel.
```

## Contenu

```
fondamentaux/   boucles de gameplay, cadres théoriques (MDA, flow, SDT…), principes de conception
ressenti/       game feel et juice, contrôles et mouvement, caméra
systemes/       combat, IA ennemie, progression, économie, équilibrage et difficulté,
                aléatoire et génération procédurale, multijoueur
contenu/        level design, narration, onboarding et tutoriels
interface/      UI/UX et HUD, audio, accessibilité
genres/         plateforme, shooter, roguelike, puzzle, RPG, stratégie, survie-crafting, deckbuilder
production/     processus et prototypage, playtest et métriques, gabarits (GDD, fiche mécanique, rapport de playtest)
glossaire.md    vocabulaire du game design
sources.md      livres, talks et articles de référence
```

La fiche [ressenti/game-feel-juice.md](ressenti/game-feel-juice.md) contient des pistes d'implémentation spécifiques à Unreal Engine 5 ; les autres fiches sont agnostiques du moteur, avec des notes UE5, Godot ou Unity quand c'est utile.

## Contribuer

Voir [CONTRIBUER.md](CONTRIBUER.md).
