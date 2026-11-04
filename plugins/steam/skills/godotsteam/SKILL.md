---
name: godotsteam
description: Intégrer Steamworks dans un jeu Godot 4 avec l'extension GodotSteam, en français, d'après sa documentation officielle. À charger quand on installe ou met à jour GodotSteam (extension GDExtension de l'Asset Library ou éditeur précompilé), qu'on écrit l'autoload d'initialisation (steamInitEx, App ID, rappels), ou qu'on ajoute au jeu des succès et statistiques, Steam Cloud et sa synchronisation dynamique, le clavier virtuel et les réglages par défaut pour Steam Deck, la présence enrichie (rich presence), l'overlay (page boutique, invitations, pages web), l'enregistrement de jeu (timeline), les classements, les DLC, ou le multijoueur par lobbies Steam et SteamMultiplayerPeer. Couvre aussi l'export (modèles, bibliothèques à livrer, steam_appid.txt), le jeu sans Steam (itch.io, consoles) et les erreurs courantes (Parse Error sur Steam, échec d'initialisation, overlay absent depuis l'éditeur, Steam Input qui capte la manette). Pour la page boutique, le calendrier et les règles de Valve, voir le skill steam:boutique.
---

# Intégrer Steamworks dans un jeu Godot avec GodotSteam

GodotSteam expose l'API Steamworks à GDScript par un singleton `Steam`. Les fonctions gardent le nom Steamworks en *camelCase* (`ISteamUserStats::SetAchievement` → `Steam.setAchievement()`), et les rappels Steamworks deviennent des **signaux** du singleton (`Steam.lobby_joined`, `Steam.leaderboard_find_result`…). Les fichiers de ce skill sont dans le même dossier que ce fichier.

Relevé le 04/11/2026 sur [godotsteam.com](https://godotsteam.com/) : GodotSteam **4.23.2**, Steamworks SDK **1.65**, pour Godot 4.x. Les signatures citées viennent de sa documentation ; plusieurs ont changé entre versions (voir [installation.md](installation.md)). Avant d'écrire du code pour une fonction qui n'est pas dans ces fiches, lis sa page dans la [référence des classes](https://godotsteam.com/classes/main/).

## Comment s'en servir

1. **Le projet prime.** Ses autoloads, sa structure de scènes, son système de sauvegarde et ses conventions l'emportent sur les exemples d'ici.
2. **Une seule porte d'entrée.** Tout appel à Steam passe par un autoload (ex. `Steamworks`), jamais par `Steam.` éparpillé dans les scènes. Pars du gabarit [gabarits/steamworks.gd](gabarits/steamworks.gd).
3. **Le jeu marche sans Steam.** Si Steam est absent ou n'a pas démarré, le jeu se lance quand même et les fonctions Steam ne font rien. Indispensable pour tester depuis l'éditeur sans client Steam, et pour une version itch.io ou console.
4. **Rien ne se configure dans le jeu.** Succès, statistiques, classements, Steam Cloud, présence enrichie et DLC se déclarent d'abord dans Steamworks, puis **se publient**. Un succès non publié échoue en silence. Tu n'as pas accès à Steamworks : prépare la liste exacte à saisir (noms d'API, types, textes) et donne-la à l'humain.
5. **Teste depuis Steam.** L'éditeur suffit pour la plupart des appels (avec l'App ID 480 ou celui du jeu), mais l'overlay, les invitations, le lancement par `+connect_lobby` et Steam Cloud se vérifient sur un build exporté, lancé par le client Steam.
6. **Ne déclare que ce qui marche.** Une fonctionnalité cochée sur la page boutique doit être dans le build envoyé à la revue de Valve (voir `steam:boutique`, fiche `page-boutique.md`).

## Table de routage

| Tu travailles sur… | Lis d'abord |
|---|---|
| Installer GodotSteam, choisir extension ou éditeur précompilé, exporter, livrer | [installation.md](installation.md) |
| L'autoload : initialisation, App ID, rappels, jeu sans Steam | [initialisation.md](initialisation.md) et [gabarits/steamworks.gd](gabarits/steamworks.gd) |
| Succès et statistiques | [recettes/succes-et-stats.md](recettes/succes-et-stats.md) |
| Sauvegardes Steam Cloud, synchronisation à la mise en veille de la Deck | [recettes/steam-cloud.md](recettes/steam-cloud.md) |
| Steam Deck : clavier virtuel, réglages par défaut, mise en veille, overlay | [recettes/steam-deck.md](recettes/steam-deck.md) |
| Présence enrichie, overlay, avatars, enregistrement de jeu (timeline) | [recettes/presence-et-overlay.md](recettes/presence-et-overlay.md) |
| Classements | [recettes/classements.md](recettes/classements.md) |
| DLC | [recettes/dlc.md](recettes/dlc.md) |
| Multijoueur : lobbies, invitations, SteamMultiplayerPeer | [recettes/multijoueur.md](recettes/multijoueur.md) |
| Une erreur | [installation.md](installation.md), section « Erreurs courantes » |

## Règles à ne jamais oublier

- Initialise avec `Steam.steamInitEx()` et **vérifie `status`** : `0` (`Steam.STEAM_API_INIT_RESULT_OK`) seulement en cas de succès.
- Les rappels n'arrivent que si `Steam.run_callbacks()` tourne à chaque image (ou *Embed Callbacks* activé), dans un nœud **qui n'est jamais mis en pause**.
- Depuis le SDK 1.61, Steam synchronise seul succès et statistiques au démarrage : plus de `requestCurrentStats()` ni de signal `current_stats_received`.
- `Steam.setAchievement()` puis `Steam.storeStats()`, sinon pas de notification.
- Ne livre jamais `steam_appid.txt`. Livre les bibliothèques de GodotSteam et de Steam avec l'exécutable.
- Ne mélange pas l'éditeur précompilé GodotSteam et l'extension de l'Asset Library dans un même projet.
- L'App ID **480** (SpaceWar, l'exemple de Valve) sert aux essais ; les succès, classements et DLC réels demandent l'App ID du jeu.
