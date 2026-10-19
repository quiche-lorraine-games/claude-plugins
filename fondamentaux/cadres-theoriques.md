# Cadres théoriques

> **En bref** : les modèles classiques du game design (MDA, flow, théorie de l'autodétermination, types de joueurs, 8 kinds of fun, théorie du fun de Koster, lentilles de Schell), présentés comme **outils de décision** : pour chacun, ce qu'il dit, quand l'utiliser et quelle question concrète il permet de trancher. Aucun n'est une loi ; ce sont des grilles de lecture.

## Quand consulter cette fiche

- Tu dois justifier ou arbitrer un choix de conception (« pourquoi ce système ? »).
- Le jeu « marche » mécaniquement mais ne produit pas l'émotion visée.
- Tu dois définir le public cible et ce qui le motive.
- Tu dois diagnostiquer de l'ennui, de la frustration ou un décrochage.
- Tu rédiges un pitch ou un GDD et veux formuler l'expérience visée.

---

## Choisir le bon cadre

| Situation | Cadre utile |
|---|---|
| Relier une émotion visée à des règles concrètes | MDA |
| Le joueur s'ennuie ou est frustré | Flow |
| Le joueur ne revient pas / joue sans envie | SDT (autodétermination) |
| Définir ou segmenter le public | Types de joueurs / motivations |
| Nommer l'expérience visée | 8 kinds of fun |
| Le jeu s'épuise après un temps | Koster (apprentissage de motifs) |
| Revue générale d'une conception | Lentilles de Schell |

---

## 1. MDA — Mécaniques, Dynamiques, Esthétiques

**Ce qu'il dit** (Hunicke, LeBlanc, Zubek, 2004) :
- **Mécaniques** : les règles, données et algorithmes (ce qu'on code).
- **Dynamiques** : le comportement qui émerge quand le joueur interagit avec les mécaniques en temps réel.
- **Esthétiques** : les réponses émotionnelles visées chez le joueur (pas le visuel !).

Le concepteur agit sur M → D → E ; le joueur perçoit E → D → M. On ne peut **pas** coder directement une émotion : on code des règles et on observe ce qui émerge.

**Utilisation pratique** :
1. Partir de l'esthétique visée (« tension », « découverte »).
2. Décrire les dynamiques qui la produiraient (« ressources rares qui forcent à fuir »).
3. En déduire les mécaniques (« munitions limitées, ennemis plus rapides que le joueur »).
4. Prototyper et vérifier que la dynamique émerge réellement.

**Question qu'il tranche** : « Cette mécanique sert-elle l'émotion visée, ou seulement elle-même ? »

**Limites** : le terme *aesthetics* prête à confusion ; le modèle sous-estime le rôle de la présentation (son, image, narration), qui produit aussi des émotions. Des variantes existent (DDE, MDA étendu), le principe d'ordre reste utile.

## 2. Flow (Csikszentmihalyi)

**Ce qu'il dit** : un état d'absorption totale apparaît quand le **défi** est proportionné à la **compétence**, avec un **but clair** et un **retour immédiat**. Trop de défi → anxiété ; trop peu → ennui. La compétence du joueur augmentant, le défi doit augmenter aussi : le « canal de flow » monte en diagonale.

Conditions pratiques du flow en jeu :
- but clair à chaque instant ;
- feedback immédiat sur chaque action ;
- sentiment de contrôle ;
- pas d'interruption (chargements, menus, cinématiques non désirées) ;
- défi ajusté au niveau du joueur.

**Utilisation pratique** :
- Courbe de difficulté en **dents de scie** plutôt que linéaire : montée de tension, pic (boss, défi), relâche (zone calme, récompense), puis nouvelle montée à un niveau supérieur. La relâche évite l'épuisement.
- Offrir plusieurs façons d'ajuster le défi : difficulté choisie, options d'assistance, chemins optionnels plus durs, difficulté adaptative (Jenova Chen recommande de laisser le **joueur** choisir plutôt que d'ajuster en cachette ; voir [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)).

**Question qu'il tranche** : « Le joueur est-il en ennui, en anxiété ou dans le canal à ce moment ? » — à vérifier en playtest (voir [Playtest et métriques](../production/playtest-et-metriques.md)).

**Limites** : le flow n'est pas l'objectif de tous les jeux (jeux narratifs, contemplatifs, sociaux). Ne pas chercher le flow en permanence : les moments de relâche font partie de l'expérience.

## 3. Théorie de l'autodétermination (SDT)

**Ce qu'il dit** (Deci & Ryan ; appliquée au jeu par Rigby & Ryan, modèle PENS) : la motivation durable (intrinsèque) repose sur trois besoins.

| Besoin | En jeu | Leviers | Ce qui le détruit |
|---|---|---|---|
| **Compétence** | Se sentir capable et progresser | Défi adapté, feedback clair, progression visible de la maîtrise | Échecs incompréhensibles, difficulté arbitraire, contrôles imprécis |
| **Autonomie** | Faire des choix qui ont du sens | Choix réels, plusieurs stratégies viables, liberté d'ordre, personnalisation | Couloirs imposés sans raison, « choix » sans conséquence, récompenses contrôlantes |
| **Appartenance** (*relatedness*) | Se sentir lié à d'autres | Coopération, PNJ attachants, communauté, partage | Toxicité, isolement forcé, interactions sociales transactionnelles |

**Utilisation pratique** : pour chaque système, demander lequel des trois besoins il nourrit. Un système qui n'en nourrit aucun ne repose que sur la motivation extrinsèque (récompense) et sera fragile.

**Point d'attention** : les récompenses perçues comme **contrôlantes** (« fais ceci pour obtenir cela », quêtes quotidiennes obligatoires) peuvent réduire la motivation intrinsèque. Les récompenses perçues comme **informatives** (« tu as bien joué ») la renforcent.

**Question qu'il tranche** : « Pourquoi le joueur voudrait-il revenir, si on enlevait les récompenses ? »

## 4. Types de joueurs et motivations

### Bartle (1996)
Quatre profils observés dans les MUD (jeux multijoueurs textuels), sur deux axes (agir sur / interagir avec ; le monde / les joueurs) :

| Type | Aime | Axe |
|---|---|---|
| *Achievers* (accomplisseurs) | Progresser, accumuler, compléter | Agir sur le monde |
| *Explorers* (explorateurs) | Découvrir, comprendre les systèmes | Interagir avec le monde |
| *Socializers* (sociaux) | Échanger, appartenir | Interagir avec les joueurs |
| *Killers* (compétiteurs / dominateurs) | S'imposer aux autres | Agir sur les joueurs |

**Limites importantes** :
- Conçu pour les MUD ; Bartle lui-même déconseille de l'appliquer tel quel à tous les jeux.
- Les joueurs ne sont pas d'un seul type ; les motivations se combinent et varient selon le jeu et le moment.
- Pas de validation empirique solide en tant que typologie.

### Alternative plus récente : modèle de motivations Quantic Foundry (Nick Yee)
Basé sur des enquêtes à grande échelle, il mesure des **motivations** (et non des types) regroupées en six familles : Action (destruction, excitation), Social (communauté, compétition), Maîtrise (défi, stratégie), Accomplissement (complétion, puissance), Immersion (fantasme, histoire), Créativité (design, découverte). Plus adapté pour décrire un public cible.

**Utilisation pratique** : choisir **2–3 motivations prioritaires** pour le public cible et vérifier que la boucle centrale les sert. Ne pas essayer de plaire à toutes.

**Question qu'il tranche** : « Ce système sert-il le public visé, ou un public qu'on n'a pas choisi ? »

## 5. Les 8 kinds of fun (Marc LeBlanc)

Taxonomie des esthétiques issue du travail sur MDA :

| Esthétique | Le jeu comme… | Exemple de levier |
|---|---|---|
| *Sensation* | plaisir des sens | Game feel, audio, visuel |
| *Fantasy* (fantasme) | faire semblant | Rôle, univers, incarnation |
| *Narrative* (narration) | drame | Histoire, enjeux, arcs |
| *Challenge* (défi) | parcours d'obstacles | Difficulté, maîtrise |
| *Fellowship* (camaraderie) | cadre social | Coop, guildes |
| *Discovery* (découverte) | territoire inconnu | Exploration, secrets, systèmes à comprendre |
| *Expression* | découverte de soi | Création, personnalisation, styles de jeu |
| *Submission* (abandon / passe-temps) | passe-temps | Activité relaxante, répétitive et agréable |

**Utilisation pratique** : choisir **2–3 esthétiques principales** et les écrire en tête du GDD (voir [GDD une page](../production/templates/gdd-une-page.md)). Toute fonctionnalité doit en servir au moins une. Utile pour couper des features : « cette fonctionnalité sert l'Expression, mais notre jeu vise Défi + Découverte : on coupe ».

## 6. Théorie du fun (Raph Koster)

**Ce qu'il dit** : le fun en jeu vient de l'**apprentissage** ; le cerveau prend plaisir à reconnaître et maîtriser des **motifs** (*patterns*). Quand le motif est entièrement maîtrisé, le jeu devient ennuyeux (*grokked*) ; quand il est trop complexe pour être perçu, il devient du bruit.

**Utilisation pratique** :
- Introduire de nouveaux motifs régulièrement (nouvel ennemi, nouvelle règle, nouvelle combinaison) avant que les anciens soient épuisés.
- Si le jeu s'épuise vite : le motif central est trop simple ou se résout en stratégie dominante.
- Si le joueur est perdu : le motif est noyé dans le bruit (trop d'informations, trop de variables aléatoires, retour peu lisible).
- Un jeu à forte rejouabilité repose sur un espace de motifs **très large** (combinatoire, adversaire humain, procédural bien conçu).

**Question qu'il tranche** : « Qu'est-ce que le joueur est encore en train d'apprendre à ce stade du jeu ? »

## 7. Les lentilles de Jesse Schell

*The Art of Game Design* propose plus d'une centaine de **lentilles** : des jeux de questions pour examiner une conception sous un angle précis. Exemples utiles en revue :

| Lentille | Question clé |
|---|---|
| Expérience essentielle | Quelle expérience veux-je que le joueur vive ? Qu'est-ce qui est essentiel à cette expérience ? |
| Surprise | Qu'est-ce qui surprendra le joueur ? Les règles, les histoires, les systèmes se surprennent-ils entre eux ? |
| Plaisir | Quels plaisirs le jeu procure-t-il ? Lesquels manquent ? |
| Curiosité | Quelles questions le joueur se pose-t-il ? Comment le pousser à vouloir y répondre ? |
| Problème à résoudre | Quels problèmes le joueur doit-il résoudre ? Lesquels émergent du jeu ? |
| Choix | Quels choix le joueur fait-il ? Sont-ils significatifs ? |
| Retour (*feedback*) | Que ressent le joueur après chaque action ? Le retour est-il clair, immédiat, encourageant ? |
| Élégance | Quels éléments ont plusieurs usages ? Lesquels ne servent qu'à une chose ? |

**Utilisation pratique** : pour une revue de conception, choisir 5 à 10 lentilles pertinentes et y répondre par écrit. Ne pas les appliquer toutes : c'est un outil de questionnement, pas une checklist exhaustive.

---

## Pièges communs à tous les cadres

- **Théoriser au lieu de prototyper** : aucun cadre ne remplace un playtest. Les utiliser pour formuler une hypothèse, puis la tester.
- **Utiliser un cadre comme justification a posteriori** : « c'est pour les *explorers* » ne rend pas une feature bonne.
- **Plaquer un cadre hors de son domaine** : Bartle pour un jeu solo narratif, flow pour un jeu contemplatif.
- **Confondre esthétique (MDA) et direction artistique.**

## Checklist

- [ ] Les 2–3 esthétiques visées (8 kinds of fun) sont écrites en tête du document de conception.
- [ ] Pour chaque mécanique principale, on sait quelle dynamique elle doit produire et quelle esthétique elle sert (MDA).
- [ ] Les motivations prioritaires du public cible sont identifiées (2–3 maximum).
- [ ] Chaque système nourrit au moins un besoin SDT (compétence, autonomie, appartenance).
- [ ] La courbe de difficulté prévoit des phases de relâche (flow).
- [ ] On sait ce que le joueur apprend encore au milieu et à la fin du jeu (Koster).
- [ ] Une revue « lentilles » a été faite sur la conception actuelle.
- [ ] Chaque hypothèse issue d'un cadre a un playtest prévu pour la vérifier.

## Pistes d'implémentation

- Ces cadres ne se codent pas ; ils servent à **décider quoi coder**. Les consigner dans le GDD sous forme d'hypothèses testables : « Hypothèse : la rareté des munitions crée de la tension (esthétique Défi). Mesure : taux de fuite face aux ennemis, ressenti déclaré en playtest. »
- Pour le flow : prévoir dès le départ des **paramètres de difficulté exposés** (multiplicateurs de dégâts, vitesse ennemie, fenêtres de timing) pour pouvoir ajuster sans recompiler.

## Voir aussi

- [Boucles de gameplay](boucles-de-gameplay.md)
- [Principes de conception](principes-de-conception.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [Playtest et métriques](../production/playtest-et-metriques.md)

## Sources

- Robin Hunicke, Marc LeBlanc, Robert Zubek, « MDA: A Formal Approach to Game Design and Game Research », AAAI Workshop on Challenges in Game AI, 2004.
- Mihaly Csikszentmihalyi, *Flow: The Psychology of Optimal Experience*, Harper & Row, 1990.
- Jenova Chen, « Flow in Games », mémoire de master, USC, 2006 ; « Flow in Games (and Everything Else) », *Communications of the ACM*, 2007.
- Edward L. Deci & Richard M. Ryan, travaux sur la théorie de l'autodétermination (*Intrinsic Motivation and Self-Determination in Human Behavior*, 1985).
- Scott Rigby & Richard M. Ryan, *Glued to Games*, Praeger, 2011.
- Richard Bartle, « Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs », *Journal of MUD Research*, 1996.
- Quantic Foundry (Nick Yee), *Gamer Motivation Model* — https://quanticfoundry.com
- Raph Koster, *A Theory of Fun for Game Design*, 2004 (2ᵉ éd. 2013).
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, CRC Press, 2008 (3ᵉ éd. 2019).
