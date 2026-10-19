# Rendre un jeu playtestable

> **En bref** : ce qu'un build doit contenir pour qu'un playtest produise des données exploitables : stabilité sur le chemin testé, version identifiable, point de départ et fin clairs, état « nouveau joueur », outils de debug maîtrisés, contrôles et options minimales, télémétrie et logs vérifiés, collecte des retours, distribution simple, consentement. Un build playtestable n'est **pas** un build fini : c'est un build qui permet de répondre à la question du playtest sans que des problèmes parasites masquent la réponse.

## Quand consulter cette fiche

- Tu prépares un build pour un playtest, interne ou externe.
- Un playtest précédent a été gâché par un crash, un blocage, un testeur perdu dans du contenu cassé ou des données manquantes.
- Tu dois choisir comment distribuer un build à des testeurs à distance.
- Tu veux ajouter au jeu de quoi faciliter les playtests (version affichée, touche de retour, télémétrie, réinitialisation).
- Tu dois décider si un build est « assez bon » pour être montré.

Pour l'organisation de la session elle-même (objectifs, observation, questions, analyse), voir [Playtest et métriques](playtest-et-metriques.md).

---

## 1. Principes

- **Le playtest répond à une question ; le build doit servir cette question.** Si la question porte sur la compréhension du saut, le décor peut être gris, mais le saut, la caméra et le niveau testé doivent être fiables. Tout ce qui ne sert pas la question peut rester brut.
- **Un problème parasite masque la donnée.** Un crash, un blocage ou une mauvaise disposition de touches occupe l'attention du testeur et du facilitateur, et les retours portent sur ce problème au lieu de la question posée.
- **Chaque retour doit pouvoir être relié à un build précis.** Sans numéro de version, un retour est inutilisable une semaine plus tard.
- **Un testeur neuf ne se recrute qu'une fois.** Le build doit le placer dans les conditions d'un vrai premier contact : aucune sauvegarde, aucun tutoriel marqué comme vu, aucun raccourci de debug actif.
- **Les exigences augmentent avec la distance.** Plus le testeur est loin de l'équipe, moins on peut rattraper un problème pendant la session.

### Niveaux de playtest et exigences

| Niveau | Testeurs | Ce qu'on peut tolérer | Exigences supplémentaires |
|---|---|---|---|
| Interne | Équipe | Bugs connus, outils de debug, lancement depuis l'éditeur | Version notée, question définie |
| Proches encadrés | Amis, collègues d'autres équipes, en présentiel | Bugs hors du chemin testé, contournés par le facilitateur | Build exporté (pas l'éditeur), réinitialisation entre testeurs |
| Externe encadré | Public cible, en présentiel ou en visio | Contenu hors périmètre bloqué | Consentement, enregistrement, questionnaire, aucun outil de debug accessible |
| Externe à distance non encadré | Public cible, seul chez lui | Presque rien : personne n'est là pour débloquer | Installation simple, collecte de retours dans le jeu, télémétrie et rapports de crash automatiques |
| Public | Inscrits (Steam Playtest, démo) | Comme une sortie, à petite échelle | Matériel varié, support, communication, politique de confidentialité |

---

## 2. Les points, par catégorie

Priorités : **B** = bloquant (pas de playtest sans), **I** = important (dégrade fortement les données), **C** = confort.

### 2.1 Stabilité

| Point | Priorité | Détail |
|---|---|---|
| Aucun crash connu sur le chemin testé | B | Jouer soi-même le parcours complet sur le **build exporté**, pas dans l'éditeur : les différences entre éditeur et build (chargement, chemins de fichiers, optimisation) cachent des bugs. |
| Aucun blocage (*softlock*) sur le chemin testé | B | Porte qui ne s'ouvre pas, ennemi requis coincé dans un mur, objet de quête perdu. |
| Échappatoire en cas de blocage | I | Option « revenir au dernier checkpoint » ou « réapparaître » dans le menu pause : le testeur repart sans redémarrer. |
| Sauvegarde automatique avant chaque section testée | I | Permet de reprendre après un crash sans refaire 20 minutes de jeu. |
| Rapport de crash automatique | I (B à distance) | Pile d'appels, plateforme, version, dernières actions ; symboles de debug archivés avec le build. Déclencher un crash volontaire pour vérifier que les rapports arrivent. |
| Test rapide (*smoke test*) sur une autre machine | I | Une machine qui n'a jamais servi au développement révèle les dépendances manquantes et les chemins codés en dur. |

### 2.2 Identification du build

| Point | Priorité | Détail |
|---|---|---|
| Numéro de version visible à l'écran | B | Dans un coin pendant le jeu ou au minimum dans le menu pause, pour qu'il apparaisse sur les captures et les vidéos. Inclure le hash du commit. |
| Version dans les logs, la télémétrie et chaque rapport | B | Généré automatiquement au moment de l'export, jamais saisi à la main. |
| Build archivé | I | Conserver l'exécutable exact et ses symboles : un retour doit pouvoir être reproduit sur le même build. |
| Liste des changements depuis le dernier playtest | C | Permet de vérifier qu'un problème signalé la dernière fois est résolu. |

### 2.3 Périmètre : début et fin

| Point | Priorité | Détail |
|---|---|---|
| Démarrage direct sur le contenu testé | I | Scène de départ dédiée ou sauvegarde préparée, pour ne pas faire passer 15 minutes d'introduction quand on teste le niveau 3. |
| Fin explicite | B | Écran « Fin du playtest, merci » à la fin du contenu testé. Sans fin, le testeur continue dans du contenu cassé ou ne sait pas quand s'arrêter. |
| Contenu hors périmètre bloqué | I | Zones, menus ou modes non prêts : inaccessibles ou clairement marqués « non disponible dans ce playtest ». |
| Durée cohérente avec la session | I | Contenu jouable dans le temps prévu par un joueur moyen, avec une marge pour les plus lents. |

### 2.4 État « nouveau joueur »

| Point | Priorité | Détail |
|---|---|---|
| Sauvegardes et profil réinitialisables | B | Entre deux testeurs, effacer sauvegarde, progression, tutoriels vus, succès et options modifiées. Prévoir une commande ou un script, pas une manipulation de fichiers à la main. |
| Options par défaut | I | Le testeur suivant ne doit pas hériter de la sensibilité ou du volume réglés par le précédent. |
| Aucun avantage de debug actif | B | Invincibilité, objets de départ, déblocages : tout est désactivé. |

### 2.5 Outils de debug

| Point | Priorité | Détail |
|---|---|---|
| Raccourcis de debug retirés des builds externes | B | Un raccourci oublié (passer le niveau, mode dieu, console) fausse les données dès qu'un testeur le déclenche par hasard. Les compiler conditionnellement selon le type de build plutôt que les cacher. |
| Accès facilitateur en playtest encadré | C | Une combinaison volontairement improbable, ou un fichier de config, qui donne au facilitateur : téléportation au checkpoint, rechargement du niveau, affichage des infos de debug. |
| Superposition d'infos activable | C | FPS, position, état du joueur : utile au facilitateur, invisible par défaut. |

### 2.6 Contrôles et options minimales

| Point | Priorité | Détail |
|---|---|---|
| Contrôles affichés | B | Dans le jeu (aide contextuelle, écran pause) ou sur une fiche à côté du testeur. Sauf si le playtest teste justement la découverte des contrôles. |
| Clavier AZERTY et QWERTY | B pour des testeurs francophones | Une disposition ZQSD ou WASD codée en dur rend le jeu injouable pour une partie des testeurs. Lire la **position physique** des touches, ou proposer le choix de disposition au premier lancement. |
| Périphériques ciblés testés | B | Manette, clavier-souris, tactile : tester ceux que les testeurs utiliseront, avec les icônes correspondantes. |
| Remapping des touches | I | Au minimum pour clavier-souris (voir [Accessibilité](../interface/accessibilite.md)). |
| Options de base | I | Volume général, musique et effets ; sensibilité de la caméra et inversion de l'axe Y ; plein écran ou fenêtré, et résolution. |
| Sous-titres | I | Dès qu'il y a du dialogue porteur d'information : le testeur peut jouer sans son, ou dans une salle bruyante. |
| Pause à tout moment | I | Le testeur ou le facilitateur doit pouvoir interrompre la session (question, problème technique). |

### 2.7 Télémétrie et logs

| Point | Priorité | Détail |
|---|---|---|
| Événements clés enregistrés | I | Début et fin de session, entrée dans chaque section, morts avec position et cause, objectifs atteints, abandons, choix importants. Voir [Playtest et métriques](playtest-et-metriques.md) pour la liste. |
| Chaque événement porte version, identifiant de session et horodatage | B si télémétrie | Sans eux, les données ne se relient ni aux retours ni au build. |
| Identifiant de session anonyme | I | Un identifiant aléatoire par session, relié au questionnaire du testeur, plutôt qu'une donnée personnelle. |
| Envoi robuste | I | File d'attente locale si le réseau tombe, envoi à la reprise ; copie locale des événements en fichier. |
| Vérification de bout en bout avant la session | B si télémétrie | Jouer 5 minutes et vérifier que les données arrivent, complètes, à l'endroit prévu. Des données perdues ne se rattrapent pas. |
| Logs écrits sur disque | I | Emplacement connu, documenté pour les testeurs à distance (« envoyez-nous le fichier situé dans… »). |

### 2.8 Collecte des retours

| Point | Priorité | Détail |
|---|---|---|
| Touche de retour dans le jeu | I (B à distance) | Une touche ouvre un champ de texte et joint automatiquement capture d'écran, version, position, scène et horodatage. Le testeur signale le problème au moment où il le vit, au lieu de s'en souvenir après. |
| Questionnaire post-session relié à la session | I | Lien ou QR code affiché sur l'écran de fin, avec l'identifiant de session prérempli. |
| Enregistrement vidéo | I | En présentiel : capture de l'écran (et si possible des mains et du visage, avec consentement). À distance : instructions d'enregistrement simples, ou outil intégré. |
| Profil du testeur | C | Questionnaire court avant la session (habitudes de jeu, motivations), pour segmenter les retours (voir [Profils de joueurs](../fondamentaux/profils-de-joueurs.md)). |

### 2.9 Performance

| Point | Priorité | Détail |
|---|---|---|
| Fluidité stable sur le matériel le plus faible des testeurs | I | Les saccades faussent le ressenti et la difficulté, surtout dans un jeu d'action. |
| Temps de chargement raisonnables | C | Un écran de chargement qui semble figé fait croire à un crash : afficher une progression ou une animation. |
| Pas de fuite de mémoire sur la durée de la session | I | Lancer une session aussi longue que le playtest prévu. |

### 2.10 Distribution et installation

| Point | Priorité | Détail |
|---|---|---|
| Installation en quelques étapes | B à distance | Archive à décompresser ou lanceur de plateforme. Chaque étape supplémentaire fait perdre des testeurs. |
| Prérequis inclus | B | Bibliothèques d'exécution nécessaires au moteur incluses, ou installées par le jeu. |
| Avertissements système anticipés | I | Un exécutable non signé déclenche des alertes (SmartScreen sous Windows, Gatekeeper sous macOS) : expliquer la marche à suivre dans les instructions, ou signer le build. |
| Instructions d'une page | I | Installation, lancement, contrôles, durée, comment envoyer ses retours, contact en cas de problème. |
| Canal adapté | I | Voir le tableau ci-dessous. |

| Canal | Pour | À savoir |
|---|---|---|
| Archive partagée (lien de téléchargement) | Petit groupe de confiance | Simple, aucun contrôle d'accès ni de mise à jour |
| itch.io en accès restreint | Tests privés de petite taille | Page invisible des recherches ; accès par clés de téléchargement ou mot de passe ; réclamer une clé demande un compte itch.io, ce qui peut rebuter certains testeurs |
| Steam Playtest | Tests à grande échelle sur Steam | Application séparée liée au jeu, inscription depuis la page du jeu, admission des joueurs par vagues, fermeture à la fin du test ; demande une page Steam |
| Build web (HTML5, WebGL) | Prototypes courts, tests rapides | Aucune installation ; performances et contrôles différents d'un build natif |
| TestFlight (iOS), test interne Google Play (Android) | Mobile | Délais de validation possibles côté plateforme |

### 2.11 Consentement et éthique

| Point | Priorité | Détail |
|---|---|---|
| Consentement explicite | B en externe | Expliquer ce qui est enregistré (vidéo, voix, visage, télémétrie) et pourquoi. Prévoir des cases séparées pour chaque usage, notamment toute réutilisation promotionnelle. |
| Données personnelles minimales (RGPD) | B en externe | Ne collecter que le nécessaire, pseudonymiser, fixer une durée de conservation, indiquer comment se retirer et demander la suppression de ses données. Faire relire le formulaire par une personne compétente. |
| Mineurs | B | Autorisation des parents ou tuteurs. |
| Avertissement photosensibilité | I | Si le jeu contient des flashs ou des motifs clignotants (voir [Accessibilité](../interface/accessibilite.md)). |
| Confidentialité | C | Accord de non-divulgation si le projet n'est pas annoncé. |
| Contreparties | C | Prévoir un remerciement (crédits, clé du jeu final, rémunération selon le cadre), annoncé à l'avance. |

### 2.12 Multijoueur

| Point | Priorité | Détail |
|---|---|---|
| Serveurs disponibles et dimensionnés | B | Tester la connexion depuis l'extérieur du réseau de l'équipe. |
| Assez de joueurs pour remplir une partie | B | Créneaux fixés à l'avance, ou bots pour compléter. |
| Conditions réseau réalistes | I | Tester avec de la latence et des pertes de paquets simulées (voir [Multijoueur](../systemes/multijoueur.md)). |

### 2.13 Côté facilitateur

| Point | Priorité | Détail |
|---|---|---|
| Liste des problèmes connus | I | Pour ne pas perdre de temps à les noter, et reconnaître immédiatement un problème nouveau. Ne pas la lire aux testeurs. |
| Répétition générale | I | Une session complète avec un membre de l'équipe : installation, enregistrement, télémétrie, questionnaire. La première vraie session ne doit pas servir à découvrir que l'enregistrement ne marche pas. |
| Plan de session écrit | I | Gabarit : [plan de playtest](templates/plan-playtest.md). |

---

## 3. Ce qui n'est pas nécessaire

Ne pas retarder un playtest pour :
- des graphismes ou un son définitifs, si la question ne porte pas dessus ;
- des menus complets, des écrans de titre ou des crédits ;
- toutes les options : seules celles de la section 2.6 comptent ;
- l'absence de bugs hors du chemin testé, si ce contenu est bloqué ;
- l'équilibrage final, si la question ne porte pas dessus.

Tester tôt avec un build brut mais stable apporte plus qu'un build soigné testé trop tard (voir [Processus et prototypage](processus-et-prototypage.md)).

---

## 4. Anti-patterns

- **Tester depuis l'éditeur avec des testeurs externes** : comportement différent du build réel, outils de debug accessibles, risque de modification accidentelle.
- **Un raccourci de debug oublié** : un testeur appuie par hasard sur la touche qui passe le niveau, et les données de la session sont faussées.
- **Pas de fin** : le testeur sort du contenu prévu, rencontre des bugs, et retient surtout ceux-là.
- **Testeur suivant sur la sauvegarde du précédent** : tutoriels déjà vus, objets déjà ramassés ; le « premier contact » n'en est plus un.
- **Télémétrie jamais vérifiée** : on découvre après la session que les événements n'ont pas été envoyés, ou sans numéro de version.
- **Retours sans version** : « le saut est bizarre », mais dans quel build ?
- **Clavier QWERTY codé en dur** pour des testeurs francophones.
- **Expliquer le jeu pour compenser un build cassé** : les données de compréhension sont alors perdues.

---

## Checklist

Avant chaque playtest (*go / no-go*) :

- [ ] La question du playtest est écrite, et le build permet d'y répondre.
- [ ] Le chemin testé a été joué en entier sur le build exporté, sur une machine autre que celle du développement.
- [ ] Aucun crash ni blocage connu sur ce chemin ; une option « revenir au checkpoint » existe.
- [ ] La version (avec le hash du commit) est visible à l'écran et présente dans les logs, la télémétrie et les rapports.
- [ ] Le jeu démarre sur le contenu testé et se termine par un écran de fin explicite ; le contenu hors périmètre est bloqué.
- [ ] Sauvegarde, profil, tutoriels et options se réinitialisent en une commande entre deux testeurs.
- [ ] Aucun raccourci de debug ni avantage actif n'est accessible aux testeurs.
- [ ] Les contrôles sont affichés ; AZERTY et QWERTY fonctionnent ; les périphériques prévus sont testés.
- [ ] Les options de base sont présentes : volumes, sensibilité, inversion de l'axe Y, mode d'affichage ; sous-titres si dialogues.
- [ ] La télémétrie a été vérifiée de bout en bout ; les rapports de crash arrivent.
- [ ] Les testeurs disposent d'un moyen de retour dans le jeu et d'un questionnaire relié à la session.
- [ ] L'enregistrement vidéo est prêt et testé.
- [ ] À distance : installation testée par quelqu'un d'extérieur à l'équipe ; instructions d'une page fournies.
- [ ] Le consentement est recueilli (enregistrement, télémétrie, données) ; autorisation parentale pour les mineurs.
- [ ] La liste des problèmes connus et le plan de session sont prêts ; une répétition générale a eu lieu.

## Pistes d'implémentation

**Un type de build « playtest »** : un drapeau de compilation ou une configuration d'export qui active la version affichée, la télémétrie, la touche de retour et l'écran de fin, et qui retire les outils de debug.

```
// Pseudo-code agnostique
if BUILD_PLAYTEST:
    show_version_overlay(VERSION + " " + GIT_HASH)
    telemetry.enable(session_id = random_uuid())
    bind(KEY_FEEDBACK, open_feedback_form)   // capture + état joint automatiquement
    debug_tools.disable()
```

**Version générée automatiquement** : à l'export, écrire dans un fichier ressource la sortie de `git describe --tags --always --dirty` et la date de build. Le suffixe `-dirty` signale un build fait avec des modifications non committées : à éviter pour un playtest.

**Touche de retour** : capture d'écran, puis un fichier JSON avec `{version, session_id, scene, position, timestamp, texte}`, envoyé au serveur ou à défaut écrit dans un dossier local que le testeur peut joindre.

**Réinitialisation** : une option de ligne de commande (ex. `--reset-profile`) ou une entrée du menu facilitateur qui efface sauvegarde, profil et options.

**Clavier** : associer les actions aux **positions physiques** des touches plutôt qu'aux caractères, et afficher dans l'interface le nom de la touche selon la disposition du testeur.

Notes moteur (à vérifier dans la documentation de ta version) :
- **Godot** : les préréglages d'export acceptent des *feature tags* personnalisés, testables avec `OS.has_feature("playtest")`. `InputEventKey.physical_keycode` lit la position physique d'une touche. Les builds de debug et de release s'exportent séparément.
- **Unity** : `Application.version` pour la version, `Debug.isDebugBuild` et les *scripting define symbols* pour séparer les builds. Le nouvel Input System lie les touches par position physique par défaut.
- **UE5** : séparer configurations *Development* et *Shipping* (la console est désactivée en *Shipping*) ; activer l'inclusion du *Crash Reporter* dans les réglages de packaging ; Enhanced Input pour le remapping.

## Voir aussi

- [Playtest et métriques](playtest-et-metriques.md) : organiser la session, observer, analyser
- [Processus et prototypage](processus-et-prototypage.md)
- [Gabarit : plan de playtest](templates/plan-playtest.md)
- [Gabarit : rapport de playtest](templates/rapport-playtest.md)
- [Profils de joueurs](../fondamentaux/profils-de-joueurs.md) : recruter et segmenter les testeurs
- [Accessibilité](../interface/accessibilite.md)
- [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)

## Sources

- Anders Drachen, Pejman Mirza-Babaei, Lennart Nacke (dir.), *Games User Research*, Oxford University Press, 2018.
- Steve Bromley, *How To Be A Games User Researcher*, 2021.
- Valve, documentation Steamworks, « Steam Playtest » — https://partner.steamgames.com/doc/features/playtest
- itch.io, documentation « Access control » (pages restreintes, clés de téléchargement) — https://itch.io/docs/creators/access-control
- Exemples de politiques de confidentialité de playtest publiées par des studios (Remedy, Eidos Montréal, Larian), consultées en 2026, à titre d'illustration et non de modèle juridique.
- Règlement (UE) 2016/679, RGPD.
