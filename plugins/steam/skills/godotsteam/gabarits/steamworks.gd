extends Node
## Autoload « Steamworks » : la seule porte d'entrée du jeu vers Steam (GodotSteam 4.x).
##
## Gabarit du skill steam:godotsteam, à copier dans le projet (ex. res://autoloads/steamworks.gd)
## puis à déclarer en autoload sous le nom « Steamworks ». Le jeu marche sans Steam :
## si GodotSteam est absent ou si Steam ne démarre pas, chaque fonction ne fait rien.
##
## Le singleton est lu par Engine.get_singleton("Steam") et non par l'identifiant Steam,
## pour que le script se charge aussi avec des modèles d'export Godot standard.
## Laisser « Embed Callbacks » et l'initialisation automatique désactivés dans
## Project Settings > Steam > Initialization : ce script initialise et appelle run_callbacks().
##
## Signatures relevées dans la documentation de GodotSteam 4.23.2 le 04/11/2026.

signal steam_ready
signal overlay_toggled(active: bool)
signal keyboard_submitted(text: String)
signal keyboard_cancelled

## App ID du jeu. 0 : prendre celui de Project Settings > Steam > Initialization.
const APP_ID: int = 0

const INIT_OK: int = 0  # Steam.STEAM_API_INIT_RESULT_OK
const FLOATING_KEYBOARD_SINGLE_LINE: int = 0  # Steam.FLOATING_GAMEPAD_TEXT_INPUT_MODE_SINGLE_LINE
const FLOATING_KEYBOARD_MULTIPLE_LINES: int = 1  # Steam.FLOATING_GAMEPAD_TEXT_INPUT_MODE_MULTIPLE_LINES

## Langues de getCurrentGameLanguage() → locales Godot ; compléter selon les langues du jeu.
const LOCALES: Dictionary = {
	"french": "fr",
	"english": "en",
	"german": "de",
	"spanish": "es",
	"italian": "it",
	"portuguese": "pt",
	"brazilian": "pt_BR",
	"japanese": "ja",
	"koreana": "ko",
	"schinese": "zh_CN",
	"tchinese": "zh_TW",
	"russian": "ru",
	"polish": "pl",
}

var steam: Object = null
var init_result: Dictionary = {}
var steam_id: int = 0
var persona_name: String = ""


func _ready() -> void:
	# Les rappels de Steam ne doivent jamais s'arrêter, même quand le jeu est en pause.
	process_mode = Node.PROCESS_MODE_ALWAYS
	_initialize()


func _process(_delta: float) -> void:
	if steam:
		steam.run_callbacks()


func _initialize() -> void:
	if not Engine.has_singleton("Steam"):
		print("[Steamworks] GodotSteam absent : fonctions Steam désactivées.")
		return
	var api: Object = Engine.get_singleton("Steam")
	init_result = api.steamInitEx(APP_ID, false)
	if int(init_result.get("status", -1)) != INIT_OK:
		# 1 : autre échec ; 2 : client Steam injoignable ; 3 : client Steam pas à jour.
		push_warning("[Steamworks] Steam non initialisé, fonctions désactivées : %s" % init_result)
		return
	steam = api
	steam_id = steam.getSteamID()
	persona_name = steam.getPersonaName()
	steam.connect("overlay_toggled", _on_overlay_toggled)
	steam.connect("gamepad_text_input_dismissed", _on_gamepad_text_input_dismissed)
	print("[Steamworks] Steam initialisé pour %s." % persona_name)
	steam_ready.emit()


## Vrai si Steam est présent et initialisé : à tester avant tout appel direct à `steam`.
func is_steam_enabled() -> bool:
	return steam != null


# --- Succès et statistiques ---------------------------------------------------

## Débloque un succès (nom d'API de Steamworks) et l'envoie, ce qui affiche la notification.
func unlock_achievement(api_name: String) -> void:
	if not steam:
		return
	if not steam.setAchievement(api_name):
		push_warning("[Steamworks] Succès inconnu ou non publié : %s" % api_name)
		return
	store_stats()


func is_achievement_unlocked(api_name: String) -> bool:
	if not steam:
		return false
	var result: Dictionary = steam.getAchievement(api_name)
	return bool(result.get("ret", false)) and bool(result.get("achieved", false))


## Ajoute `amount` à une statistique entière, sans l'envoyer : appeler store_stats()
## aux moments opportuns (fin de niveau, point de contrôle, sortie du jeu).
func add_to_stat(api_name: String, amount: int = 1) -> void:
	if not steam:
		return
	var value: int = steam.getStatInt(api_name) + amount
	if not steam.setStatInt(api_name, value):
		push_warning("[Steamworks] Statistique inconnue, non publiée ou « increment only » : %s" % api_name)


func store_stats() -> void:
	if steam and not steam.storeStats():
		push_warning("[Steamworks] storeStats() a échoué ; Steam réessaiera plus tard.")


# --- Présence enrichie --------------------------------------------------------

## Affiche dans la liste d'amis le jeton `token` (ex. "#EnNiveau") défini dans le fichier
## de présence enrichie de Steamworks, avec ses variables (ex. {"niveau": "3"}).
func set_presence(token: String, values: Dictionary = {}) -> void:
	if not steam:
		return
	for key in values:
		steam.setRichPresence(str(key), str(values[key]))
	steam.setRichPresence("steam_display", token)


func clear_presence() -> void:
	if steam:
		steam.clearRichPresence()


# --- Overlay ------------------------------------------------------------------

## Ouvre la page boutique d'un jeu dans l'overlay ; par défaut celle du jeu en cours.
## (L'App ID 0 ouvrirait l'accueil de la boutique.)
func open_store_page(app_id: int = 0) -> void:
	if not steam:
		return
	steam.activateGameOverlayToStore(app_id if app_id > 0 else steam.getAppID())


func open_web_page(url: String) -> void:
	if steam:
		steam.activateGameOverlayToWebPage(url)
	else:
		OS.shell_open(url)


func _on_overlay_toggled(active: bool, _user_initiated: bool, _app_id: int) -> void:
	# À relier à la pause du jeu solo.
	overlay_toggled.emit(active)


# --- Steam Deck et matériel Steam ---------------------------------------------

func is_on_steam_deck() -> bool:
	return steam != null and steam.isSteamRunningOnSteamDeck()


## Réglage graphique conseillé par Steam pour ce matériel (GodotSteam 4.21 et plus) :
## 0 aucun, 1 bas, 2 moyen, 3 haut, 4 max, 5 Steam Deck, 6 Steam Machine…
## Renvoie 0 sans Steam ou avec une version plus ancienne.
func hardware_default_config() -> int:
	if not steam or not steam.has_method("getSteamHardwareDefaultConfig"):
		return 0
	return int(steam.getSteamHardwareDefaultConfig())


## Ouvre le clavier virtuel flottant sous un champ de saisie (le texte arrive dans le
## champ comme des frappes). Ne fait rien hors de Steam ; sur PC avec un clavier,
## Steam ne l'affiche pas toujours.
func show_keyboard_for(field: Control, multiline: bool = false) -> void:
	if not steam:
		return
	# Coordonnées en pixels de la fenêtre, étirement de l'écran compris.
	var rect: Rect2 = field.get_viewport().get_screen_transform() * field.get_global_rect()
	var mode: int = FLOATING_KEYBOARD_MULTIPLE_LINES if multiline else FLOATING_KEYBOARD_SINGLE_LINE
	steam.showFloatingGamepadTextInput(mode, int(rect.position.x), int(rect.position.y),
			int(rect.size.x), int(rect.size.y))


## Variante plein écran de Big Picture : le texte revient par keyboard_submitted.
func ask_text(description: String, max_length: int = 32, preset: String = "") -> bool:
	if not steam:
		return false
	# 0, 0 : Steam.GAMEPAD_TEXT_INPUT_MODE_NORMAL, Steam.GAMEPAD_TEXT_INPUT_LINE_MODE_SINGLE_LINE
	return steam.showGamepadTextInput(0, 0, description, max_length, preset)


func _on_gamepad_text_input_dismissed(submitted: bool, text: String, _app_id: int) -> void:
	if submitted:
		keyboard_submitted.emit(text)
	else:
		keyboard_cancelled.emit()


# --- Langue et DLC --------------------------------------------------------------

## Locale Godot correspondant à la langue choisie dans Steam, ou `fallback`.
func steam_locale(fallback: String = "en") -> String:
	if not steam:
		return fallback
	return LOCALES.get(steam.getCurrentGameLanguage(), fallback)


## Vrai si le joueur possède le DLC et qu'il est installé. Contrôle côté client
## seulement : ne pas s'en servir pour accorder des objets échangeables.
func owns_dlc(dlc_app_id: int) -> bool:
	return steam != null and steam.isDLCInstalled(dlc_app_id)
