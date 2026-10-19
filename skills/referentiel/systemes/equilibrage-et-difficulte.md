# Équilibrage et difficulté

> **En bref** : comment construire une courbe de difficulté, quand et comment adapter la difficulté, et comment équilibrer des options entre elles (coûts, stratégies dominantes, intransitivité). Méthodes concrètes : tableur, simulation, métriques.

## Quand consulter cette fiche

- Le jeu est jugé trop dur, trop facile, ou les deux selon les joueurs.
- Tu ajoutes des modes de difficulté ou une difficulté adaptative.
- Une arme, une unité, un build est utilisé par tout le monde (ou par personne).
- Tu dois fixer les prix, coûts ou stats d'un ensemble d'options.
- Tu prépares un patch d'équilibrage.

---

## 1. Difficulté : principes

- **Flow** (Csikszentmihalyi) : le joueur reste engagé quand le défi suit sa compétence. Trop dur → anxiété ; trop facile → ennui. Voir [Cadres théoriques](../fondamentaux/cadres-theoriques.md).
- La difficulté se compose de plusieurs axes, à régler séparément :

| Axe | Leviers |
|---|---|
| **Exécution** (réflexes, précision) | Fenêtres de timing, vitesse des ennemis, durée de télégraphie |
| **Décision** (tactique, stratégie) | Nombre d'options, information disponible, complexité des combinaisons |
| **Connaissance** (apprendre le jeu) | Nouveauté des mécaniques, clarté des règles |
| **Endurance** (tenir dans la durée) | Longueur des séquences, distance entre checkpoints |
| **Ressources** (gestion) | Rareté des soins, munitions, argent |

- **La punition de l'échec** fait partie de la difficulté : perdre 10 s vs perdre 1 h n'est pas le même défi. Ajuster la **distance aux checkpoints** est souvent plus efficace que d'ajuster les dégâts.
- **Difficulté perçue ≠ difficulté réelle** : un jeu peut être très dur et jugé juste s'il est lisible, ou facile et jugé injuste s'il est opaque.

## 2. Courbes de difficulté

- **Dents de scie** (*sawtooth*) : la difficulté monte au sein d'un segment (niveau, monde), retombe au début du suivant (nouvelle mécanique, respiration), puis monte plus haut. C'est la forme de référence.
- **Pic de boss** suivi d'un **creux** : récompenser la victoire par un moment de calme et de puissance.
- **Courbe de puissance du joueur** à mettre en regard : quand le joueur gagne une amélioration, lui laisser du temps pour en profiter avant de remonter la difficulté.
- **Rampe d'entrée douce** : les premières minutes doivent être réussies par presque tous les joueurs.

```text
difficulté
  ^          /|        /|
  |       /| / |    /| / |   <- pics : boss / fin de monde
  |    /| / |/  | /  |/   |
  |  / |/        |
  +--------------------------> progression
     monde 1     monde 2
```

## 3. Modes et adaptation de la difficulté

### Modes explicites

- **Choix initial** (facile / normal / difficile) : simple, mais le joueur choisit sans connaître le jeu. Permettre de **changer à tout moment** sans pénalité morale (éviter les noms humiliants).
- **Options d'assistance granulaires** (style *Assist Mode* de Celeste) : vitesse du jeu, invincibilité, sauts infinis… Laissent le joueur composer. Excellentes pour l'[accessibilité](../interface/accessibilite.md).
- **Difficulté par opt-in** : défis optionnels (collectables difficiles, modificateurs, *heat* de Hades, niveaux d'ascension de Slay the Spire) plutôt que de durcir le chemin principal.

### Difficulté adaptative (DDA)

Ajustement automatique selon la performance (ex. Resident Evil 4, le *AI Director* de Left 4 Dead qui module l'intensité).

| Avantages | Risques |
|---|---|
| Garde les joueurs dans le flow | Le joueur se sent **manipulé** s'il le découvre |
| Réduit l'abandon des joueurs en difficulté | **Punit la performance** : bien jouer rend le jeu plus dur, ce qui peut démotiver |
| Évite le choix initial | Exploitable (jouer mal volontairement) |
| | Rend l'équilibrage et les tests plus complexes |

Règles pour une DDA saine :
- **Aider discrètement plutôt que punir** : réduire la difficulté après des échecs répétés, rarement l'augmenter au-delà de la base.
- **Moduler le rythme et les ressources** (moins d'ennemis simultanés, plus de soins lâchés) plutôt que les règles visibles (dégâts, PV).
- **Inertie** : ajuster lentement, sur plusieurs tentatives, pas sur un seul coup.
- **Bornes** : plafonner l'ajustement dans les deux sens.
- Si l'adaptation est forte, **l'annoncer** (« Le jeu peut proposer une aide après plusieurs échecs »).

## 4. Équilibrage : objectifs

Équilibrer ne signifie pas rendre tout égal. Objectifs typiques :
- **Pas de stratégie dominante** : aucune option n'est meilleure dans toutes les situations.
- **Chaque option a une situation où elle brille.**
- **Diversité viable** : plusieurs stratégies mènent à la victoire.
- **Équité perçue** : le joueur qui perd comprend pourquoi et pense pouvoir faire mieux.
- En solo, **l'équilibre peut pencher vers le joueur** : une option un peu trop forte est souvent plus amusante qu'une option faible. En compétitif, l'équilibre entre joueurs prime.

## 5. Équilibrage transitif

Les options sont rangées sur une échelle : plus chère = plus forte. Typique des objets d'un RPG, des unités par tier.

- **Courbe de coût** : établir une relation `coût → puissance`, puis vérifier que chaque option se place sur la courbe.
- Méthode : attribuer une **valeur à chaque attribut** (1 point de dégât = x, 1 PV = y, effet spécial = z), calculer la somme, comparer au coût.
- Les options **hors courbe** (trop de puissance pour le coût) sont les candidates aux stratégies dominantes.
- La courbe n'a pas à être linéaire : les options chères peuvent valoir **plus** que leur prix (récompense de l'investissement) ou **moins** (rendements décroissants) selon l'intention.

```text
puissance(option) = Σ attribut_i × valeur_i + Σ effets_spéciaux
écart = puissance(option) - courbe_cible(coût(option))
-> écart > seuil : trop forte ; écart < -seuil : trop faible
```

## 6. Équilibrage intransitif

Pierre-feuille-ciseaux : A bat B, B bat C, C bat A. Aucune option n'est meilleure absolument.

- Crée du **contre-jeu** et des décisions basées sur la lecture de l'adversaire.
- Les relations peuvent être **partielles** (avantage de 60/40 plutôt que 100/0) : plus nuancé, laisse la compétence compter.
- Utile pour : types d'unités (infanterie / cavalerie / piquiers), types de dégâts, archétypes de decks, verbes de combat (attaque / garde / saisie).
- **Information** : l'intransitivité n'a de sens que si les joueurs peuvent **observer et réagir** (au moins partiellement). Sans information, c'est du hasard.

## 7. Symétrie et asymétrie

| Type | Description | Équilibrage |
|---|---|---|
| **Symétrique** | Mêmes options pour tous (échecs, la plupart des jeux de sport) | Facile ; seul l'avantage du premier joueur est à compenser |
| **Asymétrique** | Factions, personnages ou rôles différents | Difficile ; exige beaucoup de tests et de données. Viser des **taux de victoire proches de 50 %** entre camps à niveau égal |
| **Asymétrique extrême** | Un contre plusieurs (ex. Dead by Daylight) | Équilibrer l'expérience des deux camps, pas seulement le taux de victoire |

- Compenser l'**avantage du premier joueur** : ressource bonus pour le second, enchères, tirage alterné (*snake draft*).

## 8. Stratégies dominantes

Une stratégie dominante est une option toujours meilleure que les autres. Elle **tue la décision**.

Diagnostic :
- Taux d'utilisation très élevé d'une option + taux de victoire élevé.
- Les joueurs expérimentés convergent tous vers le même choix.
- Une option n'a aucun contre identifiable.

Corrections possibles (de la moins à la plus invasive) :
1. **Ajouter un contre** (option, ennemi, situation) qui la punit.
2. **Augmenter son coût** (ressource, temps, risque, exposition).
3. **Renforcer les alternatives** (buff).
4. **Réduire sa puissance** (nerf).
5. **Changer sa règle** (refonte) si elle casse un système.

Attention aux **stratégies dégénérées** : techniques gagnantes mais ennuyeuses (*cheese*, farming infini, camping). Les rendre moins efficaces que le jeu « normal », pas forcément impossibles.

## 9. Nerf ou buff ?

| Préférer le **buff** quand… | Préférer le **nerf** quand… |
|---|---|
| Le jeu est solo ou coopératif | L'option est la seule viable et tout le reste est correct |
| Plusieurs options sont faibles | Buffer tout le reste ferait exploser la puissance globale |
| On veut éviter la frustration (« on m'a cassé mon perso ») | L'option rend le jeu ennuyeux ou toxique |

- Les nerfs frustrent plus que les buffs ne réjouissent : **communiquer la raison**.
- Changer **une variable à la fois**, mesurer, itérer.
- Viser les **seuils** (nombre de coups pour tuer, temps de recharge par rapport à une durée de combat) plutôt que des pourcentages arbitraires.

## 10. Méthodes

### Tableur
- Lister toutes les options avec attributs, coût, valeur calculée.
- Calculer DPS, TTK, valeur par coût, ratios. Repérer les valeurs aberrantes.
- Garder **les données du jeu exportables vers/depuis le tableur** (CSV, JSON) pour éviter les divergences.

### Simulation
- Simuler des combats ou des parties (Monte Carlo) avec des stratégies scriptées simples : détecte les déséquilibres grossiers avant le playtest.
- Simuler l'**économie** sur une partie complète (voir [Économie](economie.md)).
- Limite : une simulation ne capture pas la créativité des joueurs ni le ressenti.

### Métriques (après lancement ou en playtest)
- **Taux de victoire** par option / faction / personnage (à niveau égal).
- **Taux de sélection** (*pick rate*) et de bannissement.
- **Points d'abandon** et de mort par niveau / rencontre : révèlent les pics de difficulté.
- **Temps de complétion** par segment.
- Croiser avec le **niveau de compétence** : une option peut être forte chez les débutants et faible chez les experts.
- Voir [Playtest et métriques](../production/playtest-et-metriques.md).

## 11. Équité perçue

Le joueur accepte de perdre s'il pense que c'est **sa faute**.

- **Lisibilité** : télégraphie claire, règles visibles, cause de la mort compréhensible.
- **Cohérence** : les mêmes causes produisent les mêmes effets.
- **Contrôle** : l'issue dépend surtout des choix du joueur, pas du hasard (voir [Aléatoire et procédural](aleatoire-et-procedural.md)).
- **Indulgence invisible** : coyote time, hitbox du joueur réduite, derniers PV qui durent un peu plus longtemps. Voir [Contrôles et mouvement](../ressenti/controles-et-mouvement.md).
- **Relance rapide** : une mort qui coûte peu est mieux acceptée.

---

## Anti-patterns et pièges

- **Augmenter uniquement les PV et dégâts** pour monter la difficulté.
- **Pic de difficulté en début de jeu** (avant que le joueur soit investi).
- **DDA détectable et punitive** pour les bons joueurs.
- **Équilibrer sur l'intuition seule**, sans tableur ni données.
- **Changer plusieurs variables à la fois** puis ne pas savoir laquelle a eu l'effet.
- **Équilibrer pour les experts uniquement** (ou pour les débutants uniquement).
- **Noms de difficulté humiliants** (« Mode bébé »).

## Checklist

- [ ] Les axes de difficulté du jeu sont identifiés (exécution, décision, connaissance, endurance, ressources).
- [ ] La courbe de difficulté suit des dents de scie avec respirations après les pics.
- [ ] La distance aux checkpoints est cohérente avec la difficulté voulue.
- [ ] La difficulté peut être changée à tout moment, ou des options d'assistance existent.
- [ ] Si DDA : elle aide plus qu'elle ne punit, est bornée et lente.
- [ ] Toutes les options sont dans un tableur avec une valeur par coût.
- [ ] Chaque option a au moins une situation où elle est le meilleur choix et au moins un contre.
- [ ] Les métriques de victoire, sélection et abandon sont collectées en playtest.
- [ ] Chaque patch modifie peu de variables et documente l'intention.

## Pistes d'implémentation

- Centraliser **toutes** les valeurs d'équilibrage dans des fichiers de données (tables, CSV, DataAsset, Resource, ScriptableObject), rechargeables à chaud.
- Exposer un **multiplicateur global de difficulté** par axe (dégâts reçus, vitesse ennemie, nombre de jetons d'attaque, densité de soins) plutôt que de dupliquer les données par mode.
- Prévoir un **mode simulation headless** (sans rendu) pour faire tourner des milliers de combats.
- Journaliser les événements clés (mort, victoire, choix d'option) avec un identifiant de version de l'équilibrage.
- **UE5** : `DataTable` / `CurveTable` importables depuis CSV ; `UDeveloperSettings` pour les multiplicateurs ; console variables pour le réglage à chaud.
- **Godot** : `Resource` personnalisées et fichiers `.tres` / CSV.
- **Unity** : `ScriptableObject` et import CSV ; `AnimationCurve` pour les courbes.

## Voir aussi

- [Combat](combat.md)
- [Progression](progression.md)
- [Économie](economie.md)
- [Aléatoire et procédural](aleatoire-et-procedural.md)
- [Multijoueur](multijoueur.md)
- [Cadres théoriques](../fondamentaux/cadres-theoriques.md)
- [Playtest et métriques](../production/playtest-et-metriques.md)

## Sources

- Ian Schreiber & Brenda Romero, *Game Balance*, CRC Press, 2021.
- Ian Schreiber, *Game Balance Concepts*, 2010 — https://gamebalanceconcepts.wordpress.com/
- Mihaly Csikszentmihalyi, *Flow: The Psychology of Optimal Experience*, Harper & Row, 1990.
- David Sirlin, *Playing to Win*, 2006 — https://www.sirlin.net/ptw ; et articles sur l'équilibrage des jeux compétitifs — https://www.sirlin.net/
- Michael Booth, « The AI Systems of Left 4 Dead », AIIDE 2009 (Valve).
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, CRC Press (3e éd. 2019).
- Celeste (Maddy Makes Games, 2018), *Assist Mode*.
