# Survie et crafting

> **En bref** : point d'entrée pour les jeux de survie, de crafting, de construction de base et d'automatisation. Ce qui fait la qualité du genre : une pression constante mais gérable, une progression matérielle visible (de la hutte à la forteresse, de l'outil en pierre à l'usine), et un monde dangereux qui donne envie d'explorer.

## Quand consulter cette fiche

- Tu conçois un jeu avec jauges de besoins (faim, soif, froid), récolte et fabrication.
- Les besoins sont perçus comme des corvées.
- Le milieu de partie est vide : la survie est acquise et rien ne motive à continuer.
- Tu dois concevoir un arbre de recettes ou un système de construction.

## Boucle centrale typique

```
Explorer → Récolter → Fabriquer (outils, armes, abri) → Survivre à la pression (nuit, faim, météo, monstres)
    ↑                                                                    ↓
 Zones plus dangereuses ← Nouvelles recettes / meilleurs outils ← Ressources plus rares
```

- **Court terme** : satisfaire un besoin, éviter un danger.
- **Moyen terme** : améliorer l'abri, débloquer un palier technologique.
- **Long terme** : objectif final (boss, évasion, fusée, colonie autonome) ou sandbox créatif.

## Piliers du genre

1. **Pression qui force des décisions** : la faim, le froid ou la nuit obligent à arbitrer entre sécurité et exploration.
2. **Progression matérielle tangible** : chaque palier change la façon de jouer (outil en fer = nouvelles ressources, nouvelles zones).
3. **Monde qui récompense l'exploration** : ressources rares, lieux, histoire environnementale.
4. **Expression du joueur** : base, organisation, style de survie.

## Besoins et pression

| Conseil | Pourquoi |
|---|---|
| Peu de jauges (2–4) avec des conséquences distinctes | Chaque jauge doit créer une décision différente, pas un entretien de plus |
| Décroissance lente, effets progressifs | Les malus graduels (lenteur, vision réduite) avant la mort laissent le temps de réagir |
| La pression diminue à mesure que le joueur progresse | Sinon les besoins restent des corvées ; la pression doit migrer vers de nouveaux défis |
| Solutions durables | Un frigo, une ferme, un puits : le joueur investit pour automatiser un besoin |
| Afficher clairement l'état et la cause | Le joueur sait pourquoi il a froid et quoi faire |

Cycle **jour / nuit** : la nuit est un rythme naturel de tension (danger accru, visibilité réduite) puis de relâchement (jour). C'est aussi un minuteur qui structure la session. Durée à régler pour laisser une vraie phase d'activité de jour.

## Crafting

- **Recettes découvrables** de façon lisible : par l'obtention d'un ingrédient, par un établi, par exploration. Éviter d'obliger à consulter un wiki (*Minecraft* à ses débuts est l'exemple souvent cité d'un crafting opaque, corrigé depuis par le livre de recettes).
- Chaque nouvelle recette doit **ouvrir une possibilité**, pas seulement +10 % de stats.
- Paliers clairs (pierre → cuivre → fer…) avec un objectif visible au palier suivant.
- **Établis / stations** : spatialisent la progression dans la base.
- Coût en ressources lisible avant la récolte (afficher les ingrédients manquants).

## Construction de base

- Grille ou placement libre avec accroche (*snapping*) : la grille facilite la lisibilité et l'IA.
- La base doit avoir une **fonction** (stockage, production, protection, confort) en plus d'être décorative.
- Défense de base : attaques signalées à l'avance et limitées pour ne pas punir les joueurs créatifs ; option pour les désactiver.

## Automatisation (variante usine)

- Le jeu passe de « faire » à « concevoir des systèmes qui font » (*Factorio*, *Satisfactory*).
- Ratios de production lisibles, goulets d'étranglement visibles.
- Chaque palier multiplie l'échelle ; le joueur refait sa base plusieurs fois, ce qui est le plaisir.

## Grind : le doser

- Récolte répétitive = acceptable si elle est **rapide et satisfaisante** (feedback de récolte, sons) et si elle sert un objectif clair.
- Réduire le grind au fil de la progression (meilleurs outils = récolte plus rapide, automatisation).
- Inventaire : pile généreuse, tri automatique, coffres proches des stations. La gestion d'inventaire est le premier ennemi du rythme.

## Pièges fréquents

- Besoins trop rapides : le joueur mange toutes les 2 minutes au lieu d'explorer.
- Milieu de partie vide : la survie est réglée, plus d'objectif.
- Crafting opaque (wiki obligatoire).
- Inventaire saturé qui force des allers-retours constants.
- Mort qui fait perdre des heures sans prévenir (proposer des niveaux de pénalité).
- Monde généré sans repères ni lieux mémorables.

## Jeux de référence à étudier

- *Minecraft* (2011) — liberté, paliers de matériaux, nuit dangereuse.
- *Don't Starve* (2013) — besoins multiples (faim, santé, santé mentale), saisons, mort coûteuse.
- *Subnautica* (2018) — exploration guidée par la profondeur, peur, narration environnementale.
- *Valheim* (2021) — boss comme jalons de progression, construction avec intégrité structurelle.
- *The Long Dark* — survie lente et réaliste, pression météo.
- *Factorio* (2020) — automatisation, ratios, refonte de base.
- *Frostpunk* (2018) — survie de colonie, choix moraux sous pression.

## Checklist

- [ ] Chaque jauge de besoin crée une décision distincte.
- [ ] Les besoins peuvent être automatisés ou allégés en progressant.
- [ ] Chaque palier technologique change la manière de jouer.
- [ ] Les recettes sont découvrables sans wiki.
- [ ] Le joueur a toujours un objectif suivant visible.
- [ ] La gestion d'inventaire est réduite au minimum.
- [ ] La pénalité de mort est connue et paramétrable.
- [ ] Le milieu de partie (après la survie de base) a ses propres objectifs.

## Pistes d'implémentation

- Recettes en données : `{ ingrédients[], station requise, produit, temps }`. L'arbre de déblocage se déduit des données.
- Jauges de besoins dans un composant unique avec taux de décroissance et seuils de malus configurables.
- Simulation hors champ simplifiée (zones non chargées : calcul approximatif de la production au retour du joueur).
- Grille de construction : stocker la base comme une liste de pièces + positions sur la grille, pratique pour sauvegarde et validation.

## Voir aussi

- [Boucles de gameplay](../fondamentaux/boucles-de-gameplay.md)
- [Progression](../systemes/progression.md)
- [Économie](../systemes/economie.md)
- [Aléatoire et procédural](../systemes/aleatoire-et-procedural.md)
- [UI, UX et HUD](../interface/ui-ux-hud.md) — inventaires
- [Level design](../contenu/level-design.md)
- [Narration](../contenu/narration.md) — narration environnementale

## Sources

- Jesse Schell, *The Art of Game Design: A Book of Lenses*, 3e éd., CRC Press, 2019.
- Ernest Adams, *Fundamentals of Game Design*, 3e éd., New Riders, 2014.
