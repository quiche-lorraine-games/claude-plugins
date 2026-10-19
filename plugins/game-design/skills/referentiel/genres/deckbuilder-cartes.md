# Deckbuilder et jeux de cartes

> **En bref** : point d'entrée pour les jeux de cartes — deckbuilders (le deck se construit pendant la partie), roguelikes deckbuilders, jeux de cartes à collectionner (CCG/TCG) numériques. Ce qui fait la qualité du genre : chaque pioche pose un petit puzzle, le deck devient l'expression d'une stratégie, et les cartes restent lisibles malgré leur nombre.

## Quand consulter cette fiche

- Tu conçois un jeu où l'action passe par des cartes piochées.
- Les decks convergent vers une seule stratégie, ou les parties dépendent trop de la chance de pioche.
- Tu dois rédiger des textes de cartes, fixer des coûts ou une rareté.
- Tu hésites entre deckbuilding en partie, collection persistante, ou les deux.

## Boucle centrale typique

```
Piocher une main → Jouer des cartes (coût en énergie/mana) → Résoudre les effets
       ↑                                                          ↓
 Défausser, mélanger ← Fin de tour ← Ennemi agit
Méta (deckbuilder) : Récompense = ajouter / retirer / améliorer une carte → deck modifié pour le combat suivant
```

Deux niveaux de décision : **tactique** (quelle carte jouer ce tour) et **stratégique** (quelles cartes mettre dans le deck).

## Variantes

| Variante | Construction du deck | Références |
|---|---|---|
| Deckbuilder (plateau) | Pendant la partie, à partir d'un marché commun | *Dominion* (2008, Donald X. Vaccarino, à l'origine du genre) |
| Roguelike deckbuilder | Pendant la run, par récompenses | *Slay the Spire*, *Monster Train*, *Inscryption* |
| CCG / TCG | Avant la partie, depuis une collection | *Magic: The Gathering*, *Hearthstone*, *Marvel Snap* |
| Hybride cartes + scoring | Deck et modificateurs de score | *Balatro* (poker + jokers) |

## Piliers du genre

1. **Lisibilité des cartes** : une carte se comprend en quelques secondes.
2. **Synergies** : les cartes se combinent en archétypes (poison, défense, combos, sacrifice…).
3. **Gestion de la variance** : la chance de pioche crée de la variété, la compétence la maîtrise.
4. **Décisions de deck significatives** : ajouter une carte a un coût (dilution).

## Mécaniques clés

| Mécanique | Conseil / repère |
|---|---|
| Taille de main | 5 cartes piochées par tour est un standard (*Dominion*, *Slay the Spire*) |
| Ressource par tour | Énergie fixe (3 dans *Slay the Spire*) = puzzle constant ; mana croissante (*Hearthstone*) = courbe de puissance sur la partie |
| Taille de deck | Petit deck = cohérence et pioche des meilleures cartes ; grand deck = variance |
| **Dilution** | Toute carte ajoutée réduit la probabilité de piocher les autres. Proposer **toujours** de passer une récompense. |
| ***Thinning*** (épuration) | Retirer des cartes faibles augmente la qualité moyenne de la main ; mécanique clé à proposer (boutique, événements) |
| Amélioration | Améliorer une carte existante sans diluer le deck |
| Mots-clés | Effets récurrents nommés (« Vulnérable », « Bloc ») plutôt que réécrits à chaque carte |
| Intentions ennemies | Afficher l'action ennemie du prochain tour (*Slay the Spire*) : transforme chaque tour en puzzle de réponse |

Probabilités de pioche : utiliser la **loi hypergéométrique** (tirage sans remise) pour estimer la chance de piocher au moins une carte donnée dans une main. Utile pour régler taille de deck et nombre d'exemplaires.

## Coûts et équilibrage

- Établir une **courbe de coût** : valeur attendue d'un point de ressource (ex. 1 énergie ≈ X dégâts ou Y bloc), puis évaluer chaque carte par rapport à elle. Voir [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md).
- Les cartes « en dessous de la courbe » doivent avoir une synergie qui les justifie.
- Cartes à 0 coût, pioche supplémentaire et gain de ressources sont les plus dangereuses pour l'équilibre (boucles infinies) : les surveiller et les tester en premier.
- Rareté : les cartes **communes** forment la base de chaque archétype, les **rares** changent la façon de jouer. Une rare ne doit pas être simplement « une commune en mieux ».

## Lisibilité des cartes

- Hiérarchie fixe : **coût** (coin, souvent en haut à gauche), **nom**, **illustration**, **type**, **texte d'effet**, éventuellement valeurs (attaque/PV).
- Gabarit de texte constant : même formulation pour le même effet (« Inflige 6 dégâts. »).
- Valeurs modifiées affichées en couleur (vert = augmenté, rouge = réduit) sur la carte même.
- Infobulles pour les mots-clés.
- Couleur ou cadre selon le type / la classe / l'archétype (*Magic* et son « camembert de couleurs », *color pie*, identité mécanique de chaque couleur).
- Aperçu agrandi au survol, prévisualisation du résultat sur la cible.

## Pièges fréquents

- Deck « soupe » : récompenses obligatoires qui diluent tout.
- Texte de carte ambigu sur l'ordre de résolution.
- Boucles infinies non prévues (pioche + coût 0 + gain d'énergie).
- Main morte : aucune carte jouable, tour perdu sans décision. Prévoir de quoi lisser (cartes basiques, mulligan).
- Archétypes qui ne se forment jamais faute de cartes de base communes.
- CCG : power creep (chaque extension plus forte que la précédente).

## Jeux de référence à étudier

- *Dominion* (2008) — fondateur, marché commun, coût de la dilution.
- *Slay the Spire* (2019) — intentions ennemies, épuration, archétypes par personnage, équilibrage par métriques.
- *Monster Train* (2020) — multi-étages, clans combinables.
- *Inscryption* (2021) — sacrifice comme coût, mise en scène.
- *Balatro* (2024) — synergies multiplicatives lisibles, score exponentiel.
- *Hearthstone* (2014) — lisibilité, animation, mana croissante.
- *Magic: The Gathering* (1993) — color pie, rareté, design de mots-clés ; articles de Mark Rosewater.

## Checklist

- [ ] Une carte se lit en moins de 5 secondes (test sur des joueurs).
- [ ] Le même effet utilise toujours la même formulation.
- [ ] Passer une récompense est toujours possible.
- [ ] Le joueur peut retirer des cartes de son deck.
- [ ] Chaque archétype a assez de cartes communes pour se former.
- [ ] Une courbe de coût de référence est documentée.
- [ ] Les boucles infinies potentielles ont été testées.
- [ ] Les valeurs modifiées sont visibles sur la carte.
- [ ] Taux de victoire / taux de sélection par carte mesurés.

## Pistes d'implémentation

- Cartes 100 % en données : coût, type, liste d'**effets** paramétrés (`Dégâts(6)`, `Piocher(2)`, `AppliquerStatut(Vulnérable, 2)`). Les effets sont des briques réutilisables.
- Résolution par **file d'actions** (*action queue*) : chaque effet empile des actions résolues dans l'ordre, ce qui rend l'ordre explicite, animable et testable.
- Piles distinctes : pioche, main, défausse, exil ; le mélange utilise un générateur aléatoire issu de la seed de la run.
- Texte de carte **généré** depuis les effets pour garantir la cohérence entre texte et comportement.

## Voir aussi

- [Roguelike](roguelike.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [Aléatoire et procédural](../systemes/aleatoire-et-procedural.md)
- [Progression](../systemes/progression.md)
- [UI, UX et HUD](../interface/ui-ux-hud.md)
- [Playtest et métriques](../production/playtest-et-metriques.md)

## Sources

- Donald X. Vaccarino, *Dominion*, Rio Grande Games, 2008.
- Anthony Giovannetti, « Slay the Spire: Metrics Driven Design and Balance », GDC 2019.
- Mark Rosewater, chroniques de design « Making Magic », Wizards of the Coast (magic.wizards.com).
