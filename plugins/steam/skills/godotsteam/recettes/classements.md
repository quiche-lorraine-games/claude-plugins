# Classements

> **En bref** : trouver un classement, envoyer un score, télécharger les scores (mondial, autour du joueur, amis) et les afficher avec avatars, avec GodotSteam. Relevé le 04/11/2026 (GodotSteam 4.23.2).

## 1. Dans Steamworks d'abord

Crée le classement (*Stats & Achievements* → *Leaderboards*) : nom d'API, tri (croissant ou décroissant), type d'affichage (nombre, secondes, millisecondes). **Publie.** Évite les tirets dans le nom : `meilleur_score`, pas `meilleur-score` (signalé par GodotSteam).

## 2. Trouver le classement

Tout passe par un *handle* (identifiant numérique) obtenu de façon asynchrone :

```gdscript
var handles: Dictionary = {"meilleur_score": 0, "temps_niveau_1": 0}

func _ready() -> void:
    Steam.leaderboard_find_result.connect(_on_leaderboard_find_result)
    for nom in handles:
        Steam.findLeaderboard(nom)
        await Steam.leaderboard_find_result

func _on_leaderboard_find_result(handle: int, trouve: int) -> void:
    if trouve != 1:
        return
    handles[Steam.getLeaderboardName(handle)] = handle
```

- `getLeaderboardName(handle)` dit à quel classement correspond la réponse.
- `findOrCreateLeaderboard()` crée le classement s'il n'existe pas : ne lui passe jamais `LEADERBOARD_SORT_METHOD_NONE` ni `LEADERBOARD_DISPLAY_TYPE_NONE`.
- GodotSteam garde aussi le dernier handle dans `Steam.leaderboard_handle`.

## 3. Envoyer un score

```gdscript
Steam.leaderboard_score_uploaded.connect(_on_score_envoye)
Steam.uploadLeaderboardScore(score, true, PackedInt32Array(), handles["meilleur_score"])

func _on_score_envoye(succes: int, handle: int, resultat: Dictionary) -> void:
    if succes == 1 and resultat["score_changed"] == 1:
        print("Nouveau rang : %s (avant : %s)" % [resultat["new_rank"], resultat["prev_rank"]])
```

- Deuxième argument (`keep_best`) : `true` garde le meilleur des deux scores.
- **Limite de Valve : 10 envois par 10 minutes, et un seul envoi en cours à la fois.** Envoie en fin de partie, pas à chaque point.
- Un temps en millisecondes s'envoie en entier (`int(secondes * 1000)`).
- Détails facultatifs : un `PackedInt32Array` (256 entiers au plus par défaut, réglable par `set_leaderboard_details_max()`), par exemple `var_to_bytes(details).to_int32_array()`, à relire avec `bytes_to_var()`.

## 4. Télécharger les scores

```gdscript
Steam.leaderboard_scores_downloaded.connect(_on_scores_recus)
Steam.downloadLeaderboardEntries(-4, 5, Steam.LEADERBOARD_DATA_REQUEST_GLOBAL_AROUND_USER, handle)

func _on_scores_recus(message: String, handle: int, entrees: Array) -> void:
    for e in entrees:  # {score, steam_id, global_rank, ugc_handle, details}
        Steam.getPlayerAvatar(e["steam_id"])
        var nom: String = Steam.getFriendPersonaName(e["steam_id"])
```

| Type de requête | Effet |
|---|---|
| `LEADERBOARD_DATA_REQUEST_GLOBAL` | rangs de `debut` à `fin` |
| `LEADERBOARD_DATA_REQUEST_GLOBAL_AROUND_USER` | autour du joueur (début négatif pour les rangs au-dessus) |
| `LEADERBOARD_DATA_REQUEST_FRIENDS` | les amis du joueur (début et fin ignorés) |
| `LEADERBOARD_DATA_REQUEST_USERS` | interne à Steam, ne pas utiliser |

Pour une liste précise de joueurs : `downloadLeaderboardEntriesForUsers(steam_ids, handle)`. Avatars : voir [presence-et-overlay.md](presence-et-overlay.md).

Un fichier (replay, fantôme) peut être attaché à un score par Steam Cloud (`fileWriteAsync`, `fileShare`, puis `attachLeaderboardUGC`) : voir le tutoriel *Leaderboards* de GodotSteam.

## Checklist

- [ ] Classements créés et publiés, noms sans tiret, identiques dans le code
- [ ] Handles récupérés avant tout envoi
- [ ] Un envoi par fin de partie, jamais plus de 10 par 10 minutes
- [ ] Vue « autour de moi » et vue « amis » proposées

## Sources

- [Tutorials - Leaderboards](https://godotsteam.com/tutorials/leaderboards/)
- Classe [User Stats](https://godotsteam.com/classes/user_stats/)
- [Common Issues](https://godotsteam.com/issues/common_issues/) (noms de classement)
