# Profils de joueurs

> **En bref** : les principaux modèles de profils et de motivations de joueurs (Bartle, Yee et Quantic Foundry, BrainHex, traits de Tondello, Hexad, Lazzaro, Timmy/Johnny/Spike, casual et hardcore), ce que chacun mesure réellement, sa solidité, et comment s'en servir pour définir un public cible, construire des personas, concevoir pour plusieurs profils et recruter des testeurs. Règle de base : un profil décrit des **motivations qui se combinent et varient**, pas une identité fixe.

## Quand consulter cette fiche

- Tu définis le public cible d'un jeu ou tu remplis la section « Public cible » du [GDD une page](../production/templates/gdd-une-page.md).
- Tu dois trancher entre deux fonctionnalités qui plaisent à des joueurs différents.
- Tu construis des personas, ou tu recrutes des testeurs pour un playtest.
- Tu ajoutes du multijoueur persistant et tu dois prévoir l'équilibre entre compétiteurs, coopératifs et explorateurs.
- Des retours de playtest se contredisent (« trop dur » contre « trop facile », « trop d'histoire » contre « pas assez ») et tu dois savoir quels joueurs écouter.
- Tu conçois de la gamification (application, outil, éducation) plutôt qu'un jeu.

---

## 1. Principes

- **Motivations, pas cases.** Les modèles récents et validés mesurent des **scores sur plusieurs dimensions** ; un joueur a un profil, pas un type. Les typologies à cases (Bartle, BrainHex, Hexad) restent utiles comme vocabulaire, pas comme mesure.
- **Le profil dépend du jeu et du moment.** Un même joueur peut chercher la compétition en ligne le soir et un jeu contemplatif le dimanche. Des travaux sur l'Hexad observent d'ailleurs que les types d'utilisateurs peuvent évoluer dans le temps.
- **Choisir, c'est exclure.** Un jeu qui vise toutes les motivations n'en sert aucune fortement. Viser **2 ou 3 motivations prioritaires**, et en tolérer d'autres en secondaire.
- **L'âge pèse plus que le genre.** Dans les données de Quantic Foundry, l'écart hommes/femmes sur la motivation Compétition s'efface en grande partie avec l'âge : l'âge explique environ trois fois plus de variation que le genre. Ne jamais déduire les motivations d'un public de son genre.
- **Les joueurs disent ce qu'ils aiment, pas pourquoi.** Les questionnaires de motivation complètent l'observation et la télémétrie ; ils ne les remplacent pas (voir [Playtest et métriques](../production/playtest-et-metriques.md)).
- **Le profil n'est pas le niveau.** La motivation (pourquoi on joue) et la compétence ou le temps disponible (comment on joue) sont deux axes séparés. Un joueur occasionnel peut aimer le défi.

---

## 2. Les modèles et ce qu'ils valent

| Modèle | Ce qu'il décrit | Solidité empirique | À utiliser pour |
|---|---|---|---|
| Bartle (1996, 2003) | 4 types (puis 8) de joueurs de MUD | Faible : observationnel, non validé comme mesure | Écologie d'un monde multijoueur persistant |
| Yee (2006) | 10 sous-composantes en 3 familles (MMO) | Analyse factorielle sur joueurs de MMO | Motivations en ligne, base de Quantic Foundry |
| Quantic Foundry (Yee et Ducheneaut) | 12 motivations en 6 paires, 3 grappes | Très grand échantillon (des centaines de milliers de répondants), modèle commercial | Définir et comparer un public cible |
| BrainHex (Bateman et Nacke, 2011) | 7 archétypes | Faible : propriétés psychométriques jugées insuffisantes par des études ultérieures | Grille de lecture, pas mesure |
| Traits de joueur (Tondello et al., 2019) | 5 traits continus | Échelle de 25 items validée | Mesurer les préférences en playtest |
| Hexad (Marczewski, 2015) | 6 types d'utilisateurs de gamification | Échelle validée (Tondello et al., 2016, 2019), fiabilité plus faible pour *Free Spirit* et *Disruptor* | Gamification, applications |
| Lazzaro (2004) | 4 types de plaisir (émotions) | Recherche qualitative (observation de joueurs) | Équilibrer les sources d'émotion d'un jeu |
| Timmy, Johnny, Spike (Rosewater, 2002) | 3 profils de joueurs de *Magic* | Outil de design interne, pas de mesure | Concevoir du contenu à collectionner ou combiner (cartes, objets, builds) |
| Méta-synthèse (Hamari et Tuunanen, 2014) | 7 dimensions communes aux typologies | Revue de la littérature | Vérifier qu'on n'oublie pas une dimension |

### 2.1 Bartle

Quatre types observés dans les MUD, sur deux axes : **agir sur / interagir avec**, **le monde / les joueurs**.

| Type | Aime | Axe |
|---|---|---|
| *Achiever* (accomplisseur) | Progresser, accumuler, « gagner » | Agir sur le monde |
| *Explorer* (explorateur) | Découvrir, comprendre les systèmes | Interagir avec le monde |
| *Socializer* (social) | Échanger, nouer des liens | Interagir avec les joueurs |
| *Killer* (dominateur) | S'imposer aux autres | Agir sur les joueurs |

**Modèle à 8 types** (*Designing Virtual Worlds*, 2003) : un troisième axe **implicite / explicite** dédouble chaque type, avec un explicite (qui planifie) et un implicite (qui agit d'instinct) :

| Type de base | Explicite | Implicite |
|---|---|---|
| Achiever | *Planner* : se fixe un but et le poursuit | *Opportunist* : saisit ce qui se présente |
| Explorer | *Scientist* : expérimente méthodiquement | *Hacker* : comprend le monde intuitivement |
| Socializer | *Networker* : choisit avec qui passer du temps | *Friend* : profite de la compagnie de ses proches |
| Killer | *Politician* : domine par l'influence | *Griefer* : domine par la nuisance |

**Ce que Bartle apporte vraiment** : l'idée d'**écologie**. Dans un monde partagé, les populations s'influencent : trop de *Killers* font fuir les *Achievers* et les *Socializers* ; sans proies, les *Killers* partent à leur tour. Utile pour régler PvP, zones protégées et outils sociaux (voir [Multijoueur](../systemes/multijoueur.md)).

**Limites** : conçu pour les MUD, et Bartle lui-même met en garde contre son application à tous les jeux. Le « test de Bartle » diffusé en ligne n'est pas de lui et n'est pas une mesure validée.

### 2.2 Yee et le modèle Quantic Foundry

**Yee (2006)**, sur des joueurs de MMO : 10 sous-composantes regroupées en 3 familles.
- **Accomplissement** : progression, mécaniques, compétition.
- **Social** : sociabilité, relations, travail d'équipe.
- **Immersion** : découverte, jeu de rôle, personnalisation, évasion.

**Gamer Motivation Model (Quantic Foundry)** : généralisation à tous les jeux, 12 motivations en 6 paires.

| Paire | Motivations | Le joueur cherche… |
|---|---|---|
| Action | Destruction, Excitation | Le chaos, les explosions, le rythme, les surprises |
| Social | Compétition, Communauté | Affronter les autres, jouer et discuter avec eux |
| Maîtrise | Défi, Stratégie | La difficulté, la réflexion, la planification |
| Accomplissement | Complétion, Puissance | Tout finir et collectionner, devenir puissant |
| Immersion | Fantasme, Histoire | Être quelqu'un d'autre, une intrigue, des personnages |
| Créativité | Design, Découverte | S'exprimer, personnaliser, explorer, expérimenter |

**Trois grappes** :
- **Action-Social** : immédiateté, adrénaline, interaction.
- **Maîtrise-Accomplissement** : jeu réfléchi, sur le long terme.
- **Immersion-Créativité** : narration, expression, exploration du monde.

Deux motivations font le pont : **Découverte** (entre Immersion-Créativité et Maîtrise-Accomplissement) et **Puissance** (entre Action-Social et Maîtrise-Accomplissement). Des motivations éloignées sur la carte sont **indépendantes**, pas opposées : un joueur peut aimer à la fois l'histoire et la compétition.

**Usage** : c'est le modèle le plus pratique pour décrire un public. Le questionnaire public (Gamer Motivation Profile) peut servir en playtest pour situer les testeurs.

### 2.3 BrainHex

Sept archétypes fondés sur des hypothèses neurobiologiques (Bateman et Nacke, 2011) :

| Archétype | Plaisir recherché |
|---|---|
| *Seeker* (chercheur) | Curiosité, émerveillement, découverte |
| *Survivor* (survivant) | Peur maîtrisée, soulagement d'y avoir échappé |
| *Daredevil* (casse-cou) | Frisson, vitesse, prise de risque |
| *Mastermind* (stratège) | Résoudre, planifier, trouver la solution efficace |
| *Conqueror* (conquérant) | Vaincre une adversité difficile, le triomphe (*fiero*) |
| *Socialiser* | Être avec les autres, confiance, entraide |
| *Achiever* | Objectifs à long terme, complétion, collection |

**Limites** : des études ultérieures (Busch et al., 2016 ; Tondello et al., 2018) jugent ses propriétés psychométriques insuffisantes. Les auteurs le présentaient d'ailleurs comme un modèle intermédiaire. Il reste une bonne **liste de contrôle des émotions**, notamment pour *Survivor* (horreur) et *Daredevil* (vitesse), absents des autres modèles.

### 2.4 Traits de joueur (Tondello et al., 2019)

Modèle issu de la synthèse de la littérature et validé par une échelle de 25 items. Cinq **traits continus**, chaque joueur ayant un score sur chacun :

| Trait | Le joueur apprécie… |
|---|---|
| Orientation esthétique | L'aspect visuel et sonore, les paysages |
| Orientation narrative | Les histoires, les personnages |
| Orientation objectifs | Accomplir des objectifs, compléter |
| Orientation sociale | Jouer avec d'autres |
| Orientation défi | La difficulté |

**Usage** : le plus solide pour **mesurer** les préférences de testeurs. Il est court, et ses scores se croisent facilement avec la télémétrie.

### 2.5 Hexad (gamification)

Conçu pour la gamification (applications, outils, formation), pas pour les jeux. Quatre types intrinsèques liés à la théorie de l'autodétermination (voir [Cadres théoriques](cadres-theoriques.md)), plus deux autres :

| Type | Motivé par | Leviers |
|---|---|---|
| *Achiever* | Maîtrise | Défis, niveaux, compétences à apprendre |
| *Socialiser* | Appartenance | Équipes, discussions, groupes |
| *Philanthropist* (altruiste) | But, sens | Aider, partager, transmettre son savoir |
| *Free Spirit* (esprit libre) | Autonomie | Exploration, personnalisation, choix |
| *Player* (joueur) | Récompenses extrinsèques | Points, badges, classements, loteries |
| *Disruptor* (perturbateur) | Le changement | Tester les limites, contourner, réformer ; à canaliser (retours, bêtas, outils de création) |

**Limite** : les sous-échelles *Free Spirit* et *Disruptor* ont une fiabilité plus faible que les autres dans plusieurs études.

### 2.6 Les 4 clés du fun (Lazzaro)

Typologie d'**émotions** plutôt que de joueurs, issue de l'observation de joueurs :

| Clé | Émotions | Leviers |
|---|---|---|
| *Hard Fun* (défi) | Frustration puis triomphe (*fiero*) | Obstacles, maîtrise, objectifs difficiles |
| *Easy Fun* (nouveauté) | Curiosité, émerveillement | Exploration, jeu de rôle, créativité, jouets |
| *Serious Fun* (sens) | Excitation, détente, sentiment d'utilité | Changer quelque chose en soi ou dans le monde, rituels, collection |
| *People Fun* (amitié) | Amusement, complicité, rivalité | Coopération, compétition, communication |

**Usage** : Lazzaro observe que les jeux qui ont le plus de succès mobilisent au moins **trois des quatre clés**. À croiser avec les [8 kinds of fun](cadres-theoriques.md) de LeBlanc.

### 2.7 Timmy, Johnny, Spike (*Magic: The Gathering*)

Profils utilisés en interne par Wizards of the Coast pour concevoir les cartes (Rosewater, 2002, puis 2006).

| Profil | Veut… | Conçu pour lui |
|---|---|---|
| **Timmy / Tammy** | **Vivre** une expérience : de grands effets, des moments mémorables | Grosses créatures, effets spectaculaires, parties épiques |
| **Johnny / Jenny** | **S'exprimer** : trouver la combinaison originale | Cartes ouvertes, interactions inattendues, combos |
| **Spike** | **Prouver** quelque chose, gagner | Cartes efficaces, profondeur stratégique, compétition |

Deux profils **esthétiques** s'y ajoutent sur un autre axe (Rosewater, 2007) : **Vorthos** apprécie l'univers et la cohérence de la fiction, **Mel** l'élégance de la mécanique.

**Usage** : excellent pour tout contenu combinatoire (cartes, objets de roguelike, talents, pièces de build). Chaque lot de contenu doit contenir quelque chose pour chacun des trois profils (voir [Deckbuilder](../genres/deckbuilder-cartes.md), [Roguelike](../genres/roguelike.md)).

### 2.8 Casual et hardcore : remplacer la dichotomie par des axes

Juul (*A Casual Revolution*, 2010) montre que les jeux « casual » réussis ne sont pas forcément courts ou faciles : ils sont **flexibles** sur le temps et la difficulté. Il identifie cinq traits de conception :
- une fiction positive ;
- une prise en main intuitive ;
- le jeu par sessions courtes et interruptibles ;
- une punition de l'échec clémente ;
- beaucoup de retours positifs (*juiciness*).

Plutôt que « casual / hardcore », décrire le public sur des **axes indépendants** :

| Axe | Faible | Élevé | Conséquence de conception |
|---|---|---|---|
| Temps par session | 2–10 min (transports, pauses) | Plusieurs heures | Points de sauvegarde, durée d'une boucle centrale |
| Régularité | Joue de temps en temps | Joue tous les jours | Rappels après une pause, méta-progression |
| Tolérance à l'échec | Abandonne après quelques échecs | Recommence volontiers | Punition, checkpoints, options d'assistance |
| Culture du jeu vidéo | Ne connaît pas les conventions | Connaît le genre | Longueur de l'onboarding, conventions de contrôle |
| Maîtrise visée | Veut voir la fin | Veut optimiser | Difficulté réglable, défis optionnels, classements |
| Contexte | Mobile, son coupé, une main | Salon ou bureau, casque | Sous-titres, contrôles, lisibilité |

La méta-synthèse de Hamari et Tuunanen (2014) retrouve dans la littérature sept dimensions communes : **intensité**, accomplissement, exploration, sociabilité, domination, immersion et données démographiques en jeu. L'intensité (l'engagement en temps et en effort) y est bien un axe à part.

---

## 3. Correspondances approximatives entre modèles

Les modèles se recoupent. Ce tableau aide à traduire de l'un à l'autre ; les correspondances sont **approximatives**.

| Famille de motivation | Bartle | Quantic Foundry | BrainHex | Traits (Tondello) | Lazzaro | *Magic* |
|---|---|---|---|---|---|---|
| Défi, maîtrise | Achiever | Défi, Stratégie | Conqueror, Mastermind | Défi | Hard Fun | Spike |
| Accomplissement, collection | Achiever | Complétion, Puissance | Achiever | Objectifs | Serious Fun | — |
| Découverte | Explorer | Découverte | Seeker | Esthétique | Easy Fun | Mel (systèmes) |
| Expression, création | — | Design | — | — | Easy Fun | Johnny |
| Immersion, histoire | — | Fantasme, Histoire | — | Narration | Easy Fun | Vorthos |
| Sensations, adrénaline | — | Destruction, Excitation | Daredevil, Survivor | — | Serious Fun | Timmy |
| Social coopératif | Socializer | Communauté | Socialiser | Social | People Fun | — |
| Compétition, domination | Killer | Compétition | Conqueror | Social, Défi | People Fun | Spike |

---

## 4. Concevoir pour un profil : leviers et signaux

Pour chaque motivation prioritaire, prévoir des **leviers** dans le jeu et des **signaux** observables (télémétrie ou playtest) qui confirment qu'elle est servie. Les signaux sont des heuristiques à adapter au projet.

| Motivation | Leviers de conception | Signaux observables | Piège |
|---|---|---|---|
| Défi | Difficulté croissante, ennemis exigeants, défis optionnels, modes difficiles | Tentatives par obstacle, taux de réussite des défis optionnels | Mur de difficulté qui exclut le reste du public |
| Stratégie | Choix à long terme, information planifiable, compromis | Diversité des stratégies gagnantes, temps de réflexion | Stratégie dominante (voir [Équilibrage](../systemes/equilibrage-et-difficulte.md)) |
| Complétion | Collections, carte qui se remplit, objectifs secondaires | Taux de complétion des contenus optionnels | Liste de tâches sans intérêt, remplissage |
| Puissance | Montée en puissance visible, moments de domination | Temps passé à optimiser son équipement | Inflation de puissance (voir [Progression](../systemes/progression.md)) |
| Découverte | Secrets, zones optionnelles, systèmes à expérimenter | Part de la carte visitée, temps hors du chemin principal | Secrets introuvables, aucune récompense à explorer |
| Design (expression) | Personnalisation, construction, builds variés | Diversité des créations, temps passé dans les éditeurs | Choix purement cosmétiques sans effet sur le jeu, si le public attend un impact |
| Histoire, fantasme | Personnages, choix narratifs, cohérence de l'univers | Dialogues lus jusqu'au bout, cinématiques passées | Dissonance ludonarrative (voir [Narration](../contenu/narration.md)) |
| Excitation, destruction | Rythme élevé, chaos, physique, surprises | Durée des sessions, intensité des combats | Fatigue, illisibilité (voir [Game feel](../ressenti/game-feel-juice.md)) |
| Communauté | Coop, guildes, partage, entraide | Taux de jeu en groupe, rétention des joueurs en groupe | Contenu impossible en solo si le public joue seul |
| Compétition | Classements, classé, modes PvP | Participation au mode classé, revanches | Toxicité, *griefing*, boule de neige (voir [Multijoueur](../systemes/multijoueur.md)) |

### Faire cohabiter plusieurs profils

- **Contenu optionnel par couches** : un chemin principal accessible, plus des couches pour d'autres profils (défis difficiles, secrets, collection). Le joueur choisit sa couche ; personne n'est forcé.
- **Ne pas faire subir une motivation aux autres** : le PvP doit être consenti (zones, serveurs, modes séparés) ; une collection ne doit pas bloquer la progression principale.
- **Même contenu, plusieurs lectures** : un boss est un défi pour l'un, un spectacle pour l'autre, une énigme mécanique pour un troisième. Concevoir un contenu riche plutôt qu'un contenu par profil.
- **Difficulté et assistance réglables** pour séparer motivation et compétence (voir [Accessibilité](../interface/accessibilite.md)).

---

## 5. Construire et utiliser des personas

Un persona est un joueur fictif représentatif d'une part du public cible, utilisé pour arbitrer les décisions. Gabarit : [persona de joueur](../production/templates/persona-joueur.md).

**Règles** :
- **2 ou 3 personas maximum**, dont un **principal** qui tranche en cas de conflit.
- **Fondé sur des motivations et des contraintes réelles** (temps, contexte, culture du jeu), pas sur des stéréotypes démographiques.
- **Ancré dans des données** dès qu'il y en a : questionnaire de motivations en playtest, retours, télémétrie, publics de jeux comparables.
- **Inclure ce que le persona n'aime pas** : les rejets sont aussi discriminants que les préférences. Vahlo et al. (2017) montrent que pour identifier les types de joueurs, il faut tenir compte des dynamiques de jeu que les joueurs **évitent**, pas seulement de celles qu'ils recherchent.
- **Un anti-persona** (optionnel) : le joueur qu'on ne vise **pas**, pour couper des fonctionnalités sans culpabilité.

**Arbitrer avec un persona** : « Lucie (persona principal) joue 20 minutes dans le train, sans son. Une cinématique non sous-titrée de 3 minutes au début ? Non. »

---

## 6. Profils et playtest

- **Recruter selon les motivations visées**, pas seulement selon le genre de jeux préférés. Faire passer un court questionnaire (traits de Tondello, ou Gamer Motivation Profile) avant la session.
- **Segmenter les retours par profil** : un « trop dur » venant de testeurs orientés défi a plus de poids qu'un « trop facile » venant de testeurs hors cible.
- **Retours contradictoires = souvent des profils différents.** Vérifier lesquels appartiennent au public cible avant de modifier le jeu.
- **Croiser déclaratif et comportemental** : un testeur qui se dit explorateur mais suit le chemin principal en ligne droite donne une information sur le niveau, pas sur lui.

---

## 7. Anti-patterns

- **Concevoir pour tout le monde** : aucune motivation n'est servie fortement, le jeu n'a pas d'identité.
- **Typer les joueurs une fois pour toutes** : « c'est un Killer ». Les profils sont des tendances, variables selon le jeu et le moment.
- **Utiliser le « test de Bartle » en ligne comme mesure** : ni conçu ni validé par Bartle.
- **Confondre motivation et compétence** : rendre le jeu plus facile pour les joueurs « casual » alors qu'ils veulent surtout des sessions courtes.
- **Déduire les motivations du genre ou du sexe** : les écarts liés à l'âge et au profil individuel sont plus grands.
- **Récompenses extrinsèques pour tous** : points et badges ne motivent qu'une partie du public (les *Players* de l'Hexad) et peuvent saper la motivation intrinsèque des autres (voir [Cadres théoriques](cadres-theoriques.md), SDT).
- **Ignorer les perturbateurs** : dans tout système, certains joueurs testent les limites. Leur donner un exutoire (modes bacs à sable, outils de création, retours), et prévoir les protections pour les autres.

---

## Checklist

- [ ] Le public cible est décrit par 2 ou 3 motivations prioritaires (Quantic Foundry ou traits de Tondello), pas par une démographie.
- [ ] Les axes de contraintes sont précisés : temps par session, tolérance à l'échec, culture du jeu, contexte d'usage.
- [ ] Un persona principal existe et sert à trancher ; ses rejets sont listés.
- [ ] Chaque motivation prioritaire a au moins un levier dans la boucle centrale (voir [Boucles de gameplay](boucles-de-gameplay.md)).
- [ ] Chaque motivation prioritaire a un signal mesurable en playtest ou en télémétrie.
- [ ] Les motivations secondaires sont servies par du contenu optionnel, sans être imposées aux autres profils.
- [ ] En multijoueur, l'écologie est pensée : le PvP est consenti, des protections contre le *griefing* existent.
- [ ] Les testeurs sont recrutés et leurs retours segmentés selon leur profil.
- [ ] Aucune décision ne repose sur un stéréotype de genre, ni sur le « test de Bartle » en ligne.

## Pistes d'implémentation

- **Étiqueter le contenu par motivation** : dans les tables de données (quêtes, objets, niveaux, cartes), ajouter un champ `motivations: [challenge, discovery, …]`. Un script peut alors vérifier la répartition du contenu par rapport au public cible, et repérer les profils oubliés.

```
// Vérifier la couverture du contenu par motivation
for item in content:
    for m in item.motivations: count[m] += 1
for m in target_motivations:
    assert count[m] >= min_share * len(content), "motivation sous-servie : " + m
```

- **Instrumenter les signaux** du tableau de la section 4 dès le prototype (événements de télémétrie : zone découverte, objectif optionnel terminé, temps dans l'éditeur, participation au classé). Voir [Playtest et métriques](../production/playtest-et-metriques.md).
- **Questionnaire de playtest** : intégrer l'échelle des traits de Tondello (25 items) ou un lien vers le Gamer Motivation Profile dans le formulaire pré-session, et stocker le profil du testeur avec ses données de session pour segmenter l'analyse.
- **Options par profil sans menus séparés** : défis optionnels signalés comme tels, classements activables, modes de difficulté et assistances découplés (voir [Accessibilité](../interface/accessibilite.md)).

## Voir aussi

- [Cadres théoriques](cadres-theoriques.md) : MDA, flow, SDT, 8 kinds of fun
- [Boucles de gameplay](boucles-de-gameplay.md)
- [Multijoueur](../systemes/multijoueur.md)
- [Progression](../systemes/progression.md)
- [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)
- [Playtest et métriques](../production/playtest-et-metriques.md)
- [Gabarit : persona de joueur](../production/templates/persona-joueur.md)

## Sources

- Richard Bartle, « Hearts, Clubs, Diamonds, Spades: Players Who Suit MUDs », *Journal of MUD Research*, 1996 ; *Designing Virtual Worlds*, New Riders, 2003.
- Nick Yee, « Motivations for Play in Online Games », *CyberPsychology & Behavior*, 9(6), 2006.
- Quantic Foundry, *Gamer Motivation Model* et Gamer Motivation Profile — https://quanticfoundry.com ; « Map of Gaming Motivations », 2015 — https://quanticfoundry.com/2015/12/21/map-of-gaming-motivations/ ; analyse des écarts liés au genre et à l'âge, 2015 — https://quanticfoundry.com/2015/08/28/gender-differences-in-gaming/
- Chris Bateman et Lennart Nacke, BrainHex, 2011 ; Lennart Nacke, Chris Bateman, Regan Mandryk, « BrainHex: A Neurobiological Gamer Typology Survey », *Entertainment Computing*, 2014.
- Marc Busch et al., « Player Type Models: Towards Empirical Validation », CHI EA 2016.
- Gustavo F. Tondello et al., « Towards a Trait Model of Video Game Preferences », *International Journal of Human-Computer Interaction*, 2018.
- Gustavo F. Tondello, Karina Arrambide, Giovanni Ribeiro, Andrew Cen, Lennart Nacke, « "I Don't Fit into a Single Type": A Trait Model and Scale of Game Playing Preferences », INTERACT 2019 — https://playertraits.hcigames.com/
- Andrzej Marczewski, *Even Ninja Monkeys Like to Play*, 2015 ; HEXAD — https://www.gamified.uk/user-types/
- Gustavo F. Tondello et al., « The Gamification User Types Hexad Scale », CHI PLAY 2016 ; « Empirical validation of the Gamification User Types Hexad scale in English and Spanish », *International Journal of Human-Computer Studies*, 127, 2019.
- « Do people's user types change over time? An exploratory study », 2021 — https://arxiv.org/abs/2106.10148
- Nicole Lazzaro, « Why We Play Games: Four Keys to More Emotion Without Story », XEODesign, 2004.
- Mark Rosewater, « Timmy, Johnny, and Spike », *Making Magic*, 2002 ; « Timmy, Johnny, and Spike Revisited », 2006 ; « Melvin and Vorthos », 2007 — https://magic.wizards.com/en/news/making-magic/melvin-and-vorthos-2007-05-07
- Jesper Juul, *A Casual Revolution: Reinventing Video Games and Their Players*, MIT Press, 2010.
- Juho Hamari et Janne Tuunanen, « Player Types: A Meta-synthesis », *Transactions of the Digital Games Research Association*, 1(2), 2014 — https://todigra.org/index.php/todigra/article/view/1697
- Jukka Vahlo, Johanna Kaakinen, Suvi Holm, Aki Koponen, « Digital Game Dynamics Preferences and Player Types », *Journal of Computer-Mediated Communication*, 22(2), 2017.
- Kirsi Pauliina Kallio, Frans Mäyrä, Kirsikka Kaipainen, « At Least Nine Ways to Play: Approaching Gamer Mentalities », *Games and Culture*, 6(4), 2011.
