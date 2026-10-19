# RPG (jeu de rôle)

> **En bref** : point d'entrée pour un jeu de rôle — personnages qui progressent par des statistiques, des capacités et de l'équipement, dans un monde avec des quêtes. Ce qui fait la qualité du genre : la sensation de croissance, l'expression du joueur par son *build*, et des choix qui ont des conséquences. Les mécaniques de détail sont dans les fiches progression, combat et narration.

## Quand consulter cette fiche

- Tu conçois un RPG (action, tour par tour, tactique, CRPG, JRPG, ARPG).
- Tu dois définir des statistiques, des classes ou un arbre de compétences.
- Les builds convergent tous vers la même solution.
- Les quêtes paraissent creuses ou répétitives.

## Boucle centrale typique

```
Explorer / recevoir une quête → Combattre / résoudre → Récompense (XP, loot, histoire)
        ↑                                                      ↓
  Nouvelles zones / défis ← Plus puissant ← Améliorer le personnage (stats, compétences, équipement)
```

Deux boucles imbriquées : la **boucle de combat** (minutes) et la **boucle de progression** (heures). La seconde donne son sens à la première.

## Piliers du genre

1. **Croissance perceptible** : le joueur sent qu'il devient plus fort, et le voit (nouvelles capacités, ennemis autrefois difficiles devenus faciles).
2. **Expression par le build** : plusieurs manières viables de jouer.
3. **Choix et conséquences** : dans le build comme dans l'histoire.
4. **Monde et personnages** : l'univers motive l'exploration. Voir [Narration](../contenu/narration.md).

## Statistiques

- **Peu de stats, chacune avec un rôle clair.** Chaque stat doit modifier une décision du joueur. Une stat que personne ne choisit jamais est à supprimer.
- Distinguer **stats primaires** (Force, Agilité… choisies par le joueur) et **stats dérivées** (PV, dégâts, esquive… calculées).
- Gains **perceptibles** : +1 % n'est pas ressenti. Mieux vaut moins de gains, plus gros.
- Éviter les stats **toujours optimales** (une stat qui augmente dégâts *et* survie *et* vitesse).
- Formules de dégâts, armure, critiques : voir [Combat](../systemes/combat.md). Courbes d'XP : voir [Progression](../systemes/progression.md).

## Classes, compétences, builds

| Approche | Avantage | Risque |
|---|---|---|
| Classes fixes | Identité forte, équilibrage maîtrisé | Rigidité |
| Sans classe (compétences libres) | Liberté, expression | Builds « tout-en-un » dominants, paralysie de choix |
| Hybride (classe + spécialisations) | Compromis | Complexité |

- Trinité classique (en groupe) : **tank** (absorbe), **soigneur** (soutient), **DPS** (inflige). Utile, mais pas obligatoire.
- Les meilleurs builds sont des **synergies** entre compétences, équipement et statuts.
- Permettre de **réattribuer** les points (*respec*) à coût modéré : l'expérimentation ne doit pas être punie par une sauvegarde gâchée.
- Montrer l'**effet chiffré** d'un choix avant validation (comparaison d'équipement, aperçu de compétence).

## Combat : tour par tour ou action

| | Tour par tour | Action / temps réel |
|---|---|---|
| Compétence centrale | Planification, gestion de ressources | Réflexes, positionnement |
| Information | Peut être totale (intentions ennemies) | Lecture des animations |
| Rythme | Contrôlé par le joueur | Imposé par le jeu |
| Pièges | Combats aléatoires répétitifs, menus lents | Stats qui annulent la compétence |
| Références | *Final Fantasy X*, *Persona 5*, *Divinity: Original Sin 2* | *Dark Souls*, *Diablo*, *Elden Ring* |

Variantes : ATB (barre de temps active, *Final Fantasy IV–IX*), tactique sur grille (*Final Fantasy Tactics*, *Fire Emblem*).

## Quêtes

- Chaque quête a **un objectif clair**, **une motivation** (pourquoi s'en soucier) et **une conséquence** (le monde change, même un peu).
- Varier les verbes : enquêter, convaincre, escorter, choisir un camp… pas seulement « tuer X » ou « rapporter Y ».
- Une quête de collecte devient acceptable si elle mène à un lieu ou une histoire intéressants.
- Journal de quêtes lisible, marqueurs optionnels pour ceux qui le souhaitent.
- Voir [Narration](../contenu/narration.md) et [Level design](../contenu/level-design.md).

## Groupe (*party*)

- Chaque membre a un **rôle mécanique** et une **personnalité** : les deux renforcent l'attachement.
- Limiter la taille active (3–4 dans beaucoup de jeux) pour garder les décisions lisibles.
- Éviter que les membres non utilisés deviennent inutilisables (XP partagée, rattrapage).

## Pièges fréquents

- **Mise à l'échelle des ennemis** sur le niveau du joueur (*level scaling* intégral) : la progression ne se sent plus. *The Elder Scrolls IV: Oblivion* en est le contre-exemple souvent cité.
- Inflation de chiffres sans changement de jeu (dégâts ×10, ennemis ×10).
- Grind obligatoire pour combler un pic de difficulté.
- Inventaire surchargé de loot sans intérêt.
- Dialogues et choix sans conséquences visibles.
- Builds « pièges » : un joueur peut rendre sa partie injouable sans le savoir.

## Jeux de référence à étudier

- *Chrono Trigger* (1995) — rythme, combats sans transition, techniques combinées.
- *Diablo II* (2000) — boucle de loot, raretés, builds.
- *Dark Souls* (2011) — RPG d'action, stats légères, apprentissage par l'échec.
- *Divinity: Original Sin 2* (2017) — combat systémique (surfaces, éléments).
- *Disco Elysium* (2019) — compétences comme voix intérieures, échec intéressant.
- *Baldur's Gate 3* (2023) — réactivité du monde aux choix, adaptation des règles de D&D 5e.
- *Pokémon* (série) — collection, types en pierre-feuille-ciseaux.

## Checklist

- [ ] Chaque stat modifie au moins une décision du joueur.
- [ ] Les gains de niveau sont perceptibles en jeu.
- [ ] Au moins 2–3 builds viables par classe / archétype.
- [ ] L'effet d'un choix est prévisualisable avant validation.
- [ ] Une respécialisation est possible.
- [ ] Les quêtes ont objectif, motivation et conséquence.
- [ ] La difficulté ne force pas de grind.
- [ ] L'équipement obtenu est comparable d'un coup d'œil.

## Pistes d'implémentation

- Stats et modificateurs en données : une valeur de base + une liste de modificateurs (source, type additif/multiplicatif, durée) recalculée à la demande.
- Séparer données (tables de classes, objets, compétences) et code : l'équilibrage se fait dans un tableur exportable.
- **UE5** : Gameplay Ability System (attributs, effets, tags) couvre stats, buffs et capacités.
- **Godot / Unity** : `Resource` / `ScriptableObject` pour décrire objets, compétences et classes.

## Voir aussi

- [Progression](../systemes/progression.md)
- [Combat](../systemes/combat.md)
- [Économie](../systemes/economie.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [Narration](../contenu/narration.md)
- [UI, UX et HUD](../interface/ui-ux-hud.md) — inventaires, comparaisons
- [Stratégie](strategie.md) — pour les RPG tactiques

## Sources

- Ian Schreiber et Brenda Romero, *Game Balance*, CRC Press, 2021.
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, 3e éd., CRC Press, 2019.
