# Installer, exporter et dépanner GodotSteam

> **En bref** : choisir entre l'extension GDExtension et l'éditeur précompilé, l'installer, régler le projet, exporter et livrer les bonnes bibliothèques, enlever Steam pour une autre plateforme, et corriger les erreurs courantes. Relevé le 04/11/2026 sur godotsteam.com (GodotSteam 4.23.2, SDK 1.65).

## Quand consulter cette fiche

- Tu ajoutes GodotSteam à un projet, ou tu le mets à jour.
- Tu prépares un export pour Steam.
- Le jeu affiche `Parse Error: The identifier "Steam" isn't declared in the current scope`, ou Steam ne s'initialise pas.

---

## 1. Extension ou éditeur précompilé

| | Extension GDExtension | Éditeur et modèles précompilés |
|---|---|---|
| Où la trouver | Asset Library de Godot (dans l'éditeur), ou téléchargement sur godotsteam.com | téléchargement sur godotsteam.com |
| Éditeur | Godot standard | éditeur GodotSteam |
| Modèles d'export | modèles Godot standard | **modèles GodotSteam obligatoires** |
| Fichiers à livrer en plus | bibliothèque GodotSteam **et** bibliothèque Steam | bibliothèque Steam |
| Documentation dans l'éditeur | oui | oui |
| Version Godot | toute version 4.x compatible avec l'extension | celle du paquet |

Pour Godot 4, la documentation dit les deux à peu près équivalentes : même code, singleton `Steam` global dans les deux cas. La plupart des utilisateurs prennent l'extension, plus simple à installer. Le mainteneur conseille l'éditeur précompilé, plus éprouvé. Le débogage de l'extension est parfois un peu plus compliqué.

Choix par défaut : l'**extension**, sauf si le projet utilise déjà l'éditeur précompilé, ou s'il a besoin d'un moteur recompilé (par exemple en double précision : l'extension n'est pas compilée pour, et fait planter un éditeur double précision).

**Ne mélange jamais les deux** dans un projet : appels en double et erreurs étranges. Pour passer de l'extension à l'éditeur précompilé, supprime le dossier `addons/godotsteam/` et la ligne de l'extension dans `.godot/extension_list.cfg`. Dans l'autre sens, supprime la bibliothèque Steam (`steam_api64.dll`, `libsteam_api.so`, `libsteam_api.dylib`) posée à la racine du projet ou à côté de l'éditeur.

Il existe aussi une version **GodotSteam Server** (serveurs maîtres et dédiés, 4.12.1 au 04/11/2026) et des liaisons C# communautaires. GodotSteam n'a pas de version .NET officielle.

## 2. Installer l'extension

1. Dans l'éditeur : onglet *AssetLib*, chercher « GodotSteam », télécharger, installer. L'extension arrive dans `addons/godotsteam/`, avec un dossier par plateforme (`win64/`, `linux64/`, `osx/`) qui contient la bibliothèque GodotSteam et celle de Steam.
2. Une GDExtension n'a pas à être activée dans *Plugins* : elle est chargée dès que le dossier est là. Redémarre l'éditeur.
3. Vérifie : `Steam` est reconnu dans un script, et sa documentation s'ouvre dans l'aide de l'éditeur.
4. Commite `addons/godotsteam/` (sauf contre-indication du projet) pour que tout le monde ait la même version.

## 3. Régler le projet

*Project Settings* → *Steam* → *Initialization* (à partir de GodotSteam 4.14) :
- **App ID** : celui du jeu, ou `480` pour essayer. GodotSteam en déduit les variables d'environnement `SteamAppId` et `SteamGameId`.
- ***Embed Callbacks*** : GodotSteam appelle lui-même `run_callbacks()` à chaque image. Il était cassé en 4.14 : avec cette version, appelle `run_callbacks()` toi-même. Il faisait aussi planter l'éditeur quand il était combiné à l'initialisation automatique avant la 4.16.
- **Initialisation automatique** : Steam démarre le plus tôt possible. Elle a été ajoutée pour aider l'overlay à s'afficher depuis l'éditeur, sans garantie, et peut gêner `restartAppIfNecessary()`. Son résultat se lit avec `Steam.get_steam_init_result()`.

Recommandation : App ID dans les réglages, initialisation par l'autoload (voir [initialisation.md](initialisation.md)), *Embed Callbacks* activé, et version de GodotSteam notée dans le README du projet.

Active aussi les journaux : *Project Settings* → *Debug* → *File Logging* → *Enable File Logging*. Ils sont écrits dans `user://logs/`.

## 4. Exporter et livrer

- **Extension** : modèles d'export Godot standard. L'export copie la bibliothèque GodotSteam (`libgodotsteam…dll`, `.so`, `.dylib`) ; vérifie qu'elle est à côté de l'exécutable, avec celle de Steam.
- **Éditeur précompilé** : renseigne les modèles GodotSteam dans *Custom Template* (*Release*, et *Debug* si besoin). Avec un modèle standard, le jeu plante sur `Parse Error: The identifier "Steam" isn't declared`.
- **Bibliothèque Steam** : `steam_api64.dll` pour Windows 64 bits (`steam_api.dll` en 32 bits), `libsteam_api.so` pour Linux (prise dans le dossier de la bonne architecture : Valve donne le même nom aux versions 32 et 64 bits), `libsteam_api.dylib` pour macOS.
- **`steam_appid.txt`** : jamais dans le build envoyé. Valve le déconseille, et il fausse `restartAppIfNecessary()`.
- **macOS** : signature et notarisation ont des étapes en plus ; voir le tutoriel *Mac Export* de GodotSteam.
- **Dépôts Steam** : un dépôt par plateforme (et un dépôt commun éventuel), à ajouter aux paquets. L'envoi se fait par SteamPipe (`steamcmd`), hors de ce skill.

## 5. Jeu sans Steam (itch.io, consoles, éditeur)

GodotSteam conseille de garder une seule base de code :
- dans l'autoload, tester `Engine.has_singleton("Steam")` et passer par `Engine.get_singleton("Steam")` plutôt que par l'identifiant `Steam`. Le script se charge alors même sans GodotSteam (export avec des modèles Godot standard) ;
- garder une fonction `is_steam_enabled()` que tout le jeu consulte avant un appel Steam ;
- avec l'extension, on peut ne pas exporter ses bibliothèques pour une plateforme sans Steam ; avec l'éditeur précompilé, la bibliothèque Steam reste nécessaire ;
- avec l'extension, des messages d'erreur sans gravité apparaissent dans les journaux si `.godot/extension_list.cfg` la référence encore.

Le gabarit [gabarits/steamworks.gd](gabarits/steamworks.gd) suit ce modèle.

## 6. Erreurs courantes

| Symptôme | Causes connues |
|---|---|
| `Parse Error: The identifier "Steam" isn't declared` | éditeur standard sans l'extension ; modèle d'export standard avec l'éditeur précompilé ; GodotSteam absent de la compilation ; fichiers de l'extension pas à jour avec le `.gdextension` |
| `status` différent de 0 à l'initialisation | 1 : autre échec ; 2 : impossible de joindre Steam (client fermé) ; 3 : client Steam pas à jour. Le plus souvent : bibliothèque Steam absente, ou App ID non fourni |
| `ConnectToGlobalUser failed` | Steam n'est pas lancé, ou le compte connecté n'a pas le jeu dans sa bibliothèque |
| Erreur 79 à l'initialisation | souvent des dépôts ou paquets mal configurés dans Steamworks |
| Le jeu n'apparaît pas dans la bibliothèque Steam du développeur | le paquet *Developer Comp* manque : à ajouter dans *Users & Permissions* de Steamworks |
| Succès qui ne se débloquent pas | succès non publiés dans Steamworks |
| Classement introuvable | classement non publié ; tiret dans le nom (préférer `_`) |
| Pas d'overlay depuis l'éditeur | connu depuis Vulkan, sans solution sûre (mode *Compatibility*, pilote, initialisation automatique aident parfois). L'overlay marche sur un export lancé par Steam |
| Manette qui ne répond plus | Steam Input capte les entrées : si le jeu n'utilise pas la classe *Input* de GodotSteam, désactiver Steam Input dans les propriétés du jeu (ou régler les paramètres Steam Input du jeu dans Steamworks) |
| Saccades en *Forward+* avec Steam initialisé | signalé avec certains pilotes NVIDIA ; disparaît en *Compatibility* |
| `steam_appid.txt` ignoré sous Windows | fichier nommé `steam_appid.txt.txt` (extensions masquées) |
| Steam installe le dépôt Windows sur Linux | bug rare : forcer puis retirer un outil de compatibilité dans les propriétés du jeu |

---

## Checklist

- [ ] Une seule forme de GodotSteam dans le projet (extension ou éditeur précompilé), version notée
- [ ] App ID réglé dans *Project Settings* → *Steam* → *Initialization*
- [ ] Journaux de fichiers activés
- [ ] Export : bons modèles, bibliothèques GodotSteam et Steam à côté de l'exécutable, pas de `steam_appid.txt`
- [ ] Le jeu démarre sans Steam (client fermé) sans planter
- [ ] Build exporté testé depuis le client Steam (overlay, succès)

## Sources

- [Getting Started](https://godotsteam.com/getting_started/introduction/)
- [What Are You Actually Making?](https://godotsteam.com/getting_started/what_are_you_making/) (versions)
- [Tutorials - Initializing Steam](https://godotsteam.com/tutorials/initializing/)
- [Tutorials - Exporting and Shipping](https://godotsteam.com/tutorials/exporting_shipping/)
- [Tutorials - Removing Steam Easily](https://godotsteam.com/tutorials/remove_steam/)
- [Common Issues](https://godotsteam.com/issues/common_issues/)
- [How To Compile GDExtension](https://godotsteam.com/howto/gdextension/) (structure de `addons/godotsteam/`)
