# Roguelike et roguelite

> **En bref** : point d'entrée pour un jeu à *runs* — mort permanente, contenu généré ou recombiné, montée en puissance par synergies. Ce qui fait la qualité du genre : chaque run raconte une histoire différente, les décisions se cumulent en *builds*, et l'échec apprend quelque chose au joueur.

## Quand consulter cette fiche

- Tu conçois un jeu avec mort permanente et des runs rejouables.
- Les runs se ressemblent toutes, ou un build domine les autres.
- Tu dois décider de la place de la méta-progression (déblocages entre les runs).
- Tu dois fixer la durée d'une run et sa structure (étages, actes, boss).

## Roguelike ou roguelite

- **Roguelike** (sens strict) : héritier de *Rogue* (1980). L'**Interprétation de Berlin** (2008) liste des facteurs :
  - *Haute valeur* : environnement généré aléatoirement, mort permanente, tour par tour, grille, non modal (tout se fait dans le même mode), complexité (plusieurs solutions), gestion de ressources, combat (*hack'n'slash*), exploration et découverte.
  - *Faible valeur* : un seul personnage, monstres soumis aux mêmes règles que le joueur, défi tactique, affichage ASCII, donjons, chiffres affichés.
- **Roguelite** (usage courant) : garde runs + mort permanente + génération, mais souvent en temps réel et avec **méta-progression** persistante.

L'étiquette importe peu : ce qui compte est le contrat avec le joueur — combien il perd en mourant et ce qu'il garde.

## Boucle centrale typique

```
Début de run → Rencontres (combat / événement) → Récompense = choix parmi N
       ↑                                                  ↓
 Méta-progression ← Mort ou victoire ← Boss ← Build qui se construit
```

- **Rencontre** : quelques secondes à quelques minutes.
- **Run** : la vraie unité de jeu.
- **Méta** : déblocages (nouveaux objets dans le pool, personnages, niveaux de difficulté).

## Piliers du genre

1. **Variété par recombinaison** : peu de pièces bien conçues qui se combinent valent mieux que beaucoup de contenu. Voir [Aléatoire et procédural](../systemes/aleatoire-et-procedural.md).
2. **Choix de récompense** : proposer 2 à 4 options et en faire choisir une. Le choix fait le build.
3. **Synergies** : des objets qui deviennent forts **ensemble**. Le plaisir du « build cassé » est central.
4. **Échec instructif** : la mort doit être compréhensible et apprendre quelque chose (connaissance > puissance).
5. **Redémarrage rapide** : relancer une run en quelques secondes.

## Mécaniques clés

| Mécanique | Conseil |
|---|---|
| Durée de run | Choisir et annoncer un ordre de grandeur (ex. 20–60 min pour la plupart des roguelites modernes). Une run longue rend la mort coûteuse. |
| Structure | Actes / biomes avec boss intermédiaires : jalons, montée de difficulté, points de décision. |
| Choix de route | Carte à embranchements (*Slay the Spire*, *Hades*) : le joueur choisit risque vs récompense. |
| Économie de run | Monnaie dépensée en boutique pendant la run, perdue à la mort. Voir [Économie](../systemes/economie.md). |
| Pool d'objets | Retirer les objets déjà obtenus, pondérer par rareté, garantir des options utiles. |
| Seeds | Graine affichée et partageable : debug, défis, speedrun. |
| Difficulté croissante | Niveaux de difficulté optionnels après la première victoire (*Ascension*, *Heat*). Voir [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md). |

## Méta-progression : doser

| Approche | Avantage | Risque |
|---|---|---|
| Aucune (connaissance seule) | Victoire = compétence pure | Courbe d'entrée raide |
| Déblocage de variété (nouveaux objets, persos) | Renouvelle sans rendre la run triviale | Pool dilué si trop d'objets faibles |
| Bonus de puissance permanents | Accessible, chaque run « compte » | Le jeu devient un grind, la victoire n'a plus de sens |

Règle : préférer **élargir les options** plutôt qu'augmenter la puissance brute. Si bonus de puissance, les plafonner et permettre de les désactiver. Détails : [Progression](../systemes/progression.md).

## Concevoir les synergies

- Donner à chaque objet un **axe** (dégâts de poison, nombre de projectiles, critiques, défense…) et créer des objets multiplicateurs sur ces axes.
- Mélanger objets **autonomes** (utiles seuls) et objets **de synergie** (forts avec d'autres) : sinon les premiers choix sont des paris.
- Accepter des combinaisons très fortes — elles font les meilleures histoires — mais éviter qu'un objet unique gagne seul la run.
- Surveiller les stratégies dominantes avec des métriques (taux de victoire par objet). Voir [Playtest et métriques](../production/playtest-et-metriques.md).

## Pièges fréquents

- **Génération « bruit »** : du contenu aléatoire sans structure = des runs toutes pareilles. L'aléatoire doit produire des **situations** différentes.
- Morts injustes : piège invisible, ennemi hors écran, combo aléatoire imparable.
- Début de run répétitif et long : le joueur rejoue 10 minutes ennuyeuses avant l'intéressant.
- Trop de choix sans information : le joueur ne peut pas évaluer les objets (texte flou).
- Méta-progression qui rend les premières runs volontairement frustrantes.
- RNG de récompense trop faible → runs « mortes » sans espoir dès le début.

## Jeux de référence à étudier

- *Spelunky* (2008/2012) — génération par gabarits de salles, systèmes qui interagissent, échec instructif.
- *The Binding of Isaac* (2011) — immense pool d'objets à synergies, mais lisibilité variable.
- *Slay the Spire* (2019) — carte à embranchements, intentions ennemies affichées, Ascension.
- *Hades* (2020) — méta-progression narrative, la mort fait avancer l'histoire.
- *Dead Cells* (2018) — action, biomes interchangeables, déblocages de variété.
- *Balatro* (2024) — synergies multiplicatives et lisibles.
- *Brogue* (2009) — roguelike classique, élégance et lisibilité.

## Checklist

- [ ] La durée cible d'une run est définie.
- [ ] Relancer une run prend moins de 10 secondes.
- [ ] Chaque récompense est un choix entre plusieurs options.
- [ ] Les objets ont des axes de synergie identifiables.
- [ ] La cause de chaque mort est compréhensible après coup.
- [ ] La méta-progression élargit les options plus qu'elle n'augmente la puissance.
- [ ] Les seeds sont reproductibles (même graine = même run).
- [ ] Métriques par objet / personnage pour repérer les dominants.
- [ ] Le début de run est court et varié.

## Pistes d'implémentation

- Un générateur pseudo-aléatoire **par sous-système** (carte, loot, combat) dérivé de la seed : un changement dans un système ne décale pas les autres.
- Objets décrits en données (tags d'axes, modificateurs) plutôt qu'en code spécifique.
- Pipeline de modificateurs ordonné (additifs puis multiplicatifs) pour garder les synergies prévisibles. Voir [Combat](../systemes/combat.md).

## Voir aussi

- [Aléatoire et procédural](../systemes/aleatoire-et-procedural.md)
- [Progression](../systemes/progression.md)
- [Économie](../systemes/economie.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [Deckbuilder et jeux de cartes](deckbuilder-cartes.md)
- [Shooter](shooter.md) — pour les roguelites de tir

## Sources

- « Berlin Interpretation », International Roguelike Development Conference, Berlin, 2008 — RogueBasin.
- Derek Yu, *Spelunky*, Boss Fight Books, 2016.
- Anthony Giovannetti (Mega Crit), « Slay the Spire: Metrics Driven Design and Balance », GDC 2019.
- Supergiant Games, *Hades* ; présentations de l'équipe sur la narration intégrée à la méta-progression.
