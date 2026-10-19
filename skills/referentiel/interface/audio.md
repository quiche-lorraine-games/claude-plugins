# Audio

> **En bref** : le son est un canal d'information de gameplay autant qu'un habillage. Cette fiche couvre le son comme feedback, la hiérarchie et le mixage, les variations anti-répétition, la musique adaptative (horizontale, verticale, stingers), l'audio spatial et les signaux audio pour l'accessibilité.

## Quand consulter cette fiche

- Tu ajoutes les sons d'une action (tir, impact, saut, ramassage, UI).
- Le jeu est « muet », ou au contraire le mix est confus quand beaucoup de choses arrivent.
- Un son devient agaçant à force de répétition.
- Tu intègres une musique qui doit réagir à la situation (exploration, combat, boss).
- Le joueur rate des menaces qui viennent de derrière ou hors champ.
- Tu prépares les options audio et les sous-titres.

---

## 1. Principes

- **Le son est le feedback le plus rapide** à percevoir pour beaucoup de joueurs et il fonctionne hors champ de vision. Il confirme qu'une action a eu lieu (« le coup a porté »).
- **Chaque son de gameplay doit porter une information** : quoi (type d'événement), qui (joueur, allié, ennemi), où (direction, distance), combien (intensité, critique).
- **Hiérarchiser** : tous les sons ne se valent pas. Un mix où tout est fort ne transmet rien.
- **Cohérence** : un même événement produit toujours la même *famille* de son. Le joueur apprend le langage sonore.
- **Redondance** : toute information sonore critique a un équivalent visuel (et inversement). Voir [Accessibilité](accessibilite.md).
- Le son est de la **présentation**, mais un signal sonore qui télégraphie une attaque est une information de **gameplay** : le traiter comme tel (timing fiable, toujours audible).

---

## 2. Le son comme feedback de gameplay

| Événement | Ce que le son doit communiquer | Conseils |
|---|---|---|
| Action du joueur (tir, saut, attaque) | L'action est partie | Attaque franche (*transient*) dès la frame de l'appui ; c'est du ressenti autant que de l'info |
| Impact / coup porté | Le coup a touché, avec quelle force | Son distinct pour : touché, critique, bloqué, raté, ennemi tué |
| Dégâts reçus | Je suis touché | Toujours audible, distinct des dégâts infligés |
| Télégraphie d'une attaque ennemie | Une attaque arrive, de tel type | Un son par type d'attaque ; timing fixe par rapport à la frame active |
| État critique | Vie basse, munitions basses | Signal persistant mais non agaçant (battement, filtre), désactivable |
| Ressource gagnée | J'ai ramassé quelque chose | Court, positif ; montée de hauteur pour les ramassages enchaînés (combo) |
| UI | Focus, validation, refus, ouverture | Discret, cohérent ; le refus a un son distinct de la validation |
| Ambiance | Où suis-je, qu'est-ce qui m'entoure | Boucles d'ambiance + sons ponctuels positionnés |

Règles :
- **Synchronisation** : le son doit partir à la même frame que l'événement visuel. Un décalage audible casse l'impact.
- Le **son du joueur** est souvent légèrement mis en avant par rapport aux sons identiques produits par les autres.
- Combiner le son avec le hit stop, le flash et le shake pour l'impact : voir [Game feel](../ressenti/game-feel-juice.md).

---

## 3. Hiérarchie, priorités et mixage

### 3.1 Priorités et limitation de voix

Le nombre de sons simultanés est limité (budget de voix) et un excès de sons rend le mix illisible.

- Donner une **priorité** à chaque son (ex. : dialogue > télégraphie ennemie > dégâts reçus > actions du joueur > impacts > ambiance).
- **Limiter les instances par événement** (ex. maximum 3–5 impacts identiques simultanés comme point de départ) et voler la voix la plus ancienne ou la plus faible.
- **Virtualiser** les sons inaudibles (trop loin) au lieu de les jouer.

### 3.2 Bus et ducking

- Organiser le mix en **bus** : Musique, Effets (sous-bus : joueur, ennemis, environnement), Dialogue, UI. Chaque bus a un réglage de volume pour le joueur.
- **Ducking / sidechain** : baisser la musique et les ambiances quand un dialogue ou un signal critique joue. Abaisser légèrement les sons secondaires lors d'un gros impact pour le faire ressortir.
- Garder une **marge** (*headroom*) : ne pas mixer chaque son au maximum, utiliser un limiteur sur le bus maître.

### 3.3 Mixage dynamique

- États de mix (*snapshots*) : exploration, combat, menu, pause, cinématique. Passer de l'un à l'autre avec un fondu.
- Pause : atténuer ou filtrer (passe-bas) les sons du monde plutôt que les couper net.

---

## 4. Variations anti-répétition

Un son identique joué souvent devient un « effet mitraillette » et fatigue l'oreille.

| Technique | Principe | Point de départ |
|---|---|---|
| Pools de variations | Plusieurs enregistrements pour un même événement | 3–8 variations pour un son fréquent (pas, tirs, impacts) |
| Tirage sans répétition immédiate (*random no-repeat / shuffle*) | Ne pas rejouer la même variation deux fois de suite | Toujours pour les pools |
| Variation de hauteur | Légère modification aléatoire du pitch | Quelques pour cent (±1–2 demi-tons au maximum) |
| Variation de volume | Légère modification aléatoire du volume | Quelques dB |
| Composition par couches | Un son = attaque + corps + queue, chacun tiré dans son pool | Multiplie les combinaisons |
| Variation contextuelle | Le son dépend de la surface, de l'arme, de la taille | Pas selon la matière du sol, impacts selon la surface |
| Refroidissement (*cooldown*) | Un même son ne peut pas rejouer avant un délai | Pour les voix/aboiements de PNJ (*barks*) surtout |

- Les **voix et répliques de PNJ** (*barks*) sont les plus sensibles à la répétition : prévoir de nombreuses variantes et un historique des répliques jouées récemment.

---

## 5. Musique adaptative

| Technique | Principe | Usage |
|---|---|---|
| Re-séquençage horizontal (*horizontal resequencing*) | La musique passe d'un segment à un autre, avec transitions calées sur la mesure ou le temps | Changement d'état net (exploration → combat), progression par phases de boss |
| Superposition verticale (*vertical layering / remixing*) | Plusieurs pistes synchronisées dont on module le volume | Intensité progressive (ajouter percussions quand les ennemis approchent) |
| Stingers | Courtes phrases musicales jouées par-dessus, calées sur le tempo | Événement ponctuel : découverte, victoire, ennemi repéré, montée de niveau |
| Transitions par segments | Segment de transition dédié entre deux morceaux | Éviter les coupures et les fondus « mous » |
| Paramètres continus | Une valeur de jeu (intensité, vie, danger) pilote filtres et couches | Tension continue |

Règles :
- **Hystérésis** sur les changements d'état musical : entrer en musique de combat vite, en sortir après un délai sans menace (plusieurs secondes), sinon la musique oscille à chaque ennemi qui apparaît et disparaît.
- Transitions **quantifiées** (au temps ou à la mesure suivante) pour rester musicales ; un stinger peut masquer une transition.
- Prévoir des boucles suffisamment longues ou des silences : une boucle courte répétée longtemps devient pénible. Le silence est un outil.
- La musique ne doit pas masquer les signaux de gameplay (ducking, choix des fréquences).

---

## 6. Audio spatial

- **Atténuation avec la distance** : courbe choisie pour la lisibilité (pas forcément physique) ; les sons importants restent audibles plus loin.
- **Panoramique / spatialisation** : la direction d'un son doit être identifiable. En 3D, la spatialisation binaurale (HRTF) aide au casque pour l'avant/arrière et la hauteur.
- **Occlusion et obstruction** : filtrer (passe-bas) les sons derrière un mur ; indique qu'une menace est proche mais pas en vue.
- **Réverbération par zone** : renforce la perception de l'espace (grotte, couloir, extérieur).
- **Écouteur** (*listener*) : en troisième personne, le placer entre la caméra et le personnage, ou sur le personnage pour l'atténuation et sur la caméra pour l'orientation. Choisir et rester cohérent.
- Le joueur doit pouvoir **localiser au son les menaces hors champ** dans un jeu d'action.

---

## 7. Signaux audio et accessibilité

- **Sous-titres et légendes** : sous-titres pour les dialogues, *et* légendes pour les sons importants (« [Pas derrière toi] », « [Grognement à gauche] »). Voir [Accessibilité](accessibilite.md).
- **Indicateurs visuels de son** : flèche ou icône directionnelle pour les sons importants (style « visualisation du son »).
- **Mono** : option de sortie mono pour les joueurs malentendants d'une oreille ; ne jamais encoder une information *uniquement* dans la stéréo.
- **Réglages séparés** pour chaque bus (musique, effets, dialogues, UI), y compris la possibilité de couper la musique.
- **Signaux audio pour joueurs malvoyants** : ces signaux sont une base pour rendre le jeu jouable sans voir (sons de navigation, de bord de plateforme, de cible). Certains jeux AAA ont montré qu'un jeu d'action peut être rendu jouable ainsi (*The Last of Us Part II*).
- **Retours haptiques** comme troisième canal, réglables.
- Éviter les sons stridents ou à très haute fréquence persistants ; plafonner les volumes soudains.

---

## 8. Anti-patterns

- Son unique répété à l'identique à chaque tir ou chaque pas.
- Pas de son distinct entre « touché » et « raté », ou entre dégâts infligés et reçus.
- Musique de combat qui démarre et s'arrête à chaque ennemi.
- Signal critique uniquement audio (ou uniquement visuel).
- Mix où tout est au maximum ; dialogues couverts par la musique.
- Sons d'UI absents (le menu paraît mort) ou trop présents (fatigue).
- Son déclenché quelques frames après l'événement visuel.

---

## Checklist

- [ ] Chaque action du joueur a un son qui part à la même frame que l'action.
- [ ] Les impacts distinguent touché / critique / bloqué / raté / mort.
- [ ] Les attaques ennemies importantes ont un signal sonore de télégraphie fiable.
- [ ] Une table de priorités de sons existe ; les instances simultanées sont limitées.
- [ ] Le mix est organisé en bus avec un volume réglable par bus.
- [ ] La musique et les ambiances sont atténuées sous les dialogues et signaux critiques.
- [ ] Les sons fréquents ont des variations (pool + pitch/volume) sans répétition immédiate.
- [ ] La musique adaptative a une hystérésis et des transitions calées sur le tempo.
- [ ] Les menaces hors champ sont localisables au son, et ont un équivalent visuel.
- [ ] Sous-titres, légendes de sons, option mono disponibles.

## Pistes d'implémentation

- **Agnostique** : déclencher les sons par **événements nommés** (`play_event("weapon/rifle/fire", position)`) plutôt que par fichiers ; le système audio choisit la variation, applique la priorité et le bus. Centraliser la table priorités / limites d'instances.
- **Middleware** : FMOD et Wwise gèrent nativement événements, conteneurs aléatoires sans répétition, limites d'instances, snapshots de mix, musique interactive (transitions quantifiées, stingers) et paramètres temps réel. Les deux s'intègrent à UE5, Unity et Godot (via extensions).
- **UE5** : MetaSounds pour les sons procéduraux, *Sound Classes* / *Submixes* pour les bus, *Sound Concurrency* pour les limites d'instances, *Quartz* pour caler des événements sur le tempo.
- **Godot** : bus audio (`AudioServer`), `AudioStreamRandomizer` pour les variations, `AudioStreamPlayer3D` pour la spatialisation, `AudioStreamInteractive` (Godot 4.3+) pour la musique adaptative.
- **Unity** : `AudioMixer` (groupes, snapshots, ducking), `AudioSource` 3D.

## Voir aussi

- [Game feel / juice](../ressenti/game-feel-juice.md)
- [UI, UX et HUD](ui-ux-hud.md)
- [Accessibilité](accessibilite.md)
- [Combat](../systemes/combat.md)
- [IA et ennemis](../systemes/ia-ennemis.md)
- [Narration](../contenu/narration.md)

## Sources

- Karen Collins, *Game Sound: An Introduction to the History, Theory, and Practice of Video Game Music and Sound Design*, MIT Press, 2008.
- Winifred Phillips, *A Composer's Guide to Game Music*, MIT Press, 2014.
- Documentation officielle FMOD Studio et Audiokinetic Wwise (événements, conteneurs, musique interactive).
- Game Accessibility Guidelines, section « Hearing », https://gameaccessibilityguidelines.com
