# Fonctionnalités Steamworks dans un jeu Godot : succès, Steam Cloud, overlay

> **En bref** : ce qu'il faut configurer et coder pour les succès, les statistiques et Steam Cloud, et leurs limites ; comment déclarer ces fonctionnalités sans échouer à la revue ; notes pour un jeu Godot avec GodotSteam. Relevé le 04/11/2026 sur la documentation Steamworks.

## Quand consulter cette fiche

- Tu ajoutes des succès ou des statistiques.
- Tu veux que les sauvegardes suivent le joueur d'un PC à une Steam Deck.
- Tu coches les fonctionnalités dans l'onglet *Basic Info* de la page.
- Tu intègres Steamworks dans un projet Godot.

---

## 1. Ne déclarer que ce qui existe

La revue du build vérifie que **chaque fonctionnalité cochée** sur la page (succès, Steam Cloud, manette, systèmes d'exploitation…) est présente dans le build. Une fonctionnalité prévue se coche le jour où elle sort.

## 2. Succès et statistiques

### Règles et limites (Valve)

- Les succès et statistiques se définissent dans Steamworks (*App Admin*), pas dans le jeu.
- **100 succès au plus** tant que l'application n'a pas été validée (*vetted*), puis 5 000 ; 40 ensembles (*sets*) au plus, base comprise. Les succès archivés comptent.
- **Icônes** : carrées, de préférence **256 × 256 en PNG** (64 × 64 au minimum ; JPG accepté). Valve conseille une icône obtenue en couleurs et une non obtenue en gris ; l'éditeur sait générer la grise.
- Noms, descriptions et icônes **adaptés à tous les âges**.
- Pour passer la checklist : cocher *Steam Achievements* dans *Basic Info*, et donner à chaque succès un nom dans chaque langue configurée et une icône.
- Un succès peut être marqué *Spoiler* (détails cachés jusqu'à l'obtention) et avoir une statistique de progression.
- Statistiques : types `INT`, `FLOAT`, `AVGRATE` (moyenne glissante), avec bornes, « croissante seulement » et variation maximale.

### Comportement à coder

- Après l'initialisation de l'API, lire statistiques et succès pour initialiser l'état du jeu.
- `SetStat` à chaque changement (peu coûteux, en mémoire), `StoreStats` aux moments opportuns (point de contrôle, changement de niveau). Débloquer : `SetAchievement`, puis `StoreStats` aussitôt.
- `IndicateAchievementProgress` pour afficher une progression (par exemple à mi-chemin).
- **Ne garde pas de copie locale des succès** : Steam en tient un cache hors ligne et fusionne entre machines ; une copie à soi entre en conflit et donne l'impression d'une progression perdue.
- Les statistiques dépendantes se calculent pour rester cohérentes (`Parties = Victoires + Défaites`, plutôt que trois compteurs).
- **Dans une démo, désactiver les succès** et les accorder dans le jeu complet à partir de la sauvegarde partagée.
- Pour tester : console Steam (`steam.exe -console`), `achievement_clear <appid> <nom>` et `reset_all_stats <appid>`. Avant la sortie, les succès ne s'affichent pas dans la communauté : le jeu doit pouvoir lister ceux qu'il a débloqués.

## 3. Steam Cloud

### Règles et fonctionnement (Valve)

- Deux façons : l'**API** (`ISteamRemoteStorage`, contrôle fin) ou **Auto-Cloud**, sans code : on déclare des chemins, Steam synchronise au lancement et à la fermeture.
- D'abord régler le **quota en octets et en nombre de fichiers par joueur** (*Steam Cloud Settings*), puis enregistrer **et publier**.
- Pour un jeu déjà sorti : le mode « développeurs seulement » permet de tester sans toucher les joueurs.
- Limites : 100 Mo au plus par écriture par l'API ; au-delà de 256 Mo, le stockage peut être moins bien placé géographiquement. Préfère des fichiers petits, séparés selon leur fréquence de changement.
- **Ne synchronise pas les réglages propres à une machine** (vidéo, résolution).
- Le chemin de sauvegarde doit être propre au compte Steam si plusieurs joueurs partagent un PC (variables `{64BitSteamID}` ou `{Steam3AccountID}` dans le sous-dossier Auto-Cloud).
- Laisse la restriction de système sur **Cross-Platform** (par défaut), même pour un seul système : un fichier lié à un système ne se synchronisera jamais avec les autres.
- **Partage avec la démo** : champ *Shared cloud APP ID* (inutile tant que le jeu principal n'est pas sorti).
- **Synchronisation dynamique** (*Dynamic Cloud Sync*) : à la mise en veille d'une Steam Deck, Steam envoie les fichiers ; au réveil, il récupère ceux d'un autre appareil et prévient le jeu (`RemoteStorageLocalFileChange_t`). À activer seulement si le jeu sait recharger sa progression à chaud.
- Fichier `steam_autocloud.vdf` créé par Steam dans chaque dossier synchronisé : à ignorer.
- Débogage : `logs/cloud_log.txt` dans le dossier de Steam ; publier puis attendre jusqu'à 10 minutes ou redémarrer Steam.

### Racines Auto-Cloud utiles

| Racine | Système | Chemin |
|---|---|---|
| `WinAppDataRoaming` | Windows | `%USERPROFILE%\AppData\Roaming\` |
| `LinuxXdgDataHome` | Linux | `$XDG_DATA_HOME/` (en général `~/.local/share/`) |
| `MacAppSupport` | macOS | `~/Library/Application Support/` |
| `SteamCloudDocuments` | tous | chemin propre à chaque système |

Pour un même jeu sur plusieurs systèmes : une racine principale en *Cross-Platform*, puis des *Root Overrides* (nouvelle racine et sous-dossier) pour les autres systèmes.

## 4. Pour un jeu Godot

### Intégration

Le code (autoload prêt à copier, recettes par fonctionnalité) est dans le skill `steam:godotsteam` ; cette section en résume l'essentiel.


- **GodotSteam** est l'extension la plus utilisée pour appeler Steamworks depuis GDScript (module ou GDExtension). Les fonctions Steamworks y gardent leur nom en *camelCase* sur le singleton `Steam`.
- **Initialisation** : `Steam.steamInitEx(app_id, embed_callbacks)` dans un autoload, au démarrage. Elle renvoie un dictionnaire `{status, verbal}` : `status` vaut `STEAM_API_INIT_RESULT_OK` en cas de succès, sinon `verbal` explique l'échec. L'App ID et l'option *Embed Callbacks* peuvent aussi se régler dans *Project Settings* → *Steam* → *Initialization* ; on appelle alors `Steam.steamInitEx()` sans argument.
- **Rappels** : sans *Embed Callbacks*, appeler `Steam.run_callbacks()` dans `_process`, sinon les résultats asynchrones n'arrivent jamais. GodotSteam signale que les rappels intégrés étaient cassés dans ses versions 3.29 et 4.14 : sur ces versions, appeler `run_callbacks()` soi-même.
- **App ID en développement** : passé à `steamInitEx` (GodotSteam règle alors les variables d'environnement `SteamAppId` et `SteamGameId`), ou par un fichier `steam_appid.txt` à côté de l'exécutable. **Ne livre pas `steam_appid.txt` dans le build envoyé à Steam** (Valve le déconseille, et il fausse `restartAppIfNecessary`).
- **Fichiers à livrer** : la bibliothèque de GodotSteam (`godotsteam.dll`, `libgodotsteam.so` ou `libgodotsteam.dylib`) et celle de Steam (`steam_api64.dll` sur Windows 64 bits, `libsteam_api.so` sur Linux, prise dans le dossier de la bonne architecture), à côté de l'exécutable.
- **Succès** : `Steam.setAchievement("NOM_API")`, puis `Steam.storeStats()` ; sans `storeStats()`, le succès est enregistré mais la notification ne s'affiche pas. Progression : `Steam.indicateAchievementProgress(...)`.
- **Langue** : `Steam.getCurrentGameLanguage()`. **Overlay vers la page du jeu** : `Steam.activateGameOverlayToStore(app_id)`.
- Teste sur un build lancé par Steam (branche bêta protégée par mot de passe), pas seulement depuis l'éditeur.

### Sauvegardes Godot et Auto-Cloud

Par défaut, `user://` vaut :

| Système | Chemin de `user://` |
|---|---|
| Windows | `%APPDATA%\Godot\app_userdata\<Nom du projet>\` |
| Linux | `~/.local/share/godot/app_userdata/<Nom du projet>/` |
| macOS | `~/Library/Application Support/Godot/app_userdata/<Nom du projet>/` |

Avec *Project Settings* → *Application* → *Config* → `use_custom_user_dir` activé, le dossier est créé directement sous `%APPDATA%`, `~/.local/share` ou `~/Library/Application Support`. Son nom vient du nom du projet, ou de `custom_user_dir_name` s'il est réglé (il peut contenir un séparateur, par exemple `Studio/Jeu`). Règle `custom_user_dir_name` : le chemin ne dépend plus du nom du projet, qui peut changer. Choisis-le avant la sortie et ne le change plus.

Exemple Auto-Cloud pour des sauvegardes `user://saves/*.save`, avec `use_custom_user_dir` activé et `custom_user_dir_name = MonJeu` :
- racine `WinAppDataRoaming`, sous-dossier `MonJeu/saves`, motif `*.save`, *Cross-Platform* ;
- *Root Override* Linux : nouvelle racine `LinuxXdgDataHome` ;
- *Root Override* macOS : nouvelle racine `MacAppSupport`.

Garde les réglages (`user://settings.cfg`) **hors** du motif synchronisé.

### Langue

L'API `GetCurrentGameLanguage` donne la langue choisie par le joueur dans Steam : utilise-la comme langue par défaut au premier lancement (`TranslationServer.set_locale`), en gardant le choix du joueur dans les options.

---

## Pièges

- Cocher Steam Cloud ou les succès sur la page avant qu'ils marchent : refus à la revue.
- Oublier de publier les réglages Steam Cloud ou de succès après les avoir enregistrés.
- Plus de 100 succès prévus pour la sortie sans validation préalable de l'application.
- Synchroniser le fichier de réglages : une résolution de PC appliquée à la Deck.
- Changer le nom du projet Godot, ou `custom_user_dir_name`, après la sortie : le dossier `user://` change, et les sauvegardes et la synchronisation ne suivent plus.
- Livrer `steam_appid.txt`.
- Succès débloqués dans la démo.

## Checklist

- [ ] Fonctionnalités cochées sur la page = fonctionnalités présentes dans le build
- [ ] Succès définis dans Steamworks, chacun avec nom traduit et icône 256 × 256, publiés
- [ ] `StoreStats` appelé après chaque déblocage
- [ ] Quotas Steam Cloud réglés, chemins Auto-Cloud déclarés en *Cross-Platform* avec les *Root Overrides*, publiés
- [ ] Réglages graphiques exclus de la synchronisation
- [ ] Dossier `user://` stable (`use_custom_user_dir`) fixé avant la sortie
- [ ] `steamInitEx` vérifié au démarrage, rappels activés (*Embed Callbacks* ou `run_callbacks()` à chaque image)
- [ ] Bibliothèques GodotSteam et Steam API livrées avec l'exécutable
- [ ] Pas de `steam_appid.txt` dans le build envoyé
- [ ] Testé sur un build lancé par Steam, sur deux machines pour Steam Cloud

## Voir aussi

- [steam-deck.md](steam-deck.md) : Steam Input, clavier virtuel, sauvegardes dans le nuage.
- [demo-playtest-next-fest.md](demo-playtest-next-fest.md) : succès et sauvegarde partagée de la démo.
- [page-boutique.md](page-boutique.md) : ce que vérifie la revue.

## Sources

- [Stats and Achievements](https://partner.steamgames.com/doc/features/achievements)
- [Achievements Guide](https://partner.steamgames.com/doc/features/achievements/ach_guide) (limites, icônes)
- [Steam Cloud](https://partner.steamgames.com/doc/features/cloud)
- [Localization and Languages](https://partner.steamgames.com/doc/store/localization)
- [Review Process](https://partner.steamgames.com/doc/store/review_process)
- [Godot, File paths in Godot projects](https://docs.godotengine.org/en/stable/tutorials/io/data_paths.html) (chemins de `user://`)
- GodotSteam : [Initializing](https://godotsteam.com/tutorials/initializing/), [Exporting and Shipping](https://godotsteam.com/tutorials/exporting_shipping/), [Stats and Achievements](https://godotsteam.com/tutorials/stats_achievements/), classes [Main](https://godotsteam.com/classes/main/), [User Stats](https://godotsteam.com/classes/user_stats/), [Apps](https://godotsteam.com/classes/apps/), [Friends](https://godotsteam.com/classes/friends/)
