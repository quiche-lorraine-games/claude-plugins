# Steam Cloud et synchronisation dynamique

> **En bref** : faire suivre les sauvegardes d'un jeu Godot entre machines avec Steam Auto-Cloud (sans code), puis, si le jeu doit reprendre une partie après la mise en veille d'une Steam Deck, la synchronisation dynamique avec GodotSteam. Relevé le 04/11/2026 (GodotSteam 4.23.2). La configuration Auto-Cloud détaillée (racines, chemins de `user://`) est dans `steam:boutique`, fiche `fonctionnalites-steamworks.md`.

## 1. Auto-Cloud : la voie par défaut

Pour un jeu Godot qui sauvegarde dans `user://` avec `FileAccess`, **Auto-Cloud suffit** : aucun appel GodotSteam.
1. Fixe le dossier `user://` (*Project Settings* → *Application* → *Config* → `use_custom_user_dir` et `custom_user_dir_name`) avant la sortie.
2. Dans Steamworks, règle les quotas, puis les chemins (racine `WinAppDataRoaming`, sous-dossier `<custom_user_dir_name>/saves`, motif `*.save`, *Cross-Platform*, et *Root Overrides* pour Linux et macOS). Publie.
3. Garde les réglages graphiques **hors** du motif synchronisé.

Steam synchronise au lancement et à la fermeture du jeu.

## 2. Vérifier que le nuage est actif

```gdscript
var nuage: bool = Steam.isCloudEnabledForAccount() and Steam.isCloudEnabledForApp()
```

Le joueur peut désactiver Steam Cloud pour son compte ou pour ce jeu. Affiche-le dans le menu de sauvegarde si c'est utile.

## 3. Synchronisation dynamique (Steam Deck en veille)

Le problème : le joueur met la Deck en veille sans quitter le jeu, continue sur son PC, puis réveille la Deck. Sans synchronisation dynamique, la Deck garde l'ancienne partie en mémoire et l'écrase à la sauvegarde suivante.

Avec la synchronisation dynamique, Steam envoie les fichiers à la mise en veille, récupère ceux de l'autre machine au réveil, et prévient le jeu. À implémenter :

1. **Encadrer chaque écriture de sauvegarde** :

```gdscript
func sauvegarder() -> void:
    if Steamworks.is_steam_enabled():
        Steam.beginFileWriteBatch()
    # ... écriture habituelle avec FileAccess ...
    if Steamworks.is_steam_enabled():
        Steam.endFileWriteBatch()
```

2. **Réagir aux fichiers changés** :

```gdscript
func _ready() -> void:
    if Steamworks.is_steam_enabled():
        Steam.local_file_changed.connect(_on_local_file_changed)

func _on_local_file_changed() -> void:
    for i in Steam.getLocalFileChangeCount():
        var change: Dictionary = Steam.getLocalFileChange(i)  # {file, change_type, path_type}
        if change["path_type"] != Steam.FILE_PATH_TYPE_ABSOLUTE:
            continue  # Auto-Cloud : chemins absolus ; l'API Cloud utilise FILE_PATH_TYPE_API_FILENAME
        match change["change_type"]:
            Steam.LOCAL_FILE_CHANGE_FILE_UPDATED:
                pass  # le fichier sur disque est déjà à jour : le recharger au bon moment
            Steam.LOCAL_FILE_CHANGE_FILE_DELETED:
                pass  # mettre à jour la liste des sauvegardes
```

Recharger une partie à l'improviste peut casser la logique du jeu : diffère si le joueur est dans un menu, par exemple, et propose plutôt de reprendre la partie la plus récente.

3. **Sauvegarder souvent** : Steam **ne prévient pas** au moment de la mise en veille. Un jeu à sauvegarde automatique doit sauvegarder aux moments clés (fin de niveau) ou à intervalle régulier ; sauvegarder à la fermeture ne suffit pas, puisque la veille ne ferme pas le jeu.

4. **Activer** dans Steamworks : *Configure Cloud Saves* → *Dynamic Cloud Saves* → *Enable Steam Cloud sync on system suspend and resume*. Valve avertit qu'une implémentation incomplète peut corrompre ou perdre la progression : pour un jeu déjà sorti, teste en local d'abord (commandes de console dans la documentation Steamworks).

Le signal `Steam.app_resuming_from_suspend` (classe *Utils*) prévient aussi du réveil de l'appareil.

## Pièges

- Synchroniser le fichier de réglages : la résolution du PC appliquée à la Deck.
- Changer `custom_user_dir_name` après la sortie.
- Activer la synchronisation dynamique sans encadrer les écritures.
- Ne sauvegarder qu'à la fermeture du jeu.

## Checklist

- [ ] Dossier `user://` fixé, chemins Auto-Cloud publiés, réglages exclus
- [ ] Testé sur deux machines (sauvegarde sur l'une, reprise sur l'autre)
- [ ] Si synchronisation dynamique : écritures encadrées, `local_file_changed` géré, sauvegardes régulières, option activée et testée

## Sources

- [Tutorials - Dynamic Cloud Sync](https://godotsteam.com/tutorials/dynamic_cloud_sync/)
- Classe [Remote Storage](https://godotsteam.com/classes/remote_storage/)
- [Steam Cloud (Steamworks)](https://partner.steamgames.com/doc/features/cloud)
