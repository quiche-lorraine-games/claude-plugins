# Succès et statistiques

> **En bref** : déclarer les succès et statistiques dans Steamworks, les lire, les débloquer, les envoyer et les remettre à zéro avec GodotSteam. Relevé le 04/11/2026 (GodotSteam 4.23.2, SDK 1.65). Les limites et règles de Valve (icônes 256 × 256, 100 succès avant validation) sont dans `steam:boutique`, fiche `fonctionnalites-steamworks.md`.

## 1. Dans Steamworks d'abord

Prépare pour l'humain la liste à saisir dans *App Admin* → *Stats & Achievements* :
- succès : nom d'API (majuscules et `_`, ex. `FIRST_WIN`), nom et description dans chaque langue, icône obtenue et non obtenue, caché ou non, statistique de progression éventuelle ;
- statistiques : nom d'API, type (`INT`, `FLOAT`, `AVGRATE`), « increment only », bornes.

Puis **publier**. Un succès ou une statistique non publié fait échouer les appels (`getAchievement()` renvoie `ret = false`, `setAchievement()` et `setStatInt()` renvoient `false`).

## 2. Lire

Depuis le SDK 1.61, les données du joueur sont chargées au démarrage par Steam : on peut lire et écrire dès l'initialisation, sans requête.

```gdscript
var etat: Dictionary = Steam.getAchievement("FIRST_WIN")  # {ret, achieved}
if etat["ret"] and etat["achieved"]:
    pass  # déjà obtenu
var victoires: int = Steam.getStatInt("WINS")
var distance: float = Steam.getStatFloat("DISTANCE")
```

`ret` est faux si le nom d'API n'existe pas dans Steamworks ou n'est pas publié.

## 3. Débloquer et envoyer

```gdscript
if Steam.setAchievement("FIRST_WIN"):
    Steam.storeStats()
```

- `setAchievement()` et `setStatInt()` / `setStatFloat()` ne modifient que l'état en mémoire de Steam (peu coûteux, conservé même en cas de plantage).
- **`storeStats()` envoie** les changements et déclenche la notification du succès. Sans lui, le succès est enregistré mais rien ne s'affiche. Appelle-le après chaque succès, et pour les statistiques aux moments opportuns (fin de niveau, point de contrôle, sortie).
- `setStatInt()` prend une **valeur absolue**, pas un incrément : lis la valeur, ajoute, écris. Avec une statistique « increment only », une valeur plus basse renvoie `false`.
- `indicateAchievementProgress(nom, actuel, max)` affiche une progression (ex. 10 sur 20).
- Depuis l'éditeur, la notification de l'overlay peut ne pas s'afficher (problème d'overlay connu avec Vulkan) ; elle s'affiche sur un build lancé par Steam.

## 4. Sauvegarde locale ou pas

Valve déconseille de garder sa propre copie des succès : Steam en tient un cache hors ligne et fusionne entre machines (voir `steam:boutique`). Si le jeu garde quand même la progression dans sa sauvegarde (pour l'afficher sans Steam, par exemple), compare au chargement et rattrape dans les deux sens : succès obtenu localement mais pas sur Steam → `setAchievement()` ; statistique locale plus haute → `setStatInt()`.

**Dans une démo**, ne débloque pas les succès : enregistre la progression, et débloque au premier lancement du jeu complet.

## 5. Remettre à zéro

- `Steam.resetAllStats(true)` : toutes les statistiques, et les succès avec `true`. Utile pendant le développement, ou dans un menu d'options si le jeu le propose.
- `Steam.clearAchievement("FIRST_WIN")` : un seul succès.
- Sans code : console du client Steam (`steam.exe -console`), `achievement_clear <appid> <nom>` ou `reset_all_stats <appid>`.

## Pièges

- Appeler `requestCurrentStats()` ou attendre `current_stats_received` : supprimés depuis le SDK 1.61.
- Oublier `storeStats()` après `setAchievement()`.
- Croire que `setStatInt("WINS", 1)` ajoute 1.
- Tester sous l'App ID 480 des succès du jeu : ils n'existent que sous son App ID.

## Checklist

- [ ] Liste des succès et statistiques prête pour Steamworks, saisie et publiée
- [ ] Noms d'API identiques dans le code et dans Steamworks (constantes dans un seul fichier)
- [ ] `storeStats()` après chaque succès, et régulièrement pour les statistiques
- [ ] Aucun succès débloqué par la démo
- [ ] Testé sur un build lancé par Steam avec l'App ID du jeu

## Sources

- [Tutorials - Stats and Achievements](https://godotsteam.com/tutorials/stats_achievements/)
- Classe [User Stats](https://godotsteam.com/classes/user_stats/)
- [Common Issues](https://godotsteam.com/issues/common_issues/)
