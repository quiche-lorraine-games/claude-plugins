# steam

Plugin Claude Code, en français, pour sortir un jeu Godot sur Steam. Il contient deux skills :
- **`steam:boutique`** : référentiel pour préparer la sortie, tiré de la [documentation Steamworks](https://partner.steamgames.com/doc/home) de Valve. Page boutique, calendrier de sortie, prix, démo et Next Fest, compatibilité Steam Deck. Une table de routage « tâche → fiche », dix fiches, un gabarit de rétroplanning et la liste des sources ;
- **`steam:godotsteam`** : intégration de Steamworks dans le code du jeu avec l'extension [GodotSteam](https://godotsteam.com/), d'après sa documentation. Installation et export, un autoload `Steamworks` prêt à copier ([`gabarits/steamworks.gd`](skills/godotsteam/gabarits/steamworks.gd)), et une recette par fonctionnalité : succès et statistiques, Steam Cloud, Steam Deck, présence et overlay, classements, DLC, multijoueur.

Il n'a ni script à lancer, ni clé, ni appel réseau, ni hook.

Ce que le plugin ne fait pas :
- **il ne touche pas à Steamworks** : le site partenaire demande un compte du studio. L'agent prépare les textes, les visuels, les checklists et le calendrier ; l'humain saisit et publie ;
- il n'envoie pas de build (SteamPipe, `steamcmd`) : ce sera un autre skill.

## Installation

```bash
claude plugin marketplace add quiche-lorraine-games/claude-plugins
claude plugin install steam@quiche-lorraine-games
```

Voir le [README de la marketplace](../../README.md) pour les sessions cloud et les mises à jour.

## Utilisation

L'agent charge `steam:boutique` quand la tâche porte sur la sortie sur Steam, et `steam:godotsteam` quand il écrit le code Steamworks du jeu. On peut aussi les appeler avec `/steam:boutique` et `/steam:godotsteam`.

Pour un projet de jeu qui vise Steam, ajouter au `CLAUDE.md` du jeu :

```markdown
## Sortie sur Steam
Avant de préparer un visuel, un texte, une date, un prix ou une démo pour Steam,
charge le skill `steam:boutique` et applique la fiche pertinente. Avant d'écrire
du code qui appelle Steam, charge `steam:godotsteam` ; tout appel passe par
l'autoload Steamworks. Le plan de sortie
du projet est dans docs/steam/plan-de-sortie.md.
```

Puis copier le [gabarit de plan de sortie](skills/boutique/gabarits/plan-de-sortie.md) dans le repo du jeu.

## Contenu

```
skills/boutique/
  SKILL.md                      règles d'usage, table de routage, règles à ne jamais oublier
  visuels.md                    capsules, bibliothèque, icônes, événements : tailles et règles
  page-boutique.md              captures, bande-annonce, description, tags, langues, revue
  calendrier-de-sortie.md       Steam Direct, revue, Coming Soon, date, bouton de sortie
  visibilite-et-wishlists.md    ce qui compte pour la visibilité, notifications de wishlists
  prix-et-reductions.md         devises, minimums, réduction de lancement, délais de 30 jours
  demo-playtest-next-fest.md    démo, Steam Playtest, clés, Next Fest (février 2027)
  acces-anticipe.md             règles, questionnaire, prix, sortie en 1.0
  steam-deck.md                 badges, critères Verified, notes Godot
  fonctionnalites-steamworks.md succès, Steam Cloud, overlay, notes Godot et GodotSteam
  apres-la-sortie.md            mises à jour, annonces, Update Visibility Rounds
  gabarits/plan-de-sortie.md    rétroplanning à copier dans le projet
  sources.md                    pages Steamworks citées
skills/godotsteam/
  SKILL.md                      règles d'usage, table de routage, règles à ne jamais oublier
  installation.md               extension ou éditeur précompilé, export, jeu sans Steam, erreurs
  initialisation.md             App ID, steamInitEx, rappels, mode d'emploi du gabarit
  gabarits/steamworks.gd        autoload Steamworks prêt à copier
  recettes/                     succès et stats, Steam Cloud, Steam Deck, présence et overlay,
                                classements, DLC, multijoueur
```

## Fiabilité et mise à jour

- Toutes les fiches ont été écrites le **04/11/2026** à partir des pages Steamworks lues directement, pas de guides tiers. Chaque fiche cite ses pages.
- Les fiches distinguent les **règles de Valve**, ses **conseils** et les **points de départ**.
- Valve change ses règles (tailles des capsules en août 2024, délai entre réductions passé de 28 à 30 jours en 2023, Steam Machine ajoutée aux critères Steam Deck). Le skill demande à l'agent de rouvrir la page source avant une décision qui engage, et de signaler tout écart.
- Pour mettre à jour une fiche : relire ses sources, corriger, changer la date de relevé dans son « En bref » et dans [SKILL.md](skills/boutique/SKILL.md).
- `steam:godotsteam` a été écrit le **04/11/2026** d'après la documentation de godotsteam.com (GodotSteam 4.23.2, SDK Steamworks 1.65) : tutoriels et référence des classes. Les signatures ont changé entre versions (SDK 1.61, GodotSteam 4.14, 4.17, 4.21) : les fiches le signalent. Pour relire cette documentation depuis une session cloud, autoriser aussi `godotsteam.com`.
- **L'autoload `gabarits/steamworks.gd` n'a pas été exécuté dans Godot** pendant l'écriture (pas de Godot dans l'environnement) : ses appels suivent la documentation, mais il faut le lancer une fois sans Steam et une fois avec avant de s'y fier.
- Pour lire la documentation Steamworks depuis une session cloud, ajouter `partner.steamgames.com` aux domaines autorisés de l'environnement.
