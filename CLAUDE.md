# claude-plugins — instructions pour travailler sur ce repo

Ce repo est la **marketplace de plugins Claude Code** `quiche-lorraine-games`. Chaque plugin vit dans son propre dossier sous `plugins/`. Il ne contient pas de code de jeu.

## Structure

```
.claude-plugin/marketplace.json   liste des plugins de la marketplace
plugins/<plugin>/
  .claude-plugin/plugin.json      manifeste du plugin
  skills/<skill>/SKILL.md         skills du plugin (fichiers de support dans le même dossier)
  hooks/hooks.json                hooks du plugin (optionnel)
  README.md                       présentation et usage du plugin
README.md                         présentation de la marketplace, installation, mises à jour
```

Plugins actuels :
- `plugins/game-design/` : référentiel de game design. Pour modifier ses fiches, suivre [plugins/game-design/CONTRIBUER.md](plugins/game-design/CONTRIBUER.md).

## Règles

- Un plugin n'installe que le contenu de son dossier : tout fichier dont un skill a besoin doit être dans le dossier du plugin, et de préférence dans le dossier du skill. Les liens relatifs d'un skill ne sortent jamais de son dossier.
- Un `SKILL.md` reste sous 500 lignes, et sa `description` sous environ 1 500 caractères (au-delà, elle est tronquée dans la liste des skills).
- Pas de champ `version` dans les manifestes : les utilisateurs suivent les commits de la branche par défaut.
- Un hook `SessionStart` s'exécute dans chaque session où le plugin est activé : son texte doit rester très court.

## Ajouter un plugin

1. Créer `plugins/<nom>/.claude-plugin/plugin.json` (au minimum `name`, plus `description`, `author`, `repository`).
2. Ajouter ses composants (`skills/`, `hooks/`, `agents/`…) à la racine du dossier du plugin, pas dans `.claude-plugin/`.
3. Ajouter une entrée dans `.claude-plugin/marketplace.json` avec `"source": "./plugins/<nom>"`.
4. Ajouter le plugin au tableau du [README.md](README.md) et lui écrire son propre `README.md`.

## Vérifier avant de pousser

```bash
claude plugin validate .
claude plugin validate plugins/<nom>
```

Puis vérifier que tous les liens relatifs des fichiers Markdown pointent vers des fichiers existants. Pour un test réel : `claude plugin marketplace add ./`, `claude plugin install <nom>@quiche-lorraine-games`, une session dans un dossier vierge, puis désinstaller.
