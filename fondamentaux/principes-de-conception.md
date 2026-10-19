# Principes de conception

> **En bref** : les principes transversaux qui reviennent dans presque tous les jeux réussis — choix intéressants, lisibilité, risque/récompense, émergence, agence, profondeur sans complexité, premier contact. Chaque principe est formulé en règles actionnables et en questions de diagnostic, pour trancher une décision de conception concrète.

## Quand consulter cette fiche

- Tu dois choisir entre deux versions d'une mécanique.
- Une mécanique est « correcte » mais personne ne s'en sert, ou tout le monde fait la même chose.
- Le joueur ne comprend pas ce qui s'est passé (mort, échec, résultat d'une action).
- Tu ajoutes une règle et te demandes si elle vaut sa complexité.
- Tu conçois les premières minutes du jeu.

---

## 1. Des choix intéressants

« Un jeu est une suite de choix intéressants » — formule attribuée à Sid Meier. Un choix est intéressant si :

1. **Aucune option n'est toujours la meilleure** (pas de stratégie dominante).
2. **Les options ont des compromis** (*trade-offs*) : gagner quelque chose = renoncer à autre chose.
3. **Le joueur a assez d'information** pour raisonner, mais pas assez pour calculer la réponse avec certitude.
4. **Le choix a des conséquences** perceptibles, et le joueur peut les relier à sa décision.
5. **Le contexte change la bonne réponse** : selon la situation, l'option A ou B devient préférable.

| Choix non intéressant | Pourquoi | Correction |
|---|---|---|
| Épée +10 vs épée +8, même coût | Évident | Ajouter un compromis (+8 mais plus rapide) |
| Deux portes identiques sans indice | Aléatoire, pas un choix | Donner un indice (bruit, lumière, trace) |
| 30 talents à +1 % | Pas de conséquence perceptible | Moins d'options, plus marquées |
| Option « gauche » toujours plus rentable | Stratégie dominante | Rééquilibrer ou rendre contextuel |
| Choix narratif sans effet | Faux choix, ruine la confiance | Conséquence visible, même petite |

Types de compromis utiles : court terme vs long terme, sécurité vs gain, spécialisation vs polyvalence, ressource A vs ressource B, maintenant vs plus tard, soi vs groupe.

## 2. Lisibilité et clarté

Le joueur doit pouvoir répondre à tout instant à : **où suis-je, que se passe-t-il, que puis-je faire, que s'est-il passé ?**

Règles :
- **Forme avant détail** : les éléments de gameplay se distinguent par leur silhouette, leur couleur et leur mouvement avant leurs détails. Un danger se reconnaît en un coup d'œil.
- **Codes visuels constants** : une couleur ou une forme associée à un sens (rouge = danger, brillant = interactif) ne change jamais de sens dans le jeu.
- **Contraste gameplay / décor** : les éléments interactifs ressortent du fond ; le décor ne ressemble pas à un élément jouable.
- **Annoncer les dangers** (*telegraphing*) : toute attaque qui peut toucher le joueur est annoncée avant d'être active (voir [Combat](../systemes/combat.md)).
- **Chaque échec doit être compréhensible** : le joueur doit savoir pourquoi il a perdu. « Je suis mort à cause de X, la prochaine fois je ferai Y » est le signe d'un échec juste.
- **Retour sur chaque action** : toute entrée du joueur produit un retour perceptible, même si l'action échoue (son de refus, animation).
- **Hiérarchie de l'information** : ce qui compte maintenant est le plus visible ; l'information secondaire est consultable sans encombrer.
- **Le juice ne doit jamais nuire à la lisibilité** : particules, shake et flashs restent subordonnés à la clarté (voir [Game feel](../ressenti/game-feel-juice.md)).

Test : montrer une capture d'écran à quelqu'un pendant 2 secondes. Peut-il dire où est le personnage, où sont les dangers et quel est l'objectif ?

## 3. Risque et récompense

- Plus le risque est grand, plus la récompense doit l'être. Le joueur doit **choisir** son niveau de risque.
- Le risque doit être **lisible** : le joueur sait qu'il prend un risque avant de le prendre.
- Exemples : attaquer de près pour plus de dégâts, garder une ressource pour un bonus plus tard, prendre un chemin dangereux pour un trésor, encaisser des gains maintenant ou continuer (*push your luck*).
- Si le chemin sûr et le chemin risqué rapportent la même chose, tout le monde prend le sûr. Si le risqué rapporte trop, il devient obligatoire.
- Les mécaniques de *push your luck* (continuer ou s'arrêter) créent de la tension à faible coût de conception.

## 4. Émergence vs scripté

| | Émergent | Scripté |
|---|---|---|
| Définition | Des règles simples qui interagissent produisent des situations non prévues | Des situations conçues une par une |
| Forces | Rejouabilité, sentiment de liberté, histoires de joueurs | Contrôle du rythme, de l'émotion, de la mise en scène |
| Faiblesses | Moins de contrôle, cas limites, exploits | Coût de production linéaire, faible rejouabilité |
| Exemples | Simulation, roguelike, immersive sim, jeux de construction | Jeux narratifs linéaires, set pieces |

Règles :
- Pour favoriser l'émergence : des systèmes qui **lisent et écrivent les mêmes états** (le feu brûle l'herbe, l'herbe brûlée ne cache plus, l'IA réagit à la visibilité). Plus il y a de connexions entre systèmes, plus il y a d'émergence.
- Préférer des règles **générales** (« le feu se propage aux objets inflammables ») aux règles **spécifiques** (« ce baril explose quand ce script le dit ») : elles se combinent.
- L'émergence doit rester **lisible** : le joueur doit comprendre la chaîne de causes.
- Combiner les deux : un cadre scripté (niveaux, histoire) dans lequel des systèmes émergents opèrent.

## 5. Agence

L'agence est le sentiment que **ses actions ont un effet significatif sur le monde**.

- Le joueur doit voir les **conséquences** de ses actions, de préférence durablement (porte détruite qui reste ouverte, PNJ qui se souvient).
- Les faux choix et les conséquences invisibles détruisent l'agence plus vite que l'absence de choix.
- Une contrainte assumée (couloir, histoire linéaire) n'empêche pas l'agence si les actions **dans** ce cadre comptent.
- Éviter de retirer le contrôle sans raison (cinématique au moment clé, QTE qui remplace l'action) : laisser le joueur accomplir les moments importants.

## 6. Contraintes créatives

- Les contraintes **produisent** le design : limite de verbes, de taille de carte, de nombre de règles, de durée de session.
- Choisir des contraintes tôt (« un seul bouton », « une salle », « 10 minutes ») accélère la conception et donne une identité.
- En production : contraintes techniques et de scope sont aussi des contraintes créatives. Concevoir **avec** elles plutôt que contre.

## 7. Profondeur vs complexité

- **Complexité** : ce que le joueur doit apprendre (nombre de règles, d'exceptions, d'éléments d'interface).
- **Profondeur** : la richesse des situations et des stratégies qui en découlent.
- Viser le **meilleur rapport profondeur/complexité** : chaque règle ajoutée doit créer beaucoup de nouvelles situations. Le go a peu de règles et une profondeur immense.

Règles :
- Avant d'ajouter une règle : combien de nouvelles décisions intéressantes crée-t-elle ? Si peu, ne pas l'ajouter.
- Préférer **réutiliser** un élément existant dans un nouveau contexte plutôt qu'ajouter un nouvel élément.
- Chaque **exception** à une règle coûte cher en compréhension ; les limiter.
- Élégance : un élément qui sert plusieurs fonctions est meilleur que plusieurs éléments à fonction unique.

### « Facile à apprendre, difficile à maîtriser »

- **Facile à apprendre** : peu de règles de base, actions de base immédiatement utiles, résultat visible dès les premières actions.
- **Difficile à maîtriser** : plafond de compétence élevé grâce aux interactions entre règles, au timing, à la lecture de l'adversaire, à l'optimisation.
- Le plafond doit venir de la **profondeur** (interactions), pas de la complexité (règles cachées, entrées obscures).
- Prévoir des **paliers de maîtrise** visibles : le joueur doit sentir qu'il progresse (techniques avancées découvrables, défis optionnels).

## 8. Trouver le fun (*find the fun*)

- Le fun se **découvre** en prototypant, il ne se décrète pas dans un document.
- Prototyper la boucle d'action en premier, sans habillage. Si elle n'est pas plaisante en carrés gris, l'habillage ne la sauvera pas.
- Quand quelque chose d'imprévu est amusant en playtest, **l'explorer** plutôt que le corriger : beaucoup de mécaniques marquantes sont nées d'accidents.
- Couper ce qui n'est pas amusant, même si c'était dans le plan.
- Principe des « 30 secondes de fun », associé à Bungie et à la conception de *Halo* (Jaime Griesemer) : si une séquence de 30 secondes est amusante et peut être rejouée dans des contextes variés, on peut construire tout le jeu dessus.

## 9. Premier contact et 30 premières secondes

Les premières secondes déterminent si le joueur continue. Règles :
- Le joueur **agit dans les premières secondes** : pas de longue cinématique, pas de mur de texte, pas d'écran de configuration obligatoire avant de jouer.
- La première action doit être **satisfaisante** : le verbe principal, avec son meilleur feedback.
- Montrer **la promesse** du jeu tôt : ce qui le rend unique doit apparaître dans les premières minutes.
- Le premier échec doit être **rapide à réparer** : relance immédiate, pas de perte importante.
- Apprendre par l'action plutôt que par l'explication (voir [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)).
- Dans un contexte de démo, de salon ou de jam, la première minute est souvent tout ce qui sera joué : la soigner en priorité.

---

## Anti-patterns transversaux

- **Stratégie dominante** non détectée : tout le monde joue pareil.
- **Fausse profondeur** : beaucoup de chiffres, peu de décisions.
- **Punition sans information** : le joueur échoue sans comprendre pourquoi.
- **Feature creep** : ajouter des systèmes pour compenser une boucle faible.
- **Récompense déconnectée** : une récompense qui ne change rien au jeu.
- **Retrait de contrôle aux moments clés.**

## Checklist

- [ ] Chaque choix majeur du joueur a un compromis explicite ; aucune option n'est toujours la meilleure.
- [ ] Le joueur dispose d'indices suffisants pour raisonner sur ses choix.
- [ ] Toute attaque ou danger est annoncé avant d'être actif.
- [ ] Après chaque échec, un testeur peut expliquer pourquoi il a échoué.
- [ ] Les codes visuels (couleurs, formes) ont un sens unique et constant.
- [ ] Le chemin risqué rapporte plus que le chemin sûr, sans être obligatoire.
- [ ] Les systèmes principaux partagent des états (interactions possibles entre eux).
- [ ] Chaque règle ajoutée a été justifiée par les décisions qu'elle crée.
- [ ] Le joueur agit dans les 30 premières secondes et utilise le verbe principal dans la première minute.
- [ ] La boucle d'action a été jugée amusante sans habillage.

## Pistes d'implémentation

- **Lisibilité** : définir une palette de gameplay (couleurs réservées aux dangers, aux interactifs, au joueur) dans un fichier de constantes ou un asset partagé, et l'utiliser partout. Faire un test « écran en niveaux de gris » pour vérifier que les silhouettes et contrastes suffisent sans couleur.
- **Émergence** : modéliser les propriétés des objets par **tags/états** génériques (`inflammable`, `conducteur`, `léger`) et des systèmes qui réagissent aux tags, plutôt que des comportements codés en dur par objet. UE5 : *Gameplay Tags*. Godot : groupes ou métadonnées. Unity : composants ou flags.
- **Choix** : instrumenter le taux de sélection de chaque option (armes, talents, chemins). Une option choisie à plus de ~70 % ou à moins de ~5 % est un signal à investiguer (seuils empiriques, à adapter au nombre d'options).
- **Premier contact** : mesurer le temps entre le lancement de l'exécutable et la première action de gameplay ; le réduire.

## Voir aussi

- [Boucles de gameplay](boucles-de-gameplay.md)
- [Cadres théoriques](cadres-theoriques.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)
- [UI / UX / HUD](../interface/ui-ux-hud.md)
- [Processus et prototypage](../production/processus-et-prototypage.md)

## Sources

- Sid Meier, « Interesting Decisions », conférence GDC 2012.
- Tynan Sylvester, *Designing Games: A Guide to Engineering Experiences*, O'Reilly, 2013.
- Raph Koster, *A Theory of Fun for Game Design*, 2004 (2ᵉ éd. 2013).
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, 2008 (3ᵉ éd. 2019).
- Greg Costikyan, *Uncertainty in Games*, MIT Press, 2013.
- Celia Hodent, *The Gamer's Brain: How Neuroscience and UX Can Impact Video Game Design*, CRC Press, 2017.
- Jaime Griesemer, propos sur les « 30 secondes de fun » de *Halo* (Bungie), largement relayés dans la presse spécialisée.
