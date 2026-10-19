# Boucles de gameplay

> **En bref** : comment décrire, construire et diagnostiquer les boucles d'un jeu — de la boucle d'action de quelques secondes (*core loop*) jusqu'à la méta-progression sur plusieurs heures. Une boucle saine fait que chaque répétition apprend quelque chose au joueur ou change son état ; une boucle malade se répète sans rien produire d'autre qu'une récompense.

## Quand consulter cette fiche

- Tu démarres un projet et dois formuler « ce que fait le joueur » en une phrase.
- Tu ajoutes un système (craft, upgrades, monnaie) et dois vérifier qu'il se branche sur la boucle centrale.
- Le joueur décroche après 10 minutes ou après quelques heures, sans raison évidente.
- Le jeu « fonctionne » mais semble répétitif ou vide.
- On te demande un GDD ou un pitch : la description des boucles en est le cœur.

---

## 1. Vocabulaire

| Terme | Échelle de temps typique | Question à laquelle elle répond | Exemple (roguelite d'action) |
|---|---|---|---|
| **Verbe** | Instant | Que peut faire le joueur ? | Tirer, esquiver, ramasser |
| **Boucle d'action** (*moment-to-moment*) | 1–30 s | Que fait le joueur en ce moment ? | Repérer un ennemi → esquiver son attaque → riposter |
| **Boucle centrale** (*core loop*) | 30 s – quelques minutes | Que fait-il encore et encore ? | Nettoyer une salle → choisir une récompense → salle suivante |
| **Boucles secondaires** | Minutes | Qu'est-ce qui enrichit ou varie la boucle centrale ? | Boutique, salles défi, événements |
| **Méta-boucle** (*meta loop*) | Session à plusieurs heures | Pourquoi revient-il ? | Mourir → dépenser la monnaie persistante → débloquer → relancer un run |
| **Arc** (*arc*) | Contenu consommé une fois | Qu'est-ce qui progresse sans se répéter ? | Histoire, boss uniques, révélations |

Les boucles s'**emboîtent** : une itération de la boucle centrale contient plusieurs boucles d'action ; une itération de méta-boucle contient plusieurs boucles centrales. Daniel Cook distingue les **boucles** (répétées, apprentissage par itération) des **arcs** (consommés une seule fois, apprentissage par exposition) : la plupart des jeux combinent les deux.

## 2. Anatomie d'une boucle

Toute boucle peut s'écrire en quatre temps :

```
Intention   → le joueur se fixe un but (même implicite : « je veux cette pièce »)
Action      → il agit avec ses verbes
Retour      → le jeu répond (feedback immédiat + changement d'état)
Évaluation  → il interprète le résultat, met à jour son modèle mental, choisit la suite
```

Une boucle n'est pas qu'un cycle de récompense : c'est un **cycle d'apprentissage**. Le joueur doit sortir de chaque itération avec un modèle mental légèrement plus juste (« ce type d'ennemi recule quand je le touche »). Quand il n'y a plus rien à apprendre, la boucle s'épuise (voir Koster dans [Cadres théoriques](cadres-theoriques.md)).

### Décrire une boucle (format recommandé)

Écrire chaque boucle sous forme de chaîne verbe → résultat → ressource :

```
[Explorer] → trouve [ressources] → [Crafter] → obtient [équipement] → [Combattre] des ennemis plus forts → accède à [zones plus riches] → (retour à Explorer)
```

Pour chaque flèche, vérifier : *quelle décision le joueur prend-il ici ?* Une flèche sans décision est une étape automatique — acceptable si elle est courte, problématique si elle prend du temps.

## 3. Les verbes du joueur

- Lister les **verbes** (actions disponibles) avant toute autre chose. Un jeu se définit d'abord par ce que le joueur *fait*, pas par son thème.
- Viser **peu de verbes, beaucoup d'interactions** : 3 à 6 verbes de base qui se combinent valent mieux que 20 verbes isolés. Mario : courir et sauter, mais sauter sur un ennemi, sur une carapace, contre un mur, etc.
- Chaque verbe doit avoir **au moins deux usages** (déplacement + attaque, défense + positionnement). Un verbe qui ne sert qu'à une chose est candidat à la suppression ou à la fusion.
- Distinguer verbes **primaires** (utilisés en permanence, doivent être parfaits au toucher — voir [Contrôles et mouvement](../ressenti/controles-et-mouvement.md)) et verbes **secondaires** (contextuels, menus, gestion).
- Test rapide : si on retire ce verbe, la boucle centrale tient-elle encore ? Si oui, il est secondaire ou superflu.

## 4. Boucle de maîtrise vs boucle de compulsion

| | Boucle de maîtrise (*mastery loop*) | Boucle de compulsion (*compulsion loop*) |
|---|---|---|
| Moteur | Le joueur devient meilleur | Le joueur reçoit une récompense |
| Ce qui progresse | La compétence du joueur | Les chiffres du personnage / du compte |
| Récompense | Intrinsèque (comprendre, réussir) | Extrinsèque (loot, XP, monnaie) |
| Signe de santé | Le joueur rejoue « pour faire mieux » | Le joueur rejoue « pour avoir le prochain » |
| Risque | Plafond de frustration, barrière d'entrée | Lassitude, sentiment de manipulation, dépendance aux chiffres |
| Exemples | Jeux de combat, plateformes de précision, speedrun | Loot shooters, idle games, gacha |

Règles :
- La plupart des bons jeux **combinent** les deux : la récompense extrinsèque sert de **signal** et de **jalon** pour une maîtrise réelle (le loot rare récompense un boss difficile).
- Si la récompense extrinsèque est la **seule** raison de répéter l'action, la boucle est fragile : dès que la récompense ralentit, le joueur part.
- Éviter les mécanismes conçus pour exploiter la compulsion (récompenses aléatoires payantes, timers punitifs, FOMO) sauf choix assumé et documenté ; ils dégradent la confiance et posent des problèmes éthiques et légaux (loot boxes réglementées dans certains pays).
- Une récompense extrinsèque doit **changer la manière de jouer** (nouvelle option, nouveau verbe, nouvelle stratégie), pas seulement un chiffre. +5 % de dégâts est une récompense faible ; « mes balles rebondissent » en est une forte.

## 5. Relier les boucles entre elles

- Chaque boucle secondaire doit **produire ou consommer** quelque chose que la boucle centrale utilise. Une boucle déconnectée (mini-jeu sans impact) est perçue comme du remplissage.
- La méta-boucle doit **réinjecter de la nouveauté** dans la boucle centrale (déblocages qui changent les runs), pas seulement la rendre plus facile.
- Vérifier le **sens des flux** : ressources gagnées dans une boucle → dépensées dans une autre. Voir [Économie](../systemes/economie.md) pour sources/puits.
- Une boucle doit pouvoir être **interrompue proprement** : la fin d'une itération est un bon point de sauvegarde et de pause naturelle. Pour un jeu mobile ou de session courte, caler la boucle centrale sur la durée de session visée.

## 6. Diagnostiquer une boucle

| Symptôme | Cause probable | Piste |
|---|---|---|
| « C'est répétitif » dès les premières minutes | Pas de variation dans la boucle d'action ; aucune décision | Ajouter de la variété de situations (ennemis, terrains) plutôt que de nouveaux verbes ; introduire des choix avec compromis |
| Ennui après quelques heures | Le joueur a « résolu » la boucle (stratégie dominante) | Équilibrage, nouvelles contraintes, variantes (voir [Équilibrage](../systemes/equilibrage-et-difficulte.md)) |
| Le joueur ne comprend pas quoi faire | Intention non communiquée ; but invisible | Rendre l'objectif suivant lisible en permanence ; signposting |
| Le joueur fait les choses mais n'y prend pas plaisir | Retour faible : action sans feedback | Travailler le ressenti (voir [Game feel](../ressenti/game-feel-juice.md)) |
| Le joueur farme une seule activité | Une boucle est beaucoup plus rentable que les autres | Rééquilibrer les gains ; rendements décroissants |
| Les systèmes secondaires sont ignorés | Ils ne nourrissent pas la boucle centrale | Les brancher sur une ressource utile ou les supprimer |
| Le joueur arrête dès que les récompenses ralentissent | Boucle portée uniquement par l'extrinsèque | Renforcer la maîtrise et la variété intrinsèque |
| La boucle centrale est longue et creuse | Trop d'étapes sans décision (trajets, attentes) | Raccourcir, automatiser ou rendre ces étapes interactives |

Questions de diagnostic à se poser :
1. Quelle est la décision la plus intéressante prise dans une itération ? (S'il n'y en a pas : problème.)
2. Qu'est-ce qui distingue la 10ᵉ itération de la 1ʳᵉ ? (Si rien : problème de profondeur ou de variété.)
3. Qu'est-ce que le joueur apprend en répétant ?
4. Combien de temps entre deux décisions significatives ?
5. Si on supprimait toute récompense chiffrée, l'action resterait-elle agréable ?

## 7. Anti-patterns

- **Boucle sans fin d'apprentissage** : la même action, sans variation, avec un chiffre qui monte. Fonctionne sur un public très ciblé (idle), lasse partout ailleurs.
- **Méta qui remplace le jeu** : la méta-progression est plus intéressante que le run lui-même ; le joueur joue « pour débloquer », pas pour jouer.
- **Boucle de corvée** (*grind*) imposée pour accéder au contenu intéressant.
- **Boucle centrale cachée derrière un tutoriel long** : le joueur doit vivre la boucle complète le plus tôt possible (voir [Onboarding](../contenu/onboarding-tutoriels.md)).
- **Inflation de verbes** : ajouter des actions pour masquer une boucle pauvre au lieu d'enrichir les interactions entre verbes existants.

---

## Checklist

- [ ] Le jeu se résume en une phrase « le joueur [verbe], pour [but], en [contrainte] ».
- [ ] Les verbes primaires sont listés (3–6) et chacun a au moins deux usages.
- [ ] La boucle d'action, la boucle centrale et la méta-boucle sont écrites sous forme de chaîne verbe → résultat.
- [ ] Chaque flèche de la boucle centrale contient une décision ou est courte.
- [ ] Chaque boucle secondaire produit ou consomme une ressource de la boucle centrale.
- [ ] Les récompenses changent la façon de jouer, pas seulement des chiffres.
- [ ] La boucle complète est vécue par le joueur dans les premières minutes.
- [ ] Il existe un point de pause naturel à la fin d'une itération de boucle centrale.
- [ ] On sait ce qui rend la 10ᵉ itération différente de la 1ʳᵉ.

## Pistes d'implémentation

- Modéliser explicitement la boucle centrale comme une **machine à états de haut niveau** (`Exploration → Combat → Récompense → Exploration`) : facilite le debug, les sauvegardes et la télémétrie (temps passé par état, voir [Playtest et métriques](../production/playtest-et-metriques.md)).
- Instrumenter dès le prototype : compter les itérations de boucle par session, la durée moyenne d'une itération et l'endroit où les sessions s'arrêtent.
- Garder les paramètres de rythme (durée de salle, quantité de récompense, coût des déblocages) dans des **données éditables** (tables, assets de données) et non dans le code, pour itérer vite.
- UE5 : `GameMode`/`GameState` pour l'état de la boucle centrale, `DataTable`/`DataAsset` pour les paramètres. Godot : autoload pour l'état global, `Resource` pour les données. Unity : `ScriptableObject` pour les données.

## Voir aussi

- [Cadres théoriques](cadres-theoriques.md) — MDA, flow, motivation
- [Principes de conception](principes-de-conception.md) — choix intéressants, profondeur
- [Progression](../systemes/progression.md) et [Économie](../systemes/economie.md) — méta-boucle et flux de ressources
- [Game feel / juice](../ressenti/game-feel-juice.md) — qualité du retour dans la boucle d'action
- [Template fiche mécanique](../production/templates/fiche-mecanique.md)

## Sources

- Daniel Cook, « The Chemistry of Game Design », Gamasutra, 2007 ; « Loops and Arcs », blog *Lostgarden*, 2012.
- Raph Koster, *A Theory of Fun for Game Design*, Paraglyph Press, 2004 (2ᵉ éd. O'Reilly, 2013).
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, CRC Press, 2008 (3ᵉ éd. 2019).
- Tracy Fullerton, *Game Design Workshop: A Playcentric Approach to Creating Innovative Games*, CRC Press (4ᵉ éd. 2018).
- Scott Rigby & Richard M. Ryan, *Glued to Games: How Video Games Draw Us In and Hold Us Spellbound*, Praeger, 2011.
