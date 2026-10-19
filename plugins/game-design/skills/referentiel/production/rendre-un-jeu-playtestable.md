# Rendre un jeu playtestable : le minimum

> **En bref** : la liste minimale de ce qu'un build doit avoir pour être envoyé en playtest. Si un point manque, le playtest produit surtout du bruit (crash, testeur perdu, retours impossibles à relier à une version). Tout le reste peut attendre. Pour organiser la session elle-même, voir [Playtest et métriques](playtest-et-metriques.md).

## Quand consulter cette fiche

- Tu veux savoir si un build peut partir en playtest.
- Tu prépares le premier playtest d'un projet et tu ne sais pas quoi faire en priorité.
- Un agent te demande « c'est prêt pour un playtest ? » : dérouler la liste ci-dessous.

---

## Le minimum

| # | Point | Pourquoi |
|---|---|---|
| 1 | **Un build exporté qui se lance sur une autre machine** que celle du développement, prérequis inclus. Pas de test depuis l'éditeur. | L'éditeur cache des bugs (chargement, chemins de fichiers) et donne accès aux outils de dev. |
| 2 | **Le parcours testé est jouable du début à la fin sans crash ni blocage**, vérifié en le jouant soi-même en entier sur ce build. | Un crash ou un blocage (*softlock*) met fin à la session ou occupe tout le retour du testeur. |
| 3 | **Une fin explicite** (« Fin du playtest, merci ») et le contenu hors périmètre inaccessible. | Sans fin, le testeur continue dans du contenu cassé et retient surtout ça. |
| 4 | **Le numéro de version affiché à l'écran** (menu pause ou coin de l'écran). | Un retour qu'on ne peut pas relier à un build est inutilisable. |
| 5 | **Les contrôles indiqués** (à l'écran ou sur une fiche) **et fonctionnels sur le matériel des testeurs** : manette prévue, et clavier AZERTY comme QWERTY. | Un testeur qui ne peut pas jouer ne teste rien. Une disposition ZQSD ou WASD codée en dur bloque une partie des testeurs. |
| 6 | **Aucun outil ni raccourci de debug accessible** (console, passer le niveau, invincibilité). | Un raccourci déclenché par hasard fausse la session. |
| 7 | **Un départ « nouveau joueur »** : sauvegarde vierge, et moyen de la remettre à zéro si plusieurs testeurs passent sur la même machine. | Un testeur qui hérite de la progression du précédent ne vit pas le premier contact. |
| 8 | **Pause et sortie propres.** | Il faut pouvoir interrompre la session sans perdre la partie ni tuer le processus. |
| 9 | **Un moyen de récupérer les retours** : questionnaire (lien affiché sur l'écran de fin) ou observation directe. | Sans collecte, le playtest n'a servi à rien. |
| 10 | **L'accord des testeurs externes** sur ce qui est enregistré (vidéo, voix, données) ; celui des parents pour un mineur. | Obligation légale (RGPD) et respect des testeurs. |

**Si les testeurs jouent à distance, sans toi**, ajouter :

| # | Point | Pourquoi |
|---|---|---|
| 11 | **Des instructions d'une page** : installer, lancer, contrôles, durée, où envoyer ses retours, qui contacter en cas de problème. | Personne n'est là pour débloquer le testeur. |
| 12 | **Les logs écrits sur disque, à un emplacement indiqué** dans les instructions. | C'est le seul moyen de comprendre un crash survenu chez un testeur. |
| 13 | **Une installation testée par quelqu'un d'extérieur à l'équipe.** | Chaque étape qui coince (alerte de sécurité Windows ou macOS, bibliothèque manquante) fait perdre des testeurs. |

---

## Ce qui peut attendre

Ne pas retarder un playtest pour :
- des graphismes ou un son définitifs, si la question du playtest ne porte pas dessus ;
- des menus complets, un écran titre, des crédits ;
- des options au-delà de la pause et du volume ;
- des bugs hors du parcours testé, si ce contenu est inaccessible ;
- la télémétrie : utile, mais un playtest observé s'en passe.

Un build brut mais stable, testé tôt, apporte plus qu'un build soigné testé trop tard (voir [Processus et prototypage](processus-et-prototypage.md)).

## Juste après le minimum

À ajouter dès que possible, par ordre d'utilité :
1. une **touche de retour dans le jeu** qui joint automatiquement capture d'écran, version et position ;
2. un **rapport de crash automatique** ;
3. une **télémétrie minimale** : début et fin de session, morts avec position, objectifs atteints, chaque événement avec la version (voir [Playtest et métriques](playtest-et-metriques.md)) ;
4. les **options de base** : volumes, sensibilité, inversion de l'axe Y, plein écran ou fenêtré, sous-titres s'il y a des dialogues.

---

## Checklist

- [ ] Le build exporté se lance sur une machine qui n'a pas servi au développement.
- [ ] J'ai joué le parcours testé en entier sur ce build, sans crash ni blocage.
- [ ] Un écran de fin explicite existe ; le contenu hors périmètre est inaccessible.
- [ ] La version est visible à l'écran.
- [ ] Les contrôles sont indiqués et fonctionnent sur le matériel des testeurs, en AZERTY comme en QWERTY.
- [ ] Aucun outil ni raccourci de debug n'est accessible.
- [ ] Le jeu démarre sur une sauvegarde vierge, réinitialisable entre testeurs.
- [ ] Pause et sortie fonctionnent.
- [ ] Le questionnaire ou la grille d'observation est prêt.
- [ ] L'accord des testeurs externes est recueilli.
- [ ] À distance : instructions d'une page, logs sur disque, installation testée par quelqu'un d'extérieur.

## Pistes d'implémentation

- **Version automatique** : à l'export, écrire dans un fichier ressource la sortie de `git describe --tags --always --dirty`, et l'afficher dans le menu pause. Le suffixe `-dirty` signale un build fait avec des modifications non committées : à éviter pour un playtest.
- **Debug retiré à la compilation** : séparer build de développement et build de playtest (drapeau de compilation, configuration d'export), plutôt que cacher les raccourcis.
- **Réinitialisation** : une option de ligne de commande (ex. `--reset-profile`) qui efface sauvegarde, profil et options.
- **Clavier** : associer les actions à la **position physique** des touches plutôt qu'au caractère.
- Notes moteur (à vérifier selon ta version) :
  - **Godot** : *feature tags* personnalisés dans les préréglages d'export, testables avec `OS.has_feature("playtest")` ; `InputEventKey.physical_keycode` pour la position physique d'une touche.
  - **Unity** : `Application.version`, `Debug.isDebugBuild` ; le nouvel Input System identifie les touches par leur position physique.
  - **UE5** : configuration *Shipping* pour les testeurs (console désactivée) ; Enhanced Input pour les contrôles.

**Distribuer le build**

| Canal | Pour |
|---|---|
| Lien de téléchargement d'une archive | Petit groupe de confiance |
| itch.io en accès restreint (clés de téléchargement ou mot de passe) | Tests privés ; réclamer une clé demande un compte itch.io |
| Steam Playtest | Tests à plus grande échelle, si le jeu a une page Steam |
| Build web | Prototypes courts, sans installation |
| TestFlight (iOS), test interne Google Play (Android) | Mobile |

## Voir aussi

- [Playtest et métriques](playtest-et-metriques.md) : organiser la session, observer, analyser
- [Gabarit : plan de playtest](templates/plan-playtest.md)
- [Gabarit : rapport de playtest](templates/rapport-playtest.md)
- [Processus et prototypage](processus-et-prototypage.md)
- [Accessibilité](../interface/accessibilite.md)

## Sources

- Anders Drachen, Pejman Mirza-Babaei, Lennart Nacke (dir.), *Games User Research*, Oxford University Press, 2018.
- Valve, documentation Steamworks, « Steam Playtest » — https://partner.steamgames.com/doc/features/playtest
- itch.io, documentation « Access control » — https://itch.io/docs/creators/access-control
- Règlement (UE) 2016/679 (RGPD).
