# Aléatoire et génération procédurale

> **En bref** : où placer le hasard dans un jeu (avant ou après la décision), comment le rendre juste aux yeux du joueur (distributions, sacs, pity timers), comment le rendre reproductible (seeds), et quelles techniques de génération procédurale choisir en garantissant la jouabilité.

## Quand consulter cette fiche

- Tu ajoutes du loot, des coups critiques, des chances de toucher, des tirages de cartes.
- Les joueurs se plaignent que « le jeu triche » ou que « la chance décide de tout ».
- Tu génères des niveaux, des cartes, des donjons ou des rencontres.
- Tu dois reproduire un bug ou proposer un défi quotidien (seed partagée).

---

## 1. Où placer le hasard : entrée vs sortie

| | **Aléatoire d'entrée** (*input randomness*) | **Aléatoire de sortie** (*output randomness*) |
|---|---|---|
| Moment | **Avant** la décision du joueur | **Après** la décision du joueur |
| Exemple | Main de cartes tirée, carte générée, choix de récompenses proposés | Jet pour toucher, coup critique, dégâts aléatoires |
| Effet | Crée des situations nouvelles auxquelles le joueur s'adapte | Ajoute de la tension mais peut annuler une bonne décision |
| Ressenti | « J'ai bien joué avec ce que j'avais » | « Je n'ai pas eu de chance » |

Règles :
- **Privilégier l'aléatoire d'entrée** pour les jeux de réflexion et de stratégie : il nourrit la décision.
- L'aléatoire de sortie est acceptable quand **la décision a modifié les probabilités** (se mettre à couvert augmente les chances d'esquive) et que l'**échec reste récupérable**.
- **Réduire la variance** de l'aléatoire de sortie si les conséquences sont lourdes (plage de dégâts étroite, chance de toucher élevée).
- Afficher les probabilités quand la décision en dépend.

## 2. Hasard perçu vs hasard réel

Les humains jugent mal les probabilités :
- Un **90 % raté** paraît une injustice ; deux échecs consécutifs à 70 % paraissent suspects.
- On repère des « séries » dans un aléatoire pur, et on attend une alternance qui n'existe pas (erreur du joueur).
- Sid Meier (GDC 2010) rapporte que les joueurs de Civilization Revolution acceptaient mal qu'une unité à 3:1 perde, et que les chances ont été ajustées en faveur du joueur.

Conséquence : pour qu'un hasard **paraisse** juste, il faut souvent le rendre **moins aléatoire** et/ou **biaisé en faveur du joueur**. Exemple connu : les XCOM de Firaxis appliquent une aide cachée à la visée du joueur après des tirs ratés, selon la difficulté.

## 3. Outils pour un hasard juste

| Outil | Principe | Usage typique |
|---|---|---|
| **Shuffle bag** (sac mélangé) | Mettre N résultats dans un sac, tirer sans remise, remplir quand vide | Garantir une répartition (Tetris moderne : sac de 7 pièces) |
| **Pseudo-random distribution (PRD)** | La chance augmente à chaque échec, revient à la base après un succès ; la probabilité moyenne reste la même | Critiques, procs (Warcraft III, Dota 2) |
| **Pity timer** / garantie | Après N échecs, succès garanti | Loot rare, gacha, drop d'objet de quête |
| **Bad luck protection** progressive | Chance qui augmente lentement après chaque échec | Objets rares en jeu à long terme |
| **Variance réduite** | Moyenne de plusieurs tirages (ex. `(rand+rand)/2` → distribution en cloche) | Dégâts, quantités de ressources |
| **Anti-répétition** | Interdire le même résultat N fois de suite | Musique, répliques, salles générées |
| **Tirage pondéré** | Poids par résultat, ajustables dynamiquement | Tables de loot, spawn d'ennemis |

```text
# Shuffle bag
bag = []
draw():
    if bag.empty(): bag = shuffled(copy(contenu_de_base))
    return bag.pop()

# PRD simplifiée : chance = C × (échecs + 1)
proc():
    n += 1
    if rand() < C * n: n = 0; return true
    return false
# C est choisi pour que la fréquence moyenne corresponde à la probabilité nominale
# (ex. ~8,5 % pour une chance nominale de 25 %).
```

## 4. Seeds et reproductibilité

- Utiliser un **générateur pseudo-aléatoire (PRNG) avec seed**, jamais l'aléatoire global non contrôlé du moteur pour la logique de jeu.
- **Séparer les flux** : un PRNG pour la génération du monde, un pour le loot, un pour le combat, un pour la présentation (particules). Sinon, ajouter un effet visuel change le niveau généré.
- Avantages : **reproduire un bug**, défis quotidiens partagés, *speedruns* sur seed, replays, synchronisation multijoueur (voir [Multijoueur](multijoueur.md)).
- Enregistrer la seed dans les rapports de bug et l'afficher (au moins en debug).
- **Dériver** des sous-seeds de façon stable : `seed_salle = hash(seed_monde, x, y)` permet de générer une salle sans générer toutes les précédentes.
- Attention au **déterminisme** : les flottants peuvent diverger entre plateformes ; l'ordre d'itération des tables de hachage peut varier.

## 5. Génération procédurale : choisir une technique

| Technique | Produit | Forces | Faiblesses |
|---|---|---|---|
| **Fragments faits main assemblés** (*chunks*, salles préconçues) | Niveaux de plateforme/action, donjons | Qualité contrôlée, lisible, le plus utilisé en pratique (Spelunky, Dead Cells) | Répétition visible si peu de fragments |
| **BSP** (partition binaire de l'espace) | Donjons en salles + couloirs | Simple, salles bien réparties | Aspect très « grille » |
| **Automates cellulaires** | Grottes organiques | Très simple, formes naturelles | Zones déconnectées à nettoyer |
| **Bruit** (Perlin, simplex, valeur) | Terrains, biomes, densités | Continu, infini, contrôlable par octaves | Pas de structure de gameplay en soi |
| **Marche aléatoire** (*drunkard's walk*) | Grottes, couloirs | Connexité garantie | Peu de contrôle de forme |
| **Wave Function Collapse** (WFC) | Tuiles respectant des contraintes d'adjacence | Résultats cohérents localement à partir d'un exemple | Échecs (contradictions), peu de structure globale |
| **Grammaires** (L-systems, grammaires de graphes) | Végétation, missions, structures de quêtes | Structure globale, progression clé/porte | Conception de règles exigeante |
| **Graphe de mission puis spatialisation** | Donjons avec clés, verrous, boss | Garantit la progression | Plus complexe à mettre en œuvre |

Recommandations :
- **Commencer par des fragments faits main** : c'est la technique au meilleur rapport qualité/effort.
- **Structure globale d'abord, détail ensuite** : générer le graphe (départ, clé, porte, boss, sortie), puis placer les salles, puis remplir les salles.
- Combiner : bruit pour le terrain + fragments pour les points d'intérêt + règles pour le placement.
- Le procédural produit du **volume** ; la **qualité** vient des contraintes et du contenu fait main.

## 6. Garantir la jouabilité

Un niveau généré injouable est un bug. Toujours **vérifier, pas espérer**.

- **Connexité** : flood fill / BFS depuis le départ ; toutes les zones obligatoires doivent être atteignables.
- **Chemin critique garanti** : générer d'abord un chemin de l'entrée à la sortie (approche de Spelunky : chemin à travers une grille de salles, puis remplissage), puis ajouter les branches.
- **Atteignabilité réelle** : tenir compte des capacités du joueur (hauteur de saut, distance de dash). Tester avec un agent simulé ou en contraignant les fragments (sorties compatibles).
- **Progression clé/porte** : la clé doit être atteignable sans passer la porte qu'elle ouvre.
- **Budget et pacing** : nombre d'ennemis, de récompenses et de difficultés réparti selon une courbe, pas uniformément.
- **Plan B** : si la validation échoue, régénérer (avec une nouvelle sous-seed) ou corriger localement. Limiter le nombre d'essais et journaliser les échecs.
- **Pas d'impasse involontaire** sans récompense.

```text
generate_level(seed):
    for attempt in 0..MAX_ATTEMPTS:
        rng = PRNG(hash(seed, attempt))
        graph = make_mission_graph(rng)      # départ, clé, porte, boss, sortie
        layout = place_rooms(graph, rng)
        fill_rooms(layout, rng)
        if validate(layout): return layout   # connexité, clé avant porte, budget
    return fallback_level()
```

## 7. Valider et évaluer

- **Génération massive** : générer des milliers de niveaux et calculer des métriques (longueur du chemin critique, nombre de salles, densité d'ennemis, temps estimé).
- **Visualiser** la distribution des métriques pour repérer les cas extrêmes.
- **Galerie de seeds** : pouvoir rejouer une seed précise depuis un menu debug.
- **Seeds de référence** pour les tests de non-régression.
- Lire des niveaux générés **comme un level designer** : lisibilité, points de repère, rythme (voir [Level design](../contenu/level-design.md)).

---

## Anti-patterns et pièges

- **Aléatoire de sortie lourd** sur des décisions importantes (90 % raté = mort de l'unité clé).
- **Aléatoire non seedé** dans la logique : bugs impossibles à reproduire.
- **Un seul flux PRNG** pour tout : le moindre changement altère la génération.
- **Procédural sans validation** : niveaux bloquants.
- **« Infini » mais monotone** : 10 000 niveaux qui se ressemblent (« bouillie d'avoine procédurale »).
- **Probabilités cachées** quand la décision du joueur en dépend.
- **Loot purement aléatoire** sans garantie sur les objets importants.

## Checklist

- [ ] Chaque usage du hasard est classé entrée ou sortie, et le choix est volontaire.
- [ ] Les jets de sortie importants ont une variance réduite ou une protection contre la malchance.
- [ ] Les objets rares importants ont un pity timer ou une garantie.
- [ ] La logique de jeu utilise des PRNG seedés, avec des flux séparés par domaine.
- [ ] La seed est affichée en debug et incluse dans les rapports de bug.
- [ ] La génération construit la structure globale avant le détail.
- [ ] Chaque niveau généré est validé (connexité, chemin critique, clé avant porte).
- [ ] Un fallback existe si la génération échoue.
- [ ] Des milliers de seeds ont été générées et mesurées.

## Pistes d'implémentation

- Encapsuler le PRNG dans une classe du projet (`GameRandom`) avec seed explicite ; interdire l'appel direct à l'aléatoire global dans la logique.
- Algorithmes PRNG simples et portables : PCG, xorshift, SplitMix64.
- Séparer génération (pure, déterministe, testable hors moteur) et instanciation (spawn dans le moteur).
- **UE5** : `FRandomStream` avec seed ; PCG Framework (Procedural Content Generation) pour le placement à grande échelle.
- **Godot** : `RandomNumberGenerator` avec `seed` ; `FastNoiseLite` pour le bruit ; `TileMap`/`TileMapLayer` pour poser les tuiles.
- **Unity** : `System.Random` ou `Unity.Mathematics.Random` avec seed ; éviter `UnityEngine.Random` global pour la logique ; `Mathf.PerlinNoise` pour un bruit simple.

## Voir aussi

- [Équilibrage et difficulté](equilibrage-et-difficulte.md)
- [Économie](economie.md)
- [Progression](progression.md)
- [Level design](../contenu/level-design.md)
- [Roguelike](../genres/roguelike.md)
- [Deckbuilder et jeux de cartes](../genres/deckbuilder-cartes.md)

## Sources

- Noor Shaker, Julian Togelius & Mark J. Nelson, *Procedural Content Generation in Games*, Springer, 2016 — http://pcgbook.com/
- Tanya X. Short & Tarn Adams (dir.), *Procedural Generation in Game Design*, CRC Press, 2017.
- Derek Yu, *Spelunky*, Boss Fight Books, 2016.
- Maxim Gumin, *WaveFunctionCollapse* (2016) — https://github.com/mxgmn/WaveFunctionCollapse
- Amit Patel, *Red Blob Games* (bruit, cartes, grilles) — https://www.redblobgames.com/
- Sid Meier, « The Psychology of Game Design (Everything You Know Is Wrong) », GDC 2010.
- Geoffrey Engelstein & Isaac Shalev, *Building Blocks of Tabletop Game Design*, CRC Press, 2019.
- Ken Perlin, « An Image Synthesizer », SIGGRAPH 1985.
- Liquipedia Dota 2, « Pseudo-random distribution » — https://liquipedia.net/dota2/Pseudo_Random_Distribution
