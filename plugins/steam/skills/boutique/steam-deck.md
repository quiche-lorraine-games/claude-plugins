# Compatibilité Steam Deck (et Steam Machine)

> **En bref** : les badges de compatibilité (Verified, Playable, Unsupported, Unknown), chaque critère du label Verified, les recommandations de Valve qui ne conditionnent pas le badge, la revue de compatibilité, et ce que cela implique pour un jeu Godot. Relevé le 04/11/2026 sur la documentation Steamworks, qui couvre désormais la Steam Deck et la Steam Machine.

## Quand consulter cette fiche

- Tu vises le badge Verified.
- Tu conçois l'interface (taille du texte), les contrôles à la manette ou la saisie de texte.
- Tu reçois les résultats d'une revue de compatibilité.
- Tu choisis entre un export Linux natif et Windows sous Proton.

---

## 1. Les badges

| Badge | Signification |
|---|---|
| **Verified** | passe tous les critères ; aucune configuration de la part du joueur |
| **Playable** | fonctionne, mais demande une manipulation (choisir une configuration de manette de la communauté, ouvrir soi-même le clavier virtuel, naviguer un lanceur à l'écran tactile…) |
| **Unsupported** | ne fonctionne pas, à cause de Proton ou d'un composant matériel |
| **Unknown** | pas encore testé |

Le badge ne change pas la disponibilité du jeu, seulement sa présentation. Steam Deck et Steam Machine ont des badges indépendants ; un jeu Verified sur Deck l'est aussi sur Machine. Échouer à un critère donne en général Playable.

## 2. Critères du label Verified (règles de Valve)

### Communs à la Deck et à la Machine

**Entrées**
- **Manette** : le jeu gère les contrôles physiques de la Deck (ou de la Steam Controller sur Machine). La **configuration par défaut donne accès à tout le contenu**, sans réglage à changer en jeu pour activer la manette.
- **Glyphes** : les icônes de boutons affichées correspondent à l'entrée utilisée (Deck, Steam Controller ou Xbox). Pas d'icônes clavier-souris quand ce n'est pas l'entrée active ; les entrées de la Deck ne doivent jamais faire apparaître d'icônes non-manette.
- **Saisie de texte** : si le jeu demande du texte (nom de personnage, de sauvegarde), il ouvre le **clavier virtuel** par l'API Steamworks, ou propose sa propre saisie entièrement utilisable à la manette, dans la langue du joueur.

**Performances**
- La configuration par défaut donne une cadence jouable : **30 i/s en 800p** sur Deck, 30 i/s en 1080p sur Machine.

**Fluidité**
- **Aucun avertissement** au joueur que son système (distribution Linux) ou son matériel (GPU) n'est pas pris en charge.
- **Lanceur** : s'il y en a un, il respecte les mêmes critères, navigation complète à la manette comprise. Valve déconseille fortement d'imposer un lanceur.

**Proton** : un jeu sans build Linux natif tourne sous Proton. Un bug bloquant propre à Proton donne Unsupported, jusqu'à ce que Valve le corrige et reteste.

### Propres à la Deck

- **Résolution** : une résolution prise en charge par la Deck ; Valve recommande sa résolution native **1280 × 800** (de préférence) ou 1280 × 720.
- **Lisibilité** : texte lisible à 30 cm de l'écran, c'est-à-dire **aucun caractère de moins de 9 pixels de haut en 1280 × 800**. Valve recommande de viser **12 px** et de proposer une taille de texte (et si possible un contraste) réglable.

## 3. Recommandations de Valve (sans effet sur le badge)

- Une configuration de manette par défaut complète, ou à défaut une configuration Steam Input qui simule clavier et souris.
- Le clavier virtuel ouvert automatiquement : `ShowFloatingGamepadTextInput` (envoie des touches) ou `ShowGamepadTextInput` (par rappel).
- **Entrée mixte** : souris (gyroscope, pavé tactile) et joystick acceptés en même temps pour la caméra, sans basculer d'un mode à l'autre ni changer les glyphes au moindre mouvement de souris. Additionner les rotations de toutes les sources avant de mettre à jour la caméra.
- Vulkan en API graphique principale ; codecs autonomes (VP9, AV1) plutôt que liés à un éditeur (WMF).
- **Sauvegardes dans le nuage** (Steam Cloud), mais **pas les réglages graphiques**, propres à chaque appareil. Des réglages par défaut adaptés à la Deck, sans en interdire aucun.
- Tous les ratios d'écran, pas seulement 16:9 et 16:10.
- **Mode hors ligne** pour tout le contenu solo, y compris au premier lancement sur un nouveau compte.
- Tout dans le jeu, pas dans un lanceur.

## 4. La revue de compatibilité

- Valve ajoute d'elle-même à la file les jeux qui répondent à certains critères automatiques ou qui comptent pour les joueurs Deck. Certains partenaires peuvent la demander (*Technical Tools* → *Steam Hardware Compatibility Review*) ; l'option n'est pas ouverte à tous.
- Elle exige d'avoir passé la revue de build normale. Elle est possible avant la sortie, et indépendante de la sortie.
- Résultats en une semaine environ, détaillés critère par critère, pour la Deck, la Machine et les autres appareils SteamOS. Ils sont **publiés automatiquement au bout d'une semaine** environ si l'on ne fait rien. On peut les publier, envoyer un nouveau build et demander un nouvel examen (si le build arrive avant la publication, Valve reteste), ou contester.
- Un jeu avec build Linux natif est testé d'abord sous Linux, puis sous Proton si le build Linux échoue : Valve garde le meilleur des deux.
- Valve reteste d'elle-même (nouvelle version de Proton, nouveaux tests, signalements).
- On peut lier une annonce sur la compatibilité (champ *Steam Hardware Compat Info*, onglet *Basic Info*).
- Seuls les jeux sont examinés (pas les démos ni les DLC, sauf exception).

---

## 5. Pour un jeu Godot

- **Build Linux natif** : Godot exporte nativement pour Linux ; Valve le teste en premier. Garde aussi l'export Windows : si le natif échoue, Valve teste sous Proton.
- **Résolution** : choisis une taille de base en 16:10 ou qui s'adapte (*Project Settings* → *Display* → *Window* : `stretch/mode = canvas_items`, `stretch/aspect = expand`) pour remplir 1280 × 800 sans bandes ni interface coupée. Teste aussi 1280 × 720 et un ratio très large.
- **Taille du texte** : le critère porte sur la hauteur du plus petit caractère affiché, pas sur la taille de police. Avec une taille de base de 1920 × 1080 et `canvas_items`, tout est réduit d'environ un tiers en 1280 × 800 : une police de 18 px n'en fait plus que 12. Point de départ, à vérifier : lance le jeu en 1280 × 800, fais une capture, et mesure les plus petites lettres (minuscules comprises).
- **Manette** : toutes les actions dans l'`InputMap` avec une entrée manette ; navigation de toute l'interface au focus (`focus_neighbor_*`, `grab_focus()` sur le premier bouton de chaque écran).
- **Glyphes** : changer d'icônes selon le dernier périphérique utilisé (`InputEventJoypadButton` contre `InputEventKey`/`InputEventMouseButton`), avec une petite tolérance pour la souris (entrée mixte).
- **Clavier virtuel** : à l'ouverture d'un champ, `Steam.showFloatingGamepadTextInput(mode, x, y, largeur, hauteur)` (le clavier envoie des touches, la zone du champ reste visible) ou `Steam.showGamepadTextInput(mode, mode_ligne, description, longueur_max, texte_initial)` (le texte revient par un signal). `Steam.isSteamRunningOnSteamDeck()` permet d'adapter les réglages par défaut sur Deck, sans en interdire aucun ailleurs.
- **Performances** : mesurer en 1280 × 800 avec les réglages par défaut ; préférer le moteur de rendu *Forward+* ou *Mobile* selon les mesures, et prévoir des préréglages graphiques.
- **Mise en veille** : la Deck suspend le jeu ; ne pas compter sur une horloge murale continue pour la logique, et gérer la perte de focus (`NOTIFICATION_APPLICATION_FOCUS_OUT`).

## Pièges

- Un champ de saisie (nom de sauvegarde) qui exige un clavier physique.
- Des icônes de clavier qui apparaissent quand le joueur touche le pavé tactile.
- Un écran de lancement ou de connexion qui ne se navigue pas à la manette.
- Un message « GPU non pris en charge ».
- Des infobulles ou chiffres de HUD en police minuscule.
- Synchroniser le fichier de réglages graphiques par Steam Cloud.

## Checklist

- [ ] Tout le jeu accessible avec la configuration de manette par défaut, sans réglage
- [ ] Glyphes qui suivent l'entrée active, jamais d'icônes clavier en jouant à la manette
- [ ] Clavier virtuel ouvert automatiquement pour chaque saisie de texte
- [ ] 30 i/s en 1280 × 800 avec les réglages par défaut
- [ ] Rendu correct en 1280 × 800, sans bandes ni interface coupée
- [ ] Plus petit caractère d'au moins 9 px (12 visés) mesuré sur une capture en 1280 × 800 ; taille de texte réglable
- [ ] Aucun avertissement système ou matériel, aucun lanceur obligatoire
- [ ] Sauvegardes dans Steam Cloud, réglages graphiques hors nuage
- [ ] Contenu solo jouable hors ligne

## Voir aussi

- [fonctionnalites-steamworks.md](fonctionnalites-steamworks.md) : Steam Cloud et Steam Input.
- Référentiel game design, `interface/accessibilite.md` et `interface/ui-ux-hud.md` (plugin `game-design`) : taille du texte, remapping.

## Sources

- [Steam Deck and Steam Machine Compatibility Review](https://partner.steamgames.com/doc/steamdeck/compat)
- [Getting your game ready for Steam Deck and Steam Machine](https://partner.steamgames.com/doc/steamdeck/recommendations)
- GodotSteam, classe [Utils](https://godotsteam.com/classes/utils/) (clavier virtuel, détection de la Deck)
