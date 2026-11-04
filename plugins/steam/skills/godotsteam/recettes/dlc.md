# DLC

> **En bref** : savoir si le joueur possède un DLC, lister les DLC, en installer un, et débloquer le contenu correspondant. Relevé le 04/11/2026 (GodotSteam 4.23.2 ; le tutoriel DLC de GodotSteam n'est pas encore écrit, cette fiche s'appuie sur la classe *Apps*).

## 1. Dans Steamworks

Chaque DLC est une application à part (App ID propre) liée au jeu, avec sa page et sa revue. Son contenu est soit **dans le jeu de base** (débloqué par la possession), soit dans un **dépôt** propre installé seulement chez ceux qui l'ont acheté. Valve conseille un DLC pour un gros contenu payant, et des achats en jeu pour les petits objets (voir `steam:boutique`, fiche `apres-la-sortie.md`).

## 2. Tester la possession

```gdscript
const DLC_EXTENSION: int = 1234560  # App ID du DLC

func contenu_extension_disponible() -> bool:
    return Steamworks.is_steam_enabled() and Steam.isDLCInstalled(DLC_EXTENSION)
```

- `isDLCInstalled(id)` : vrai si le joueur **possède** le DLC **et** qu'il est installé. La documentation précise : contrôle côté client seulement, à ne pas utiliser pour accorder des objets échangeables (passer par l'inventaire Steam ou un serveur).
- `isSubscribedApp(app_id)` : possession d'une autre application (par exemple le jeu complet, depuis la démo).
- `getDLCData()` : liste `[{id, available, name}, …]` des DLC du jeu ; `getDLCCount()` peut plafonner à 64 si le joueur ne possède pas beaucoup de DLC d'un jeu qui en a beaucoup : garde ta propre liste d'App ID.
- `installDLC(id)` installe un DLC facultatif ; le signal `dlc_installed(app_id)` arrive quand un DLC acheté est installé, y compris pendant la partie : débloque alors le contenu sans redémarrer.

## 3. Débloquer sans casser les sauvegardes

- Teste la possession au démarrage et à chaque `dlc_installed`, pas une seule fois à l'installation du jeu.
- Une sauvegarde qui utilise du contenu de DLC doit rester lisible si le DLC n'est plus là (remboursement, compte prêté) : remplacer ou masquer le contenu, jamais planter.
- Sans Steam (version itch.io, éditeur), décide explicitement : contenu absent, ou présent pour les tests (`OS.has_feature("debug")`).

## Checklist

- [ ] App ID de chaque DLC dans une constante
- [ ] Possession testée au démarrage et à `dlc_installed`
- [ ] Sauvegarde lisible sans le DLC
- [ ] Testé avec un compte qui a le DLC et un compte qui ne l'a pas

## Sources

- Classe [Apps](https://godotsteam.com/classes/apps/)
- [Tutorials - DLC](https://godotsteam.com/tutorials/dlc/) (en attente au 04/11/2026)
