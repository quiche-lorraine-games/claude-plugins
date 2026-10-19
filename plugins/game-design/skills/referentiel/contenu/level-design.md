# Level design

> **En bref** : comment construire des espaces jouables qui enseignent, guident, rythment et mettent en valeur les mécaniques. Couvre le rythme et les courbes d'intensité, la structure apprendre-tester-twister (kishōtenketsu), le guidage du joueur (lignes de vue, repères, lumière, couleur, miettes de pain), le *gating* et le *backtracking*, les verrous et clés des metroidvanias, le *blockout*, les métriques de personnage, les espaces de combat et les points d'étranglement.

## Quand consulter cette fiche

- Tu crées un niveau, une salle, une zone, une carte ou un générateur de niveaux.
- Les playtesteurs se perdent, ne trouvent pas la sortie ou ratent un chemin important.
- Un niveau paraît monotone ou épuisant.
- Tu introduis une nouvelle mécanique et cherches comment l'enseigner par l'espace.
- Tu conçois un metroidvania ou un monde avec retours en arrière.
- Tu dois définir les dimensions standard (largeur de couloir, hauteur de plateforme).

---

## 1. Principes

- **Le niveau sert les mécaniques.** Chaque espace existe pour proposer un défi, enseigner, reposer, récompenser ou raconter. Un espace sans fonction est à supprimer ou à justifier.
- **Le joueur ne lit pas, il regarde.** Le guidage se fait par la géométrie, la lumière et le mouvement, pas par du texte.
- **Une idée par séquence.** Une séquence de niveau développe une mécanique ou une combinaison, puis passe à la suivante.
- **Gameplay d'abord, habillage ensuite.** Valider le niveau en *greybox* avant d'investir dans l'art.

Les « dix principes du bon level design » de Dan Taylor (GDC 2013) résument bien l'objectif : un bon niveau est amusant à parcourir, ne repose pas sur des mots pour raconter, dit quoi faire sans dire comment, enseigne constamment quelque chose, surprend, rend le joueur puissant, gère la difficulté, est efficace à produire, crée des émotions et est piloté par les mécaniques du jeu.

## 2. Rythme et courbes d'intensité

L'intensité (danger, nombre d'ennemis, exigence) doit **varier** dans le temps. Une intensité constante, haute ou basse, épuise ou ennuie.

```
intensité
   ^                         ___ boss
   |            /\          /   |
   |      /\   /  \   /\   /    |
   |  /\ /  \_/    \_/  \_/     |
   |_/  v                       \_ repos
   +-------------------------------> temps
```

Règles :
- **Pics et vallées** : après un pic d'intensité, prévoir une **zone de repos** (exploration, narration, sauvegarde, boutique).
- **Montée globale** : les pics grandissent jusqu'au climax du niveau ou du jeu.
- **Varier les types d'intensité** : combat, plateforme, puzzle, exploration, narration. Alterner évite la saturation.
- **Points de respiration explicites** : salles de sauvegarde, feux de camp, couloirs vides avant un boss (préparation psychologique).
- Le *AI Director* de *Left 4 Dead* applique ce cycle dynamiquement : montée, maintien du pic, retombée, relâche (Michael Booth, 2009). Voir [IA des ennemis](../systemes/ia-ennemis.md).

## 3. Apprendre, tester, twister : le kishōtenketsu

Structure narrative en quatre temps venue de la poésie chinoise et japonaise, utilisée explicitement par Koichi Hayashida (*Super Mario 3D Land*, *Super Mario 3D World*) pour construire ses niveaux :

| Temps | Japonais | Rôle dans un niveau | Exemple : plateforme qui bascule |
|---|---|---|---|
| 1 | **Ki** (introduction) | Présenter la mécanique dans un contexte sûr | Une plateforme bascule au-dessus du sol, pas de risque |
| 2 | **Shō** (développement) | Tester la mécanique avec un peu de risque | Plusieurs plateformes au-dessus du vide |
| 3 | **Ten** (retournement) | Twist : combiner ou détourner la mécanique | Les plateformes basculent selon un rythme musical, ou avec des ennemis |
| 4 | **Ketsu** (conclusion) | Démonstration de maîtrise, fin satisfaisante | Séquence finale plus exigeante, puis drapeau |

Règles :
- **Une mécanique principale par niveau** (approche Nintendo), développée puis abandonnée : le jeu reste frais.
- **Le twist est le moment mémorable** : c'est là que le joueur découvre une nouvelle utilisation de ce qu'il sait.
- Version simplifiée pour un agent : **introduire → répéter avec variation → combiner → maîtriser**.
- Voir aussi [Onboarding et tutoriels](onboarding-tutoriels.md).

## 4. Guidage du joueur

Le joueur doit savoir **où aller** sans qu'on le lui dise. Outils, du plus discret au plus explicite :

| Outil | Principe | Exemple |
|---|---|---|
| **Lignes de vue** (*sightlines*) | Ce que le joueur voit en entrant dans un espace détermine où il va | Encadrer la sortie au bout d'un couloir, en face de l'entrée |
| **Repères** (*landmarks*) | Objets visibles de loin servant d'orientation | Tour, montagne, phare |
| **« Weenie »** | Repère attractif qui attire le joueur vers lui (terme de Walt Disney pour le château de Disneyland, popularisé en jeu par Scott Rogers) | La Citadelle de *Half-Life 2*, l'Arbre-Monde (*Erdtree*) d'*Elden Ring* |
| **Vistas** | Point de vue panoramique qui montre la suite ou le chemin parcouru | Sortie de grotte dominant la vallée |
| **Lumière** | L'œil va vers la zone la plus lumineuse ou la plus contrastée | Porte éclairée dans une pièce sombre |
| **Couleur** | Une couleur de signalisation constante pour les éléments interactifs | Peinture jaune sur les rebords escaladables, tissu blanc sur les chemins |
| **Mouvement** | L'œil suit ce qui bouge | Oiseaux qui s'envolent vers la sortie, PNJ qui court |
| **Miettes de pain** (*breadcrumbs*) | Suite d'objets ramassables qui trace un chemin | Pièces en ligne au-dessus d'un saut |
| **Formes et affordances** | La forme suggère l'usage | Une caisse sous un rebord suggère « grimpe ici » |
| **Son** | Une source sonore attire | Musique, cascade, voix |
| **Marqueurs d'UI** | Boussole, flèche, marqueur de quête | Dernier recours ou option d'accessibilité |

Règles :
- **Un langage visuel constant** : si le jaune signifie « escaladable », il le signifie partout et rien d'autre n'est jaune vif. Documenter ce langage.
- **Chemin principal contrasté**, chemins secondaires moins visibles mais découvrables : la découverte récompense l'exploration.
- **Ne pas compter sur la couleur seule** (daltonisme) : doubler par la forme ou le motif (voir [Accessibilité](../interface/accessibilite.md)).
- **Tester le guidage** : observer des joueurs neufs en silence ; noter où ils hésitent, où ils regardent en entrant dans une salle (voir [Playtest et métriques](../production/playtest-et-metriques.md)).
- **Portes fermées lisibles** : une porte infranchissable doit avoir l'air infranchissable (et si possible indiquer ce qui l'ouvre).

## 5. Gating et backtracking

Le *gating* contrôle l'accès à une zone. Le *backtracking* consiste à revenir dans une zone déjà visitée.

| Type de verrou (*gate*) | Exemple |
|---|---|
| **Clé** (objet) | Clé rouge pour porte rouge |
| **Capacité** | Double saut, grappin, nage |
| **Narratif** | La zone s'ouvre après un événement |
| **Compétence** | Obstacle exigeant (le joueur passe quand il en est capable) |
| **Puissance / niveau** | Ennemis trop forts (verrou souple) |
| **Ressource** | Payer pour passer |

Règles :
- **Montrer le verrou avant la clé** : le joueur voit d'abord le rebord trop haut, puis obtient le double saut et pense « je sais où aller ». C'est le cœur du plaisir metroidvania.
- **Raccourcis** : après avoir atteint le fond d'une zone, ouvrir un raccourci vers le début (porte déverrouillable d'un seul côté, échelle à déployer). Rend le backtracking rapide et satisfaisant (*Dark Souls* en fait un principe central).
- **Backtracking enrichi** : revenir dans une zone doit offrir du nouveau (ennemis différents, chemins débloqués, raccourcis), sinon le joueur le vit comme du remplissage.
- **Réduire le coût du retour** : téléporteurs, raccourcis, déplacement plus rapide acquis avec la progression.
- **Carte** : indispensable dès que le backtracking est important ; marquer les verrous rencontrés.

### Verrous et clés : la structure d'un metroidvania

- Représenter le niveau comme un **graphe** : nœuds = zones, arêtes = passages, certaines arêtes portent un verrou.
- Vérifier que le graphe est **résoluble** : pour chaque verrou, la clé est accessible sans ce verrou.
- **Verrous à double usage** : une capacité ouvre plusieurs verrous et sert aussi en combat ou en déplacement.
- **Linéarité réelle vs perçue** : beaucoup de metroidvanias sont presque linéaires dans leur ordre de clés, mais l'espace ouvert donne une sensation de liberté. Plusieurs clés accessibles en parallèle augmentent la liberté réelle.
- **Séquence brisée** (*sequence breaking*) : les joueurs experts contourneront les verrous. Décider si c'est toléré (souvent apprécié des *speedrunners*) et s'assurer que le jeu ne casse pas (scripts qui supposent un ordre).

Référence : la série vidéo *Boss Keys* de Mark Brown (Game Maker's Toolkit) analyse les graphes de verrous de nombreux donjons Zelda et metroidvanias.

## 6. Blockout (greybox)

Le *blockout* est la construction du niveau avec des formes simples (cubes, rampes) avant tout habillage.

Règles :
- **Toujours commencer par un blockout jouable** et le tester.
- **Couleurs fonctionnelles** : une couleur par fonction (sol, mur, escaladable, danger, interactif).
- **Plan papier ou diagramme de flux** avant le blockout : chemin principal, chemins secondaires, pics d'intensité, points de repos.
- **Itérer vite** : modifier un blockout coûte quelques minutes ; modifier un niveau habillé coûte des jours.
- **Modularité** : construire avec des modules aux dimensions standard (grille) facilite le passage à l'art (approche *Skyrim*, Joel Burgess, GDC 2013).
- **Ne pas tomber amoureux du blockout** : il doit être laid et jetable.

## 7. Métriques de personnage

Les métriques sont les dimensions et capacités du personnage qui dictent celles du monde. **Définir les métriques avant de construire les niveaux.**

À mesurer depuis le contrôleur réel du personnage :

| Métrique | Usage |
|---|---|
| Taille et largeur de la collision | Largeur des passages, hauteur des plafonds |
| Hauteur de saut max (simple, double) | Hauteur des rebords franchissables / infranchissables |
| Distance de saut max (à l'arrêt, en course) | Largeur des trous |
| Hauteur de marche franchie automatiquement | Hauteur des marches, des bordures |
| Vitesse de déplacement | Temps de traversée, distance entre points d'intérêt |
| Hauteur accroupie | Passages bas |
| Portée des attaques et capacités | Taille des arènes |

Règles :
- **Marges franches** : un obstacle est soit clairement franchissable, soit clairement infranchissable. Éviter les écarts à quelques pourcents de la limite, sauf pour un défi volontaire. Règle empirique : rester **au moins 10–20 % en dessous** du maximum pour un saut « normal », et **nettement au-dessus** pour un mur infranchissable.
- **Niveau de test des métriques** (*metrics gym*) : une scène avec des trous, rebords, couloirs de tailles graduées, étiquetées. Indispensable pour calibrer et pour revalider après tout changement du contrôleur.
- **Toute modification du contrôleur (vitesse, saut) invalide potentiellement tous les niveaux** : figer les métriques tôt.
- **Échelle** : savoir que 1 unité = 1 cm dans Unreal, 1 m dans Unity et Godot. Les proportions réalistes paraissent souvent trop petites en jeu : les espaces de jeu sont généralement plus grands que la réalité (portes, couloirs) pour la caméra et la maniabilité.
- Voir [Contrôles et mouvement](../ressenti/controles-et-mouvement.md) et [Caméra](../ressenti/camera.md).

## 8. Espaces de combat

| Élément | Rôle |
|---|---|
| **Couverture** | Protège, crée des positions ; varier hauteur (basse / haute) et solidité (destructible) |
| **Hauteur** | Avantage tactique ; doit être accessible et contestable |
| **Flancs** | Chemins alternatifs pour contourner ; récompensent l'initiative |
| **Points d'étranglement** (*choke points*) | Passages étroits où les forces se concentrent ; créent des moments de tension et des défenses |
| **Zones ouvertes** | Mouvement, esquive, combats contre groupes |
| **Entrées / sorties** | Le joueur doit pouvoir lire l'arène en entrant ; prévoir une issue ou un repli |
| **Dangers environnementaux** | Barils explosifs, vide, pièges : outils pour le joueur et les ennemis |

Règles :
- **Lisibilité de l'arène** : depuis l'entrée, le joueur doit voir la forme générale, les couvertures et les ennemis principaux.
- **Laisser le joueur choisir son approche** : au moins deux options (frontale, flanc, discrétion).
- **Taille adaptée** aux portées : une arène trop petite rend les armes à distance inutiles, trop grande rend la mêlée frustrante.
- **Placement des ennemis** : en partie visibles à l'arrivée ; ne pas faire apparaître d'ennemis dans le dos sans signal (son, porte qui s'ouvre).
- **Boucles** (*loops*) : en multijoueur et en action, des parcours circulaires évitent les impasses et permettent de fuir.
- **Multijoueur** : équilibrer les spawns et les lignes de vue des deux camps ; la symétrie est la solution la plus simple, l'asymétrie demande beaucoup de tests.
- Voir [Combat](../systemes/combat.md) et [IA des ennemis](../systemes/ia-ennemis.md).

---

## Anti-patterns et pièges

- **Couloir sans fonction** : déplacement long sans choix ni événement.
- **Mort invisible** : piège ou trou impossible à anticiper la première fois (*trial and error* imposé).
- **Langage visuel incohérent** : le joueur essaie d'escalader tout ce qui est jaune, mais seuls certains rebords fonctionnent.
- **Habiller avant de tester** : plusieurs jours d'art jetés après le premier playtest.
- **Métriques floues** : sauts « presque » possibles, frustration et exploits.
- **Backtracking vide** : revenir sans raccourci ni nouveauté.
- **Intensité plate** : 20 minutes de combat sans pause.
- **Guidage uniquement par marqueur d'UI** : le joueur regarde la boussole au lieu du monde.

## Checklist

- [ ] Les métriques du personnage sont mesurées et documentées ; un niveau de test existe.
- [ ] Le niveau a un diagramme de flux (chemin principal, secondaires, pics, repos).
- [ ] Le niveau a été joué en blockout avant tout habillage.
- [ ] Chaque séquence suit introduire → développer → twister → conclure (ou équivalent).
- [ ] La courbe d'intensité a des pics et des vallées, avec une montée globale.
- [ ] Depuis chaque entrée de salle, la sortie ou la direction principale est visible ou suggérée.
- [ ] Un langage visuel (couleurs, formes) est défini et appliqué de façon constante, sans reposer sur la couleur seule.
- [ ] Chaque verrou est montré avant sa clé ; le graphe de verrous est résoluble.
- [ ] Les zones à backtracking ont des raccourcis ou du nouveau contenu.
- [ ] Les arènes offrent au moins deux approches et sont lisibles depuis l'entrée.
- [ ] Le guidage a été testé avec au moins un joueur qui n'a jamais vu le niveau.

## Pistes d'implémentation

- **Niveau de métriques** généré ou construit une fois, rejoué à chaque changement du contrôleur (idéalement avec un test automatisé : un bot rejoue des sauts de référence).
- **Graphe de verrous en données** pour vérifier automatiquement la résolubilité :

```
// zones: nœuds ; edges: (a, b, requiredKey ou null) ; keys: zone -> clé obtenue
function isSolvable(start, goal):
    owned = {}
    reachable = {start}
    changed = true
    while changed:
        changed = false
        for zone in reachable: owned.add(keysIn(zone))
        for (a, b, key) in edges:
            if a in reachable and b not in reachable and (key == null or key in owned):
                reachable.add(b); changed = true
    return goal in reachable
```

- **Couleurs de blockout** via un matériau/shader unique paramétré par fonction.
- **Télémétrie de position** : enregistrer la trajectoire et les morts des testeurs pour produire des cartes de chaleur (*heatmaps*), voir [Playtest et métriques](../production/playtest-et-metriques.md).
- **UE5** : outils de modélisation intégrés (*Modeling Mode*, anciennement BSP / *Geometry Brushes*) pour le blockout ; *Level Instances* pour les modules réutilisables ; *World Partition* pour les mondes ouverts.
- **Godot** : nœuds CSG pour le blockout 3D ; `TileMap` / `TileMapLayer` en 2D.
- **Unity** : ProBuilder pour le blockout ; Tilemap en 2D.

## Voir aussi

- [Onboarding et tutoriels](onboarding-tutoriels.md) — enseigner par l'espace.
- [Narration](narration.md) — narration environnementale.
- [Contrôles et mouvement](../ressenti/controles-et-mouvement.md), [Caméra](../ressenti/camera.md).
- [Combat](../systemes/combat.md), [IA des ennemis](../systemes/ia-ennemis.md).
- [Aléatoire et procédural](../systemes/aleatoire-et-procedural.md) — génération de niveaux.
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md).
- Genres : [Plateforme](../genres/plateforme.md), [Shooter](../genres/shooter.md), [Puzzle](../genres/puzzle.md).

## Sources

- Christopher W. Totten, *An Architectural Approach to Level Design*, 2e éd., CRC Press, 2019.
- Scott Rogers, *Level Up! The Guide to Great Video Game Design*, 2e éd., Wiley, 2014 (weenies, métriques).
- Dan Taylor, « Ten Principles of Good Level Design », GDC 2013.
- Koichi Hayashida, entretien sur le kishōtenketsu dans *Super Mario 3D Land*, Gamasutra, 2012.
- Mark Brown, *Super Mario 3D World's 4 Step Level Design*, Game Maker's Toolkit, 2015, et série *Boss Keys* — https://www.youtube.com/@GMTK
- Michael Booth, « The AI Systems of Left 4 Dead », Valve, 2009.
- Joel Burgess, « Skyrim's Modular Approach to Level Design », GDC 2013.
- Joris Dormans, « Adventures in Level Design: Generating Missions and Spaces for Action Adventure Games », PCG Workshop, 2010.
