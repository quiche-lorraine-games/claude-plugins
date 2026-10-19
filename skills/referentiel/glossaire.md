# Glossaire

> **En bref** : vocabulaire du game design utilisé dans les fiches, en français avec le terme anglais d'usage. Classement alphabétique. Le lien indique la fiche qui développe la notion.

## 0–9

- **4X** (*eXplore, eXpand, eXploit, eXterminate*) : sous-genre de stratégie fondé sur l'expansion d'un empire. → [Stratégie](genres/strategie.md)

## A

- **Affordance / signifiant** (*affordance / signifier*) : possibilité d'action offerte par un élément, et indice qui la signale au joueur. → [UI/UX](interface/ui-ux-hud.md)
- **Agence** (*agency*) : sentiment que ses actions ont un effet significatif sur le monde du jeu. → [Principes](fondamentaux/principes-de-conception.md)
- **Aléatoire d'entrée / de sortie** (*input / output randomness*) : hasard placé avant la décision du joueur (il s'y adapte) ou après (il la sanctionne). → [Aléatoire](systemes/aleatoire-et-procedural.md)
- **Ancrage aux plateformes** (*platform snapping*) : en 2D, la caméra ne suit verticalement le joueur qu'à l'atterrissage. → [Caméra](ressenti/camera.md)
- **Annonce d'attaque, télégraphie** (*telegraphing*) : signaux visuels et sonores qui précèdent un danger avant qu'il soit actif. → [Combat](systemes/combat.md)
- **Anti-persona** : joueur qu'on décide de ne pas viser, pour trancher ce qu'on coupe. → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Anticipation** (*startup, windup*) : phase d'une attaque avant que la hitbox soit active ; elle rend l'attaque lisible. → [Combat](systemes/combat.md)
- **Anticipation de caméra** (*lookahead*) : décalage de la caméra dans la direction du mouvement. → [Caméra](ressenti/camera.md)
- **APM** (*actions per minute*) : nombre d'actions par minute, mesure de la vitesse d'exécution en RTS. → [Stratégie](genres/strategie.md)
- **Arc** (*arc*) : contenu consommé une seule fois (histoire, boss unique), par opposition à une boucle. → [Boucles](fondamentaux/boucles-de-gameplay.md)
- **Assistance à la visée** (*aim assist*) : friction, magnétisme ou déviation qui aident à viser au stick. → [Contrôles](ressenti/controles-et-mouvement.md)

## B

- **Bark** (réplique contextuelle) : courte réplique déclenchée par le système, qui informe sur l'état de l'IA ou du monde. → [Narration](contenu/narration.md)
- **Behavior tree** (arbre de comportement) : architecture d'IA en arbre de sélecteurs et de séquences évalués par priorité. → [IA ennemie](systemes/ia-ennemis.md)
- **Boucle centrale** (*core loop*) : activité principale répétée, de quelques dizaines de secondes à quelques minutes. → [Boucles](fondamentaux/boucles-de-gameplay.md)
- **Boucle d'action** (*moment-to-moment loop*) : cycle de quelques secondes : percevoir, agir, recevoir un retour. → [Boucles](fondamentaux/boucles-de-gameplay.md)
- **Boucle de compulsion** (*compulsion loop*) : boucle portée par une récompense extrinsèque répétée. → [Boucles](fondamentaux/boucles-de-gameplay.md)
- **Boucle de maîtrise** (*mastery loop*) : boucle portée par l'amélioration de la compétence du joueur. → [Boucles](fondamentaux/boucles-de-gameplay.md)
- **Boule de neige** (*snowballing*) : avantage précoce qui s'amplifie jusqu'à décider la partie. → [Multijoueur](systemes/multijoueur.md)
- **BrainHex** : typologie à 7 archétypes (Seeker, Survivor, Daredevil, Mastermind, Conqueror, Socialiser, Achiever), utile comme grille mais peu validée. → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Bras de caméra** (*spring arm*) : bras qui place la caméra derrière le personnage en gérant les collisions. → [Caméra](ressenti/camera.md)

## C

- **Choix intéressant** (*interesting decision*) : choix avec compromis, sans option toujours meilleure, aux conséquences perceptibles. → [Principes](fondamentaux/principes-de-conception.md)
- **Compensation de latence** (*lag compensation*) : le serveur valide un tir selon ce que voyait le tireur au moment du tir. → [Multijoueur](systemes/multijoueur.md)
- **Compromis** (*trade-off*) : gagner quelque chose en renonçant à autre chose. → [Principes](fondamentaux/principes-de-conception.md)
- **Contrôle aérien** (*air control*) : capacité à modifier sa trajectoire horizontale en l'air. → [Contrôles](ressenti/controles-et-mouvement.md)
- **Convertisseur** (*converter*) : mécanisme qui transforme une ressource en une autre (crafting, boutique). → [Économie](systemes/economie.md)
- **Correction de coin** (*corner correction*) : décalage automatique de quelques pixels quand la tête accroche l'arête d'un plafond ou d'une plateforme. → [Contrôles](ressenti/controles-et-mouvement.md)
- **Courbe d'XP** (*XP curve*) : fonction qui donne l'expérience cumulée nécessaire pour atteindre chaque niveau. → [Progression](systemes/progression.md)
- **Courbe de coût** (*cost curve*) : relation cible entre le coût d'une option et sa puissance ; sert de référence pour équilibrer cartes, unités ou objets. → [Équilibrage](systemes/equilibrage-et-difficulte.md)
- **Courbe de réponse** (*response curve*) : fonction qui transforme l'amplitude du stick en vitesse de mouvement ou de visée. → [Contrôles](ressenti/controles-et-mouvement.md)
- **Coyote time** (temps de coyote) : courte fenêtre après avoir quitté un rebord pendant laquelle le saut reste possible. → [Contrôles](ressenti/controles-et-mouvement.md)

## D

- **Danmaku** : sous-genre du shmup aux motifs de balles très denses mais déterministes. → [Shooter](genres/shooter.md)
- **Dark pattern** : mécanique conçue pour pousser le joueur contre son intérêt (temps, argent, pression sociale). → [Économie](systemes/economie.md)
- **DDA** (*dynamic difficulty adjustment*) : difficulté ajustée automatiquement selon la performance du joueur. → [Équilibrage](systemes/equilibrage-et-difficulte.md)
- **Dents de scie** (*sawtooth curve*) : courbe de difficulté qui monte dans un segment puis redescend au début du suivant. → [Équilibrage](systemes/equilibrage-et-difficulte.md)
- **Dilution** : baisse de la probabilité de piocher une carte donnée quand le deck grossit. → [Deckbuilder](genres/deckbuilder-cartes.md)
- **Dissonance ludonarrative** (*ludonarrative dissonance*) : contradiction entre ce que racontent les mécaniques et ce que raconte l'histoire. → [Narration](contenu/narration.md)
- **Ducking** (*ducking, sidechain*) : baisse automatique d'un bus audio quand un son prioritaire joue. → [Audio](interface/audio.md)

## E

- **Écologie des joueurs** : équilibre entre populations de profils dans un monde partagé, chaque population influençant les autres (Bartle). → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Effet de gradient d'objectif** (*goal-gradient effect*) : la motivation augmente à l'approche d'un but. → [Progression](systemes/progression.md)
- **Embranchements qui se rejoignent** (*branch and bottleneck*) : branches narratives qui divergent puis reconvergent à des nœuds clés. → [Narration](contenu/narration.md)
- **Émergence** (*emergence*) : situations non prévues qui naissent de l'interaction de règles simples. → [Principes](fondamentaux/principes-de-conception.md)
- **Épuration** (*thinning*) : retrait de cartes faibles pour améliorer la qualité moyenne de la main. → [Deckbuilder](genres/deckbuilder-cartes.md)
- **Équilibrage intransitif** : relations circulaires de type pierre-feuille-ciseaux entre options. → [Équilibrage](systemes/equilibrage-et-difficulte.md)
- **Esthétique (MDA)** (*aesthetics*) : réponse émotionnelle visée chez le joueur, à ne pas confondre avec le style visuel. → [Cadres théoriques](fondamentaux/cadres-theoriques.md)

## F

- **Fausse piste** (*red herring*) : solution apparente qui échoue et révèle une contrainte. → [Puzzle](genres/puzzle.md)
- **Feature creep** : ajout continu de fonctionnalités qui fait dériver le périmètre. → [Processus](production/processus-et-prototypage.md)
- **Fenêtre d'annulation** (*cancel window*) : moment où une action peut en interrompre une autre. → [Combat](systemes/combat.md)
- **Fenêtre de caméra** (*camera window*) : cadre dans lequel le joueur bouge sans que la caméra le suive. → [Caméra](ressenti/camera.md)
- **Fiero** : sentiment de triomphe après avoir surmonté une difficulté (Lazzaro). → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Flow** : état d'absorption quand le défi correspond à la compétence, avec but clair et retour immédiat. → [Cadres théoriques](fondamentaux/cadres-theoriques.md)
- **Frames actives** (*active frames*) : fenêtre pendant laquelle une attaque peut toucher. → [Combat](systemes/combat.md)
- **Funnel** (entonnoir) : suite d'étapes où l'on mesure la part de joueurs qui atteint chacune. → [Playtest](production/playtest-et-metriques.md)

## G

- **Gamer Motivation Model** : modèle de Quantic Foundry à 12 motivations en 6 paires et 3 grappes. → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Gating** (verrouillage) : contrôle de l'accès à une zone par une clé, une capacité ou un événement. → [Level design](contenu/level-design.md)
- **GOAP** (*Goal-Oriented Action Planning*) : planification d'une suite d'actions pour atteindre un but. → [IA ennemie](systemes/ia-ennemis.md)
- **Graine** (*seed*) : valeur initiale d'un générateur pseudo-aléatoire ; la même graine reproduit la même génération. → [Aléatoire](systemes/aleatoire-et-procedural.md)
- **Gravité de descente** (*fall multiplier*) : gravité plus forte à la descente qu'à la montée, pour un saut moins flottant. → [Contrôles](ressenti/controles-et-mouvement.md)
- **Graze** : fait de frôler les projectiles, récompensé en points dans certains shmups. → [Shooter](genres/shooter.md)
- **Greybox, blockout** (prototype gris) : niveau ou prototype jouable fait de primitives géométriques, pour tester ressenti et espace. → [Level design](contenu/level-design.md)

## H

- **Hard / Easy / Serious / People Fun** : les 4 clés du fun de Lazzaro : défi, nouveauté, sens, relations. → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Hauteur de saut variable** (*variable jump height*) : la hauteur du saut dépend de la durée d'appui. → [Contrôles](ressenti/controles-et-mouvement.md)
- **Heatmap** (carte de chaleur) : carte de densité des positions, morts ou trajets des joueurs. → [Playtest](production/playtest-et-metriques.md)
- **Hexad** : 6 types d'utilisateurs de gamification (Achiever, Socialiser, Philanthropist, Free Spirit, Player, Disruptor). → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Hit stop** (*hit pause*) : gel de quelques frames à l'impact pour donner du poids. → [Combat](systemes/combat.md)
- **Hit stun** : temps pendant lequel la cible touchée ne peut pas agir. → [Combat](systemes/combat.md)
- **Hitbox / hurtbox** : volume qui inflige des dégâts / volume qui les reçoit, distincts de la collision physique. → [Combat](systemes/combat.md)
- **Hitscan** : tir résolu instantanément par un rayon, sans projectile simulé. → [Shooter](genres/shooter.md)
- **HUD contextuel** (*contextual HUD*) : éléments d'interface affichés seulement quand ils sont pertinents. → [UI/UX](interface/ui-ux-hud.md)

## I

- **i-frames** (*invincibility frames*) : courte période d'invulnérabilité (esquive, après un dégât). → [Combat](systemes/combat.md)
- **Inflation de puissance** (*power creep*) : chaque ajout surpasse le précédent et rend l'ancien contenu obsolète. → [Progression](systemes/progression.md)
- **Interface diégétique** (*diegetic UI*) : élément d'interface qui existe dans la fiction et dans l'espace du jeu. → [UI/UX](interface/ui-ux-hud.md)
- **Interprétation de Berlin** (*Berlin Interpretation*) : liste de facteurs définissant le roguelike, établie en 2008. → [Roguelike](genres/roguelike.md)

## J

- **Jetons d'attaque** (*attack tokens*, *kung-fu circle*) : pool limité qui régule le nombre d'ennemis attaquant en même temps. → [Combat](systemes/combat.md)
- **Juice** : ensemble des retours de présentation (flash, shake, particules, son) qui rendent une action satisfaisante sans changer sa logique. → [Game feel](ressenti/game-feel-juice.md)
- **Jump buffer** (mémoire tampon de saut) : un appui sur saut fait juste avant l'atterrissage est mémorisé puis exécuté au contact du sol. → [Contrôles](ressenti/controles-et-mouvement.md)

## K

- **Kishōtenketsu** : structure en quatre temps (introduire, développer, tordre, conclure) appliquée à un niveau autour d'une seule idée. → [Level design](contenu/level-design.md)

## L

- **Lentille** (*lens*) : série de questions de Jesse Schell pour examiner une conception sous un angle précis. → [Cadres théoriques](fondamentaux/cadres-theoriques.md)
- **Level scaling** (mise à l'échelle) : ajustement de la puissance des ennemis au niveau du joueur. → [RPG](genres/rpg.md)
- **Loi de Fitts** (*Fitts's law*) : le temps pour atteindre une cible croît avec la distance et diminue avec sa taille. → [UI/UX](interface/ui-ux-hud.md)
- **Loi de Hick-Hyman** (*Hick's law*) : le temps de décision croît de façon logarithmique avec le nombre de choix. → [UI/UX](interface/ui-ux-hud.md)

## M

- **Maintien / bascule** (*hold / toggle*) : option qui remplace une action à maintenir par un appui unique. → [Accessibilité](interface/accessibilite.md)
- **MDA** (*Mechanics-Dynamics-Aesthetics*) : cadre qui relie les règles, les comportements qui en émergent et les émotions visées. → [Cadres théoriques](fondamentaux/cadres-theoriques.md)
- **Méta-boucle** (*meta loop*) : boucle sur plusieurs sessions qui donne une raison de revenir. → [Boucles](fondamentaux/boucles-de-gameplay.md)
- **Méta-progression** (*meta-progression*) : ce qui est conservé et débloqué d'une run à l'autre. → [Roguelike](genres/roguelike.md)
- **Métriques de personnage** (*player metrics*) : dimensions et capacités de l'avatar qui dictent celles du monde (hauteur de passage, portée de saut). → [Level design](contenu/level-design.md)
- **Metroidvania** : jeu d'exploration où de nouvelles capacités ouvrent des zones jusque-là inaccessibles. → [Level design](contenu/level-design.md)
- **Miettes de pain** (*breadcrumbs*) : suite d'objets ou d'indices qui tracent un chemin. → [Level design](contenu/level-design.md)
- **MMR** (*matchmaking rating*) : cote cachée servant à apparier les joueurs. → [Multijoueur](systemes/multijoueur.md)
- **Moment aha** (*aha moment*) : instant où le joueur comprend l'idée qui résout un puzzle. → [Puzzle](genres/puzzle.md)
- **Monnaie douce / dure** (*soft / hard currency*) : monnaie gagnée en jouant / monnaie rare, souvent achetable. → [Économie](systemes/economie.md)
- **MVP** (*minimum viable product*) : plus petite version complète et jouable qui délivre l'expérience essentielle. → [Processus](production/processus-et-prototypage.md)

## N

- **Narration émergente** (*emergent narrative*) : histoire produite par l'interaction des systèmes plutôt qu'écrite. → [Narration](contenu/narration.md)

## P

- **Penser à voix haute** (*think aloud*) : protocole de playtest où le joueur verbalise ce qu'il pense en jouant. → [Playtest](production/playtest-et-metriques.md)
- **Persona** : joueur fictif représentatif du public cible, utilisé pour arbitrer les décisions. → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Piliers** (*design pillars*) : 3 à 5 phrases qui définissent l'expérience et servent à trier les fonctionnalités. → [Processus](production/processus-et-prototypage.md)
- **Pity timer, protection contre la malchance** (*bad luck protection*) : garantie de succès, ou probabilité croissante, après N échecs. → [Aléatoire](systemes/aleatoire-et-procedural.md)
- **Point d'étranglement** (*choke point*) : passage étroit où les forces se concentrent. → [Level design](contenu/level-design.md)
- **PRD** (*pseudo-random distribution*) : la probabilité augmente après chaque échec et revient à sa base après un succès. → [Aléatoire](systemes/aleatoire-et-procedural.md)
- **Prédiction côté client** (*client-side prediction*) : le client applique ses entrées immédiatement, puis se corrige selon le serveur. → [Multijoueur](systemes/multijoueur.md)
- **Programme à ratio variable** (*variable ratio schedule*) : récompense après un nombre aléatoire d'actions, très résistant à l'extinction ; à manier avec précaution éthique. → [Progression](systemes/progression.md)
- **Progression verticale / horizontale** (*vertical / horizontal progression*) : gain de puissance brute / gain d'options sans gain net de puissance. → [Progression](systemes/progression.md)
- **Push your luck** : mécanique où l'on choisit entre encaisser ses gains et continuer au risque de les perdre. → [Principes](fondamentaux/principes-de-conception.md)

## R

- **Rattrapage** (*catch-up mechanic*) : mécanisme qui aide le joueur en retard à revenir dans la partie. → [Multijoueur](systemes/multijoueur.md)
- **Re-séquençage horizontal** (*horizontal resequencing*) : la musique passe d'un segment à l'autre selon l'état du jeu. → [Audio](interface/audio.md)
- **Récupération** (*recovery*) : phase après l'attaque où l'attaquant est vulnérable ; c'est le prix de l'attaque. → [Combat](systemes/combat.md)
- **Respec** : réattribution des points de compétence ou de statistiques d'un personnage. → [RPG](genres/rpg.md)
- **Roguelite** : jeu qui reprend les runs et la mort permanente du roguelike, souvent avec une méta-progression. → [Roguelike](genres/roguelike.md)
- **Rollback** : le client prédit les entrées adverses, puis resimule s'il s'est trompé. → [Multijoueur](systemes/multijoueur.md)

## S

- **SDT** (*Self-Determination Theory*) : théorie de la motivation fondée sur trois besoins : compétence, autonomie, appartenance. → [Cadres théoriques](fondamentaux/cadres-theoriques.md)
- **Shuffle bag** (sac mélangé) : tirage sans remise qui garantit une répartition des résultats. → [Aléatoire](systemes/aleatoire-et-procedural.md)
- **Skill atom** (atome de compétence) : unité d'apprentissage action → simulation → feedback → modèle mental (Daniel Cook). → [Onboarding](contenu/onboarding-tutoriels.md)
- **Softlock** (blocage) : situation où le jeu tourne mais où le joueur ne peut plus progresser. → [Rendre un jeu playtestable](production/rendre-un-jeu-playtestable.md)
- **Source / puits** (*faucet / sink*) : mécanisme qui crée / détruit une ressource dans l'économie. → [Économie](systemes/economie.md)
- **Squash & stretch** (écrasement et étirement) : déformation du visuel d'un personnage pour exprimer l'élan et l'impact. → [Game feel](ressenti/game-feel-juice.md)
- **Steering** (comportements de pilotage) : règles de déplacement local d'un agent (seek, flee, séparation…). → [IA ennemie](systemes/ia-ennemis.md)
- **Stinger** : courte phrase musicale jouée par-dessus la musique pour souligner un événement. → [Audio](interface/audio.md)
- **Storylet** (narration par qualités, *quality-based narrative*) : fragment de récit débloqué par des conditions sur l'état du joueur. → [Narration](contenu/narration.md)
- **Stratégie dominante** (*dominant strategy*) : option meilleure que toutes les autres dans toutes les situations, qui rend les autres inutiles. → [Équilibrage](systemes/equilibrage-et-difficulte.md)
- **Superposition verticale** (*vertical layering*) : pistes musicales synchronisées ajoutées ou retirées selon l'intensité. → [Audio](interface/audio.md)
- **Synergie** (*synergy*) : combinaison d'éléments plus forte que la somme de ses parties. → [Roguelike](genres/roguelike.md)

## T

- **Table de butin pondérée** (*weighted loot table*) : liste d'objets associés à des poids qui donnent leur probabilité de tirage. → [Économie](systemes/economie.md)
- **Timmy, Johnny, Spike** : profils de *Magic: The Gathering* : vivre une expérience, s'exprimer, prouver. → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Traits de joueur** (*player traits*) : 5 orientations continues (esthétique, narration, objectifs, social, défi) mesurées par une échelle validée (Tondello et al.). → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)
- **Trauma** : valeur entre 0 et 1 qui s'accumule et décroît ; son carré pilote l'intensité du tremblement de caméra. → [Caméra](ressenti/camera.md)
- **TTK / TTD** (*time to kill / time to die*) : temps pour éliminer une cible / temps pour mourir. → [Combat](systemes/combat.md)
- **Types de Bartle** : Achiever, Explorer, Socializer, Killer ; 8 types avec l'axe implicite / explicite. → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)

## U

- **Utility AI** (IA par utilité) : l'agent choisit l'action au meilleur score, calculé à partir de courbes. → [IA ennemie](systemes/ia-ennemis.md)

## V

- **Verbe** (*verb*) : action de base que le joueur peut effectuer (sauter, tirer, ramasser). → [Boucles](fondamentaux/boucles-de-gameplay.md)
- **Verrouillage de cible** (*lock-on*) : mode où la caméra et les actions sont orientées vers une cible choisie. → [Caméra](ressenti/camera.md)
- **Vertical slice** (tranche verticale) : portion courte du jeu à qualité finale sur tous les plans. → [Processus](production/processus-et-prototypage.md)
- **Vorthos / Mel** : profils esthétiques de *Magic* : sensible à l'univers / à l'élégance de la mécanique. → [Profils de joueurs](fondamentaux/profils-de-joueurs.md)

## W

- **Weenie** : repère visuel attractif, visible de loin, qui attire le joueur vers lui. → [Level design](contenu/level-design.md)
- **WFC** (*Wave Function Collapse*) : génération de tuiles sous contraintes d'adjacence apprises d'un exemple. → [Aléatoire](systemes/aleatoire-et-procedural.md)

## Z

- **Zone morte** (*dead zone*) : plage d'entrée du stick ignorée près du centre ; une zone morte radiale remise à l'échelle est recommandée. → [Contrôles](ressenti/controles-et-mouvement.md)
