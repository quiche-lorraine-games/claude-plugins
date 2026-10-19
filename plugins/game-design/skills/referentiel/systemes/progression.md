# Progression

> **En bref** : comment le joueur et son avatar deviennent plus forts, plus capables ou plus libres au fil du jeu. Couvre la distinction compétence du joueur / puissance du personnage, les courbes d'expérience (formules et effets), les déblocages, les arbres de compétences, la progression verticale et horizontale, le *power creep*, la méta-progression, le rythme des récompenses et l'éthique des programmes de renforcement.

## Quand consulter cette fiche

- Tu conçois ou implémentes un système de niveaux, d'XP, de compétences ou de déblocages.
- Tu dois choisir une formule de courbe d'XP et estimer le temps de jeu par niveau.
- Les playtesteurs disent « je stagne », « je suis trop fort trop vite » ou « je ne sens pas la différence quand je monte de niveau ».
- Tu ajoutes une méta-progression à un roguelike/roguelite.
- Tu hésites entre donner plus de puissance (vertical) ou plus d'options (horizontal).
- Tu ajoutes des récompenses récurrentes (quêtes journalières, passes de saison) et veux éviter les mécaniques manipulatrices.

---

## 1. Deux progressions distinctes

| Axe | Ce qui progresse | Exemple | Mesure |
|---|---|---|---|
| **Progression du joueur** (*player skill*) | La maîtrise réelle : réflexes, connaissance des systèmes, stratégie | Battre un boss de *Dark Souls* au niveau 1 | Taux de réussite, temps, erreurs |
| **Progression du personnage** (*character power*) | Les chiffres et capacités de l'avatar | Monter niveau 50 dans un RPG | Stats, capacités, équipement |
| **Progression de l'accès** (*content / options*) | Ce que le joueur peut faire ou visiter | Nouveaux biomes, armes, modes | Contenu débloqué |

Règles :
- **Toujours décider quel axe porte le jeu.** Un jeu d'action exigeant mise sur la compétence ; un RPG accessible mise sur la puissance du personnage. La plupart des jeux mélangent, mais l'un domine.
- La puissance du personnage peut **compenser** un manque de compétence (*grinding* pour passer un obstacle). C'est une aide de difficulté implicite : la conserver volontairement, ou la plafonner si le jeu doit tester la compétence.
- Si la puissance progresse **plus vite** que la difficulté, le jeu devient trivial. Si elle progresse **moins vite**, le joueur se sent bloqué. Le ratio puissance/difficulté est le paramètre clé (voir [Équilibrage et difficulté](equilibrage-et-difficulte.md)).

## 2. Courbes d'expérience

### Formules de base

Notations : `n` = niveau visé, `XP(n)` = XP **cumulée** requise pour atteindre `n`, `Δ(n) = XP(n) − XP(n−1)` = XP à gagner pour passer de `n−1` à `n`.

| Type | XP cumulée | Δ par niveau | Effet ressenti |
|---|---|---|---|
| **Linéaire** | `XP(n) = a·(n−1)` | constant `a` | Rythme régulier ; si les gains d'XP augmentent, les niveaux accélèrent → à combiner avec des gains fixes |
| **Polynomiale** (quadratique, cubique) | `XP(n) = a·(n−1)^k`, k ≈ 1,5 à 3 | croît en `n^(k−1)` | Ralentissement progressif et prévisible ; le plus courant |
| **Triangulaire** | `XP(n) = a·n(n−1)/2` | `a·(n−1)` (croît de `a` à chaque niveau) | Cas particulier quadratique, facile à lire pour le joueur |
| **Exponentielle** | `XP(n) = a·(b^(n−1) − 1)`, b ≈ 1,05 à 1,2 | croît en `b^n` | Les derniers niveaux deviennent extrêmement longs : crée un « mur » ; utile pour des niveaux de prestige ou un plafond doux |
| **Par paliers** (table manuelle) | table | libre | Contrôle total ; recommandé une fois la forme générale validée |

Exemples réels :
- *D&D 3.5* : XP cumulée = `500·n·(n−1)` (1 000 pour le niveau 2, 3 000 pour le 3, 6 000 pour le 4) → triangulaire.
- *Pokémon*, courbe « Moyenne rapide » : XP cumulée = `n³` → cubique.

### Ce qui compte vraiment : le temps par niveau

La forme de la courbe d'XP **seule ne dit rien**. Le joueur ressent le **temps** (ou le nombre d'actions) par niveau :

```
temps_par_niveau(n) = Δ(n) / gain_XP_par_minute(n)
```

Le gain d'XP par minute augmente presque toujours (ennemis plus forts, quêtes plus riches). Donc :
- Courbe d'XP quadratique + gains qui croissent linéairement ≈ temps par niveau **constant**.
- Courbe d'XP exponentielle + gains linéaires = temps par niveau **qui explose**.

**Méthode recommandée** :
1. Fixer d'abord la **durée cible** : temps total du jeu, et temps par niveau au début, au milieu, à la fin (ex. point de départ : premiers niveaux en quelques minutes, puis allongement progressif).
2. Fixer la courbe de **gains** (XP par ennemi/quête selon le niveau).
3. **En déduire** `Δ(n)`, puis lisser avec une formule ou une table.
4. Simuler dans un tableur avec un profil de joueur (actions/minute, temps d'exploration), puis valider en playtest.

### Règles empiriques

- **Premiers niveaux rapides** : donner un ou deux niveaux dans la première session courte pour montrer que le système existe.
- **Éviter les niveaux « vides »** : chaque niveau doit apporter quelque chose de perceptible (stat visible, point de compétence, déblocage). Sinon, réduire le nombre de niveaux.
- **XP de rattrapage** (*catch-up*) : un bonus d'XP quand le joueur est en dessous du niveau attendu de la zone limite les écarts.
- **Plafond** : un niveau maximum facilite l'équilibrage du contenu final. Au-delà, utiliser une progression horizontale ou de prestige.

## 3. Déblocages

Un déblocage donne accès à une nouvelle chose : arme, capacité, zone, mode, personnage, cosmétique.

- **Espacer les déblocages** pour qu'il y ait toujours un « prochain objectif » visible (voir § 7, rythme).
- **Annoncer les déblocages à venir** (silhouettes grisées, « niveau 10 : double saut ») : la connaissance d'un objectif proche motive.
- **Déblocage = enseignement** : chaque nouvelle capacité est l'occasion d'un mini-tutoriel et d'un espace conçu pour la mettre en valeur (voir [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)).
- **Ne pas verrouiller le fun central derrière des heures de jeu** : la mécanique principale doit être disponible et satisfaisante dès le début.
- Pour un **metroidvania**, chaque capacité est aussi une clé de navigation (voir [Level design](../contenu/level-design.md), section gating).

## 4. Arbres de compétences

| Structure | Description | Usage |
|---|---|---|
| **Liste plate** | Améliorations indépendantes achetables | Jeux courts, peu de choix |
| **Arbre** | Prérequis ; branches spécialisées | RPG, choix de build |
| **Graphe / grille** | Nœuds connectés, plusieurs chemins (*Path of Exile*, *Final Fantasy X*) | Builds complexes, joueurs experts |
| **Paliers** | Choisir 1 option parmi N à chaque palier | Choix lisibles, limite les combinaisons |

Règles :
- **Choix intéressants** : chaque nœud doit être une vraie alternative, pas « +2 % de dégâts » contre « +2 % de dégâts critiques ». Privilégier les nœuds qui **changent le comportement** (nouvelle action, nouvelle interaction) aux nœuds purement statistiques.
- **Pièges à débutant** (*noob traps*) : un nœud qui paraît attirant mais rend le personnage faible. Les identifier en playtest et les supprimer, ou rendre leur coût évident.
- **Respécialisation** (*respec*) : la proposer, au moins payante. Sans respec, un mauvais choix tôt peut ruiner une partie de 40 heures.
- **Lisibilité** : afficher l'effet concret (« Tes flèches traversent 1 ennemi ») plutôt que des formules internes.
- **Nœuds « clés de voûte »** (*keystones*) : de rares nœuds qui transforment le style de jeu (avec un inconvénient) créent des builds mémorables.
- **Ne pas multiplier les monnaies de compétence** : un seul type de point est plus lisible (voir [Économie](economie.md)).

## 5. Progression verticale vs horizontale

| | Verticale | Horizontale |
|---|---|---|
| Principe | Plus de puissance (dégâts, PV, niveau) | Plus d'options (nouvelles armes, capacités, styles) sans gain net de puissance |
| Exemple | Épée +1 → +2 → +3 | Épée, arc, bâton : forces et faiblesses différentes |
| Avantages | Sensation forte et lisible, facile à produire | Préserve l'équilibrage, encourage l'expérimentation, contenu ancien reste pertinent |
| Risques | *Power creep*, contenu ancien obsolète, écarts entre joueurs en multijoueur | Sensation de progression plus faible, demande plus de design |

Règles :
- **Mélanger** : progression verticale au début (sentiment clair de croissance), horizontale ensuite (options, spécialisation).
- En **multijoueur compétitif**, privilégier fortement l'horizontal : la puissance verticale entre joueurs crée des combats injustes.
- **Normaliser la puissance** (*level scaling*) seulement avec précaution : si les ennemis montent au même rythme que le joueur, la progression devient invisible (critique classique de *The Elder Scrolls IV: Oblivion*). Si on normalise, garder des repères fixes que le joueur peut écraser.

## 6. Power creep

Le *power creep* est l'inflation progressive de la puissance : chaque nouvel ajout doit être un peu meilleur que le précédent pour être attirant, ce qui rend l'ancien contenu obsolète et compresse la difficulté.

Causes typiques : ajouts réguliers de contenu (jeux-services, cartes), peur de sortir un ajout « faible », progression verticale sans plafond.

Contre-mesures :
- **Plafonds** de niveau et de stats ; progression horizontale au-delà.
- **Rotation** du contenu autorisé (formats « Standard » des jeux de cartes).
- **Nerfs** ciblés (impopulaires mais nécessaires) plutôt que buff de tout le reste.
- **Mécaniques nouvelles plutôt que chiffres plus gros** : un nouvel objet qui fait autre chose ne remplace pas l'ancien.
- **Réinitialisations saisonnières** (*seasons*, *ladders*) quand le genre s'y prête.

## 7. Sentiment de progression et rythme des récompenses

Le joueur doit **voir** qu'il progresse. Outils :

- **Barres de progression** visibles et souvent mises à jour ; elles exploitent l'**effet de gradient d'objectif** (*goal-gradient effect*) : on accélère à l'approche du but.
- **Effet de progression offerte** (*endowed progress effect*) : une barre qui démarre partiellement remplie motive plus qu'une barre vide de même longueur restante (Nunes & Drèze, 2006).
- **Comparaison avant/après** : retourner dans une zone du début et écraser les ennemis qui posaient problème donne une mesure tangible de la progression.
- **Feedback de montée de niveau** : moment marqué (son, animation, écran de résumé), voir [Game feel](../ressenti/game-feel-juice.md).
- **Objectifs imbriqués** à plusieurs échelles de temps :

| Échelle | Durée indicative | Exemple |
|---|---|---|
| Micro | secondes | Tuer un ennemi, ramasser une pièce |
| Court terme | minutes | Finir une salle, acheter une amélioration |
| Moyen terme | une session | Monter de niveau, battre un boss |
| Long terme | plusieurs sessions | Finir le jeu, compléter un arbre, un *build* complet |

**Règle** : à tout moment, le joueur devrait avoir **au moins un objectif proche** en vue. Si une échelle est vide, le joueur ressent un creux.

## 8. Méta-progression (roguelites)

La méta-progression est ce qui persiste entre les parties : déblocages permanents, monnaie conservée, améliorations de base (*Rogue Legacy*, *Hades*, *Dead Cells*).

- **Rôle** : donner de la valeur aux parties ratées et lisser la courbe de difficulté pour les joueurs moins habiles.
- **Risque** : si la méta-progression est trop forte, la victoire vient du temps passé et non de la compétence ; le cœur roguelike (chaque partie compte) s'affaiblit.
- **Préférer les déblocages horizontaux** (nouvelles armes, nouveaux objets dans le pool, nouveaux personnages) aux bonus statistiques permanents, ou plafonner ces derniers.
- **Rendre la méta-progression optionnelle** quand possible (*Hades* : le « Pacte du Châtiment » ajoute de la difficulté pour compenser).
- Voir [Roguelike](../genres/roguelike.md).

## 9. Programmes de renforcement et éthique

Les récompenses suivent un **programme de renforcement** (psychologie comportementale, B. F. Skinner) :

| Programme | Récompense quand… | Exemple en jeu | Comportement induit |
|---|---|---|---|
| Ratio fixe | toutes les N actions | 10 ennemis = 1 potion | Rafales d'activité puis pause après la récompense |
| Ratio variable | après un nombre aléatoire d'actions | Butin aléatoire, coffre, gacha | Activité élevée et soutenue, très résistante à l'extinction |
| Intervalle fixe | après un temps fixe | Récompense quotidienne | Retour au moment prévu |
| Intervalle variable | après un temps aléatoire | Événement surprise dans le monde | Vérifications régulières |

Le **ratio variable** est le plus puissant pour maintenir un comportement, c'est aussi la base des machines à sous. Règles :

- **Utiliser la surprise pour enrichir, pas pour retenir** : un butin aléatoire rend l'exploration excitante ; mais si le jeu repose uniquement sur ce ressort, les joueurs restent par compulsion, pas par plaisir.
- **Le fun intrinsèque d'abord** : si la boucle centrale n'est amusante que grâce aux récompenses, la retravailler (voir [Boucles de gameplay](../fondamentaux/boucles-de-gameplay.md)).
- **Éviter** : récompenses qui disparaissent si on ne se connecte pas (*streaks* punitifs), minuteurs conçus pour créer de l'anxiété, aléatoire payant sans transparence (voir [Économie](economie.md), section monétisation).
- **Bonnes pratiques** : laisser le joueur rattraper un jour manqué, afficher les probabilités, garantir une récompense après une série de malchance (*pity*, voir [Économie](economie.md), section loot tables), permettre de s'arrêter à un point naturel.

---

## Anti-patterns et pièges

- **Progression invisible** : stats qui augmentent sans effet ressenti. Toujours relier un gain à un changement observable.
- **Niveau qui annule la compétence** : un joueur qui « grinde » 3 h écrase un boss conçu pour tester une mécanique. Si c'est voulu, tant mieux ; sinon plafonner par zone.
- **Mise à l'échelle totale** des ennemis : le joueur ne sent plus de progression.
- **Arbre de compétences à 95 % de +x %** : choix sans intérêt.
- **Récompense principale = monnaie pour d'autres récompenses** : chaîne trop longue entre l'action et le gain concret.
- **Mur de grind** non annoncé en fin de jeu dû à une courbe exponentielle non simulée.
- **Tout débloquer en même temps** : le joueur est submergé et n'apprend rien.

## Checklist

- [ ] L'axe dominant (compétence, puissance, accès) est identifié et assumé.
- [ ] La durée cible du jeu et le temps par niveau (début / milieu / fin) sont définis avant la formule.
- [ ] La courbe XP et la courbe de gains ont été simulées ensemble dans un tableur.
- [ ] Chaque niveau ou palier apporte un changement perceptible.
- [ ] Le joueur a toujours un objectif proche visible (barre, déblocage annoncé).
- [ ] Les nœuds de l'arbre changent le comportement, pas seulement des pourcentages.
- [ ] Une respécialisation existe (gratuite ou payante).
- [ ] La puissance a un plafond ou une contre-mesure au *power creep*.
- [ ] En roguelite : la méta-progression ne remplace pas la compétence.
- [ ] Aucune récompense ne repose sur l'anxiété ou la punition de l'absence.
- [ ] Les valeurs de progression sont externalisées (fichiers de données), pas codées en dur.

## Pistes d'implémentation

Courbe d'XP pilotée par données, avec formule de secours et table de surcharge :

```
// Données : base a, exposant k, overrides[n] facultatif
function xpCumulative(n):
    if n <= 1: return 0
    if overrides.has(n): return overrides[n]
    return round(a * pow(n - 1, k))

function addXP(amount):
    xp += amount
    while level < maxLevel and xp >= xpCumulative(level + 1):
        level += 1
        onLevelUp(level)          // gameplay : stats, points, déblocages
        emit("level_up", level)   // présentation : son, VFX, UI (séparé)
```

- **Séparer la logique (`onLevelUp`) de la présentation (événement écouté par l'UI/l'audio)**, conformément à la règle de [Game feel](../ressenti/game-feel-juice.md).
- Gérer **plusieurs montées de niveau d'un coup** (boucle `while`, pas `if`).
- Stocker la progression en XP **cumulée** : plus simple à sauvegarder et à rééquilibrer qu'une XP « dans le niveau courant ».
- Exporter un **CSV de simulation** (niveau, XP cumulée, Δ, temps estimé) pour relire la courbe.
- **UE5** : `UDataTable` ou `UCurveFloat` pour la courbe ; attributs et effets via GAS (`UAttributeSet`, `GameplayEffect`) pour les bonus de stats.
- **Godot** : `Resource` personnalisée (`.tres`) ou `Curve` ; signal `level_up`.
- **Unity** : `ScriptableObject` pour la table, `AnimationCurve` pour un prototype rapide.

## Voir aussi

- [Économie](economie.md) — monnaies, loot, monétisation.
- [Équilibrage et difficulté](equilibrage-et-difficulte.md) — ratio puissance/difficulté, courbes de difficulté.
- [Boucles de gameplay](../fondamentaux/boucles-de-gameplay.md) — boucle centrale et méta-boucle.
- [Cadres théoriques](../fondamentaux/cadres-theoriques.md) — motivation (SDT), flow.
- [Roguelike](../genres/roguelike.md) et [RPG](../genres/rpg.md).
- [Aléatoire et procédural](aleatoire-et-procedural.md) — distribution des récompenses aléatoires.

## Sources

- Ian Schreiber & Brenda Romero, *Game Balance*, CRC Press, 2021 (chapitres sur les courbes de progression et les économies).
- Ian Schreiber, *Game Balance Concepts* (cours en ligne), 2010 — https://gamebalanceconcepts.wordpress.com/
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, 3e éd., CRC Press, 2019.
- Wizards of the Coast, *Dungeons & Dragons 3.5 Player's Handbook*, 2003 (table d'expérience).
- Joseph C. Nunes & Xavier Drèze, « The Endowed Progress Effect », *Journal of Consumer Research*, 2006.
- Ran Kivetz, Oleg Urminsky & Yuhuang Zheng, « The Goal-Gradient Hypothesis Resurrected », *Journal of Marketing Research*, 2006.
- B. F. Skinner & C. B. Ferster, *Schedules of Reinforcement*, 1957.
- Jamie Madigan, *Getting Gamers: The Psychology of Video Games and Their Impact on the People Who Play Them*, 2015.
