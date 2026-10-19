# Processus et prototypage

> **En bref** : comment passer d'une idée à un jeu jouable sans se perdre — prototypes ciblés qui répondent à une question, vertical slice, MVP, gestion du scope, itération, et règles spécifiques aux game jams. Le principe directeur : réduire le risque le plus tôt possible en jouant, pas en documentant.

## Quand consulter cette fiche

- Tu démarres un nouveau jeu ou une nouvelle mécanique.
- Tu dois décider quoi construire en premier.
- Le projet grossit et la date de fin recule.
- Tu participes à une game jam.
- On te demande d'« ajouter une feature » et tu dois évaluer son coût et son intérêt.

---

## 1. Étapes d'un projet

| Phase | But | Livrable | Durée relative (heuristique) |
|---|---|---|---|
| **Conception initiale** | Formuler l'expérience visée, le public, la contrainte | [GDD une page](templates/gdd-une-page.md) | Courte |
| **Prototypage** | Trouver le fun, réduire les risques majeurs | Prototypes jetables, chacun répondant à une question | Autant que nécessaire pour valider la boucle |
| **Pré-production** | Fixer les piliers, les pipelines, le scope | Vertical slice | Moyenne |
| **Production** | Fabriquer le contenu | Jeu complet en *alpha* (tout est là, pas fini) puis *beta* (fini, à polir) | La plus longue |
| **Polish / finition** | Ressenti, bugs, équilibrage, accessibilité | Release candidate | Toujours plus longue que prévu |
| **Après sortie** | Correctifs, mises à jour | Patchs | Variable |

Règle : **ne pas passer en production** tant que la boucle centrale n'est pas amusante en prototype. Le contenu ne répare pas une boucle faible.

## 2. Le prototype : répondre à une question

Un prototype est une **expérience** : il répond à une question précise, puis on le jette (ou on le garde comme référence).

Formuler la question avant de prototyper :
- « Le grappin est-il amusant à utiliser pour se déplacer ? »
- « Le joueur comprend-il qu'il peut pousser les ennemis dans le vide ? »
- « Un tour de jeu dure-t-il moins de 2 minutes ? »
- « Le moteur tient-il 500 ennemis à l'écran ? »

Types de prototypes :

| Type | Répond à | Outils | Coût |
|---|---|---|---|
| **Papier** | Règles, économie, tours, cartes, équilibre de base | Papier, cartes, dés, tableur | Très faible |
| **Gris** (*greybox*) | Ressenti, contrôles, espace, rythme | Primitives géométriques dans le moteur | Faible |
| **Technique** | Faisabilité, performance | Code isolé | Variable |
| **Visuel / ambiance** | Direction artistique, ton | Mockups, concept art, scène fixe | Faible à moyen |
| **Narratif** | Structure, embranchements | Twine, Ink, document | Faible |

Règles :
- **Un prototype = une question.** Ne pas mélanger « est-ce amusant ? » et « est-ce beau ? ».
- **Rapide et sale** : code jetable, pas d'architecture, pas d'assets finaux. Viser des heures ou des jours, pas des semaines.
- **Assets de remplacement** clairement reconnaissables comme tels.
- **Exposer les paramètres** (vitesse, gravité, dégâts) pour les ajuster en jouant.
- **Jouer soi-même puis faire jouer** quelqu'un d'autre dès que possible.
- **Conserver les conclusions** (une ligne par prototype : question, réponse, décision) même si le code est jeté.
- Prototyper d'abord le **risque le plus grand** : ce qui, s'il ne marche pas, tue le projet.

## 3. Vertical slice et MVP

- **Vertical slice** : une portion courte du jeu (un niveau, 10–20 minutes) **à qualité finale** sur tous les plans : gameplay, art, son, UI. Prouve que l'équipe sait produire le jeu au niveau visé et sert à estimer le coût du reste.
- **MVP** (*minimum viable product*) : la plus petite version du jeu complète et jouable de bout en bout qui délivre l'expérience essentielle. Utile pour tester une sortie anticipée ou valider un concept auprès de joueurs.
- **Horizontal slice** (variante) : tout le jeu de bout en bout, à qualité minimale. Utile pour valider la structure et le rythme global.

Choisir :
- Doute sur la **qualité atteignable** ou sur le coût de production → vertical slice.
- Doute sur la **structure globale** ou la durée → horizontal slice.
- Doute sur l'**intérêt du public** → MVP / démo.

## 4. Gestion du scope

Le scope est la première cause d'échec des projets de jeu. Règles :
- **Piliers** : 3 à 5 phrases qui définissent l'expérience. Toute feature doit servir au moins un pilier ; sinon, elle est coupée.
- **Classer les features** : indispensable / important / bonus (méthode MoSCoW ou équivalent). Construire d'abord tous les indispensables à bas niveau de qualité avant d'en polir un seul.
- **Estimer puis multiplier** : les estimations initiales sont systématiquement trop optimistes. Prévoir une marge importante, surtout pour le polish, l'intégration et la correction de bugs.
- **Couper tôt** : couper une feature au début coûte peu ; la couper à la fin gaspille le travail fait.
- **Réutiliser** : chaque asset, mécanique et système doit servir plusieurs fois (variantes d'ennemis, recombinaison de salles).
- **Contenu vs systèmes** : un système qui génère de la variété (procédural, combinatoire) peut réduire le besoin en contenu fait main, mais demande plus de conception et d'équilibrage.
- Questions avant d'ajouter une feature :
  1. Quel pilier sert-elle ?
  2. Que coûte-t-elle (conception, code, assets, tests, équilibrage, UI, tutoriel, localisation) ?
  3. Que se passe-t-il si on ne la fait pas ?
  4. Peut-on obtenir 80 % de l'effet avec une version plus simple ?

## 5. Itération

Cycle de base : **concevoir → construire → tester → analyser → recommencer.**

- Raccourcir le cycle autant que possible : rechargement à chaud, paramètres modifiables en jeu, raccourcis de debug (téléportation, invincibilité, spawn d'ennemis, saut de niveau).
- Changer **une chose à la fois** quand on cherche la cause d'un problème.
- Garder une trace des changements de paramètres et de leur effet observé.
- Savoir quand **arrêter d'itérer** : quand les changements n'améliorent plus le ressenti en playtest, ou quand le coût dépasse le gain. Le polish infini est un piège.
- Itérer sur ce qui est **le plus joué** en priorité : la boucle d'action et les premières minutes.

## 6. Game jam

Contraintes : 24 à 72 h typiquement, souvent un thème imposé.

- **Heure 0–2** : choisir une idée **petite**. Diviser son ambition par deux, puis encore par deux. Une mécanique, un niveau ou une salle, une fin.
- **Avoir la boucle jouable à mi-parcours** au plus tard (souvent bien avant) ; le reste du temps sert au contenu, au ressenti et au polish.
- **Le ressenti compte énormément** en jam : les joueurs testent quelques minutes. Juice, son, retour clair (voir [Game feel](../ressenti/game-feel-juice.md)).
- **Le son** est souvent oublié et fait une grosse différence : prévoir du temps (générateurs type sfxr/jsfxr/Bfxr pour aller vite).
- **Écran titre, instructions minimales, condition de fin, bouton recommencer** : indispensables, souvent oubliés.
- **Builder tôt et souvent** pour la plateforme cible (web, Windows) : les problèmes d'export arrivent toujours au dernier moment.
- **Livrer à l'avance** : soumettre une version jouable plusieurs heures avant la fin, puis mettre à jour.
- Pas de nouvelle technologie inconnue en jam, sauf si l'apprendre est le but.

## 7. Pièges classiques

| Piège | Symptôme | Remède |
|---|---|---|
| Documenter au lieu de prototyper | GDD de 50 pages, rien de jouable | Prototype gris en premier |
| Architecture prématurée | Semaines de « moteur » avant de jouer | Code jetable pour le prototype ; refactorer une fois la boucle validée |
| Polir trop tôt | Un niveau magnifique, le reste inexistant | Tout en qualité basse d'abord |
| Feature creep | La liste des features grandit chaque semaine | Piliers + coupe systématique |
| Ne pas faire tester | « C'est évident » pour l'équipe | Playtest externe régulier (voir [Playtest et métriques](playtest-et-metriques.md)) |
| Ignorer les retours | Les mêmes remarques reviennent | Tableau des problèmes récurrents, traités en priorité |
| Contenu avant systèmes | Des dizaines de niveaux sur une mécanique qui change | Figer la mécanique avant de produire en masse |
| Sous-estimer la fin | Menus, sauvegardes, options, export, bugs | Les planifier dès la pré-production |
| Tout en même temps | Dix systèmes à moitié faits | Finir une chose avant d'en commencer une autre |

---

## Checklist

- [ ] L'expérience visée et 3–5 piliers sont écrits (GDD une page).
- [ ] Le risque principal du projet est identifié et a son prototype.
- [ ] Chaque prototype a une question écrite et une conclusion consignée.
- [ ] La boucle centrale a été jugée amusante en prototype avant la production.
- [ ] Les features sont classées indispensable / important / bonus.
- [ ] Les paramètres de gameplay sont modifiables sans recompiler.
- [ ] Des outils de debug existent (téléportation, invincibilité, spawn, saut de niveau).
- [ ] Menus, sauvegarde, options et export sont planifiés.
- [ ] Un build pour la plateforme cible a été produit tôt.
- [ ] Des playtests externes sont planifiés à intervalles réguliers.

## Pistes d'implémentation

- **Paramètres exposés** : centraliser les valeurs de réglage (*tuning*) dans des fichiers de données (JSON, CSV, assets) rechargeables à chaud. UE5 : `DataAsset`, `DataTable`, console variables (`CVar`). Godot : `Resource` exportées et `@export`. Unity : `ScriptableObject`, `[SerializeField]`.
- **Menu de debug** in-game (ImGui ou équivalent, ou overlay simple) pour modifier les paramètres en jouant.
- **Contrôle de version dès le premier jour** (git, avec LFS pour les assets binaires lourds) ; un commit par prototype ou étape.
- **Build automatique** dès que possible pour la plateforme cible.
- Pour un agent IA : avant d'implémenter une feature, vérifier qu'elle sert un pilier du GDD ; si aucun GDD n'existe, proposer d'en écrire un avec le [template](templates/gdd-une-page.md).

## Voir aussi

- [Playtest et métriques](playtest-et-metriques.md)
- [Template GDD une page](templates/gdd-une-page.md)
- [Template fiche mécanique](templates/fiche-mecanique.md)
- [Boucles de gameplay](../fondamentaux/boucles-de-gameplay.md)
- [Principes de conception](../fondamentaux/principes-de-conception.md)

## Sources

- Tracy Fullerton, *Game Design Workshop: A Playcentric Approach to Creating Innovative Games*, CRC Press (4ᵉ éd. 2018).
- Chris Hecker & Chaim Gingold, « Advanced Prototyping », conférence GDC 2006.
- Kyle Gabler, Kyle Gray, Matt Kucic, Shalin Shodhan, « How to Prototype a Game in Under 7 Days », Gamasutra, 2005 (Experimental Gameplay Project).
- Derek Yu, *Spelunky*, Boss Fight Books, 2016 (chapitres sur la finition d'un projet).
- Eric Ries, *The Lean Startup*, Crown Business, 2011 (notion de MVP).
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, 2008 (3ᵉ éd. 2019).
