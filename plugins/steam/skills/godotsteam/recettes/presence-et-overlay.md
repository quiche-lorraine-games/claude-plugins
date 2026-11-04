# Présence enrichie, overlay, avatars et enregistrement de jeu

> **En bref** : afficher ce que fait le joueur dans la liste d'amis, ouvrir l'overlay (page boutique, page web, invitations), récupérer noms et avatars, et marquer les moments forts dans l'enregistrement de jeu de Steam (timeline). Relevé le 04/11/2026 (GodotSteam 4.23.2).

## 1. Présence enrichie (*rich presence*)

La liste d'amis affiche une ligne sous le nom du jeu : « Niveau 3 : boss final ».

1. **Dans Steamworks**, envoie un fichier de jetons par langue, puis **publie** :

```
"lang"
{
	"Language"	"french"
	"Tokens"
	{
		"#Menu"	"Dans les menus"
		"#EnNiveau"	"Niveau %niveau% : %zone%"
	}
}
```

Les jetons commencent par `#`, les variables s'écrivent `%nom%`, les champs sont séparés par des tabulations. Un bloc par langue.

2. **Dans le jeu** : d'abord les variables, puis le jeton dans la clé spéciale `steam_display`.

```gdscript
Steam.setRichPresence("niveau", "3")
Steam.setRichPresence("zone", "boss final")
Steam.setRichPresence("steam_display", "#EnNiveau")
```

- 20 clés au plus par joueur ; clé de 64 caractères au plus, valeur de 256. Une valeur vide retire la clé. `clearRichPresence()` efface tout.
- Clés spéciales : `status` (texte de « Voir les infos du jeu ») et `connect` (ligne de commande qui permet à un ami de rejoindre la partie depuis la liste d'amis).
- Pour vérifier : survoler sa propre photo de profil dans la liste d'amis.

Le gabarit `steamworks.gd` fournit `set_presence(jeton, variables)`.

## 2. Overlay

| Appel | Ouvre |
|---|---|
| `Steam.activateGameOverlayToStore(app_id)` | la page boutique (par exemple du jeu complet, depuis la démo). **L'App ID 0 ouvre l'accueil de la boutique** : passe `Steam.getAppID()` pour le jeu en cours |
| `Steam.activateGameOverlayToWebPage(url)` | une page web (URL complète avec `https://`) |
| `Steam.activateGameOverlayInviteDialog(lobby_id)` | la fenêtre d'invitation d'amis vers un lobby |
| `Steam.activateGameOverlay("friends")` | une section : `friends`, `community`, `players`, `settings`, `officialgamegroup`… |

Le signal `overlay_toggled(actif, demande_par_joueur, app_id)` sert à mettre le jeu en pause. L'overlay ne s'affiche pas toujours depuis l'éditeur : teste sur un build lancé par Steam.

## 3. Noms et avatars

- `Steam.getPersonaName()` : nom du joueur local ; `Steam.getFriendPersonaName(steam_id)` : nom d'un autre joueur.
- Avatar : `Steam.getPlayerAvatar(steam_id)`, puis le signal `avatar_loaded(avatar_id, taille, donnees)` :

```gdscript
func _on_avatar_loaded(avatar_id: int, taille: int, donnees) -> void:
    var image: Image = Image.create_from_data(taille, taille, false, Image.FORMAT_RGBA8, donnees)
    var texture: ImageTexture = ImageTexture.create_from_image(image)
```

`avatar_id` est le Steam ID du joueur : il sert à retrouver à qui appartient l'avatar quand on en demande plusieurs.

## 4. Enregistrement de jeu (timeline)

L'enregistrement de jeu de Steam garde une vidéo de la partie ; le jeu peut l'annoter pour que le joueur retrouve et partage ses moments forts.
- `Steam.setTimelineGameMode(mode)` : couleur de la barre selon l'état (`TIMELINE_GAME_MODE_MENUS`, `..._STAGING`, `..._PLAYING`…) ;
- `Steam.setTimelineTooltip(description, decalage)` : description de l'état en cours (lieu, niveau), dans la langue de `getSteamUILanguage()` ;
- `Steam.addInstantaneousTimelineEvent(titre, description, icone, priorite_icone, decalage, priorite_clip)` : un moment (boss vaincu, record) ;
- `Steam.startGamePhase()` / `Steam.endGamePhase()` : une phase de 10 minutes à quelques heures (une partie, un chapitre, une run de roguelike), avec tags et attributs.

Les icônes se déposent dans Steamworks ou viennent de celles fournies par Steam.

## 5. Filtrage de texte

Pour les pseudos et messages affichés à d'autres joueurs : `Steam.initFilterText()` au démarrage (sans argument depuis GodotSteam 4.20), puis la fonction de filtrage de la classe *Utils*. Le joueur règle lui-même le niveau de filtrage dans Steam.

## Checklist

- [ ] Fichier de présence enrichie par langue publié dans Steamworks ; jetons utilisés dans le code identiques
- [ ] `activateGameOverlayToStore` appelé avec l'App ID voulu (jamais 0 par erreur)
- [ ] Pause du jeu solo à l'ouverture de l'overlay
- [ ] Avatars associés au bon joueur par `avatar_id`

## Sources

- [Tutorials - Rich Presence](https://godotsteam.com/tutorials/rich_presence/)
- [Tutorials - Avatars](https://godotsteam.com/tutorials/avatars/)
- [Tutorials - Text Filtering](https://godotsteam.com/tutorials/text_filtering/)
- Classes [Friends](https://godotsteam.com/classes/friends/), [Timeline](https://godotsteam.com/classes/timeline/), [Utils](https://godotsteam.com/classes/utils/)
