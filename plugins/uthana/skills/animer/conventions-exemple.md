# Conventions d'animation Uthana — gabarit

Gabarit à copier dans le projet du jeu, par exemple dans `.claude/uthana.md`, puis à remplir. Le skill `uthana:animer` lit ce fichier avant chaque génération. Les valeurs ci-dessous sont des exemples, pas des recommandations : seul le projet décide.

```markdown
# Conventions d'animation générées avec Uthana

## Personnages
| Personnage | character_id Uthana | Fichier source | Squelette |
|---|---|---|---|
| Garde | cAbc123def45 | res://assets/persos/garde.glb (Tripo) | Mixamo (rigging Uthana) |
| Test | tar (fourni) | — | Mixamo |

## Destination et nommage
- Dossier : res://assets/anims/<personnage>/
- Nom : <personnage>_<action>[_<variante>].glb, en minuscules et snake_case (ex. garde_salut.glb)
- La fiche .uthana.json reste à côté et se commite avec l'animation.

## Export
- Format : .glb, 30 i/s
- Maillage : sans (--sans-maillage) ; les animations vont dans une bibliothèque d'animations
  ajoutée à l'AnimationPlayer du personnage
- Déplacement : sur place (--sur-place) ; le CharacterBody3D se déplace en code

## Modèles
- Animations : text-to-motion 3.0 ; premiers jets en 3.0-mini
- Locomotion : style neutral_male_a, vitesse marche 1.4 m/s, course 3.5 m/s

## Godot
- Binaire : godot
- Boucle : Loop Mode Linear dans l'import pour les idles et la locomotion

## Crédits
- Accord préalable : dès 2 générations ou un rigging (règle par défaut du skill)
- Compte : paiement à l'usage, crédit acheté (usage commercial sans mention)
```
