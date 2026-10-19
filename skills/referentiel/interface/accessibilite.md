# Accessibilité

> **En bref** : rendre le jeu jouable par le plus grand nombre, y compris les joueurs en situation de handicap moteur, visuel, auditif ou cognitif. Synthèse des Game Accessibility Guidelines (niveaux basique, intermédiaire, avancé) et des Xbox Accessibility Guidelines, bonnes pratiques sur le daltonisme, les sous-titres, la difficulté, les flashs et le remapping, avec une checklist minimum viable.

## Quand consulter cette fiche

- Au début d'un projet : beaucoup de mesures coûtent peu si elles sont prévues tôt et cher si elles sont ajoutées à la fin.
- Tu crées le menu d'options.
- Tu ajoutes des effets de flash, de shake, des couleurs porteuses de sens, des QTE, du martelage de bouton.
- Tu écris des dialogues ou des sous-titres.
- Tu règles la difficulté ou ajoutes des assistances.

---

## 1. Principes

- **Le handicap est une interaction entre une personne et un environnement.** Une barrière dans le jeu peut être permanente (cécité), temporaire (bras cassé) ou situationnelle (bébé dans les bras, jeu sans son dans le métro). Les options d'accessibilité servent beaucoup plus de joueurs qu'on ne le pense.
- **Éviter les barrières inutiles** : la question n'est pas « faut-il rendre le défi facile ? » mais « ce qui rend le jeu difficile est-il le défi voulu, ou une barrière accidentelle ? » (lire un texte minuscule n'est pas le défi d'un jeu de plateforme).
- **Redondance des canaux** : toute information importante passe par au moins deux canaux parmi visuel, sonore, haptique.
- **Prévoir tôt** : architecture d'entrées abstraite (remapping), texte non intégré aux images, UI à taille variable, sons déclenchés par événements (légendes automatiques possibles).
- **Rendre les options trouvables** : proposer les réglages essentiels dès le premier lancement (taille du texte, sous-titres) et les rendre accessibles à tout moment en jeu.

---

## 2. Game Accessibility Guidelines (synthèse)

Les Game Accessibility Guidelines (GAG) classent les recommandations en trois niveaux selon le rapport effort / bénéfice. Résumé non exhaustif ; consulter le site pour la liste complète et les exemples.

### Basique (peu coûteux, large impact, à viser partout)

| Catégorie | Recommandations clés |
|---|---|
| Moteur | Remapping ou au minimum plusieurs schémas de contrôle ; commandes simples (éviter les combinaisons complexes) ; pas de martelage de bouton obligatoire ; sensibilité réglable ; interactions sans timing serré quand ce n'est pas le défi |
| Visuel | Taille de texte par défaut lisible ; contraste suffisant texte/fond ; pas d'information uniquement par la couleur ; éviter les motifs et flashs à risque |
| Auditif | Sous-titres pour toute parole importante ; volumes séparés (musique, effets, voix) ; pas d'information uniquement par le son |
| Cognitif | Choix de difficulté ; rappel des contrôles et des objectifs accessible à tout moment ; langage clair ; tutoriels ; pouvoir rejouer les tutoriels |
| Général | Options accessibles avant de jouer et en jeu ; sauvegarde fréquente / reprise facile ; jouer sans forcer la lecture rapide |

### Intermédiaire

- Remapping complet sur tous les périphériques ; maintien ↔ bascule pour les actions maintenues.
- Taille de texte réglable ; sous-titres réglables (taille, fond) avec nom du locuteur ; légendes pour les sons importants.
- Désactivation ou réduction du shake, du flou de mouvement, du *head bob* ; réglage du FOV.
- Indicateurs visuels pour les sons importants (direction).
- Vitesse de jeu réglable ou assistances (ralenti, aide à la visée).
- Marqueurs d'objectif et de chemin ; possibilité de passer les énigmes ou séquences bloquantes.
- Compatibilité avec les manettes adaptées (Xbox Adaptive Controller, etc.).

### Avancé

- Lecteur d'écran / synthèse vocale de l'UI et des textes.
- Audio description des cinématiques.
- Modes de jeu entièrement navigables à l'audio (signaux sonores de navigation).
- Contrôle à un seul bouton / balayage (*switch access*), saisie vocale.
- Langue des signes pour les cinématiques.

---

## 3. Xbox Accessibility Guidelines (XAG)

Microsoft publie les **Xbox Accessibility Guidelines**, un ensemble de recommandations numérotées par thème (texte, contraste, couleur, sous-titres, audio, remapping, difficulté, UI, cinématiques, etc.), avec objectifs, scénarios et critères de vérification. Elles s'appliquent bien au-delà de la Xbox et sont une bonne base pour une **grille d'audit**. Points notables :
- Taille de texte minimale recommandée et texte agrandissable.
- Sous-titres avec options de présentation et identification du locuteur.
- Remapping complet, maintien/bascule, réglage des temps d'entrée.
- Options de difficulté et d'assistance décrites clairement, sans jugement.
- Indication des fonctionnalités d'accessibilité dans la fiche du jeu (les joueurs veulent savoir avant d'acheter).

---

## 4. Par type de besoin

### 4.1 Moteur

- **Remapping complet** clavier, souris et manette, y compris les menus. Voir [Contrôles](../ressenti/controles-et-mouvement.md).
- **Maintien ↔ bascule** (viser, sprinter, s'accroupir, charger).
- **Pas de martelage obligatoire** : alternative en maintien ou automatique.
- **QTE** : option pour les rendre automatiques ou à maintien, fenêtre de timing plus large.
- Jouable **à une main** quand c'est possible (schéma de contrôle alternatif).
- Réglage de la sensibilité, des zones mortes, de l'aim assist.
- Fenêtres de timing élargies en option (parade, combo).

### 4.2 Visuel

- Texte lisible par défaut et agrandissable ; police simple ; fond derrière le texte.
- Contraste élevé pour les éléments importants ; option de mode contraste élevé (par exemple ennemis, objets interactifs et décor en couleurs unies distinctes).
- Réticule réglable (taille, couleur, forme).
- Agrandissement de l'UI / du HUD.
- Option de **réduction des mouvements** (shake, flou, head bob, FOV réglable). Voir [Caméra](../ressenti/camera.md).
- Narration de l'UI pour les joueurs malvoyants (avancé).

### 4.3 Daltonisme

- Le daltonisme rouge-vert concerne environ **8 % des hommes et 0,5 % des femmes** d'origine nord-européenne. Formes principales : deutéranopie / deutéranomalie (vert), protanopie / protanomalie (rouge), tritanopie (bleu-jaune, rare).
- **Règle principale : ne jamais porter une information par la couleur seule.** Ajouter forme, icône, motif, texte, position.
- Éviter les paires critiques rouge/vert, vert/marron, bleu/violet sans autre distinction.
- Les **filtres de daltonisme** plein écran sont une solution partielle : mieux vaut des **palettes alternatives** pour les éléments porteurs de sens (allié/ennemi, rareté, équipes).
- Tester avec un simulateur de daltonisme (outils de capture ou filtres moteur) sur les écrans clés.

### 4.4 Auditif

- **Sous-titres activés par défaut** ou proposés au premier lancement.
- **Légendes** pour les sons de gameplay importants (« [explosion au loin] »).
- Indicateurs visuels directionnels pour les sons importants.
- Volumes séparés, sortie mono.
- Ne pas encoder une information uniquement dans l'audio (alarme, dialogue d'indice). Voir [Audio](audio.md).

### 4.5 Cognitif

- Objectif actuel consultable à tout moment ; journal / résumé « précédemment ».
- Rappel des contrôles contextuel ; tutoriels rejouables.
- Langage simple dans l'UI ; termes cohérents.
- Pas de limite de temps sur la lecture des dialogues et des textes (avancer manuellement).
- Indicateurs de chemin ou d'objectif optionnels ; possibilité de passer une énigme.
- Éviter la surcharge d'informations simultanées. Voir [UI, UX et HUD](ui-ux-hud.md).

---

## 5. Sous-titres : bonnes pratiques

| Aspect | Recommandation |
|---|---|
| Activation | Proposés au premier lancement ou actifs par défaut |
| Taille | Lisible par défaut à distance de téléviseur, plusieurs tailles réglables |
| Fond | Fond semi-opaque derrière le texte, opacité réglable |
| Longueur | Deux lignes maximum à la fois ; lignes courtes (de l'ordre de 40 caractères, comme dans les normes de sous-titrage audiovisuel) |
| Locuteur | Nom du locuteur affiché (option), éventuellement couleur par personnage **en plus** du nom |
| Direction | Indication de direction pour un locuteur hors champ (flèche) |
| Légendes | Sons importants entre crochets, distinguables des dialogues |
| Durée | Affichés assez longtemps pour être lus ; ne pas avancer trop vite |
| Position | En bas de l'écran, à l'écart du HUD ; ne pas les mettre dans des bulles diégétiques illisibles |
| Fidélité | Le texte correspond à l'audio ; pas de censure ni de résumé non signalé |
| Couverture | Toute parole importante, y compris les répliques de combat et les cinématiques |

---

## 6. Difficulté et assistances

- **Plusieurs niveaux de difficulté** décrits par ce qu'ils changent (« les ennemis infligent moins de dégâts »), pas par des jugements (« mode bébé »).
- **Assistances granulaires** plutôt qu'un seul curseur : dégâts reçus, vitesse du jeu, invincibilité, sauts infinis, aide à la visée, fenêtre de parade, passer un combat ou une énigme. *Celeste* (« Assist Mode ») est une référence connue de cette approche.
- Pouvoir **changer la difficulté à tout moment** sans recommencer.
- Ne pas punir l'usage des assistances par des moqueries ; si des succès / trophées sont désactivés, le dire clairement.
- Voir [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md).

---

## 7. Épilepsie photosensible et flashs

- Éviter les flashs de forte luminosité, en particulier le **rouge saturé**, et les motifs rayés à fort contraste.
- Le WCAG fixe comme seuil de ne pas dépasser **trois flashs par seconde** (critère 2.3.1). L'analyse **Harding** (test « FPA ») est utilisée au Royaume-Uni pour la diffusion et par certains éditeurs ; elle s'appuie notamment sur la recommandation ITU-R BT.1702.
- Les flashs plein écran (explosion, éclair, `flashbang` dans [Game feel](../ressenti/game-feel-juice.md)) : opacité limitée, durée courte, **option de réduction ou de désactivation**.
- Afficher un avertissement de photosensibilité au lancement (pratique standard), mais il ne remplace pas la réduction du risque.
- Tester les séquences à risque (effets de particules stroboscopiques, éclairs, écrans de chargement clignotants).

---

## 8. Anti-patterns

- Options d'accessibilité dans un sous-menu profond, ou seulement accessibles depuis le menu principal.
- Remapping partiel (certaines actions figées) ou impossible pour les menus.
- Code couleur seul pour allié/ennemi, rareté, état.
- Sous-titres minuscules sans fond, sans nom de locuteur.
- QTE à martelage obligatoire sans alternative.
- Flashs plein écran stroboscopiques sans option.
- Libellés de difficulté moqueurs.
- Texte intégré aux images (ni agrandissable, ni traduisible, ni lisible par synthèse vocale).

---

## Checklist minimum viable

À viser pour tout projet, même un prototype destiné à être montré :

- [ ] Remapping des contrôles (au minimum plusieurs schémas, idéalement complet sur tous les périphériques).
- [ ] Option maintien ↔ bascule pour les actions maintenues.
- [ ] Pas de martelage de bouton obligatoire.
- [ ] Sous-titres disponibles (proposés au premier lancement), avec fond et taille réglable.
- [ ] Volumes séparés : musique, effets, voix.
- [ ] Taille de texte lisible par défaut ; texte sur fond.
- [ ] Aucune information portée uniquement par la couleur ou uniquement par le son.
- [ ] Réglage d'intensité du camera shake ; désactivation du flou de mouvement et du head bob.
- [ ] Flashs plein écran limités et réductibles ; moins de 3 flashs par seconde.
- [ ] Choix de difficulté décrit par ses effets, modifiable en cours de partie.
- [ ] Objectif actuel et contrôles consultables à tout moment.
- [ ] Options accessibles depuis le jeu (menu pause), pas seulement depuis le menu principal.

## Pistes d'implémentation

- **Agnostique** : une structure `AccessibilitySettings` centralisée et persistée (taille de texte, sous-titres, intensité de shake, flashs, palette, maintien/bascule…), lue par tous les systèmes. Les effets visuels (shake, flash) multiplient leur intensité par le réglage correspondant. Les sons de gameplay déclarés par événements peuvent porter une légende textuelle associée.
- **UE5** : CommonUI pour la navigation et la mise à l'échelle de l'UI ; Enhanced Input pour le remapping et les modificateurs maintien/bascule ; *Text-to-speech* via les plugins de plateforme ; filtres de daltonisme intégrés (`SetColorVisionDeficiencyType`).
- **Godot** : `Theme` pour la taille du texte, Input Map modifiable à l'exécution pour le remapping ; `DisplayServer.tts_speak()` pour la synthèse vocale.
- **Unity** : Input System (rebinding), UI Toolkit (mise à l'échelle, thèmes) ; package d'accessibilité / lecteur d'écran selon la version.

## Voir aussi

- [UI, UX et HUD](ui-ux-hud.md)
- [Audio](audio.md)
- [Contrôles et mouvement](../ressenti/controles-et-mouvement.md)
- [Caméra](../ressenti/camera.md)
- [Game feel / juice](../ressenti/game-feel-juice.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)

## Sources

- Game Accessibility Guidelines (Ellis, Ford, Hamilton, Lee, Shepherd, Thompson et al.), https://gameaccessibilityguidelines.com
- Microsoft, *Xbox Accessibility Guidelines*, https://learn.microsoft.com/gaming/accessibility/guidelines
- AbleGamers Foundation, *Includification: A Practical Guide to Game Accessibility*, 2012.
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.1*, critères 1.4.1 (Utilisation de la couleur), 1.4.3 (Contraste), 2.3.1 (Pas plus de trois flashs).
- ITU-R BT.1702, *Guidance for the reduction of photosensitive epileptic seizures caused by television*.
- Celia Hodent, *The Gamer's Brain*, CRC Press, 2017 (chapitres UX et accessibilité).
