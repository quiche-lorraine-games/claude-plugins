# Démo, Steam Playtest et Steam Next Fest

> **En bref** : les trois façons de faire jouer avant la sortie (démo, Steam Playtest, clés de test), leurs règles et leurs différences, puis la Steam Next Fest : éligibilité, calendrier type, dates de l'édition de février 2027 et conseils de Valve. Relevé le 04/11/2026 sur la documentation Steamworks.

## Quand consulter cette fiche

- Tu hésites entre une démo et un playtest.
- Tu prépares une démo pour la Next Fest ou un festival.
- Tu veux faire tester un jeu non annoncé.
- Tu choisis à quelle Next Fest participer.

---

## 1. Démo, Playtest ou clés : lequel choisir

| | Démo | Steam Playtest | Clés *Release State Override* du jeu |
|---|---|---|---|
| But | faire essayer une portion finie du jeu | recueillir des retours sur un build en cours | test confidentiel (« amis et famille ») |
| App ID | à part, liée au jeu | à part (« enfant »), liée au jeu | celui du jeu |
| Page | bouton sur la page du jeu, ou page à part | section d'inscription sur la page du jeu | aucune |
| Avis des joueurs | oui, si page à part | non | non |
| Accès | public, libre | sur inscription (par lots, ou ouvert), ou par clés | par clés |
| Limite de clés | — | jusqu'à environ 50 000 en général, au cas par cas | 2 500 par app |
| Compte pour la Next Fest | **oui, obligatoire** | non | non |
| Payant | non | **jamais** (ni accès, ni achats en jeu) | non |

Règles communes : une démo ou un playtest a ses propres dépôts (*depots*) et builds, sa revue (plus courte) et ses visuels. Le temps de jeu, les avis, les remboursements, les succès et les cartes ne se mélangent pas avec ceux du jeu.

## 2. La démo

Règles et fonctionnement (Valve) :
- App ID à part, créée depuis la page du jeu (*All associated packages, DLC, demos and tools* → *Add Demo*), avec sa checklist, sa revue de page et de build.
- Option : **une page boutique à part** pour la démo (avis des joueurs, description propre). Elle doit alors ne décrire que le contenu de la démo, avoir une bande-annonce et **au moins 5 captures** de la démo, et des capsules qui montrent clairement que c'est une démo. Une démo n'a jamais de communauté propre.
- Une démo peut sortir avant le jeu ; la page du jeu doit alors être en Coming Soon, pour que les joueurs l'ajoutent à leur liste de souhaits.
- **Après la sortie de la démo, republie la page du jeu** pour que le bouton « Télécharger la démo » apparaisse. Son affichage (discret à droite, ou encadré vert au centre) se règle dans *Special Settings* → *Associated Demos*.
- **Notification aux wishlists** : un seul envoi possible, dans les **14 jours** après la première sortie de la démo, en pressant le bouton sur la page de la démo. Ne pas le rater, ne pas le gaspiller.
- Une démo peut être désactivée puis réactivée (*Technical Tools*). Les joueurs qui l'ont ne peuvent plus la lancer par Steam, mais peut-être hors de Steam si elle ne vérifie pas la licence (`BIsSubscribedApp`).
- Pas de multijoueur Steam entre la démo et le jeu.

Conseils de Valve :
- qualité égale au jeu : la démo sert à décider l'achat ;
- assez de contenu pour donner envie, pas au point de tout montrer ;
- **désactiver les succès dans la démo** ; partager la sauvegarde avec le jeu par Steam Cloud (*Shared cloud APP ID*) et accorder les succès au premier lancement du jeu complet ;
- mettre dans le menu de la démo un lien vers la page du jeu (overlay : `ActivateGameOverlayToStore`) ;
- une fois le jeu sorti, partager les dépôts communs entre la démo et le jeu.

## 3. Le Steam Playtest

- App ID enfant créée depuis la page du jeu. Revue simplifiée : seulement les visuels de bibliothèque, de communauté et les icônes. Le nom visible ne se change plus après la sortie du playtest.
- Les joueurs **s'inscrivent sur la page du jeu** (ils peuvent aussi l'ajouter à leur liste de souhaits) ; le studio en accepte par lots, tirés au hasard, éventuellement par pays. Ou inscription ouverte, automatique.
- Ou par **clés**, même sans page publique.
- Arrêt : passer le playtest en *Not Playable* (désactiver d'abord l'inscription). Une clé déjà accordée n'est pas révoquée. On peut le relancer, ou le remettre à zéro (irréversible : tous les participants et toutes les clés sont retirés).
- Option expérimentale : invitations d'amis (1 à 3 par joueur, entre amis depuis au moins 30 jours).
- **Pas confidentiel** : les testeurs n'ont signé aucun accord de confidentialité.
- Recueillir les retours est à la charge du studio : Valve conseille un grand bouton « Avis » dans le menu, vers un forum, un Discord ou un outil de suivi.

Pour un **jeu non annoncé**, Valve conseille d'annoncer d'abord. Sinon, la voie la plus sûre est la clé *Release State Override* sur le jeu (2 500 au plus), avec ses propres accords de confidentialité, un nom de code, et la conscience que des extensions de navigateur ou des sites tiers repèrent les jeux lancés. Un jeu devient visible dès que sa page est publiée, qu'il passe en préchargement ou qu'il sort, même caché.

## 4. La Steam Next Fest

Festival d'une semaine consacré aux jeux à venir avec une démo jouable, **trois fois par an : février, juin, octobre**.

### Éligibilité (règles de Valve)

- le jeu n'a **jamais participé** à une Next Fest : **une seule par jeu** ;
- la page du jeu est **publiée et publique** ;
- une **démo publique et jouable** au début du festival ;
- **sortie après la fin** du festival (sortir avant ou pendant rend inéligible) ;
- pas un prologue, un chapitre 1 ou une version courte d'un jeu déjà sorti sur Steam, ni une nouvelle édition d'un jeu existant ;
- un compte développeur en règle.

Aucune exigence sur la date de sortie (tant qu'elle est après), l'exclusivité, la nouveauté ou la durée de la démo. Les jeux gratuits ou destinés à l'accès anticipé participent s'ils ne sont pas encore sortis. L'inscription se fait **depuis le jeu, pas depuis la démo**. Valve déconseille d'avoir un playtest ouvert pendant le festival : les joueurs se dispersent.

### Calendrier type (Valve)

| Quand | Quoi |
|---|---|
| Date limite d'inscription | page à jour (visuels, description, tags, au moins une bande-annonce publique) pour être retenu dans la bande-annonce officielle |
| J − 5 semaines | aperçu développeur (où le jeu sera classé) ; **démo soumise à la revue** pour être en ligne pendant l'aperçu presse |
| J − 3 semaines | **démo soumise à la revue au plus tard**, sinon risque de ne pas participer |
| J − 11 jours | aperçu presse : la presse voit la liste des jeux et joue aux démos déjà sorties |
| J − 4 jours | bande-annonce officielle |
| J | début ; démo en ligne **au moins 30 minutes avant** (conseil de Valve) |
| J + 7 jours | fin ; page récapitulative des démos les plus jouées |

Les dates exactes de chaque édition sont sur sa page et peuvent s'écarter un peu de ce calendrier.

### Édition de février 2027 (page Valve relevée le 04/11/2026)

- Festival : du **22 février 2027 à 10 h** au **1er mars 2027 à 10 h**, heure du Pacifique (UTC−8).
- 8 décembre 2026 : séance de questions-réponses en direct.
- **10 janvier 2027, 23 h 59** : date limite d'inscription, et de mise à jour des visuels pour la bande-annonce officielle.
- 18 janvier : Valve récupère les bandes-annonces ; démo et sa page soumises à la revue pour être en ligne à l'aperçu presse (la revue de page est nécessaire même sans page de démo à part).
- **1er février** : tout doit être soumis à la revue.
- 11 février : aperçu presse ; dernier jour pour retirer son accord à la bande-annonce officielle.
- 22 février : démo en ligne avant 10 h.

Édition suivante : 14 – 21 juin 2027 (dates à vérifier sur sa page).

### Pendant le festival

- Le classement se fait selon **une ou deux catégories** choisies à l'inscription, puis selon les tags : sans catégorie, le jeu n'apparaît pas dans les sections « Par genre » et « Par fonctionnalité ». Vérifie l'aperçu développeur et ajuste les tags.
- Les premiers jours, l'ordre est **aléatoire** (sauf listes nommées et sections personnalisées) ; ensuite, il est personnalisé selon ce que jouent les joueurs semblables.
- Diffusion en direct facultative, sur la page du jeu : à tester plusieurs fois avant, avec le chat ouvert par défaut et un outil RTMP. Diffuser une démo demande une configuration particulière.

### Conseils de Valve

- un bouton « Avis » dans le menu de la démo ;
- dire dans la démo si et quand elle sera désactivée ; Valve encourage à la laisser en ligne après le festival ;
- un sous-forum dédié aux retours sur la démo ;
- le bouton de la démo bien visible sur la page du jeu (*display above purchase options*) ;
- de la marge pour la revue du build : elle vérifie que le jeu tourne et tient ses promesses, pas les bugs. Une mise à jour après la revue n'est pas revue : ne casse pas la démo.

La notification de sortie de démo aux wishlists est indépendante du festival : si elle a été envoyée des mois avant, il n'y en a pas de seconde.

---

## Pièges

- Participer trop tôt avec une démo pas prête : il n'y a qu'une Next Fest par jeu.
- S'inscrire depuis la démo au lieu du jeu.
- Soumettre la démo après J − 3 semaines.
- Oublier de republier la page du jeu après la sortie de la démo.
- Annoncer une sortie pendant le festival.
- Vendre ou faire payer un playtest, ou ses clés.
- Compter sur la confidentialité d'un playtest.

## Checklist

- [ ] Choix démo, playtest ou clés motivé par le but (essai, retours, confidentialité)
- [ ] App ID de démo créée, checklist remplie, page et build soumis à temps
- [ ] Succès désactivés dans la démo, sauvegarde partagée par Steam Cloud avec le jeu
- [ ] Lien vers la page du jeu et bouton « Avis » dans le menu de la démo
- [ ] Page du jeu republiée après la sortie de la démo, bouton de démo visible
- [ ] Notification aux wishlists envoyée dans les 14 jours, espacée de deux semaines des autres
- [ ] Next Fest : inscription depuis le jeu avant la date limite, une ou deux catégories choisies
- [ ] Next Fest : démo soumise au plus tard 3 semaines avant (5 pour l'aperçu presse), en ligne 30 minutes avant
- [ ] Next Fest : sortie du jeu après la fin du festival

## Pistes d'implémentation

- **Godot** : une même base de code pour le jeu et la démo, avec un *feature tag* d'export (ex. `demo`) testé par `OS.has_feature("demo")` pour limiter le contenu, et un préréglage d'export par App ID.
- Sauvegarde partagée : enregistrer la progression de la démo dans un format que le jeu complet sait relire, au même chemin `user://`, et régler *Shared cloud APP ID* (voir [fonctionnalites-steamworks.md](fonctionnalites-steamworks.md)).
- Écran « Merci d'avoir joué » à la fin de la démo, avec le lien vers la page du jeu par l'overlay Steam (API Steamworks `ISteamFriends::ActivateGameOverlayToStore`, exposée par GodotSteam sur le singleton `Steam` ; vérifie le nom exact dans sa documentation).

## Voir aussi

- [visibilite-et-wishlists.md](visibilite-et-wishlists.md) : notifications et délai de deux semaines.
- [calendrier-de-sortie.md](calendrier-de-sortie.md)
- [gabarits/plan-de-sortie.md](gabarits/plan-de-sortie.md)

## Sources

- [Demos](https://partner.steamgames.com/doc/store/application/demos)
- [Steam Playtest](https://partner.steamgames.com/doc/features/playtest)
- [Steam Next Fest](https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest)
- [Steam Next Fest: February 2027](https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest/feb_2027)
- [Steam Next Fest - Tips](https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest/tips)
- [Upcoming Steam Events](https://partner.steamgames.com/doc/marketing/upcoming_events)
