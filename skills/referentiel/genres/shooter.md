# Shooter

> **En bref** : point d'entrée pour les jeux de tir — *top-down* / *twin-stick*, FPS/TPS et *shmup*. Ce qui fait la qualité d'un shooter : un tir qui « sonne » bien (feedback), des ennemis aux rôles lisibles et un rythme qui alterne tension et relâchement. Les détails vivent dans les fiches combat, IA et game feel.

## Quand consulter cette fiche

- Tu démarres un jeu dont l'action principale est de tirer.
- Le tir manque d'impact (« on tire dans du vide »).
- Les combats sont monotones ou toujours résolus de la même façon.
- Tu dois choisir entre *hitscan* et projectiles, ou régler un *time-to-kill*.

## Boucle centrale typique

```
Se positionner → Viser → Tirer → Feedback d'impact → Ennemi éliminé
      ↑                                                  ↓
 Gérer ressources (munitions, santé, cooldowns) ← Nouvelle vague / zone
```

- **Micro** : un tir et son impact (< 0,5 s). Il doit être satisfaisant seul.
- **Rencontre** (30 s – 3 min) : un groupe d'ennemis dans une arène.
- **Méta** : armes, améliorations, progression de niveau.

## Piliers transverses

1. **Feedback du tir** : son, muzzle flash, recul, impact, hit flash, réaction de l'ennemi. Catalogue complet dans [Game feel / juice](../ressenti/game-feel-juice.md) (sections 1 à 6).
2. **Lisibilité** : projectiles ennemis toujours plus visibles que ceux du joueur ; ennemis identifiables par silhouette.
3. **Rôles d'ennemis** : chaque type pose un problème différent (voir [IA et ennemis](../systemes/ia-ennemis.md)).
4. **Identité des armes** : chaque arme résout un problème différent, pas seulement « plus de dégâts ».
5. **Rythme** : alterner arènes intenses et moments calmes (voir [Level design](../contenu/level-design.md)).

## Paramètres clés

| Paramètre | Effet de design | Repère |
|---|---|---|
| *Time-to-kill* (TTK) | Court = réflexes et positionnement ; long = duels, tactique | Calculer TTK = PV / (dégâts × cadence) pour chaque arme |
| *Hitscan* vs projectile | Hitscan = instantané, précision pure ; projectile = anticipation, esquive possible | Ennemis en projectiles lents = esquivables donc justes |
| Dispersion / recul | Récompense le tir contrôlé, limite la portée efficace | Petit angle aléatoire, ou motif de recul fixe apprenable |
| Cadence | Ressenti de l'arme | Tirs lents = feedback fort par tir ; tirs rapides = feedback léger mais continu |
| Munitions | Force la variété d'armes | Pénurie modérée pousse à changer d'arme |
| Aide à la visée | Indispensable à la manette | Ralentissement du curseur près d'une cible, légère attraction |

Formules et télégraphie des attaques : [Combat](../systemes/combat.md).

## Sous-genre : *top-down* / *twin-stick*

- Stick gauche = déplacement, stick droit = visée (ou souris). Le déplacement et la visée sont **indépendants**.
- La **caméra** doit montrer plus d'espace dans la direction de visée (look-ahead vers le curseur). Voir [Caméra](../ressenti/camera.md).
- Une **esquive** (dash / roulade avec frames d'invincibilité) est quasi standard : elle transforme l'évitement en compétence.
- Densité d'ennemis élevée → feedback par tir plus léger, mais impacts et morts très marqués.
- Références : *Nuclear Throne* (feedback, rythme), *Enter the Gungeon* (roulade, patterns de balles lisibles), *Geometry Wars* (lisibilité néon, scoring).

## Sous-genre : FPS / TPS

- Le **mouvement** fait autant partie du combat que le tir (strafe, sprint, glissade, saut).
- Le recul est **visuel** (caméra, arme) et éventuellement **mécanique** (dispersion). Les distinguer.
- Indicateurs de touche : hitmarker, son de touche, son distinct pour les coups critiques / tirs à la tête.
- Indicateur directionnel de dégâts subis.
- Combat « *push-forward* » (*DOOM*, 2016) : récompenser l'agression (soin en achevant les ennemis) plutôt que la mise à couvert.
- Principe des « 30 secondes de fun » (attribué à Jaime Griesemer, *Halo*) : une boucle de rencontre courte, rejouée dans des contextes variés.
- TPS : gérer l'épaule de la caméra et les obstacles entre caméra et cible ; le tir part du réticule, pas du canon.
- Références : *DOOM* (2016), *Halo: Combat Evolved*, *Titanfall 2* (mouvement), *Gears of War* (couvert).

## Sous-genre : *shmup* (*shoot 'em up*)

- **Hitbox du joueur bien plus petite que le sprite**, idéalement affichée (un point visible) en mode concentré.
- Projectiles ennemis : formes et couleurs contrastées, vitesse modérée, motifs (*patterns*) apprenables. Le *danmaku* repose sur des motifs denses mais déterministes.
- Mode focus (ralentir le vaisseau en maintenant un bouton) pour les esquives fines.
- Systèmes de score (multiplicateurs, *graze* = frôler les balles) : ils donnent une raison de prendre des risques.
- Bombe comme bouton panique à usage limité.
- Références : *Ikaruga* (polarité), série *Touhou* (danmaku, hitbox), *DoDonPachi*.

## Pièges fréquents

- Feedback faible : le joueur ne sait pas s'il touche.
- Ennemis « éponges à balles » : PV élevés sans comportement intéressant = ennui.
- Toutes les armes se valent (même DPS, même portée) : aucun choix.
- Dégâts reçus sans source visible (tir hors écran, son absent).
- Projectiles ennemis qui se fondent dans le décor ou les effets du joueur.
- Effets de juice si chargés qu'ils masquent l'information (fumée, flashs sur les balles ennemies).
- Aide à la visée absente à la manette, ou si forte qu'elle joue à la place du joueur.

## Checklist

- [ ] Chaque tir a un son, un flash et un impact visibles.
- [ ] Toucher un ennemi produit un feedback distinct (hit flash, son, réaction).
- [ ] Les projectiles ennemis restent lisibles par-dessus tous les effets.
- [ ] Chaque type d'ennemi a un rôle et une silhouette distincts.
- [ ] Chaque arme a une niche (portée, cadence, zone, ressource).
- [ ] TTK calculé et comparé pour toutes les armes et tous les ennemis.
- [ ] Dégâts subis : direction et source toujours compréhensibles.
- [ ] Options : intensité du screen shake, des flashs, aide à la visée.

## Pistes d'implémentation

- Projectiles nombreux : *object pooling* obligatoire (balles, douilles, impacts).
- Séparer la direction de tir logique (gameplay) du recul visuel (présentation).
- Shmup : motifs de balles décrits en données (angle, nombre, vitesse, délai) pour itérer vite.
- **UE5** : `LineTraceSingleByChannel` pour le hitscan, `ProjectileMovementComponent` pour les projectiles.
- **Godot** : `RayCast2D/3D` pour le hitscan, `Area2D` pour les projectiles.
- **Unity** : `Physics.Raycast` ; projectiles en *pool* avec `ObjectPool<T>`.

## Voir aussi

- [Game feel / juice](../ressenti/game-feel-juice.md)
- [Combat](../systemes/combat.md)
- [IA et ennemis](../systemes/ia-ennemis.md)
- [Caméra](../ressenti/camera.md)
- [Contrôles et mouvement](../ressenti/controles-et-mouvement.md)
- [Audio](../interface/audio.md)
- [Multijoueur](../systemes/multijoueur.md) — pour le tir en ligne (compensation de latence)
- [Roguelike](roguelike.md) — pour les shooters à runs

## Sources

- Jan Willem Nijman (Vlambeer), « The Art of Screenshake », INDIGO 2013.
- Sébastien Bénard, prototype `deepnight/gamefeel`, 2019 — https://github.com/deepnight/gamefeel
- id Software, *DOOM* (2016), conférences de l'équipe sur le combat « push-forward » (GDC 2017).
- Jaime Griesemer, propos sur les « 30 secondes de fun » de *Halo* (rapportés notamment dans des entretiens Bungie).
