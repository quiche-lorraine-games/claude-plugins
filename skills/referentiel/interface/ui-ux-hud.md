# UI, UX et HUD

> **En bref** : comment faire passer l'information du jeu au joueur sans le noyer. Hiérarchie de l'information, types d'interface (diégétique, non diégétique, spatiale, méta), feedback et états d'erreur, menus et navigation manette, lisibilité des chiffres, tooltips, affordances, et quelques lois de psychologie cognitive utiles (Fitts, Hick, charge cognitive).

## Quand consulter cette fiche

- Tu conçois ou ajoutes un élément de HUD (vie, munitions, mini-carte, objectifs).
- Tu crées un menu, un inventaire, un écran de compétences, une boutique.
- Le joueur « n'a pas vu » une information, ou il y a trop d'éléments à l'écran.
- Tu ajoutes le support manette à une interface conçue pour la souris (ou l'inverse).
- Tu affiches des chiffres (dégâts, stats, prix) ou des descriptions de règles.

---

## 1. Principes

- **L'UX, c'est l'expérience voulue par le designer telle que le joueur la vit réellement.** Le joueur ne lit pas la doc : il perçoit, il interprète, il retient peu (Hodent, *The Gamer's Brain*).
- **Chaque élément affiché doit répondre à une question du joueur** à ce moment précis : « suis-je en danger ? », « où aller ? », « puis-je faire cette action ? ».
- **Montrer, ne pas encombrer** : ce qui n'est pas utile maintenant se masque, se réduit ou apparaît au besoin (HUD contextuel).
- **Cohérence** : une couleur, une icône, une position = un sens, partout dans le jeu.
- **Ne jamais encoder une information uniquement par la couleur** (voir [Accessibilité](accessibilite.md)).
- **L'UI est de la présentation**, mais une information manquante ou illisible devient un problème de gameplay (le joueur ne peut pas faire de choix éclairé).

---

## 2. Hiérarchie de l'information

Classer chaque information selon **urgence** et **fréquence de consultation** :

| Niveau | Exemples | Traitement |
|---|---|---|
| Critique, immédiat | Vie basse, attaque imminente, munitions à 0 | Fort contraste, mouvement, son, près du centre d'attention |
| Important, fréquent | Vie, munitions, compétence prête | Position fixe en périphérie, toujours au même endroit |
| Contextuel | Prompt d'interaction, PV d'un ennemi ciblé | N'apparaît que quand c'est pertinent, près de l'objet concerné |
| Consultable | Stats détaillées, carte complète, journal | Écran ou panneau dédié, à la demande |

Règles :
- **Le regard du joueur est au centre** (sur son personnage ou le réticule) en jeu d'action. Les informations critiques doivent y apparaître ou y être signalées.
- Une information critique doit être **redondante** : visuel + son (+ vibration).
- Grouper ce qui est lié (vie et bouclier ensemble), séparer ce qui ne l'est pas (lois de la Gestalt : proximité, similarité).
- Limiter le nombre d'éléments animés simultanément : le mouvement attire l'œil, trop de mouvement ne signale plus rien.

---

## 3. Types d'interface

Classification de Fagerholt & Lorentzon (2009), selon que l'élément existe dans la fiction et dans l'espace 3D du jeu :

| Type | Dans la fiction ? | Dans l'espace du jeu ? | Exemple |
|---|---|---|---|
| Diégétique | Oui | Oui | Jauge de vie sur le dos du personnage, munitions sur l'arme |
| Non diégétique | Non | Non | Barre de vie classique en coin d'écran |
| Spatiale | Non | Oui | Contour de l'objet interactif, marqueur d'objectif dans le monde, chemin au sol |
| Méta | Oui | Non | Sang sur l'écran, écran fissuré, effet de vision troublée |

Arbitrage :
- Le diégétique renforce l'immersion mais se lit souvent moins vite. Le réserver aux informations non critiques ou très bien lisibles.
- Le non diégétique est le plus lisible et le plus rapide à implémenter. C'est le défaut raisonnable.
- Le méta (vignettage rouge à vie basse) est efficace pour l'urgence mais peut masquer la scène : le garder bref et réglable.

---

## 4. Feedback et états

Toute action du joueur appelle une réponse. Toute interface a des états.

- **Feedback immédiat** pour chaque entrée : survol, appui, validation, refus. Voir [Game feel](../ressenti/game-feel-juice.md) pour le feedback en jeu.
- **États d'un élément interactif** : normal, survolé/focalisé, pressé, désactivé, sélectionné. Chacun doit être visuellement distinct (pas seulement par la couleur).
- **Action impossible** : ne pas cacher silencieusement. Griser **et** expliquer pourquoi (« Niveau 5 requis », « Pas assez d'or : 120/200 »). Un clic sans réponse est le pire feedback.
- **Erreurs** : message près de la cause, formulé en action (« Libère un emplacement d'inventaire »), pas en code d'erreur.
- **Actions irréversibles** (vendre un objet rare, supprimer une sauvegarde) : confirmation, ou mieux, possibilité d'annuler (rachat possible).
- **Attente / chargement** : indicateur d'activité ; au-delà de quelques secondes, progression ou astuce.
- **Changement d'une valeur** : animer le delta (barre de vie qui descend avec une traîne, `+25` qui apparaît) plutôt que changer le chiffre instantanément.

---

## 5. Menus et navigation

### 5.1 Structure

- **Profondeur faible** : les actions fréquentes à 1–2 niveaux maximum.
- **Nommer les choses comme le joueur les pense**, pas comme le code les nomme.
- L'option de reprise (« Continuer ») est l'élément par défaut au lancement quand une sauvegarde existe.
- Le joueur doit pouvoir **lancer le jeu sans passer par les options**, mais les options critiques (sous-titres, taille de texte, langue) peuvent être proposées au premier lancement.
- Les réglages s'appliquent avec **aperçu** (luminosité, taille de texte) et peuvent être réinitialisés.

### 5.2 Navigation manette

- Tout élément doit être atteignable au D-pad/stick dans un **ordre spatial logique** (haut/bas/gauche/droite correspondent à la disposition visuelle).
- **Un focus toujours visible**, jamais perdu (après fermeture d'une popup, le focus revient à l'élément d'origine).
- Conventions : bouton du bas = valider, bouton de droite = retour/annuler (inversé sur certaines plateformes et régions : suivre la convention de la plateforme cible). Gâchettes/bumpers = changer d'onglet.
- Afficher les **prompts de boutons** du périphérique actif et changer dynamiquement entre clavier/souris et manette.
- Listes longues : défilement accéléré au maintien, saut par page ou par catégorie.
- Éviter les curseurs libres à la manette, sauf jeu pensé pour.

### 5.3 Souris et clavier

- Zones cliquables généreuses (voir loi de Fitts), survol avec feedback, clic droit cohérent.
- Raccourcis clavier pour les actions fréquentes ; `Échap` ferme toujours le panneau courant.

---

## 6. Lisibilité des chiffres et du texte

- **Taille** : prévoir le jeu sur téléviseur à distance de canapé. Le texte doit rester lisible en 720p ; proposer un réglage de taille de texte.
- **Contraste** : texte sur fond uni ou semi-opaque, jamais directement sur le décor. Le WCAG recommande un ratio de contraste d'au moins 4,5:1 pour le texte courant.
- **Chiffres** : police à chiffres de largeur fixe (*tabular figures*) pour les valeurs qui changent (évite que le texte « danse »).
- **Grands nombres** : abréger de façon cohérente (`12,4 k`, `3,1 M`) ; séparateurs de milliers selon la langue.
- **Comparaisons** : afficher le delta par rapport à l'équipement actuel (`+12` en vert **avec** flèche ↑), pas seulement la valeur brute.
- **Moins de chiffres** quand c'est possible : une barre ou une jauge se lit plus vite qu'un nombre. Les chiffres servent quand le joueur doit calculer.
- **Chiffres de dégâts** flottants : regrouper ou cumuler les petits coups, distinguer critiques, soins et dégâts reçus par forme/taille et pas seulement par couleur.
- **Localisation** : prévoir de la place (l'allemand ou le français sont souvent plus longs que l'anglais), des polices couvrant tous les alphabets cibles, et ne jamais intégrer du texte dans les images.

---

## 7. Tooltips et descriptions de règles

- Structure : **nom → effet principal en une ligne → détails → texte d'ambiance** (le texte d'ambiance en dernier, séparé visuellement).
- Écrire les effets **avec des mots-clés cohérents** (« Brûlure », « Étourdi ») définis une fois et expliqués via un tooltip imbriqué.
- Valeurs exactes visibles (ou disponibles en un geste), surtout dans les jeux de build et de stratégie.
- Délai d'apparition court au survol (souris) ; à la manette, tooltip attaché à l'élément focalisé, ou bouton dédié pour détailler.
- Le tooltip ne doit pas masquer l'élément qu'il décrit ni les éléments à comparer.

---

## 8. Affordances et signifiants

- Une **affordance** est une possibilité d'action ; un **signifiant** est ce qui l'indique (Norman).
- En UI : un bouton ressemble à un bouton (relief, contour, changement au survol).
- Dans le monde : rebords escaladables marqués (peinture, texture), portes interactives distinctes des portes décoratives, objets ramassables qui brillent ou ont un contour. Le même langage visuel partout (voir [Level design](../contenu/level-design.md)).
- **Ne pas tromper** : un élément qui a l'air interactif et ne l'est pas crée de la frustration. Si c'est décoratif, le rendre visuellement différent.

---

## 9. Lois et notions cognitives utiles

| Loi / notion | Énoncé | Application |
|---|---|---|
| Loi de Fitts | Le temps pour atteindre une cible croît avec la distance et diminue avec la taille de la cible | Gros boutons pour les actions fréquentes, bords et coins d'écran faciles à atteindre à la souris, actions liées proches les unes des autres |
| Loi de Hick-Hyman | Le temps de décision croît avec le nombre (logarithme) de choix équiprobables | Limiter les options présentées à la fois, regrouper par catégories, mettre en avant l'option recommandée |
| Charge cognitive / mémoire de travail | La mémoire de travail est très limitée (de l'ordre de 4 éléments selon Cowan) | Ne pas demander au joueur de retenir des infos entre écrans ; afficher ce dont il a besoin là où il en a besoin |
| Attention sélective | En situation de concentration, le joueur ne voit pas ce qui est hors de son focus (cécité d'inattention) | Les tutoriels et infos importantes n'arrivent pas pendant un combat intense |
| Gestalt | Proximité, similarité, continuité, région commune structurent la perception | Grouper visuellement les éléments liés |
| Reconnaissance > rappel | Reconnaître est plus facile que se souvenir | Icônes + libellés, rappel des contrôles contextuel |

---

## 10. Anti-patterns

- HUD qui affiche tout en permanence « au cas où ».
- Information critique uniquement en couleur, ou uniquement en son.
- Bouton désactivé sans explication.
- Texte sur décor sans fond, police fine en petite taille.
- Focus manette invisible ou perdu après une popup.
- Tutoriel textuel affiché pendant l'action.
- Icônes différentes pour un même concept selon l'écran.
- Menu d'options qui ne s'applique qu'après redémarrage sans le dire.

---

## Checklist

- [ ] Chaque élément du HUD répond à une question précise du joueur.
- [ ] Les informations critiques sont près du centre d'attention et redondantes (visuel + son).
- [ ] Le HUD contextuel masque ce qui n'est pas pertinent.
- [ ] Aucune information n'est encodée uniquement par la couleur.
- [ ] Tous les éléments interactifs ont des états distincts (normal, focus, pressé, désactivé).
- [ ] Toute action refusée explique pourquoi.
- [ ] Les actions irréversibles sont confirmées ou annulables.
- [ ] Toute l'interface est navigable à la manette avec un focus toujours visible.
- [ ] Les prompts suivent le périphérique actif.
- [ ] Le texte est lisible à distance de téléviseur ; la taille du texte est réglable ; contraste suffisant.
- [ ] Les valeurs changeantes utilisent des chiffres à largeur fixe.
- [ ] Les comparaisons d'objets montrent le delta.
- [ ] Les tooltips suivent la structure nom → effet → détails → ambiance.
- [ ] L'interface supporte des textes plus longs (localisation).

## Pistes d'implémentation

- **Agnostique** : séparer les **données** (modèle : vie, inventaire) de la **vue** (widgets) ; la vue s'abonne à des événements de changement plutôt que d'interroger le jeu à chaque frame. Centraliser couleurs, tailles et icônes dans une feuille de style / un thème unique.
- **UE5** : UMG + CommonUI (navigation manette, piles d'écrans activables, prompts de boutons par plateforme via *Input Action Data*). Les marqueurs spatiaux utilisent des `WidgetComponent` ou une projection écran.
- **Godot** : nœuds `Control`, `Theme` partagé, `focus_neighbor_*` pour la navigation manette, `grab_focus()` à l'ouverture d'un menu.
- **Unity** : UI Toolkit ou uGUI ; `EventSystem` + navigation explicite pour la manette ; Input System pour détecter le périphérique actif.

## Voir aussi

- [Game feel / juice](../ressenti/game-feel-juice.md)
- [Audio](audio.md)
- [Accessibilité](accessibilite.md)
- [Onboarding et tutoriels](../contenu/onboarding-tutoriels.md)
- [Level design](../contenu/level-design.md)
- [Playtest et métriques](../production/playtest-et-metriques.md)

## Sources

- Celia Hodent, *The Gamer's Brain: How Neuroscience and UX Can Impact Video Game Design*, CRC Press, 2017.
- Erik Fagerholt & Magnus Lorentzon, *Beyond the HUD: User Interfaces for Increased Player Immersion in FPS Games*, mémoire de master, Chalmers University of Technology, 2009.
- Don Norman, *The Design of Everyday Things*, édition révisée, Basic Books, 2013.
- Paul M. Fitts, « The information capacity of the human motor system in controlling the amplitude of movement », *Journal of Experimental Psychology*, 1954.
- W. E. Hick, « On the rate of gain of information », *Quarterly Journal of Experimental Psychology*, 1952 ; R. Hyman, 1953.
- Nelson Cowan, « The magical number 4 in short-term memory », *Behavioral and Brain Sciences*, 2001.
- W3C, *Web Content Accessibility Guidelines (WCAG) 2.1*, critère 1.4.3 Contraste.
