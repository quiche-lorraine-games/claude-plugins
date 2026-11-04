# Steam Deck et matériel Steam

> **En bref** : ce que GodotSteam apporte pour le badge Verified et le confort sur Steam Deck et Steam Machine : clavier virtuel, réglages graphiques par défaut, détection du matériel, pause à l'ouverture de l'overlay, réveil après veille. Relevé le 04/11/2026 (GodotSteam 4.23.2, SDK 1.65). Les critères du badge sont dans `steam:boutique`, fiche `steam-deck.md`.

## 1. Clavier virtuel

Critère Verified : toute saisie de texte doit ouvrir le clavier virtuel quand le joueur utilise une manette.

**Clavier flottant** (recommandé pour un `LineEdit`) : le clavier s'affiche sans cacher le champ et envoie des frappes au jeu, qui les reçoit comme un vrai clavier.

```gdscript
func _on_line_edit_focus_entered() -> void:
    var r: Rect2 = $LineEdit.get_viewport().get_screen_transform() * $LineEdit.get_global_rect()
    Steam.showFloatingGamepadTextInput(Steam.FLOATING_GAMEPAD_TEXT_INPUT_MODE_SINGLE_LINE,
            int(r.position.x), int(r.position.y), int(r.size.x), int(r.size.y))
```

- Les coordonnées sont en pixels de la fenêtre : convertis le rectangle du contrôle si l'écran est étiré (`stretch`).
- Modes : `..._SINGLE_LINE` (Entrée ferme), `..._MULTIPLE_LINES`, `..._EMAIL`, `..._NUMERIC`.
- Signal `floating_gamepad_text_input_dismissed` à la fermeture ; `dismissFloatingGamepadTextInput()` pour le fermer.

**Saisie plein écran de Big Picture** : une boîte de saisie de Steam, qui renvoie le texte.

```gdscript
Steam.gamepad_text_input_dismissed.connect(_on_saisie_fermee)
Steam.showGamepadTextInput(Steam.GAMEPAD_TEXT_INPUT_MODE_NORMAL,
        Steam.GAMEPAD_TEXT_INPUT_LINE_MODE_SINGLE_LINE, "Nom du héros", 24, "")

func _on_saisie_fermee(validee: bool, texte: String, _app_id: int) -> void:
    if validee:
        $LineEdit.text = texte
```

Elle renvoie `false` si l'overlay Big Picture ne tourne pas : garde alors la saisie normale.

Le gabarit `steamworks.gd` fournit `show_keyboard_for(champ)` et `ask_text(...)`.

## 2. Réglages par défaut selon le matériel

`Steam.getSteamHardwareDefaultConfig()` (GodotSteam 4.21 et plus) est la méthode recommandée pour choisir les réglages graphiques du premier lancement. Elle renvoie :
- une valeur propre à un appareil (`STEAM_HARDWARE_DEFAULT_CONFIG_STEAM_DECK`, `..._STEAM_MACHINE`, `..._STEAM_FRAME`), à associer à des réglages réglés pour lui ;
- ou une valeur générale (`..._LOW`, `..._MEDIUM`, `..._HIGH`, `..._MAX`), à associer aux préréglages du jeu ;
- ou `..._NONE` : garder l'heuristique habituelle.

Le studio peut changer, dans Steamworks, la valeur renvoyée pour un appareil futur, sans recompiler le jeu. Ne bloque jamais un réglage selon le matériel : propose des valeurs par défaut, le joueur garde la main.

Autres fonctions :
- `Steam.isSteamRunningOnSteamDeck()` : la Deck seulement ;
- `Steam.isRunningOnSteamHardware()` : type de matériel Steam (Deck, Machine, Frame…), réservé selon la documentation aux statistiques, au support et au diagnostic, pas aux décisions de fonctionnalités ;
- `Steam.isSteamInBigPictureMode()` : joueur probablement à la manette, loin de l'écran ;
- `Steam.isRunningUnderProton()` : build Windows lancé sous Proton.

## 3. Overlay et mise en veille

- `Steam.overlay_toggled(actif, demande_par_joueur, app_id)` : à l'ouverture de l'overlay (bouton Steam), **mets en pause** un jeu solo.
- `Steam.app_resuming_from_suspend` : l'appareil sort de veille. Utile pour recalculer un minuteur basé sur l'heure réelle ou vérifier la connexion. Steam ne prévient pas de la mise en veille.

## 4. Steam Input

Steam Input remappe la manette pour le jeu. Deux cas :
- le jeu gère les manettes avec l'`InputMap` de Godot : laisse Steam Input présenter la manette comme une manette Xbox, ou désactive-le pour le jeu (réglages Steam Input de Steamworks). Si la manette ne répond plus, c'est souvent Steam Input qui capte les entrées ;
- le jeu utilise la classe *Input* de GodotSteam (fichier d'actions VDF, `inputInit()`, `getActionSetHandle()`, `activateActionSet()`, `getDigitalActionHandle()`, `getGlyphPNGForActionOrigin()`…) : glyphes corrects pour toutes les manettes et entrée mixte gérées par Steam. Plus de travail, voir le tutoriel *Inputs* de GodotSteam.

## Checklist

- [ ] Chaque champ de texte ouvre le clavier flottant à la prise de focus
- [ ] Préréglages graphiques choisis par `getSteamHardwareDefaultConfig()` au premier lancement
- [ ] Pause à l'ouverture de l'overlay
- [ ] Testé sur une Deck (ou en Big Picture) avec un build lancé par Steam

## Sources

- Classe [Utils](https://godotsteam.com/classes/utils/)
- Classe [Friends](https://godotsteam.com/classes/friends/) (`overlay_toggled`)
- Classe [Input](https://godotsteam.com/classes/input/) et [Tutorials - Inputs](https://godotsteam.com/tutorials/inputs/)
- [Common Issues](https://godotsteam.com/issues/common_issues/) (Steam Input qui capte la manette)
