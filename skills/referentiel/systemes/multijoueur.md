# Multijoueur

> **En bref** : concevoir les interactions entre joueurs (coopération, compétition, asymétrie), limiter les comportements toxiques par le design, apparier les joueurs, gérer l'effet boule de neige, et comprendre les contraintes réseau qui influencent directement le game design.

## Quand consulter cette fiche

- Tu ajoutes un mode coopératif ou compétitif, local ou en ligne.
- Tu conçois des rôles ou classes complémentaires.
- Les parties sont décidées trop tôt (effet boule de neige) ou les joueurs se plaignent d'injustice.
- Tu choisis comment les joueurs communiquent.
- Tu dois décider ce qui tourne côté serveur ou client, ou comment masquer la latence.

---

## 1. Types d'interaction sociale

| Type | Ce qui motive | Points d'attention |
|---|---|---|
| **Coopératif** | Réussir ensemble, complémentarité | Éviter qu'un joueur fasse tout (*quarterbacking* en jeu de société) ; donner à chacun un rôle et une information propres |
| **Compétitif** | Se mesurer, maîtrise, statut | Équité, matchmaking, gestion de la frustration de la défaite |
| **Équipe contre équipe** | Coordination + compétition | Communication, dépendance aux coéquipiers, toxicité |
| **Asymétrique** | Expériences différentes dans une même partie (1 contre 4, rôles différents) | Équilibrer l'expérience de chaque camp, pas seulement le taux de victoire |
| **Coopétitif** / semi-coopératif | Collaborer puis trahir, objectifs cachés | Lisibilité des objectifs, éviter le « faiseur de roi » |
| **Asynchrone** | Interaction sans présence simultanée (messages, fantômes, classements) | Peu de toxicité, très bon rapport coût/effet |
| **Multijoueur indirect** | Présence d'autres joueurs sans interaction directe (Journey, messages de Dark Souls) | Crée du lien social à faible risque |

Questions de conception :
- Qu'est-ce qu'un joueur **peut faire pour un autre** ? Contre un autre ?
- Qu'est-ce qu'un joueur **sait** que les autres ignorent ? (L'asymétrie d'information crée la communication.)
- Que se passe-t-il quand **un joueur quitte** la partie ?

## 2. Rôles et complémentarité

- Rôles classiques : **tank** (absorbe, contrôle l'espace), **dégâts** (élimine), **soutien** (soigne, renforce), **contrôle** (entrave l'adversaire), **éclaireur** (information, mobilité).
- Un rôle doit avoir des **moments où il est indispensable** et des **actions visibles** par l'équipe (le soutien qui sauve un allié doit être vu et reconnu).
- **Interdépendance** : les capacités doivent se combiner (combo d'un contrôle + des dégâts de zone). C'est ce qui rend la coopération intéressante.
- Éviter qu'un rôle soit **ennuyeux** (soigneur qui ne fait que regarder des barres de vie) ou **ingrat** (personne ne veut le prendre → files d'attente).
- Prévoir l'**équilibrage par composition** : la force d'une équipe dépend de la combinaison, pas seulement de chaque élément.

## 3. Communication

| Outil | Avantages | Risques |
|---|---|---|
| Chat vocal | Coordination fine | Toxicité, barrière pour beaucoup de joueurs |
| Chat texte | Accessible | Lent en action, toxicité |
| **Système de ping contextuel** (popularisé par Apex Legends) | Rapide, sans langue commune, peu toxique, accessible | Moins expressif |
| Émotes, répliques prédéfinies | Expressif, inoffensif | Spam, provocation (prévoir un délai) |
| Communication implicite (gestes, positionnement) | Universel | Limité |

Recommandations :
- **Toujours offrir un moyen de coordination sans voix ni texte** (ping). Le jeu doit être jouable sans chat.
- Pings **contextuels** : la même touche indique un ennemi, un objet, une destination selon ce qu'on vise.
- Répliques prédéfinies **positives** et utiles ; limiter celles qui servent à provoquer.

## 4. Toxicité et anti-griefing par le design

Le design peut prévenir une grande partie des comportements nuisibles **avant** la modération.

- **Réduire les vecteurs** : pas de collisions entre alliés si elles permettent de bloquer, pas de *friendly fire* par défaut (ou réduit), pas de vol de loot (loot individuel), pas de vote d'exclusion abusable.
- **Ne pas exposer d'informations comparatives humiliantes** en cours de partie (scores individuels très visibles en jeu d'équipe).
- **Réduire la dépendance à un seul joueur** : un joueur faible ne doit pas condamner l'équipe à lui seul.
- **Gérer les abandons** : remplacement par bot, rejoindre en cours de partie, possibilité de capituler ensemble (*surrender vote*), pénalités pour abandon répété.
- **Renforcement positif** : récompenser le jeu d'équipe (assistance, soin, objectif) et les recommandations entre joueurs.
- **Outils** : signalement simple, coupure du son/chat par joueur, chat désactivé par défaut pour les mineurs, filtres.
- **Anti-triche** : ne jamais faire confiance au client (voir section netcode).

## 5. Matchmaking et classement

- **Objectif** : des parties serrées (proches de 50/50) et une attente raisonnable. Les deux sont en tension.
- Systèmes de cote :
  - **Elo** : chaque partie fait varier la cote selon l'écart attendu ; simple, conçu pour le 1 contre 1.
  - **Glicko / Glicko-2** : ajoute une incertitude sur la cote (un joueur peu actif a une cote plus incertaine).
  - **TrueSkill** (Microsoft Research) : gère les équipes et les parties à plusieurs joueurs.
- **MMR caché vs rang affiché** : courant de séparer la cote réelle (pour apparier) du rang visible (pour motiver, avec paliers, divisions et protections contre la descente).
- **Placement** : premières parties avec forte variation de cote.
- **Groupes** (*premades*) : un groupe coordonné est plus fort que sa cote moyenne ; l'apparier avec d'autres groupes ou ajuster.
- **Nouveaux joueurs** : les protéger des joueurs expérimentés (files séparées, bots en début de progression) ; surveiller les *smurfs* (comptes secondaires).
- **Petite population** : élargir les critères avec le temps d'attente, proposer des bots, limiter le nombre de modes pour ne pas fragmenter la base de joueurs.

## 6. Effet boule de neige et rattrapage

**Boule de neige** (*snowballing*) : l'avantage initial donne plus d'avantage, la partie est jouée d'avance bien avant sa fin.

| Mécanique de rattrapage | Exemple | Risque |
|---|---|---|
| Bonus aux derniers | Objets plus forts pour les derniers (Mario Kart) | Punit l'excellence, frustre le meneur |
| Prime sur le meneur | Plus de récompense pour éliminer celui qui mène | Acceptable, cohérent |
| Rendements décroissants | L'avantage rapporte de moins en moins | Peut rendre l'avance inutile |
| Objectifs tardifs décisifs | Objectifs de fin de partie qui peuvent renverser | Rend le début de partie moins important |
| Réapparition plus rapide pour les perdants | Jeux d'équipe | Ralentit la conclusion |
| Information cachée sur le score | Empêche de savoir qui mène | Réduit la tension |

Règles :
- Garder **l'avantage mérité** : le rattrapage doit **ralentir** l'écart, pas l'annuler. Sinon le début de partie n'a plus de sens.
- Préférer le rattrapage **par opportunité** (une chance de revenir en jouant bien) au rattrapage **automatique**.
- Permettre de **conclure** : si l'issue est jouée, abréger la partie (capitulation, condition de victoire anticipée).
- Inversement, une partie jamais décidée avant la dernière seconde dévalorise tout ce qui précède.

---

## 7. Netcode : notions pour designers

Les contraintes réseau **changent le design**. À décider tôt, pas après le prototype.

### Autorité

| Modèle | Principe | Usage |
|---|---|---|
| **Serveur autoritaire** | Le serveur décide de l'état ; les clients envoient des entrées | Standard en compétitif, anti-triche |
| **Hôte joueur** (*listen server*) | Un joueur fait office de serveur | Coop, petits jeux ; avantage à l'hôte, problème si l'hôte quitte |
| **Pair à pair déterministe** | Chaque client simule le même jeu à partir des mêmes entrées (*lockstep*) | Jeux de stratégie (RTS), jeux de combat ; exige un déterminisme strict |

Règle d'or : **ne jamais faire confiance au client** pour ce qui compte (dégâts, inventaire, monnaie, position validée).

### Latence et techniques de masquage

- **Latence** (*ping*) : temps aller-retour, de quelques dizaines à quelques centaines de ms. Elle **ne disparaît jamais** ; on la masque.
- **Prédiction côté client** : le client applique immédiatement ses propres entrées, puis se corrige (*reconciliation*) si le serveur diffère. Indispensable pour le mouvement du joueur.
- **Interpolation** : les autres joueurs sont affichés légèrement dans le passé, interpolés entre deux états reçus. Mouvement fluide, mais décalé.
- **Compensation de latence** (*lag compensation*) : le serveur « remonte le temps » pour valider un tir selon ce que le tireur voyait. Effet : la victime peut être touchée « derrière un mur ».
- **Rollback** (popularisé par GGPO) : chaque client prédit les entrées adverses, simule, puis revient en arrière et resimule si la prédiction était fausse. Standard actuel des jeux de combat.
- **Délai d'entrée** (*delay-based*) : on retarde toutes les entrées pour attendre celles de l'adversaire. Simple, mais la latence se ressent sur les commandes.

### Conséquences sur le design

- **Actions instantanées à fort impact** (hitscan, parade à quelques frames) = plus sensibles à la latence. Prévoir des fenêtres un peu plus larges en ligne, ou de l'anticipation qui masque la latence.
- **Anticipation des attaques** : une animation de préparation laisse le temps au réseau de transmettre l'information. C'est un outil de netcode autant que de lisibilité.
- **Collisions entre joueurs** et objets physiques partagés : coûteux et sources de désynchronisation. Les limiter.
- **Physique et aléatoire** : déterministes et seedés si la simulation est partagée (voir [Aléatoire et procédural](aleatoire-et-procedural.md)).
- **Nombre de joueurs et d'entités** : chaque entité répliquée coûte de la bande passante. Répliquer l'**intention** (entrées, événements) plutôt que tout l'état quand c'est possible.
- **Effets cosmétiques en local** : particules, sons, juice ne sont pas répliqués, seulement les événements qui les déclenchent.
- **Rejoindre en cours** et **reconnexion** : à concevoir dès le départ (sérialisation de l'état complet).

---

## Anti-patterns et pièges

- **Ajouter le multijoueur après coup** à un jeu solo : la logique doit être séparée de la présentation et autoritaire dès le début.
- **Faire confiance au client** pour les dégâts ou l'inventaire.
- **Jeu d'équipe sans communication non verbale**.
- **Rattrapage qui annule le mérite**.
- **Trop de modes** pour la population de joueurs (files vides).
- **Vecteurs de griefing** laissés ouverts (blocage par collision, friendly fire, vol de loot).
- **Pas de gestion des abandons**.

## Checklist

- [ ] Le type d'interaction sociale est explicite (coop, compétitif, asymétrique, asynchrone).
- [ ] Chaque rôle a des moments indispensables et des actions visibles par l'équipe.
- [ ] Un système de communication non verbale (ping) existe.
- [ ] Les vecteurs de griefing connus sont fermés par le design.
- [ ] Les abandons et reconnexions sont gérés.
- [ ] Le matchmaking vise l'équilibre et une attente raisonnable, avec protection des nouveaux joueurs.
- [ ] L'effet boule de neige est mesuré, et le rattrapage ralentit l'écart sans l'annuler.
- [ ] Le modèle d'autorité réseau est choisi avant la production.
- [ ] La logique critique tourne côté serveur (ou est déterministe et vérifiée).
- [ ] Le mouvement du joueur utilise la prédiction client ; les autres sont interpolés.
- [ ] Les fenêtres de timing serrées ont été testées avec latence simulée.

## Pistes d'implémentation

- Séparer strictement **simulation** (état, règles, entrées) et **présentation** (rendu, sons, juice) : condition nécessaire au réseau, aux replays et au rollback.
- Tester systématiquement avec **latence, gigue et perte de paquets simulées** (outils du moteur ou proxy réseau).
- **UE5** : réplication intégrée (`Replicated`, RPC `Server`/`Client`/`NetMulticast`), `CharacterMovementComponent` avec prédiction intégrée, GAS avec prédiction des capacités, émulation réseau (`Net PktLag`, `PktLoss`) dans les paramètres de l'éditeur.
- **Godot** : `MultiplayerAPI`, `MultiplayerSynchronizer`, `MultiplayerSpawner`, RPC avec `@rpc`.
- **Unity** : Netcode for GameObjects ou solutions tierces (Mirror, Fish-Net, Photon) ; Unity Transport avec simulateur réseau.
- Rollback pour jeu de combat : GGPO (open source) ou bibliothèques dérivées ; exige une simulation déterministe à pas fixe et la capacité de sauvegarder/restaurer l'état rapidement.

## Voir aussi

- [Équilibrage et difficulté](equilibrage-et-difficulte.md)
- [Combat](combat.md)
- [Aléatoire et procédural](aleatoire-et-procedural.md)
- [Économie](economie.md)
- [Accessibilité](../interface/accessibilite.md)

## Sources

- Gabriel Gambetta, *Fast-Paced Multiplayer* (série d'articles) — https://www.gabrielgambetta.com/client-server-game-architecture.html
- Glenn Fiedler, *Gaffer On Games* (networking, déterminisme) — https://gafferongames.com/
- Valve, « Source Multiplayer Networking » (Valve Developer Community) — https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking
- Tim Ford, « Overwatch Gameplay Architecture and Netcode », GDC 2017.
- GGPO (Tony Cannon), rollback netcode — https://www.ggpo.net/
- Ralf Herbrich, Tom Minka & Thore Graepel, « TrueSkill: A Bayesian Skill Rating System », NIPS 2006.
- Mark Glickman, *The Glicko System* — http://www.glicko.net/glicko.html
- Arpad Elo, *The Rating of Chessplayers, Past and Present*, Arco, 1978.
- David Sirlin, *Playing to Win*, 2006 — https://www.sirlin.net/ptw
