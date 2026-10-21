# Conventions d'assets Tripo — gabarit

Gabarit à copier dans le projet du jeu, par exemple dans `.claude/tripo.md`, puis à remplir. Le skill `tripo:generer` lit ce fichier avant chaque génération. Les valeurs ci-dessous sont des exemples, pas des recommandations : seul le projet décide.

```markdown
# Conventions d'assets générés avec Tripo

## Destination et nommage
- Dossier : res://assets/props/<catégorie>/   (ex. res://assets/props/caisses/)
- Nom de fichier : <catégorie>_<objet>_<variante>.glb, en minuscules et snake_case
  (ex. caisse_bois_01.glb)
- Le fichier .tripo.json reste à côté du modèle et se commite avec lui.

## Budget
- Limite de faces par défaut : 3000 (props de décor), 8000 (props de premier plan)
- Poids maximal d'un fichier : 5 Mo
- Textures : oui, PBR ; qualité standard (detailed sur demande explicite)

## Style
- Direction artistique : (une phrase, ex. « réalisme sale, industriel, années 1980 »)
- Mots à ajouter à chaque prompt : (ex. « game asset, single object, neutral lighting »)
- À éviter (prompt négatif) : (ex. « text, logo, base, pedestal »)

## Échelle et orientation
- 1 unité Godot = 1 m.
- Tailles de référence : porte 2,1 m, caisse standard 0,6 m, personnage 1,8 m.
- Avant de l'objet vers -Z dans Godot, pivot au sol.
- Correction d'échelle : dans l'import Godot (nodes/root_scale), jamais en régénérant.

## Godot
- Binaire : godot   (ou chemin complet, ex. /opt/godot/godot)
- Version : 4.x
- Collisions, LOD, matériaux : (ce que le projet attend après import)

## Crédits
- Accord préalable : dès 2 générations ou une option payante (règle par défaut du skill ;
  écrire « toujours » pour exiger un accord même pour une seule génération)
- Modèle Tripo : v3.1-20260211
```
