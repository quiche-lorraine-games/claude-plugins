# Initialisation : l'autoload Steamworks

> **En bref** : comment démarrer Steam dans le jeu, fournir l'App ID, recevoir les rappels, réagir à un échec et rester jouable sans Steam ; mode d'emploi du gabarit [gabarits/steamworks.gd](gabarits/steamworks.gd). Relevé le 04/11/2026 sur godotsteam.com (GodotSteam 4.23.2).

## Quand consulter cette fiche

- Tu ajoutes Steam à un projet.
- Les signaux de Steam n'arrivent jamais.
- Le jeu doit aussi sortir ailleurs que sur Steam.

---

## 1. Fournir l'App ID

Lancé par le client Steam, le jeu connaît son App ID. Pendant le développement, il faut le fournir, de l'une de ces façons (par ordre de préférence de GodotSteam) :
1. *Project Settings* → *Steam* → *Initialization* → *App ID* (GodotSteam 4.14 et plus) ;
2. premier argument de `Steam.steamInitEx(app_id, embed_callbacks)` ;
3. variables d'environnement `SteamAppId` et `SteamGameId`, réglées dans `_init()` du premier script (`OS.set_environment`) ;
4. un fichier `steam_appid.txt` contenant le seul App ID, à côté de l'éditeur (parfois à la racine du projet avec l'extension) : déconseillé, facile à oublier dans un build.

Sans App ID propre, `480` (SpaceWar, l'exemple de Valve) permet d'essayer. Ses lobbies sont noyés parmi ceux de tous les développeurs, et il ne permet ni l'inventaire, ni le Workshop, ni rien de ce qui se règle dans Steamworks.

## 2. Initialiser

```gdscript
var result: Dictionary = Steam.steamInitEx()
if result["status"] != Steam.STEAM_API_INIT_RESULT_OK:
    push_warning("Steam non initialisé : %s" % result)
```

`steamInitEx()` renvoie `{status, verbal}`. Codes de `status` : `0` succès, `1` autre échec, `2` Steam injoignable (client fermé, le plus souvent), `3` client Steam pas à jour. `verbal` donne le message en clair. `steamInit()` ne renvoie qu'un booléen et ne remplit pas `get_steam_init_result()` : préfère `steamInitEx()`.

Les causes d'échec les plus fréquentes : bibliothèque Steam absente, App ID non fourni.

**Depuis le SDK 1.61**, Steam synchronise lui-même succès et statistiques au démarrage : plus de premier argument booléen pour les statistiques, plus de `requestCurrentStats()`, plus de signal `current_stats_received`. Un vieux tutoriel qui les utilise date d'avant GodotSteam 4.14.

## 3. Recevoir les rappels

Les résultats asynchrones (lobby créé, classement trouvé, clavier fermé…) arrivent comme **signaux** du singleton, mais seulement si `Steam.run_callbacks()` est appelé :
- soit à chaque image, dans `_process` de l'autoload ;
- soit par *Embed Callbacks* (réglage du projet, ou `true` en second argument de `steamInitEx`). Cassé en GodotSteam 4.14.

**Le nœud qui appelle `run_callbacks()` ne doit jamais être en pause** : sinon les rappels cessent. Avec un autoload, mets `process_mode = Node.PROCESS_MODE_ALWAYS`.

Les signaux se connectent comme les autres : `Steam.lobby_joined.connect(_on_lobby_joined)`. Leurs arguments sont, dans l'ordre, les champs listés dans la section *Signals* de chaque classe de la documentation.

## 4. Échec et absence de Steam

Deux choix, selon le jeu :
- **désactiver les fonctions Steam** et continuer (recommandé : le jeu reste testable sans client, et la même base sert à itch.io ou aux consoles) ;
- ou **quitter** avec un message, si le jeu n'a pas de sens sans Steam (multijoueur Steam uniquement). Ne quitte jamais sans message.

`Steam.isSubscribed()` dit si le compte possède le jeu. Valve et GodotSteam mettent en garde : quitter sur ce seul test gêne le partage familial, les week-ends gratuits et les autres essais.

`Steam.restartAppIfNecessary(app_id)` relance le jeu par Steam s'il a été lancé hors de Steam (renvoie `true` : quitter aussitôt). Elle renvoie toujours `false` si `steam_appid.txt` est présent, et peut gêner l'initialisation automatique.

## 5. Le gabarit

[gabarits/steamworks.gd](gabarits/steamworks.gd) est un autoload prêt à copier :
- il passe par `Engine.get_singleton("Steam")`, donc il se charge même sans GodotSteam ;
- il appelle `steamInitEx()` puis `run_callbacks()` à chaque image, en `PROCESS_MODE_ALWAYS` (laisser *Embed Callbacks* et l'initialisation automatique désactivés) ;
- il expose `is_steam_enabled()`, les succès et statistiques, la présence enrichie, l'overlay, le clavier virtuel, le réglage conseillé pour le matériel, la langue et les DLC, et ne fait rien sans Steam ;
- il réémet les signaux utiles (`steam_ready`, `overlay_toggled`, `keyboard_submitted`).

Pour l'utiliser : copie-le (ex. `res://autoloads/steamworks.gd`), déclare-le en autoload sous le nom `Steamworks`, règle l'App ID, puis appelle `Steamworks.unlock_achievement("FIRST_WIN")` depuis le jeu. Ajoute les fonctions propres au jeu (classements, lobbies) dans le même autoload ou dans des autoloads voisins qui passent par `Steamworks.steam`.

Le gabarit n'a pas été exécuté dans Godot pendant l'écriture de ce skill : lance le projet une fois sans Steam et une fois avec, et corrige ce que Godot signale.

Autres infos disponibles après l'initialisation : `Steam.getSteamID()`, `Steam.getPersonaName()`, `Steam.loggedOn()`, `Steam.getAppBuildId()`, `Steam.getAvailableGameLanguages()`, `Steam.getLaunchCommandLine()`, `Steam.isSteamRunningInVR()`.

---

## Checklist

- [ ] App ID fourni pour le développement (réglage du projet), pas de `steam_appid.txt` livré
- [ ] `steamInitEx()` testé, `status` journalisé en cas d'échec
- [ ] `run_callbacks()` à chaque image dans un nœud jamais en pause, ou *Embed Callbacks* (hors 4.14)
- [ ] Aucun appel aux fonctions supprimées par le SDK 1.61 (`requestCurrentStats`, `current_stats_received`)
- [ ] Jeu lancé sans client Steam : pas de plantage, fonctions Steam inactives
- [ ] Tout le jeu passe par l'autoload, jamais par `Steam.` dans les scènes

## Sources

- [Tutorials - Initializing Steam](https://godotsteam.com/tutorials/initializing/)
- [Tutorials - Removing Steam Easily](https://godotsteam.com/tutorials/remove_steam/)
- Classe [Main](https://godotsteam.com/classes/main/) (`steamInitEx`, `run_callbacks`, `restartAppIfNecessary`, `get_steam_init_result`)
