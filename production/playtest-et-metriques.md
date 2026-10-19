# Playtest et métriques

> **En bref** : comment organiser un playtest utile, observer sans influencer, poser les bonnes questions, éviter les biais, et compléter l'observation par de la télémétrie (métriques, funnels, heatmaps). Principe central : les joueurs repèrent très bien **ce qui ne va pas**, mais leurs solutions proposées sont rarement les bonnes — c'est au concepteur de trouver la cause.

## Quand consulter cette fiche

- Tu dois faire tester le jeu et ne sais pas comment t'y prendre.
- Les retours de testeurs se contredisent ou ne mènent à rien.
- Tu dois décider quelles données de télémétrie enregistrer.
- Tu veux savoir où et pourquoi les joueurs abandonnent.
- Un testeur propose une solution et tu dois décider quoi en faire.

---

## 1. Préparer un playtest

**Définir l'objectif** : 1 à 3 questions précises par session.
- « Les joueurs comprennent-ils comment utiliser le bouclier sans tutoriel ? »
- « Combien de temps pour finir le niveau 2 ? Où meurent-ils ? »
- « Le boss est-il perçu comme juste ? »

**Choisir les testeurs** :
- Proches du **public cible** (genre habituel, niveau d'expérience, motivations : voir [Profils de joueurs](../fondamentaux/profils-de-joueurs.md)).
- **Nouveaux** testeurs pour tester la compréhension et l'onboarding : un testeur qui a déjà joué ne peut plus « désapprendre ».
- Testeurs **récurrents** pour tester la profondeur, l'équilibrage et la progression longue.
- L'équipe et les proches sont de mauvais testeurs pour la compréhension (biais de connaissance, biais de bienveillance).
- Nombre : pour les problèmes d'utilisabilité, un petit nombre de testeurs (5 environ par itération, règle issue de l'UX logicielle, Nielsen) révèle la majorité des problèmes majeurs ; mieux vaut plusieurs petites sessions itératives qu'une grosse.

**Préparer le build** : stable, avec télémétrie active, enregistrement vidéo de l'écran (et si possible du visage et des mains / manette), point de départ prévu. La liste complète des points à vérifier est dans [Rendre un jeu playtestable](rendre-un-jeu-playtestable.md) ; le [plan de playtest](templates/plan-playtest.md) sert de feuille de préparation.

## 2. Pendant la session : observer sans guider

Règles d'or :
- **Ne pas aider.** Ne pas expliquer, ne pas montrer, ne pas pointer l'écran. Si le joueur est bloqué, c'est une donnée. Fixer à l'avance un seuil (ex. plusieurs minutes de blocage) au-delà duquel on intervient, et le noter.
- **Ne pas se justifier** ni défendre le jeu.
- **Prendre des notes horodatées** : ce que le joueur fait, dit, et son expression (hésitation, sourire, soupir, se penche en avant).
- **Observer le comportement plus que les paroles** : ce que les joueurs font est plus fiable que ce qu'ils disent.
- **Protocole « penser à voix haute »** (*think aloud*) : demander au joueur de verbaliser ce qu'il pense et essaie de faire. Utile pour la compréhension ; perturbe le ressenti et le timing, donc à éviter pour juger la difficulté ou l'immersion.
- Si on doit relancer : questions neutres (« Qu'essaies-tu de faire ? », « Qu'attends-tu qu'il se passe ? »), jamais suggestives (« Tu as vu le levier ? »).

Signaux à noter :
| Signal | Indique souvent |
|---|---|
| Hésitation longue | Objectif ou action peu clairs |
| Essais répétés de la même action | Retour insuffisant ou affordance trompeuse |
| Ignorer un élément important | Lisibilité, hiérarchie visuelle |
| Morts répétées au même endroit | Pic de difficulté, danger mal annoncé |
| Regarder ailleurs, téléphone | Ennui, temps mort |
| Se pencher en avant, silence concentré | Engagement |
| Rire, exclamation | Moment marquant (positif ou frustration) |
| Utiliser une stratégie unique | Stratégie dominante, ou autres options non comprises |

## 3. Après la session : questions à poser

Entretien court, questions ouvertes d'abord, fermées ensuite.

Questions ouvertes :
- « Raconte-moi ce que tu viens de jouer. » (révèle ce qui a été compris et retenu)
- « Qu'est-ce qui t'a le plus plu ? Le moins plu ? »
- « Y a-t-il un moment où tu ne savais pas quoi faire ? »
- « Y a-t-il un moment où tu t'es senti injustement puni ? »
- « Si tu pouvais changer une seule chose, ce serait quoi ? » (utile pour repérer le problème, pas pour la solution)
- « À qui recommanderais-tu ce jeu ? »

Questions fermées / échelles (1 à 5 ou 1 à 7) : difficulté perçue, clarté des objectifs, envie de continuer, ressenti des contrôles.

Questions de compréhension : « Comment fonctionne [mécanique] ? » — comparer la réponse au fonctionnement réel.

Éviter :
- Les questions suggestives (« Tu as trouvé le combat dynamique ? »).
- Les questions hypothétiques (« Achèterais-tu ce jeu ? » — peu prédictif).
- Demander de juger des features non jouées.

## 4. Interpréter les retours

« Les joueurs savent ce qui ne va pas, pas comment le réparer. » (idée formulée notamment par Mark Rosewater, et sous une forme proche par Neil Gaiman à propos de l'écriture.)

- **Le ressenti est une donnée fiable** : « c'est frustrant », « je m'ennuie ici » est vrai pour ce joueur.
- **Le diagnostic et la solution proposés sont des hypothèses** : « il faut plus de munitions » peut signifier « les ennemis sont trop résistants », « je ne vois pas les munitions au sol » ou « je ne comprends pas que je peux esquiver ».
- Pour chaque retour : **remonter à la cause** (que s'est-il passé juste avant ? qu'a observé l'enregistrement ?) avant de choisir une solution.
- **Regrouper** les retours par problème, compter les occurrences, classer par gravité × fréquence.
- **Un retour isolé** peut être une préférence personnelle ; **le même retour chez plusieurs testeurs** est un problème.
- **Se méfier du retour du concepteur** : on connaît trop le jeu pour juger la compréhension.
- Distinguer **« je n'aime pas »** (goût, public) de **« je n'ai pas compris »** (problème de conception à corriger).

Gravité (exemple d'échelle) :
| Niveau | Définition | Action |
|---|---|---|
| Bloquant | Empêche de progresser ou fait quitter | Corriger avant le prochain test |
| Majeur | Frustration forte, compréhension erronée d'une mécanique clé | Corriger en priorité |
| Mineur | Gêne, confusion passagère | Planifier |
| Cosmétique | Remarque de goût, détail | Noter |

## 5. Biais à connaître

| Biais | Effet | Parade |
|---|---|---|
| Bienveillance / désirabilité sociale | Les testeurs sont gentils, surtout devant le créateur | Observer le comportement ; questionnaire anonyme ; testeur qui ne connaît pas l'équipe |
| Effet observateur | Le joueur se comporte différemment car observé | Sessions longues, observateur discret, télémétrie |
| Malédiction du savoir (concepteur) | « C'est évident » | Testeurs neufs uniquement pour la compréhension |
| Biais de confirmation | On retient ce qui confirme l'idée | Questions écrites à l'avance, critères de succès définis avant |
| Échantillon non représentatif | Amis, collègues, experts du genre | Recruter selon le public cible |
| Effet de nouveauté | Tout plaît la première fois | Sessions répétées pour juger la durée de vie |
| Rationalisation a posteriori | Le joueur invente une raison à son comportement | Croiser déclaratif et observation |

## 6. Télémétrie et métriques

La télémétrie dit **quoi** et **où** ; le playtest observé dit **pourquoi**. Les deux sont complémentaires.

### Événements à enregistrer en priorité
- Début et fin de session (durée, raison de fin si connue).
- Début, fin, abandon de niveau / run / mission.
- Mort ou échec : position, cause (ennemi, piège, chute), temps écoulé, état du joueur.
- Choix du joueur : armes, talents, chemins, options de dialogue, achats.
- Utilisation des mécaniques (fréquence de chaque verbe).
- Ouverture des menus, de l'aide, des options d'accessibilité et de difficulté.
- Économie : gains et dépenses par ressource.
- Performance : FPS, temps de chargement, crashs.

Chaque événement : horodatage, identifiant de session (anonyme), version du build, position, contexte minimal.

### Métriques utiles
| Métrique | Sert à repérer |
|---|---|
| Taux de complétion par niveau / étape | Points de décrochage |
| Taux de mort et causes par zone | Pics de difficulté, dangers illisibles |
| Temps par niveau / étape | Rythme, zones de blocage |
| Taux de sélection des options (armes, talents) | Stratégies dominantes, options inutiles |
| Durée de session moyenne et médiane | Adéquation avec la session visée |
| Rétention (J1, J7, J30) | Intérêt à long terme (jeux service, mobile) |
| Utilisation de chaque verbe | Mécaniques ignorées ou incomprises |
| Courbe de ressources dans le temps | Inflation, pénurie (voir [Économie](../systemes/economie.md)) |

Préférer la **médiane** à la moyenne pour les durées (les valeurs extrêmes faussent la moyenne) et regarder les distributions.

### Funnels (entonnoirs)
Suite d'étapes ordonnées ; on mesure le pourcentage de joueurs qui atteint chaque étape.

```
Lancement → Fin tutoriel → Niveau 1 terminé → Niveau 2 terminé → Premier boss → ...
  100 %        85 %             70 %               40 %  ← chute à investiguer
```

Une chute brutale entre deux étapes indique un problème localisé (difficulté, confusion, bug, longueur). Investiguer avec un playtest observé ciblé sur ce passage.

### Heatmaps
Cartes de densité positionnelles : morts, positions, trajets, temps passé.
- Morts concentrées : danger mal annoncé ou pic de difficulté.
- Zones jamais visitées : contenu invisible ou peu attractif (voir [Level design](../contenu/level-design.md)).
- Trajets inattendus : raccourcis, exploits, signposting trompeur.
- Temps élevé sans progression : joueur perdu.

### Pièges de la télémétrie
- Mesurer tout sans question : beaucoup de données, aucune décision. Partir des questions.
- Optimiser une métrique au détriment de l'expérience (rétention par la culpabilisation, durée de session par la corvée).
- Conclure sans contexte : un taux de mort élevé peut être voulu (jeu exigeant).
- Respect de la vie privée : anonymiser, minimiser, informer le joueur, respecter le RGPD et les règles des plateformes ; consentement si nécessaire.

---

## Checklist

- [ ] Chaque session de playtest a 1–3 questions écrites et des critères de succès définis à l'avance.
- [ ] Les testeurs correspondent au public cible ; des testeurs neufs pour la compréhension.
- [ ] Les sessions sont enregistrées (écran au minimum) avec notes horodatées.
- [ ] L'observateur n'aide pas et n'explique pas pendant la session.
- [ ] L'entretien commence par des questions ouvertes non suggestives.
- [ ] Les retours sont regroupés par problème, comptés et classés par gravité.
- [ ] Pour chaque problème, la cause est identifiée avant de choisir une solution.
- [ ] La télémétrie enregistre au minimum : sessions, progression, morts (position + cause), choix.
- [ ] Un funnel de progression existe et est relu après chaque campagne de tests.
- [ ] Les données sont anonymisées et la collecte est conforme aux règles applicables.
- [ ] Les résultats sont consignés dans un [rapport de playtest](templates/rapport-playtest.md).

## Pistes d'implémentation

- **Système d'événements central** : une fonction unique `Telemetry.log(event_name, params)` appelée partout ; écriture dans un fichier local (JSON lines / CSV) pour les prototypes, envoi serveur plus tard. Inclure la version du build dans chaque événement.

```
Telemetry.log("player_death", {
  session: session_id, build: BUILD_VERSION, level: "L2",
  pos: player.position, cause: "spike_trap", t_level: 83.4
})
```

- **Heatmaps** : exporter les positions et les projeter sur une capture vue de dessus du niveau (script Python + matplotlib, ou outil interne dans le moteur).
- **Replays** : enregistrer les entrées (si la simulation est déterministe) permet de rejouer exactement une session problématique.
- UE5 : `Analytics` plugin et *Analytics Providers* ; Unity : Unity Analytics / solutions tierces ; Godot : pas de solution intégrée, écrire un logger simple. Pour un jeu web : requêtes HTTP vers un petit service de collecte.
- Pour un agent IA : quand une nouvelle mécanique est implémentée, ajouter les événements de télémétrie correspondants (utilisation, succès/échec) dans la même modification.

## Voir aussi

- [Rendre un jeu playtestable](rendre-un-jeu-playtestable.md)
- [Profils de joueurs](../fondamentaux/profils-de-joueurs.md)
- [Processus et prototypage](processus-et-prototypage.md)
- [Template plan de playtest](templates/plan-playtest.md)
- [Template rapport de playtest](templates/rapport-playtest.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)
- [Level design](../contenu/level-design.md)

## Sources

- Anders Drachen, Pejman Mirza-Babaei, Lennart Nacke (dir.), *Games User Research*, Oxford University Press, 2018.
- Magy Seif El-Nasr, Anders Drachen, Alessandro Canossa (dir.), *Game Analytics: Maximizing the Value of Player Data*, Springer, 2013.
- Celia Hodent, *The Gamer's Brain*, CRC Press, 2017.
- Tracy Fullerton, *Game Design Workshop*, CRC Press (4ᵉ éd. 2018) — chapitre sur le playtest.
- Jakob Nielsen, « Why You Only Need to Test with 5 Users », Nielsen Norman Group, 2000.
- Mark Rosewater, « Twenty Years, Twenty Lessons », conférence GDC 2016.
