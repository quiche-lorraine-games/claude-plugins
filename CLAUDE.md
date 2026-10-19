# game-design — instructions pour travailler sur ce repo

Ce repo est un **plugin Claude Code** (et sa propre marketplace) qui distribue un référentiel de game design. Il ne contient pas de code de jeu. Si tu cherches à te servir du référentiel pour un jeu, lis [skills/referentiel/SKILL.md](skills/referentiel/SKILL.md).

## Structure

```
.claude-plugin/plugin.json        manifeste du plugin « game-design »
.claude-plugin/marketplace.json   marketplace « quiche-lorraine-games », qui pointe vers ce repo (source ".")
hooks/hooks.json                  hook SessionStart qui affiche hooks/rappel.md
hooks/rappel.md                   rappel injecté au démarrage des sessions (garder court)
skills/referentiel/SKILL.md       point d'entrée du skill : règles d'usage et table de routage
skills/referentiel/<dossiers>/    les fiches (fondamentaux, ressenti, systemes, contenu, interface, genres, production)
skills/referentiel/glossaire.md   glossaire
skills/referentiel/sources.md     bibliographie
```

## Règles

- Toute fiche vit sous `skills/referentiel/` : seul le contenu du plugin est installé chez l'utilisateur, un fichier hors du dossier du skill ne serait pas lisible par l'agent.
- Les liens entre fiches sont **relatifs** et ne sortent jamais de `skills/referentiel/`.
- `SKILL.md` doit rester sous 500 lignes, et sa `description` sous environ 1 500 caractères (au-delà, elle est tronquée dans la liste des skills).
- Pas de champ `version` dans les manifestes : les utilisateurs suivent les commits de la branche par défaut.
- Pour ajouter ou modifier une fiche, suivre [CONTRIBUER.md](CONTRIBUER.md).

## Vérifier avant de pousser

```bash
claude plugin validate .
```

Et vérifier que tous les liens relatifs des fichiers Markdown pointent vers des fichiers existants.
