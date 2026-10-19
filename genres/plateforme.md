# Plateforme

> **En bref** : point d'entrée pour un jeu de plateforme (2D ou 3D). Résume ce qui fait la qualité du genre — un contrôle du personnage irréprochable et des niveaux qui enseignent par la pratique — et renvoie vers les fiches détaillées sur le mouvement, la caméra et le level design.

## Quand consulter cette fiche

- Tu démarres un jeu de plateforme ou un jeu où le saut est une action centrale.
- Le saut est jugé « raide », « flottant » ou « injuste » en playtest.
- Tu dois concevoir une suite de niveaux et ne sais pas comment introduire les mécaniques.
- Tu hésites entre plateforme de précision, plateforme d'exploration (metroidvania) ou collectathon 3D.

## Boucle centrale typique

```
Observer l'obstacle → Planifier un trajet → Exécuter (courir, sauter, esquiver)
      ↑                                                   ↓
 Respawn immédiat ← Échec            Réussite → Checkpoint / collectible / nouvelle zone
```

- **Micro-boucle** (1–5 s) : un saut, une séquence d'obstacles.
- **Boucle de niveau** (1–10 min) : introduire une idée, la tester, la tordre, conclure.
- **Méta** : collectibles, capacités débloquées (metroidvania), temps à battre (speedrun).

## Piliers du genre

1. **Le contrôle avant tout.** Le joueur doit sentir que chaque échec est de sa faute. Le personnage obéit instantanément, de façon prévisible et cohérente.
2. **Lisibilité spatiale.** Plateformes, dangers et zones sûres se distinguent au premier coup d'œil (couleur, forme, contraste). Voir [Lisibilité](../fondamentaux/principes-de-conception.md).
3. **Apprentissage par le niveau.** La mécanique s'enseigne par la géométrie, pas par du texte (Super Mario Bros. 1-1).
4. **Coût d'échec faible.** Respawn rapide, checkpoints fréquents, surtout en plateforme de précision.

## Mécaniques clés et valeurs de départ

Détails et formules dans [Contrôles et mouvement](../ressenti/controles-et-mouvement.md). Valeurs indicatives, à régler en playtest :

| Mécanique | Rôle | Point de départ (règle empirique) |
|---|---|---|
| *Coyote time* | Sauter juste après avoir quitté un rebord | ~0,08–0,15 s (5–9 frames à 60 fps) |
| *Jump buffer* (saut anticipé) | Saut pressé juste avant de toucher le sol pris en compte | ~0,1–0,15 s |
| Hauteur de saut variable | Relâcher le bouton coupe la montée | Multiplier la vitesse verticale par ~0,5 au relâchement, ou augmenter la gravité |
| Gravité asymétrique | Descente plus rapide que la montée = saut moins « flottant » | Gravité de chute ~1,5–3× la gravité de montée |
| Apex adouci | Gravité réduite au sommet pour faciliter le contrôle aérien | Gravité ÷2 quand \|vy\| est faible (technique utilisée par *Celeste*) |
| *Corner correction* | Glisser de quelques pixels au lieu de se cogner sur un coin | Quelques pixels de tolérance |
| Vitesse de chute max | Garde la lisibilité et évite les traversées de collision | Plafonner `vy` |
| Contrôle aérien | Ajuster la trajectoire en l'air | Accélération aérienne < accélération au sol, mais non nulle |

Paramétrer le saut par **hauteur et durée jusqu'à l'apex** plutôt que par gravité/impulsion brutes (méthode de Kyle Pittman, GDC 2016) :

```
gravite   = 2 * hauteur / (temps_apex ^ 2)
impulsion = 2 * hauteur / temps_apex
```

Autres mécaniques fréquentes : double saut, *wall jump* / *wall slide*, dash, accroche au rebord (*ledge grab*), plateformes mobiles (transmettre la vélocité de la plateforme au joueur qui saute), ressorts, interrupteurs.

## Sous-genres

| Sous-genre | Priorité de design | Références |
|---|---|---|
| Plateforme de précision | Contrôle millimétré, respawn instantané, écrans courts | *Celeste*, *Super Meat Boy* |
| Plateforme « classique » | Rythme, variété des idées, secrets | *Super Mario Bros. 3*, *Rayman Legends* |
| Metroidvania | Capacités qui ouvrent la carte, backtracking, carte lisible | *Hollow Knight*, *Super Metroid*, *Ori* |
| Collectathon 3D | Caméra, mouvement riche, densité de collectibles | *Super Mario 64*, *A Hat in Time* |
| *Puzzle-platformer* | Une idée par écran, logique plutôt que réflexes | *Braid*, *Limbo* |

## Level design spécifique

Détails dans [Level design](../contenu/level-design.md) et [Onboarding](../contenu/onboarding-tutoriels.md).

- **Introduire → développer → tordre → conclure** (structure *kishōtenketsu* décrite par Koichi Hayashida à propos de *Super Mario 3D Land*) : chaque niveau explore une seule idée.
- Présenter un danger d'abord **dans une situation sûre** (pas de trou dessous), puis avec enjeu.
- Construire les niveaux sur une **grille** cohérente avec la hauteur/longueur de saut. Documenter les distances franchissables (saut simple, avec élan, double saut) et s'y tenir.
- Les sauts « de foi » (atterrissage hors champ) sont à proscrire, sauf signalés.
- Placer des collectibles sur la trajectoire idéale pour **guider** le joueur.

## Pièges fréquents

- **Physique « réaliste »** : un saut parabolique pur avec gravité constante paraît lourd et flottant à la fois. Les jeux de plateforme trichent.
- **Latence d'input** : animation d'anticipation avant le saut → le saut doit partir à la frame de l'input.
- **Hitbox du héros trop grande** : préférer une hitbox de dégâts légèrement plus petite que le sprite, une hitbox de collision au sol légèrement généreuse.
- **Caméra qui cache la destination** : voir [Caméra](../ressenti/camera.md) (look-ahead, cadrage vers le haut lors d'une chute).
- **Morts longues** : animation de mort + rechargement > 1–2 s en précision = frustration.
- **Collectibles punitifs** : obliger à refaire tout le niveau pour un oubli.

## Jeux de référence à étudier

- *Super Mario Bros.* (1985) — monde 1-1 : l'enseignement sans texte.
- *Celeste* (2018) — catalogue d'aides invisibles (coyote time, buffer, apex, correction de coins) et mode Assistance exemplaire.
- *Super Meat Boy* (2010) — respawn instantané, replays de toutes les morts.
- *Hollow Knight* (2017) — metroidvania, combat intégré au mouvement, carte à acheter.
- *Super Mario Odyssey* (2017) — moveset riche, densité de récompenses.

## Checklist

- [ ] Le saut part à la frame de l'input (pas de délai d'anticipation bloquant).
- [ ] Coyote time et jump buffer implémentés et réglables.
- [ ] Hauteur de saut variable (relâcher le bouton raccourcit le saut).
- [ ] Gravité de chute supérieure à la gravité de montée.
- [ ] Distances de saut documentées et utilisées comme métrique de level design.
- [ ] Dangers, plateformes et décor distinguables d'un coup d'œil.
- [ ] Respawn < 1 s après une mort en séquence de précision.
- [ ] La caméra montre toujours la zone d'atterrissage.
- [ ] Chaque niveau a une idée principale introduite en sécurité.
- [ ] Options d'accessibilité (ralenti, invincibilité, sauts supplémentaires) envisagées.

## Pistes d'implémentation

- Utiliser un *character controller* cinématique (vitesse calculée à la main) plutôt qu'un corps physique simulé : le contrôle doit être déterministe.
- Paramètres (hauteur, temps d'apex, coyote, buffer) exposés dans un asset de réglage modifiable à chaud.
- **UE5** : `CharacterMovementComponent` (`JumpZVelocity`, `GravityScale`, `AirControl`, `JumpMaxHoldTime`) ; le coyote time et le buffer sont à ajouter.
- **Godot** : `CharacterBody2D/3D` + `move_and_slide()`, timers pour coyote et buffer.
- **Unity** : `CharacterController` ou `Rigidbody2D` en mode kinematic avec vélocité gérée manuellement.

## Voir aussi

- [Contrôles et mouvement](../ressenti/controles-et-mouvement.md)
- [Game feel / juice](../ressenti/game-feel-juice.md) — section 7 (aides à la jouabilité), squash & stretch, `jumpFx`
- [Caméra](../ressenti/camera.md)
- [Level design](../contenu/level-design.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [Accessibilité](../interface/accessibilite.md)

## Sources

- Kyle Pittman, « Math for Game Programmers: Building a Better Jump », GDC 2016.
- Maddy Thorson, fil de messages sur les aides de jouabilité de *Celeste* (coyote time, jump buffer, apex), 2018.
- Steve Swink, *Game Feel*, Morgan Kaufmann, 2008.
- Koichi Hayashida, entretien sur le level design de *Super Mario 3D Land* (structure kishōtenketsu), Gamasutra, 2012.
