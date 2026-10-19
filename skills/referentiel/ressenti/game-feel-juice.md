# Game Feel / Juice — Référence d'effets

> Source : prototype `deepnight/gamefeel` (Sébastien Bénard, talk ENJMIN 2019, mis à jour en 2024) — https://github.com/deepnight/gamefeel
> Liste extraite de `src/game/Options.hx`. Chaque effet y est une option booléenne activable/désactivable en jeu.

## Comment utiliser ce document (pour Claude Code)

- Ce fichier sert de **catalogue de référence** quand on travaille sur le ressenti d'une action (tir, impact, saut, dash, mort…).
- Avant d'implémenter une action de gameplay, **consulter la section correspondante** et proposer les effets pertinents.
- Les **ID** (`camShakesXY`, `blinkImpact`…) sont les noms d'origine du prototype : les réutiliser comme noms de flags pour garder une correspondance claire.
- Les pistes UE5 sont des **suggestions de départ**, pas une implémentation imposée. Vérifier l'existant du projet avant d'ajouter un nouveau système.

## Principe d'architecture recommandé

Reproduire le pattern du prototype : **chaque effet derrière un flag booléen indépendant**, regroupés dans une structure de settings unique (ex. `UGameFeelSettings` en `UDeveloperSettings` ou un `DataAsset`), modifiable à chaud via un menu debug ou des console variables.

Bénéfices :
- comparaison A/B immédiate (tout activer / tout désactiver) ;
- réglage fin effet par effet ;
- désactivation possible pour l'accessibilité (camera shake, flashs).

Règle générale : un effet de juice **ne doit jamais modifier la logique de gameplay** sauf s'il est explicitement marqué « gameplay » ci-dessous (recul physique, verrouillage des contrôles, aides de jouabilité, ralenti).

---

## 1. Flash et caméra

| ID | Effet | Déclencheur | Piste UE5 |
|---|---|---|---|
| `blinkImpact` | Bref flash blanc sur l'entité touchée | Balle qui touche un ennemi | Paramètre scalaire `HitFlash` dans le matériau (Dynamic Material Instance), remis à 0 après ~0,05–0,1 s |
| `flashbang` | Flash jaune plein écran | Tir du joueur | Post-process ou widget plein écran à opacité très faible et très courte ; à garder subtil |
| `lighting` | Halo de lumière jaune | Tir, et impact sur n'importe quoi | Point light éphémère ou sprite additif Niagara |
| `camShakesXY` | Tremblement de caméra, axe X ou Y | Tir (X), atterrissage après une chute (Y) | `UCameraShakeBase` + `ClientStartCameraShake`, patterns distincts par axe |
| `camBumpXY` | Décalage brusque et court de la caméra | Tir, atterrissage de haut | Offset additif sur la caméra, retour amorti vers 0 (pas une oscillation) |
| `camBumpZoom` | Zoom avant brusque et court | Atterrissage, dash | Variation brève du FOV ou de l'`ArmLength` du spring arm, retour amorti |

## 2. Déformation (squash & stretch)

| ID | Effet | Déclencheur | Piste UE5 |
|---|---|---|---|
| `mobSquashAndStrech` | L'ennemi se déforme comme de la gelée | Ennemi touché | Échelle du mesh visuel (pas de la capsule) avec retour élastique ; ou World Position Offset dans le matériau |
| `heroSquashAndStrech` | Le héros se déforme comme de la gelée | Saut, atterrissage, dash, tir | Idem, sur le mesh visuel uniquement |

> Ne jamais déformer le composant de collision : seulement la représentation visuelle.

## 3. Tir et animation

| ID | Effet | Déclencheur | Piste UE5 |
|---|---|---|---|
| `randomizeBullets` | Légère dispersion aléatoire des balles | Chaque tir | Petit angle aléatoire sur la direction du projectile (`FMath::VRandCone`) |
| `basicAnimations` | Animations de base du joueur | Permanent | Anim Blueprint / State Machine |
| `gunAnimations` | Animations de visée et de tir | Tir | Montage de tir + aim offset |

## 4. Particules et retour visuel du tir

| ID | Effet | Déclencheur | Piste UE5 |
|---|---|---|---|
| `cartridges` | Douilles éjectées qui tombent, rebondissent et restent longtemps au sol | Tir | Niagara avec collision et durée de vie longue (prévoir un plafond de particules) |
| `gunShotFx` | Éclat bref à la bouche du canon | Tir | Niagara muzzle flash attaché à un socket de l'arme |
| `bulletTail` | Traînée lumineuse derrière la balle | Balle en mouvement | Niagara ribbon ou trail sur le projectile |
| `bulletImpactFx` | Particules au point d'impact | Impact sur n'importe quoi | Niagara spawné au point de hit, orienté selon la normale |
| `bulletImpactDustFx` | Poussière qui retombe au point d'impact | Impact sur n'importe quoi | Niagara avec gravité |
| `bulletWallBurnFx` | Particules sur le mur qui passent du jaune au rouge puis disparaissent | Impact sur un mur | Niagara avec color over life ; ou decal émissif qui s'éteint |
| `blood` | Beaucoup de sang, qui colle aux murs et au sol et reste très longtemps | Ennemi touché | Niagara + decals persistants (plafonner le nombre, recycler les plus anciens) |
| `jumpFx` | Petit nuage de fumée | Saut, double saut, atterrissage | Niagara aux pieds |
| `dashFx` | Traînée de lignes bleues | Dash | Niagara ribbon ou ghost trail |
| `gunRecoilVisual` | Recul du sprite/mesh, sans toucher à la position physique | Tir | Offset du mesh visuel avec retour amorti |
| `gunRecoilMovement` | **Gameplay** — Recul physique réel du joueur | Tir | Petite impulsion opposée à la direction de tir sur le `CharacterMovementComponent` |

## 5. Contrôle et physique (gameplay)

| ID | Effet | Déclencheur | Piste UE5 |
|---|---|---|---|
| `controlLocks` | Contrôles bloqués un court instant (effet « sonné ») | Atterrissage de haut | Flag de lock temporaire côté Controller ou tag GAS ; à combiner avec `ctrlQueue` |
| `enemyPhysicalReactions` | Ennemis repoussés, peuvent tomber d'une falaise | Ennemi touché, atterrissage du joueur à proximité | `LaunchCharacter` ou impulsion physique (knockback) |

## 6. Mort

| ID | Effet | Déclencheur | Piste UE5 |
|---|---|---|---|
| `cadavers` | Un ennemi tué laisse un cadavre qui tombe au sol | Mort d'un ennemi | Ragdoll ou acteur cadavre séparé, avec durée de vie / pool |

## 7. Aides à la jouabilité (gameplay)

| ID | Effet | Déclencheur | Piste UE5 |
|---|---|---|---|
| `smallStepsHelper` | Montée automatique des petites marches en marchant | Déplacement | `MaxStepHeight` du `CharacterMovementComponent` |
| `cliffGrabHelper` | Accroche au rebord quand on le rate de quelques pixels | Saut près d'un rebord | Trace de détection de rebord + correction de position (ledge assist) |
| `climbFx` | Poussière quand une aide se déclenche | Marche ou rebord assisté | Niagara aux pieds / aux mains |
| `justInTimeJump` | Saut encore possible juste après avoir quitté le sol (coyote time) | Saut | Timer après la sortie du sol ; à implémenter (pas natif) |
| `ctrlQueue` | Entrées mises en file d'attente pendant un lock pour ne pas les perdre (input buffering) | Entrée pendant un lock | Buffer d'input avec fenêtre de validité courte (~0,1–0,2 s) |
| `slowMos` | Léger ralenti pour mieux anticiper | Dash | `UGameplayStatics::SetGlobalTimeDilation` brève, ou time dilation locale |

## 8. Rendu de base (référence du prototype)

| ID | Effet |
|---|---|
| `levelTextures` | Affichage des textures du niveau |
| `heroSprite` | Affichage du sprite du héros et de ses animations |

> Ces deux options servent dans la démo à montrer le jeu « nu ». Pas d'équivalent utile à implémenter.

---

## Pertinence par type de jeu

- **Top-down shooter** : sections 1 à 6 presque entièrement applicables (flash, shake, bump, recul, douilles, impacts, hit flash, knockback, cadavres). `ctrlQueue` et `slowMos` restent utiles. `randomizeBullets` à doser selon le design des armes.
- **Plateforme** : section 7 en priorité (coyote time, ledge assist, input buffering), plus `jumpFx`, `camBumpZoom` et le squash & stretch du héros.

## Points de vigilance

- **Empiler, mais doser** : le juice vient de la combinaison de nombreux petits effets ; chacun pris isolément doit rester discret.
- **Durées très courtes** : la plupart de ces effets durent entre 1 et quelques frames, ou quelques dixièmes de seconde.
- **Accessibilité** : prévoir au minimum des réglages pour le camera shake et les flashs plein écran.
- **Performance** : plafonner et recycler tout ce qui persiste (douilles, sang, cadavres, decals).
