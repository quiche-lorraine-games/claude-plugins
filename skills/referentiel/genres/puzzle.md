# Puzzle

> **En bref** : point d'entrée pour un jeu de réflexion (puzzles logiques, spatiaux, de règles). Ce qui fait la qualité du genre : des règles simples et cohérentes, une idée claire par puzzle, et le moment « aha » où le joueur comprend quelque chose qu'il ne savait pas. Le contenu est la conception des puzzles eux-mêmes.

## Quand consulter cette fiche

- Tu conçois un jeu ou une section de jeu fondée sur des puzzles.
- Des joueurs restent bloqués longtemps, ou au contraire résolvent tout sans réfléchir.
- Tu dois ordonner une série de puzzles ou ajouter un système d'indices.
- Tu hésites entre puzzles conçus à la main et puzzles générés.

## Boucle centrale typique

```
Observer l'état → Formuler une hypothèse → Tester (manipuler)
       ↑                                         ↓
  Nouveau puzzle ← Solution (aha) ← Échec : révise l'hypothèse
```

La récompense principale n'est pas un objet : c'est la **compréhension**. Tout ce qui l'escamote (solution par essais aléatoires, indice trop direct) détruit le plaisir.

## Piliers du genre

1. **Règles simples, conséquences profondes.** Peu de règles qui interagissent. *Baba Is You* et *Stephen's Sausage Roll* tirent des dizaines de niveaux de quelques règles.
2. **Une idée par puzzle.** Chaque puzzle enseigne ou exploite **une** compréhension précise (une interaction entre règles). Si tu ne peux pas énoncer l'idée en une phrase, le puzzle n'est pas prêt.
3. **Cohérence absolue.** Une règle ne change jamais sans être signalée. Le joueur doit pouvoir raisonner.
4. **Lisibilité de l'état.** Tout ce qui compte pour la solution est visible (ou déductible).
5. **Pas de *pixel hunting*.** La difficulté vient de la réflexion, pas de la recherche d'un élément caché.

## Anatomie d'un bon puzzle

- **Fausse piste naturelle** (*red herring* intrinsèque) : la solution évidente échoue, ce qui révèle la contrainte. Bien mieux qu'un leurre ajouté artificiellement.
- **Moment aha** : la solution est courte une fois comprise. Un puzzle dont la solution demande 40 étapes après la compréhension est fastidieux.
- **Espace de recherche réduit** : retirer tout élément qui ne sert pas l'idée. Chaque pièce présente doit compter.
- **Vérification facile** : le joueur sait immédiatement s'il a réussi.

Diagnostic d'un puzzle :

| Question | Si non… |
|---|---|
| Peux-tu énoncer l'idée en une phrase ? | Puzzle flou, à recentrer |
| Tous les éléments servent-ils ? | Retirer le superflu |
| La solution est-elle déductible, pas seulement trouvable par essais ? | Ajouter de l'information ou réduire l'espace |
| La solution échoue-t-elle de façon instructive ? | Rendre les échecs plus parlants |
| Existe-t-il une solution non prévue plus simple ? | Corriger, ou l'accepter si elle est élégante |

## Progression et ordre

- **Introduire** une règle dans un puzzle trivial, **combiner** avec une règle connue, **tordre** (cas limite inattendu). Voir [Onboarding](../contenu/onboarding-tutoriels.md).
- Courbe en **dents de scie** : après un puzzle difficile, un puzzle plus simple qui consolide.
- Offrir **plusieurs puzzles disponibles** en parallèle (*The Witness*, *Baba Is You*) : le joueur bloqué peut aller ailleurs et revenir.
- Rendre optionnels les puzzles les plus durs (zones bonus, étoiles).

## Indices progressifs

- Paliers : 1) orienter l'attention (« regarde ce bloc »), 2) énoncer la contrainte, 3) donner une étape, 4) solution complète.
- Coût léger (monnaie d'indice comme les pièces de *Professeur Layton*, délai) pour éviter le réflexe.
- Proposer l'indice, ne pas l'imposer ; certains joueurs veulent rester bloqués.
- **Annuler** (*undo*) illimité et **réinitialiser** instantané : quasi obligatoires. Ils retirent la punition de l'expérimentation.

## Systémique vs scripté

| | Puzzle scripté (conçu à la main) | Puzzle systémique / généré |
|---|---|---|
| Qualité de l'idée | Élevée, contrôlée | Variable |
| Volume | Coûteux | Illimité |
| Aha | Fort | Rare (plutôt maîtrise) |
| Exemples | *The Witness*, *Portal* | *Tetris*, *Picross* générés, *Sudoku* |

Pour les puzzles générés : utiliser un **solveur** pour garantir une solution (et idéalement l'unicité), puis classer par difficulté (nombre d'étapes de déduction). Voir [Aléatoire et procédural](../systemes/aleatoire-et-procedural.md).

## Pièges fréquents

- Puzzles de « lecture dans les pensées du designer » (logique arbitraire, objet improbable).
- Règle introduite sans avoir été montrée.
- Exécution exigeante (timing serré) sur un puzzle de réflexion : frustrant, la compréhension ne suffit plus.
- Pas d'undo : chaque erreur oblige à refaire de longues séquences.
- Trop d'éléments : le joueur essaie toutes les combinaisons au lieu de réfléchir.
- Solutions non prévues qui court-circuitent un chapitre entier (tester avec un solveur si possible).

## Jeux de référence à étudier

- *Portal* (2007) — chambres de test : chaque salle introduit ou combine une idée.
- *The Witness* (2016) — enseignement sans texte par séries de panneaux, plusieurs chemins parallèles.
- *Baba Is You* (2019) — règles manipulables, solutions élégantes, undo.
- *Stephen's Sausage Roll* (2016) — profondeur extrême à partir de règles minimales.
- *Snakebird* (2015) — difficulté par contraintes très serrées.
- *Professeur Layton* — système d'indices payants à paliers.
- *Return of the Obra Dinn* (2018) — déduction, vérification par paquets de trois pour éviter le brute-force.

## Checklist

- [ ] Chaque puzzle a une idée énoncée en une phrase dans le doc de design.
- [ ] Toute règle est montrée avant d'être exigée.
- [ ] Undo et reset disponibles et instantanés.
- [ ] Tout élément inutile à l'idée est retiré.
- [ ] L'ordre des puzzles alterne difficulté et consolidation.
- [ ] Le joueur bloqué a une alternative (autre puzzle, indice).
- [ ] Les puzzles ont été testés par des joueurs qui ne connaissent pas la solution.
- [ ] Temps de résolution médian mesuré par puzzle (voir [Playtest et métriques](../production/playtest-et-metriques.md)).

## Pistes d'implémentation

- Modéliser l'état du puzzle comme une **structure de données pure** (grille, liste d'entités), séparée de l'affichage : undo = pile d'états, solveur = recherche sur cet état.
- Solveur en recherche en largeur (BFS) sur les états pour les petits puzzles : vérifie la solvabilité et la longueur minimale de solution.
- Rendu et animations dérivés de l'état ; les animations peuvent être accélérées ou sautées sans changer la logique.

## Voir aussi

- [Principes de conception](../fondamentaux/principes-de-conception.md)
- [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)
- [Level design](../contenu/level-design.md)
- [Aléatoire et procédural](../systemes/aleatoire-et-procedural.md)
- [Playtest et métriques](../production/playtest-et-metriques.md)

## Sources

- Jonathan Blow, conférences sur la conception de puzzles et de *The Witness* (notamment « Designing to Reveal the Nature of the Universe », IndieCade 2011).
- Valve, commentaires développeurs de *Portal* (2007).
- Mark Brown, *Game Maker's Toolkit*, vidéos sur la conception de puzzles (YouTube).
