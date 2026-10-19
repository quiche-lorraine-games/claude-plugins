# Caméra

> **En bref** : la caméra décide de ce que le joueur peut lire et anticiper. Cette fiche couvre les caméras 2D à défilement (fenêtre, lissage, anticipation, ancrage aux plateformes, zones), les caméras 3D à la troisième personne (collision, FOV, cadrage, verrouillage de cible), le mal des transports et le tremblement de caméra par « trauma ».

## Quand consulter cette fiche

- Tu implémentes une caméra qui suit le joueur (2D ou 3D).
- Le joueur ne voit pas ce qui arrive, meurt « hors champ », ou se plaint du mal des transports.
- La caméra « tremble », « traîne » ou traverse les murs.
- Tu ajoutes un camera shake, un zoom, un verrouillage de cible.
- Tu conçois une salle de boss, une arène ou une séquence scénarisée.

---

## 1. Principes

- **La caméra sert la lecture, pas le spectacle.** Priorité : voir la menace et la destination. Le cinématographique vient ensuite.
- **Montrer plus de terrain dans la direction où le joueur va** (et d'où viennent les menaces).
- **Le mouvement de caméra doit être plus calme que le mouvement du personnage.** Chaque micro-mouvement du joueur ne doit pas secouer l'écran.
- **Le joueur doit garder le contrôle** : ne jamais lui retirer la caméra contre sa volonté en jeu actif, sauf brièvement et pour une bonne raison.
- **La caméra est de la présentation**, mais ce qu'elle montre change la difficulté réelle (informations disponibles). La régler avec le level design.

---

## 2. Caméra 2D à défilement

Référence principale : Itay Keren, « Scroll Back » (GDC 2015), qui catalogue les techniques de nombreux jeux. Les techniques se **combinent**.

| Technique | Principe | Usage |
|---|---|---|
| Verrouillage (*position locking*) | Caméra centrée sur le joueur en permanence | Simple, mais nerveux et peu d'anticipation |
| Fenêtre (*camera window*) | Le joueur bouge librement dans un cadre ; la caméra ne bouge que s'il en sort | Évite les micro-mouvements ; base de beaucoup de plateformers |
| Lissage (*lerp smoothing*) | La caméra rejoint sa cible avec un amorti | Adoucit tout ; trop d'amorti = sensation de retard |
| Anticipation (*lookahead / forward focus*) | La cible est décalée devant le joueur selon sa direction ou sa vitesse | Voir ce qui arrive ; indispensable en scrolling rapide |
| Ancrage aux plateformes (*platform snapping*) | Verticalement, la caméra ne suit qu'à l'atterrissage sur une nouvelle plateforme | Évite que chaque saut fasse monter/descendre l'écran |
| Zones de caméra (*camera zones / regions*) | Le niveau définit des volumes qui contraignent la caméra (bornes, cadrage fixe) | Salles de boss, couloirs, mise en scène |
| Bornes de niveau | La caméra ne montre pas l'extérieur du niveau | Toujours |
| Attracteurs / points d'intérêt | La cible est tirée vers un objet important (ennemi, sortie) | Guidage, boss |
| Caméra pilotée par le joueur | Le joueur peut regarder en haut/bas (maintien) | Plateformers verticaux, exploration |

### Règles pratiques 2D

- **Vertical ≠ horizontal** : axe horizontal avec anticipation, axe vertical avec ancrage aux plateformes + rattrapage si le joueur tombe (sinon il chute hors champ).
- Changer la direction de l'anticipation **progressivement** et seulement après un déplacement confirmé (seuil de distance ou de temps), sinon la caméra oscille quand le joueur hésite.
- Chute : quand la vitesse verticale dépasse un seuil, suivre directement, voire anticiper vers le bas.
- Lissage indépendant du framerate : `pos = lerp(pos, target, 1 - exp(-k * dt))`.
- **Pixel art** : arrondir la position *rendue* de la caméra au pixel (ou rendre à basse résolution puis agrandir) pour éviter le scintillement, tout en gardant la position logique en flottant.
- Transitions entre zones : interpoler la cible et les bornes, ne pas téléporter la caméra.

```
// Caméra 2D combinée (pseudo-code)
target_x = player.x + facing * lookahead_dist            // anticipation
if abs(target_x - cam.x) < window_half_w: target_x = cam.x // fenêtre
if player.grounded: anchor_y = player.y                  // ancrage plateforme
if player.vel_y < -fall_threshold: anchor_y = player.y   // rattrapage en chute
target = clamp_to_zone(vec2(target_x, anchor_y))
cam = damp(cam, target, k, dt)
```

---

## 3. Caméra 3D à la troisième personne

### 3.1 Structure

- Pivot (*pivot / focus*) placé légèrement au-dessus du personnage (épaule ou tête), **pas** sur ses pieds.
- Bras de caméra (*spring arm / boom*) avec une distance cible, des angles de tangage (*pitch*) bornés (par exemple −60° / +70° comme point de départ).
- Décalage latéral (*over-the-shoulder*) pour les jeux de tir : le personnage d'un côté, le réticule au centre. Permettre de changer d'épaule.

### 3.2 Collision et occlusion

- Lancer un *sphere cast* du pivot vers la position désirée ; rapprocher la caméra au point d'impact.
- **Rapprocher vite, s'éloigner lentement** : rentrer instantanément quand un mur arrive (éviter de voir à travers), ressortir avec amorti (éviter le pompage).
- Objets fins (poteaux, feuillages) : les ignorer dans le test de collision et les rendre transparents ou en fondu plutôt que de faire sauter la caméra.
- Personnage masqué : silhouette visible à travers les murs plutôt que caméra qui bondit.

### 3.3 Champ de vision (FOV)

- Valeurs usuelles : environ **60–75° vertical** sur console en troisième personne ; la première personne utilise souvent un FOV horizontal de 90° ou plus sur PC. Toujours **exposer un réglage de FOV**, surtout en première personne (mal des transports).
- Variations de FOV pour la vitesse (sprint, dash) : légères et progressives (quelques degrés). Voir `camBumpZoom` dans [Game feel](game-feel-juice.md).
- Adapter le FOV au format d'écran (ultralarge) en conservant le FOV vertical (*Hor+*).

### 3.4 Cadrage et contrôle

- Laisser de l'espace devant le personnage dans la direction du mouvement et du regard.
- Recentrage automatique derrière le joueur : **uniquement après inactivité du stick caméra** (1–2 s comme point de départ) et progressivement ; jamais pendant une entrée active.
- Sensibilité caméra et inversion des axes réglables (voir [Contrôles](controles-et-mouvement.md)).
- Plateformes en 3D : montrer l'ombre portée verticale du personnage (aide à juger la position d'atterrissage) ; incliner légèrement vers le bas pendant les phases de saut.

### 3.5 Verrouillage de cible (*lock-on*)

- La caméra cadre **le joueur et la cible** : viser un point entre les deux, avec plus de poids sur la cible ; reculer ou élever la caméra si les deux ne tiennent pas dans le cadre.
- Changer de cible au stick (direction) ; prévoir un indicateur clair de la cible verrouillée.
- Décrocher automatiquement si la cible est trop loin ou hors de vue prolongée.
- Pour les grands ennemis, viser un point d'intérêt (tête, point faible), pas le centre de la capsule.

### 3.6 Caméras fixes et scénarisées

- Changement d'angle de caméra fixe : **conserver la direction de l'entrée** du joueur jusqu'à ce qu'il relâche le stick, sinon le personnage repart en arrière.
- Respecter la règle des 180° lors des coupes pour ne pas désorienter.

---

## 4. Tremblement de caméra par trauma

Méthode de Squirrel Eiserloh (GDC 2016) :

1. Une variable `trauma` entre 0 et 1. Les événements **ajoutent** du trauma (petit impact +0,2, explosion +0,5…), plafonné à 1.
2. Le trauma **décroît linéairement** dans le temps (ex. −1 par seconde comme point de départ).
3. L'intensité du shake = `trauma²` (ou `trauma³`) : les petits chocs restent discrets, les gros dominent.
4. Les offsets sont tirés d'un **bruit continu** (Perlin/simplex) échantillonné dans le temps, pas d'un aléatoire par frame : mouvement plus organique, compatible avec le ralenti.
5. En 2D : translation + légère rotation. En 3D : privilégier la **rotation** (lacet, tangage, roulis) ; la translation peut faire traverser la géométrie.

```
trauma = max(trauma - decay * dt, 0)
shake = trauma * trauma
offset_x = max_offset * shake * noise(seed1, t * freq)
offset_y = max_offset * shake * noise(seed2, t * freq)
angle    = max_angle  * shake * noise(seed3, t * freq)
```

Règles :
- Appliquer le shake comme **couche additive** sur la caméra finale, jamais sur la cible de suivi (sinon le lissage l'avale ou l'amplifie).
- Shake **directionnel** quand l'impact a une direction (recul vers l'arrière au tir) : plus lisible qu'un shake omnidirectionnel. Voir `camShakesXY` et `camBumpXY` dans [Game feel](game-feel-juice.md).
- Toujours un réglage d'intensité du shake (0–100 %) dans les options.

---

## 5. Mal des transports (*motion sickness*)

Causes fréquentes : FOV étroit, mouvements de caméra que le joueur ne contrôle pas, oscillations de tête (*head bob*), accélérations angulaires brusques, flou de mouvement, horizon qui bascule, framerate instable.

Mesures :
- Réglage du FOV, désactivation du *head bob*, du flou de mouvement et du shake.
- Point fixe à l'écran optionnel (réticule permanent au centre).
- Éviter les rotations de caméra automatiques en jeu actif ; garder l'horizon stable.
- Framerate stable plus important que la qualité visuelle.
- Voir [Accessibilité](../interface/accessibilite.md).

---

## 6. Anti-patterns

- Caméra rigidement collée au joueur en 2D : chaque saut fait bouger l'écran.
- Lissage tellement fort que le joueur sort du cadre en vitesse.
- Anticipation qui bascule à chaque changement de direction.
- Caméra 3D qui ressort brutalement après une collision (pompage).
- Recentrage automatique qui se bat contre le joueur.
- Ennemis qui attaquent depuis hors champ sans indicateur.
- Shake aléatoire par frame, sans décroissance, appliqué à tous les événements avec la même force.

---

## Checklist

- [ ] Le joueur voit plus loin dans la direction où il va.
- [ ] En 2D, l'axe vertical ne suit pas chaque saut (ancrage aux plateformes) mais rattrape les chutes.
- [ ] Le lissage est indépendant du framerate.
- [ ] La caméra ne montre jamais l'extérieur du niveau (bornes / zones).
- [ ] En 3D, la collision rentre vite et ressort lentement ; les objets fins ne font pas sauter la caméra.
- [ ] Le recentrage automatique ne s'active qu'après inactivité du stick caméra.
- [ ] Le lock-on cadre le joueur et la cible.
- [ ] Le shake utilise un trauma décroissant, un bruit continu, et est réglable.
- [ ] FOV, sensibilité, inversion, head bob, flou de mouvement et shake sont réglables.
- [ ] Les menaces hors champ ont un indicateur.

## Pistes d'implémentation

- **Agnostique** : séparer *cible de suivi* (logique), *position lissée*, puis *couche d'effets* (shake, bump, zoom) appliquée en dernier. Paramètres dans une structure unique modifiable à chaud.
- **UE5** : `USpringArmComponent` (collision via `ProbeSize`, `bEnableCameraLag`, `CameraLagSpeed`), `APlayerCameraManager` pour les modificateurs ; `UCameraShakeBase` avec *Perlin Noise Camera Shake Pattern*. Zones : volumes déclenchant un changement de caméra ou un `SetViewTargetWithBlend`.
- **Godot** : `Camera2D` intègre `drag margins` (fenêtre), `position smoothing` et `limits` ; `SpringArm3D` pour la collision 3D. Le shake se fait via `offset` + `FastNoiseLite`.
- **Unity** : Cinemachine fournit fenêtres (*dead zone / soft zone*), lookahead, confiner 2D, collision 3D, *Target Group* pour le lock-on et l'*Impulse* pour le shake.

## Voir aussi

- [Game feel / juice](game-feel-juice.md)
- [Contrôles et mouvement](controles-et-mouvement.md)
- [Level design](../contenu/level-design.md)
- [Combat](../systemes/combat.md)
- [Accessibilité](../interface/accessibilite.md)
- [Genre : plateforme](../genres/plateforme.md)

## Sources

- Itay Keren, « Scroll Back: The Theory and Practice of Cameras in Side-Scrollers », GDC 2015 (et article Gamasutra associé).
- Squirrel Eiserloh, « Math for Game Programmers: Juicing Your Cameras With Math », GDC 2016.
- John Nesky, « 50 Game Camera Mistakes », GDC 2014.
- Mark Haigh-Hutchinson, *Real-Time Cameras: A Guide for Game Designers and Developers*, Morgan Kaufmann, 2009.
