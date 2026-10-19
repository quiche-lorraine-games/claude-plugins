# Contrôles et mouvement

> **En bref** : comment rendre un personnage agréable à contrôler. Latence, courbes d'accélération, saut paramétré par la hauteur et la durée, aides de tolérance (*coyote time*, *jump buffer*, *corner correction*), sticks analogiques (zones mortes, courbes de réponse), assistance à la visée et remapping. Les valeurs données sont des **points de départ** à régler en jeu, pas des vérités.

## Quand consulter cette fiche

- Tu implémentes ou retouches un déplacement, un saut, un dash, une visée.
- Le joueur dit que le personnage est « mou », « glissant », « flottant », « raide » ou « imprécis ».
- Les sauts « ne partent pas » ou le joueur tombe alors qu'il « avait appuyé ».
- Tu ajoutes le support manette ou un système de visée au stick.
- Tu prépares les options de contrôle (remapping, sensibilité, inversion).

---

## 1. Principes

- **Le contrôle est la première boucle de feedback** : entrée → réponse visible en quelques frames. Si cette boucle est mauvaise, aucun contenu ne la rattrape (Swink, *Game Feel*).
- **Réactivité d'abord, réalisme ensuite.** Un personnage de jeu n'obéit pas à la physique réelle : il accélère plus vite, change de direction en l'air, retombe plus vite qu'il ne monte.
- **Tolérance invisible** : la plupart des aides (coyote time, buffer, correction de coin) ne doivent jamais être remarquées. Le joueur doit avoir l'impression que *c'est lui* qui a réussi.
- **Paramétrer en unités de design** (hauteur de saut en tuiles, durée en secondes), pas en constantes physiques opaques. Dériver la physique à partir de ces valeurs.
- **Le mouvement est du gameplay**, le juice est de la présentation. Une modification de vitesse, de gravité ou de tolérance change la difficulté du level design ; un squash & stretch non. Voir [Game feel / juice](game-feel-juice.md).

---

## 2. Latence d'entrée

La latence perçue = échantillonnage de l'entrée + logique + rendu + affichage. Le joueur ne la mesure pas, il la *ressent* comme de la mollesse.

| Source de latence | Ce qu'on contrôle | Action |
|---|---|---|
| Lecture de l'entrée | Moment de lecture dans la frame | Lire l'entrée au plus tard possible avant la simulation |
| Simulation | Frames de « démarrage » d'une action | Appliquer la réponse dès la frame de l'appui (au moins un retour visuel immédiat) |
| Animation | Anticipation trop longue | Garder l'anticipation très courte sur les actions du joueur ; la réserver aux ennemis (télégraphie) |
| Rendu | Buffering (triple buffering, VSync) | Proposer une option, limiter les images en file |
| Lissage | Filtres sur l'entrée, interpolation de caméra | Ne pas lisser l'entrée brute du joueur sur les actions instantanées |

Règles :
- **Toujours une réponse visible à la frame suivant l'appui**, même si l'action réelle démarre plus tard (son, frame d'anticipation, particule).
- Une animation qui « doit finir » avant de répondre est un bug de ressenti. Prévoir des **frames d'annulation** (*cancel windows*) pour les actions du joueur.
- Viser une latence totale aussi basse que possible ; au-delà d'environ 100 ms, la plupart des joueurs perçoivent un retard sur un jeu d'action (ordre de grandeur, à vérifier par mesure sur ton projet).

---

## 3. Accélération, décélération, vitesse maximale

Trois paramètres définissent le caractère du déplacement horizontal :

| Paramètre | Faible | Élevé |
|---|---|---|
| Accélération | Lourd, inertiel, « glissant au démarrage » | Nerveux, précis |
| Décélération (friction) | Glissant, patinoire | Arrêt net, précis |
| Vitesse max | Lent, contemplatif | Rapide, demande plus d'espace de lecture |

Points de départ (2D de plateforme précise) :
- Atteindre la vitesse max en **~0,05 à 0,15 s** ; s'arrêter en **~0,03 à 0,1 s**.
- **Demi-tour plus rapide que l'accélération** : appliquer une accélération majorée (×1,5 à ×3) quand l'entrée est opposée à la vitesse actuelle (*turn-around boost*).
- Personnage « lourd » (action, réalisme) : allonger ces durées, mais compenser par des animations de transition lisibles.

```
// Pseudo-code agnostique, par frame
target = input_x * max_speed
rate = (sign(input_x) == sign(vel_x) or vel_x == 0) ? accel : turn_accel
if input_x == 0: rate = decel
vel_x = move_toward(vel_x, target, rate * dt)
```

- Préférer `move_toward` (variation linéaire bornée) à un `lerp` dépendant du framerate. Si tu utilises un lerp, le rendre indépendant du `dt` : `a = lerp(a, b, 1 - exp(-k * dt))`.
- Contrôle en l'air (*air control*) : en général **inférieur au sol** (50–80 % de l'accélération au sol comme point de départ), mais rarement nul dans un jeu de plateforme. Zéro contrôle aérien = sauts « engagés » (Castlevania classique) : choix de design légitime, mais exigeant.

---

## 4. Saut paramétré par hauteur et durée

Ne pas régler directement gravité et vitesse initiale. Choisir :
- `h` : hauteur au sommet (en unités monde, ex. 3 tuiles) ;
- `t` : temps pour atteindre le sommet (ex. 0,35–0,45 s pour un jeu de plateforme nerveux).

Puis dériver (Pittman, GDC 2016) :

```
g  = 2 * h / t²        // gravité (positive vers le bas)
v0 = 2 * h / t         // vitesse verticale initiale (vers le haut)
```

Si le saut est contraint par une **distance horizontale** `x_h` jusqu'au sommet à vitesse max `vx` : `t = x_h / vx`. Cela relie directement le saut au level design (« un saut couvre 4 tuiles à pleine vitesse »).

### 4.1 Gravité accrue à la descente

Un saut parabolique symétrique paraît flottant. Utiliser une **gravité de descente plus forte** :
- `g_fall = g * k`, avec `k` ≈ **1,5 à 3** comme point de départ ;
- ou bien recalculer `g_fall = 2 * h / t_fall²` avec un `t_fall` plus court que `t`.
- Plafonner la vitesse de chute (*terminal velocity*) pour garder la lecture et éviter de traverser les collisions.

### 4.2 Hauteur de saut variable

Le joueur doit pouvoir doser le saut avec la durée d'appui. Deux méthodes courantes :

| Méthode | Principe | Ressenti |
|---|---|---|
| Coupure de vitesse | Au relâchement, si `vel_y` monte, `vel_y *= 0.4–0.6` (ou `vel_y = min(vel_y, v_min)`) | Réactif, net |
| Gravité majorée | Tant que le bouton n'est pas tenu en montée, appliquer `g * k_release` | Plus doux, plus « physique » |

Pour une hauteur minimale `h_min` garantie : `v_min = sqrt(2 * g * h_min)`, et au relâchement `vel_y = min(vel_y, v_min)`.

### 4.3 Sommet du saut (*apex*)

- Réduire légèrement la gravité près du sommet (quand `|vel_y|` est faible et que le bouton est tenu) donne plus de temps pour viser l'atterrissage. Celeste utilise ce type d'aide (Thorson).
- Le sommet est le moment où le joueur corrige sa trajectoire : l'air control y est le plus utile.

---

## 5. Aides de tolérance (*forgiveness*)

Elles sont du **gameplay** : elles changent ce qui est réussi ou raté. Les régler en même temps que le level design.

| Aide | Problème résolu | Point de départ |
|---|---|---|
| *Coyote time* | Le joueur appuie juste après avoir quitté le bord | ~0,08–0,15 s après la perte du sol (≈ 5–9 frames à 60 fps) |
| *Jump buffer* | Le joueur appuie juste avant d'atterrir | Mémoriser l'appui ~0,1–0,15 s, déclencher à l'atterrissage |
| *Corner correction* | La tête touche un coin de plafond de quelques pixels | Décaler latéralement de quelques pixels/unités si cela libère le passage |
| *Ledge assist* | Le pied rate le rebord de quelques pixels | Remonter le personnage si le rebord est sous un seuil |
| Tolérance d'atterrissage sur plateforme | Le pied touche à peine le bord | Hitbox de pieds légèrement plus étroite que le sprite |
| *Input buffer* (général) | Entrée pendant une animation non annulable | File d'entrée valide ~0,1–0,2 s, voir `ctrlQueue` dans [Game feel](game-feel-juice.md) |
| Hitbox réduite du joueur | Morts « injustes » | Hurtbox du joueur plus petite que son visuel ; hitbox des collectables plus grande |

Règles :
- **Consommer le coyote time et le buffer une seule fois** : réinitialiser le timer après usage pour éviter les doubles sauts involontaires.
- Le coyote time ne doit pas s'appliquer si le joueur a quitté le sol *en sautant* (sinon double saut gratuit).
- Implémenter les aides **avec un flag de debug** pour pouvoir les désactiver et vérifier leur effet en A/B.

```
// Coyote time + jump buffer
if on_ground: coyote_timer = COYOTE
else: coyote_timer -= dt
if jump_pressed: buffer_timer = BUFFER
else: buffer_timer -= dt

if buffer_timer > 0 and coyote_timer > 0:
    vel_y = v0
    buffer_timer = 0
    coyote_timer = 0
```

---

## 6. Autres mouvements

- **Dash** : vitesse constante pendant une durée fixe (0,1–0,25 s comme point de départ), gravité suspendue ou réduite, invulnérabilité éventuelle (voir [Combat](../systemes/combat.md)). Garder une courte fenêtre de buffer en sortie de dash.
- **Wall jump / wall slide** : limiter la vitesse de glissement, pousser à l'opposé du mur au saut avec un bref verrouillage partiel du contrôle horizontal (0,1–0,2 s) pour éviter de recoller immédiatement au mur. Tolérer le saut quelques frames après avoir quitté le mur (coyote time mural).
- **Pentes et marches** : coller au sol en descente (*snap to ground*) pour ne pas décoller à chaque bosse ; monter les petites marches automatiquement.
- **Plateformes mobiles** : hériter de la vitesse de la plateforme ; au saut, conserver tout ou partie de cette vitesse (cohérence attendue par le joueur).

---

## 7. Sticks analogiques

### 7.1 Zones mortes (*dead zones*)

Un stick au repos ne renvoie jamais exactement 0. Il faut une zone morte, et **la bonne forme** compte (Sutphin) :

| Type | Principe | Problème |
|---|---|---|
| Axiale (par axe) | `x = 0 si |x| < d`, idem `y` | Accroche sur les axes, diagonales difficiles |
| Radiale | `v = 0 si |v| < d` | Saut brutal de 0 à `d` en sortie de zone |
| **Radiale remise à l'échelle** (recommandée) | `v = normalize(v) * ((|v| - d) / (1 - d))` si `|v| ≥ d` | Aucun pour l'usage courant |

Points de départ : zone morte intérieure **~0,1–0,25**, zone extérieure (saturation) **~0,9–0,95** pour atteindre la valeur max sans pousser à fond. Exposer la zone morte dans les options (les sticks usés dérivent).

### 7.2 Courbes de réponse

- Mouvement : réponse souvent linéaire ou légèrement courbée.
- Visée : réponse **exponentielle** (`out = sign(in) * |in|^p`, `p` ≈ 2–3 comme point de départ) pour la précision à faible amplitude et la vitesse à fond de course.
- Proposer « Linéaire / Standard / Exponentielle » et la sensibilité séparée **horizontale / verticale**.
- Accélération de visée : augmenter la vitesse de rotation si le stick reste en butée (rampe sur 0,2–0,5 s comme point de départ).

### 7.3 Directions discrètes

Pour un jeu en 4 ou 8 directions au stick, utiliser des secteurs angulaires avec **hystérésis** (une direction ne change qu'après dépassement d'une marge) pour éviter le clignotement entre deux directions.

---

## 8. Assistance à la visée (*aim assist*)

Indispensable pour la visée au stick dans un jeu de tir ; à doser et à rendre réglable.

| Technique | Principe |
|---|---|
| Friction / ralentissement | Réduire la sensibilité quand le réticule passe sur une cible |
| Magnétisme / adhérence | Le réticule suit légèrement une cible en mouvement |
| *Bullet magnetism* | Les projectiles dévient légèrement vers la cible proche de la ligne de tir |
| Hitbox élargie | Zone de touche plus grande que le modèle pour la détection de visée |
| *Snap* / verrouillage au zoom | Le réticule se cale sur la cible à l'entrée en visée (le plus intrusif) |

Règles :
- Décroître l'assistance avec la distance et la désactiver hors champ ou derrière un obstacle.
- Ne jamais arracher la caméra au joueur contre son entrée.
- Séparer clairement assistance au **solo** et en **multijoueur** compétitif (équité entre périphériques).
- En 2D (twin-stick), une légère attraction vers l'ennemi le plus proche dans un cône de ~10–20° est un point de départ courant.

---

## 9. Mapping et remapping

- **Conventions de plateforme** : bouton du bas (A / Croix) = confirmer / sauter ; respecter les conventions de genre (gâchette droite = tirer).
- **Une action = une intention**. Éviter les boutons surchargés selon le contexte sauf si le contexte est évident.
- Prévoir dès le départ une **couche d'actions abstraites** (`Jump`, `Fire`) entre entrées physiques et gameplay : c'est ce qui rend le remapping trivial.
- Remapping complet clavier **et** manette, y compris les actions de menu. Afficher les icônes du périphérique actif et basculer dynamiquement.
- Proposer **maintien ↔ bascule** (*hold / toggle*) pour viser, sprinter, s'accroupir. Voir [Accessibilité](../interface/accessibilite.md).
- Éviter le martelage de bouton (*button mashing*) obligatoire ; offrir une alternative (maintien).
- Inversion des axes Y et X de caméra, séparément.

---

## 10. Anti-patterns

- Gravité et vitesse réglées « au feeling » sans lien avec la taille des sauts du level design.
- Lissage (`lerp`) dépendant du framerate : le jeu ne se joue pas pareil à 30 et à 144 fps.
- Physique simulée entièrement par le moteur (rigidbody) pour un personnage de plateforme : difficile à rendre précis. Préférer un contrôleur cinématique.
- Animation qui pilote le déplacement (*root motion*) pour des actions qui doivent être réactives.
- Aides de tolérance codées en dur et impossibles à désactiver pour tester.
- Zone morte axiale sur un stick de visée.
- Actions critiques uniquement accessibles via combinaison de touches non remappable.

---

## Checklist

- [ ] Les déplacements utilisent un pas de temps fixe ou sont indépendants du framerate.
- [ ] Le saut est paramétré par hauteur et durée, et ces valeurs sont documentées pour le level design.
- [ ] La gravité de descente est supérieure à la gravité de montée ; la vitesse de chute est plafonnée.
- [ ] La hauteur de saut est variable selon la durée d'appui.
- [ ] Coyote time et jump buffer sont en place, consommés une seule fois, désactivables en debug.
- [ ] La correction de coin et l'assistance de rebord sont évaluées.
- [ ] Le demi-tour est plus rapide que l'accélération initiale.
- [ ] Chaque action du joueur a une réponse visible ou audible à la frame suivant l'appui.
- [ ] Zone morte radiale remise à l'échelle sur les sticks ; zone morte réglable.
- [ ] Courbe de réponse et sensibilité réglables (H/V séparés) pour la visée.
- [ ] L'aim assist est réglable et désactivable.
- [ ] Toutes les actions passent par une couche d'actions abstraites ; remapping complet clavier et manette.
- [ ] Options maintien/bascule et inversion des axes disponibles.

## Pistes d'implémentation

- **Agnostique** : structure de paramètres unique (`MovementTuning`) avec `jump_height`, `time_to_apex`, `fall_multiplier`, `coyote_time`, `jump_buffer`, etc. ; dériver `g` et `v0` au chargement ou à chaque modification à chaud. Exposer le tout dans un menu debug.
- **UE5** : `CharacterMovementComponent` expose `JumpZVelocity`, `GravityScale`, `AirControl`, `MaxStepHeight`, `BrakingDecelerationWalking`. La gravité de descente se gère en modifiant `GravityScale` selon le signe de `Velocity.Z`. Coyote time et buffer sont à implémenter. Enhanced Input fournit modificateurs de zone morte (*Dead Zone* radial) et courbes de réponse, ainsi que le remapping par *Player Mappable Keys*.
- **Godot** : `CharacterBody2D/3D` + `move_and_slide()` ; Input Map pour l'abstraction ; `Input.get_vector()` applique une zone morte circulaire.
- **Unity** : Input System (actions, *processors* de zone morte radiale, rebinding interactif) ; contrôleur cinématique (`CharacterController` ou corps kinematic) plutôt qu'un `Rigidbody` dynamique pour la plateforme.

## Voir aussi

- [Game feel / juice](game-feel-juice.md)
- [Caméra](camera.md)
- [Combat](../systemes/combat.md)
- [Level design](../contenu/level-design.md)
- [Accessibilité](../interface/accessibilite.md)
- [Genre : plateforme](../genres/plateforme.md)
- [Genre : shooter](../genres/shooter.md)

## Sources

- Steve Swink, *Game Feel: A Game Designer's Guide to Virtual Sensation*, Morgan Kaufmann, 2008.
- Kyle Pittman, « Math for Game Programmers: Building a Better Jump », GDC 2016.
- Josh Sutphin, « Doing Thumbstick Dead Zones Right », blog Third Helix, 2013.
- Maddy Thorson, fil sur les aides de tolérance de *Celeste* (coyote time, jump buffer, correction de coin, demi-gravité au sommet), 2018.
- Martin Jonasson & Petri Purho, « Juice it or lose it », GDC Europe / Nordic Game 2012.
