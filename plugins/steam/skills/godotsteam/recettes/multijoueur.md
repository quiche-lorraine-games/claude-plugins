# Multijoueur : lobbies et SteamMultiplayerPeer

> **En bref** : créer, chercher et rejoindre des lobbies Steam, gérer les invitations (jeu lancé ou non), puis brancher le multijoueur de haut niveau de Godot (`@rpc`, `MultiplayerSpawner`, `MultiplayerSynchronizer`) sur le réseau de Steam avec `SteamMultiplayerPeer`. Relevé le 04/11/2026 (GodotSteam 4.23.2). Point de départ seulement : le multijoueur demande une conception propre au jeu.

## Quand consulter cette fiche

- Le jeu a du multijoueur en ligne entre amis ou par matchmaking, hébergé par un joueur.
- Tu veux éviter de louer un serveur et d'exposer des adresses IP.

Pour un serveur dédié, il existe GodotSteam Server, mais il n'a pas encore `SteamMultiplayerPeer`.

---

## 1. Lobbies

Un lobby est une salle d'attente hébergée par Steam : liste de membres, données clé-valeur, chat. Le créateur en devient propriétaire.

### Créer

```gdscript
Steam.lobby_created.connect(_on_lobby_created)
Steam.lobby_joined.connect(_on_lobby_joined)
Steam.createLobby(Steam.LOBBY_TYPE_FRIENDS_ONLY, 4)

func _on_lobby_created(resultat: int, lobby_id: int) -> void:
    if resultat == Steam.RESULT_OK:
        Steam.setLobbyData(lobby_id, "nom", "Partie de %s" % Steam.getPersonaName())
        Steam.setLobbyData(lobby_id, "mode", "coop")
```

| Type | Visibilité |
|---|---|
| `LOBBY_TYPE_PRIVATE` | sur invitation seulement |
| `LOBBY_TYPE_FRIENDS_ONLY` | amis et invités, pas dans les recherches |
| `LOBBY_TYPE_PUBLIC` | amis et recherches |
| `LOBBY_TYPE_INVISIBLE` | recherches seulement, invisible aux amis |

250 membres au plus. `createLobby()` déclenche `lobby_created`, puis `lobby_joined` (le créateur entre dans son lobby).

### Chercher

```gdscript
Steam.lobby_match_list.connect(_on_lobby_match_list)
Steam.addRequestLobbyListDistanceFilter(Steam.LOBBY_DISTANCE_FILTER_DEFAULT)
Steam.addRequestLobbyListStringFilter("mode", "coop", Steam.LOBBY_COMPARISON_EQUAL)
Steam.addRequestLobbyListFilterSlotsAvailable(1)
Steam.addRequestLobbyListResultCountFilter(20)
Steam.requestLobbyList()

func _on_lobby_match_list(lobbies: Array) -> void:
    for lobby_id in lobbies:
        var nom: String = Steam.getLobbyData(lobby_id, "nom")
```

Les filtres valent pour la requête suivante seulement. 50 résultats au plus. Avec l'App ID 480, ajoute toujours un filtre propre au jeu : la liste est remplie des lobbies d'autres développeurs.

### Rejoindre, quitter, suivre

```gdscript
Steam.joinLobby(lobby_id)

func _on_lobby_joined(lobby_id: int, _permissions: int, _verrouille: bool, reponse: int) -> void:
    if reponse != Steam.CHAT_ROOM_ENTER_RESPONSE_SUCCESS:
        return  # plein, n'existe plus, banni, compte limité… : afficher la raison
```

- `Steam.leaveLobby(lobby_id)` pour partir ; `lobby_chat_update(lobby_id, membre, auteur, etat)` à chaque arrivée ou départ ; `lobby_kicked` si le joueur perd la connexion.
- Membres : `getNumLobbyMembers(lobby_id)`, `getLobbyMemberByIndex(lobby_id, i)`, `getLobbyOwner(lobby_id)`.
- Données d'un membre (personnage choisi, « prêt ») : `setLobbyMemberData(lobby_id, cle, valeur)` (pour soi seulement) ; `lobby_data_update` prévient tout le monde.
- Chat : `sendLobbyChatMsg(lobby_id, texte)` et le signal `lobby_message`.
- Fermer aux nouveaux venus une fois la partie lancée : `setLobbyJoinable(lobby_id, false)`.

### Invitations

- **Inviter** : `Steam.activateGameOverlayInviteDialog(lobby_id)` ouvre la fenêtre d'invitation de Steam.
- **Jeu lancé**, le joueur accepte une invitation ou clique « Rejoindre » dans la liste d'amis : signal `join_requested(lobby_id, steam_id_ami)` → `joinLobby(lobby_id)`. Connecte-le dans un autoload, il peut arriver n'importe quand.
- **Jeu fermé** : Steam lance le jeu avec `+connect_lobby <lobby_id>` dans la ligne de commande. Lis `OS.get_cmdline_args()` au démarrage, garde l'ID et rejoins le lobby une fois Steam initialisé.

## 2. SteamMultiplayerPeer

Intégré à GodotSteam depuis la 4.17. Il remplace `ENetMultiplayerPeer` : les connexions se font par Steam ID, à travers le réseau de Steam (pas d'IP, pas de redirection de ports).

**Hôte** (créateur du lobby, peer 1) :

```gdscript
func _on_lobby_created(resultat: int, _lobby_id: int) -> void:
    if resultat != Steam.RESULT_OK:
        return
    var peer := SteamMultiplayerPeer.new()
    peer.create_host(0)
    peer.server_relay = true
    multiplayer.multiplayer_peer = peer
```

**Client** (les autres membres) :

```gdscript
func _on_lobby_joined(lobby_id: int, _p: int, _v: bool, reponse: int) -> void:
    if reponse != Steam.CHAT_ROOM_ENTER_RESPONSE_SUCCESS:
        return
    var hote: int = Steam.getLobbyOwner(lobby_id)
    if hote == Steam.getSteamID():
        return  # l'hôte a déjà son peer
    var peer := SteamMultiplayerPeer.new()
    peer.create_client(hote, 0)
    peer.server_relay = true
    multiplayer.multiplayer_peer = peer
```

`server_relay = true` fait passer les messages entre clients par l'hôte : un seul lien par client, et un client peut rejoindre une partie déjà lancée (scène avec `MultiplayerSpawner` déjà chargée).

Ensuite, tout le multijoueur de haut niveau de Godot s'applique tel quel :
- l'hôte crée un joueur par peer (nommé d'après son ID de peer) sous un nœud surveillé par un `MultiplayerSpawner` ;
- chaque joueur prend l'autorité sur son nœud dans `_enter_tree()` (`set_multiplayer_authority(int(name))`), pas dans `_ready()` : la synchronisation initiale du `MultiplayerSynchronizer` commence après `_enter_tree()` ;
- seul l'autorité calcule les déplacements (`if not is_multiplayer_authority(): return`) ;
- l'hôte retire le joueur d'un peer déconnecté (`multiplayer.peer_disconnected`).

À prévoir en plus : départ de l'hôte (fin de partie ou migration), reconnexion, triche (l'hôte fait autorité sur l'état important).

## 3. Autres voies réseau

Les classes *Networking Messages* et *Networking Sockets* donnent un accès plus bas niveau au réseau de Steam, sans le multijoueur de haut niveau de Godot. **Remote Play Together** permet de jouer à distance à un coop local sans écrire de code réseau.

## Pièges

- Tester sous l'App ID 480 sans filtre de recherche propre au jeu.
- Oublier `join_requested` et `+connect_lobby` : les invitations ne marchent pas.
- Donner l'autorité dans `_ready()`.
- Laisser un playtest et une démo ouverts en même temps pendant la Next Fest (voir `steam:boutique`) : les joueurs se dispersent entre les deux builds.

## Checklist

- [ ] Création, recherche (avec filtres), entrée et sortie de lobby
- [ ] Invitations par l'overlay, `join_requested` et `+connect_lobby` gérés
- [ ] Hôte en `create_host`, clients en `create_client(steam_id_hote)`, `server_relay` activé
- [ ] Autorité réglée dans `_enter_tree()`, joueurs retirés à la déconnexion
- [ ] Départ de l'hôte géré
- [ ] Testé avec deux comptes Steam sur deux machines

## Sources

- [Tutorials - Lobbies](https://godotsteam.com/tutorials/lobbies/)
- [Tutorials - MultiplayerPeer](https://godotsteam.com/tutorials/multiplayer_peer/)
- [What Are You Actually Making?](https://godotsteam.com/getting_started/what_are_you_making/)
- Classes [Matchmaking](https://godotsteam.com/classes/matchmaking/), [Friends](https://godotsteam.com/classes/friends/)
