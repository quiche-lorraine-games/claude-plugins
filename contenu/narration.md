# Narration

> **En bref** : comment raconter avec un jeu sans trahir le gameplay. Couvre la narration environnementale, la cohérence ludonarrative, les structures narratives (linéaire, arborescente, embranchements qui se rejoignent, hub, narration par qualités et *storylets*), les dialogues et les choix, le rythme de l'exposition, la narration émergente et l'écriture propre au jeu vidéo (concision, *barks*).

## Quand consulter cette fiche

- Tu écris l'histoire, les dialogues, les textes d'objets ou les répliques des PNJ.
- Tu dois choisir une structure narrative (linéaire, à choix, ouverte).
- Tu implémentes un système de dialogue, de quêtes ou de répliques contextuelles.
- Les joueurs sautent les cinématiques ou ne lisent pas les textes.
- L'histoire dit une chose et le gameplay en fait faire une autre.
- Tu veux raconter sans cinématique ni texte (budget, rythme).

---

## 1. Principes

- **Le joueur est un acteur, pas un spectateur.** Ce qu'il **fait** raconte plus que ce qu'il **voit**.
- **Montrer par le jeu, sinon par l'image, et seulement en dernier recours par le texte.** Ordre de préférence : mécanique > environnement > animation/son > dialogue court > texte long > cinématique.
- **Le joueur doit vouloir l'information** avant qu'on la lui donne : créer la question (mystère, enjeu) avant la réponse.
- **Respecter le temps du joueur** : tout texte ou cinématique doit pouvoir être passé, accéléré ou relu.
- **Trois couches** souvent utilisées :
  - **Histoire principale** (obligatoire, courte) ;
  - **Contexte** (optionnel, accessible : dialogues secondaires, quêtes) ;
  - **Lore profond** (caché, pour les curieux : descriptions d'objets, documents).

## 2. Narration environnementale

Raconter par l'espace et les objets. L'environnement est conçu comme un **témoin** de ce qui s'est passé (Henry Jenkins, 2004 ; Harvey Smith et Matthias Worch, GDC 2010, « What Happened Here? »).

Techniques :
- **Mise en scène d'objets** (*vignettes*) : un squelette tenant une lettre, une table dressée pour deux avec une chaise renversée.
- **Traces d'événements** : impacts de balles, barricades, traînées de sang, objets abandonnés en fuite.
- **Évolution de l'espace** : la zone change après un événement (village incendié au retour).
- **Architecture et usure** : qui vivait ici, comment, depuis combien de temps.
- **Documents et enregistrements** : journaux, audiologs. À garder courts et à placer sur le chemin naturel du joueur.

Règles :
- **Laisser le joueur reconstituer** : l'inférence est plus gratifiante que l'explication. Une vignette efficace pose une question et donne assez d'indices pour y répondre.
- **Ne pas bloquer le gameplay** : la narration environnementale se consomme en mouvement.
- **Cohérence** : chaque élément doit être plausible dans l'univers (pourquoi cet objet est-il ici ?).
- Voir [Level design](level-design.md) pour le placement et les lignes de vue.

## 3. Cohérence ludonarrative

La **dissonance ludonarrative** (terme de Clint Hocking, 2007, à propos de *BioShock*) apparaît quand les mécaniques contredisent l'histoire. Exemples typiques : un héros présenté comme pacifiste qui tue des centaines d'ennemis ; une urgence absolue dans le récit alors que le joueur peut faire des quêtes secondaires pendant des semaines.

Règles :
- **Aligner verbes et thème** : les actions principales du joueur doivent exprimer ce que le jeu veut dire. Si le jeu parle de soin, le soin doit être une mécanique centrale.
- **Ne pas promettre ce que le gameplay ne tient pas** : si l'urgence est narrative, limiter le temps ou l'accès aux activités secondaires, ou abandonner l'urgence.
- **Les conséquences mécaniques renforcent le récit** : une trahison narrative qui fait perdre un allié jouable marque plus qu'une cinématique.
- **La dissonance peut être un outil** si elle est voulue et commentée par le jeu (*Spec Ops: The Line*), mais c'est un choix risqué.

Question de diagnostic : *« Si on retire tout texte et toute cinématique, que raconte le jeu ? »* Si la réponse contredit l'histoire, revoir l'un ou l'autre.

## 4. Structures narratives

| Structure | Description | Coût de production | Agence ressentie |
|---|---|---|---|
| **Linéaire** | Une seule suite d'événements | Faible | Faible ; compensée par le gameplay |
| **Arborescente** (*branching*) | Chaque choix ouvre une branche distincte | Explosif (croissance exponentielle) | Forte mais peu de contenu vu par partie |
| **Embranchements qui se rejoignent** (*branch and bottleneck*) | Les branches divergent puis se rejoignent à des nœuds clés ; l'état garde la trace des choix | Maîtrisé | Bonne, si les choix ont des échos |
| **Hub** (*hub and spoke*) | Une zone centrale d'où partent des arcs indépendants, dans l'ordre choisi | Moyen | Bonne sur l'ordre, faible sur la fin |
| **Narration par qualités** (*quality-based narrative*, QBN) | Le contenu est découpé en fragments (*storylets*) débloqués par des conditions sur l'état du joueur | Moyen, très extensible | Forte, émergente |
| **Saillance** (*salience-based*) | Le système choisit le fragment le plus pertinent pour le contexte | Moyen | Implicite (répliques adaptées) |
| **Monde ouvert à quêtes** | Quêtes indépendantes + fil principal | Élevé | Forte sur l'ordre et la liberté |

Recommandations :
- **Par défaut, pour un petit projet : linéaire ou embranchements qui se rejoignent.** Une arborescence pure est presque toujours trop coûteuse.
- **Variables d'état plutôt que branches** : enregistrer les choix (flags, compteurs de relation) et les faire résonner dans des répliques ou détails plus tard, sans dupliquer des chapitres entiers.
- **Storylets** (*Fallen London*, Failbetter Games ; formalisé par Emily Short) : chaque fragment a des **conditions** (requiert « Réputation ≥ 3 », « A rencontré X ») et des **effets** (modifie l'état). Excellent pour du contenu modulaire, des événements aléatoires ou des jeux de gestion.
- Les catalogues de structures de Sam Kabo Ashwell (« Standard Patterns in Choice-Based Games », 2015) nomment les variantes classiques (*time cave*, *gauntlet*, *branch and bottleneck*, *quest*, *open map*…).

## 5. Dialogues et choix

### Ce qui fait un bon choix

- **Clarté** : le joueur comprend ce qu'il choisit. Une option paraphrasée doit correspondre à ce que dit le personnage (problème connu des roues de dialogue où l'intention perçue diffère de la réplique).
- **Enjeu** : les options diffèrent vraiment (valeur, relation, information), pas seulement en ton.
- **Conséquence visible** : le jeu montre que le choix a été retenu, immédiatement (réaction) ou plus tard (écho). Un rappel explicite (« X s'en souviendra », popularisé par Telltale) rend des conséquences mineures perceptibles.
- **Pas de bonne réponse évidente** : les choix intéressants opposent deux valeurs légitimes.

### Règles pratiques

- **2 à 4 options** par choix ; au-delà, la lecture ralentit.
- **Options courtes** (quelques mots), réplique complète ensuite.
- **Indiquer les options qui font avancer** vs celles qui donnent de l'information (icône, ordre constant).
- **Ne pas punir l'exploration des dialogues** : poser toutes les questions informatives doit être possible sans conséquence cachée.
- **Ton du personnage joueur** : décider s'il est un personnage défini (voix et opinions propres) ou une projection du joueur ; ne pas mélanger.
- **Choix à durée limitée** : à réserver aux moments de tension ; prévoir un réglage d'accessibilité pour désactiver le minuteur.

## 6. Rythme de l'exposition

- **Commencer par l'action ou le mystère**, pas par l'historique du monde. Le lore vient quand le joueur se pose des questions.
- **Une information à la fois**, liée à ce que le joueur fait maintenant.
- **Exposition pendant le mouvement** : dialogues pendant les trajets, répliques d'ambiance, plutôt que des cinématiques qui arrêtent le jeu.
- **Coïncider avec le rythme du level design** : les révélations dans les **vallées** d'intensité (voir [Level design](level-design.md)), jamais au milieu d'un combat exigeant.
- **Noms propres limités** : chaque nom inventé est une charge mémoire. Introduire peu de noms, les répéter, les associer à un visage ou un lieu.
- **Rappels** : journal, résumé « précédemment », codex. Indispensables pour les jeux joués en plusieurs sessions (voir [Onboarding et tutoriels](onboarding-tutoriels.md)).

## 7. Narration émergente

Histoires produites par l'interaction des systèmes, pas écrites à l'avance (*Dwarf Fortress*, *RimWorld*, *XCOM*, *Crusader Kings*).

Ingrédients :
- **Des personnages avec identité** : nom, trait, relation, historique. Le joueur s'attache à « Marie la cuisinière borgne », pas à « l'unité 12 ».
- **Des systèmes qui interagissent** : besoins, relations, météo, économie, combat.
- **De la mémoire** : le jeu retient les événements et les fait réapparaître (rancunes, cicatrices, épitaphes).
- **De la perte possible** : sans risque réel (mort permanente), peu d'histoire.
- **Un narrateur systémique** : un système qui dose les événements selon l'état du jeu (les « storytellers » de *RimWorld*, conçus par Tynan Sylvester) — même principe que le rythme d'intensité.
- **Des outils de restitution** : journaux, chroniques, captures, qui aident le joueur à raconter ce qui s'est passé.

## 8. Écrire pour le jeu

- **Court.** Une réplique de dialogue tient en une ou deux phrases. Un texte d'objet en deux ou trois lignes. Couper tout ce qui ne sert pas.
- **Lisible en jeu** : sous-titres en taille réglable, contraste suffisant, nom du locuteur (voir [Accessibilité](../interface/accessibilite.md)).
- **Écrire pour la voix** : lire à voix haute ; éviter les phrases que l'on ne peut pas dire en un souffle.
- **Prévoir la localisation** : éviter les jeux de mots intraduisibles dans les textes critiques, prévoir +30 % de longueur pour certaines langues (règle empirique courante pour l'interface, l'allemand et le français étant souvent plus longs que l'anglais), ne pas concaténer des fragments de phrases dans le code.
- **Variables de texte** : prévoir genre, pluriel et accords pour les noms dynamiques.

### Barks (répliques contextuelles)

Les *barks* sont les courtes répliques déclenchées par le système : « Je recharge ! », « Il est passé par là ! », remarques d'un compagnon.

- **Rôle de gameplay** : informer le joueur de l'état de l'IA (alerte, recherche, fuite) — c'est du feedback avant d'être de la narration (voir [IA des ennemis](../systemes/ia-ennemis.md)).
- **Variantes** : plusieurs versions par situation pour éviter la répétition ; mémoriser les dernières jouées.
- **Fréquence** : temps de recharge par réplique et global ; priorité aux répliques importantes.
- **Sélection par règles** : *Left 4 Dead* choisit la réplique dont les critères correspondent le mieux au contexte (Elan Ruskin, GDC 2012, « AI-driven Dynamic Dialog through Fuzzy Pattern Matching »).

---

## Anti-patterns et pièges

- **Mur de texte d'introduction** sur l'histoire du monde avant toute action.
- **Cinématique non passable**, surtout avant un boss difficile (revue à chaque essai).
- **Choix illusoires répétés** : le joueur finit par comprendre que rien ne compte.
- **Arborescence non maîtrisée** : contenu explosif, la majorité jamais vue.
- **Information critique uniquement dans un audiolog optionnel.**
- **Dialogue pendant un combat intense** : non entendu, non lu.
- **Barks répétitifs** : la même réplique trois fois par minute.
- **Texte codé en dur et concaténé** : localisation impossible.

## Checklist

- [ ] On peut résumer ce que raconte le jeu par ses mécaniques seules, et cela concorde avec l'histoire.
- [ ] La structure narrative est choisie en fonction du budget (pas d'arborescence pure sans nécessité).
- [ ] Les choix sont stockés en variables d'état et ont des échos visibles.
- [ ] Chaque choix a 2 à 4 options claires, sans bonne réponse évidente.
- [ ] Les révélations tombent dans les phases calmes.
- [ ] Toute cinématique et tout dialogue peuvent être passés, accélérés et relus.
- [ ] Les documents et lore profond sont optionnels ; l'information critique est sur le chemin principal.
- [ ] Les barks ont des variantes et des temps de recharge.
- [ ] Les textes sont externalisés, avec identifiants, prêts pour la localisation.
- [ ] Les sous-titres sont réglables et indiquent le locuteur.

## Pistes d'implémentation

Storylet minimal piloté par données :

```
storylet "aide_forgeron":
    conditions: met_blacksmith == true and reputation_village >= 2 and not quest_done("aide_forgeron")
    weight: 10                     // priorité si plusieurs storylets éligibles
    effects: reputation_village += 1, give_item("marteau")
    text_id: "STORY_BLACKSMITH_01"

function pickStorylet(state):
    eligible = [s for s in storylets if s.conditions(state)]
    return weightedPick(eligible) or null
```

- **Séparer contenu et code** : dialogues dans des fichiers de données (JSON, YAML, CSV) ou un langage dédié, avec identifiants de texte pour la localisation.
- **Outils existants** à privilégier plutôt que réinventer : *Ink* (inkle), *Yarn Spinner*, *Dialogic* (Godot), *articy:draft*.
- **Un seul magasin d'état narratif** (flags, compteurs) sérialisé avec la sauvegarde.
- **Système de barks** : table (événement, conditions, répliques, cooldown) + historique des dernières répliques jouées.
- **UE5** : `UDataTable` ou `UDataAsset` pour les dialogues, *String Tables* pour la localisation ; plugins Ink et Yarn existent.
- **Godot** : `tr()` et fichiers de traduction ; Dialogic ou plugin Ink.
- **Unity** : package *Localization* ; Ink ou Yarn Spinner.

## Voir aussi

- [Level design](level-design.md) — narration environnementale, rythme.
- [Onboarding et tutoriels](onboarding-tutoriels.md) — rappels après une pause.
- [IA des ennemis](../systemes/ia-ennemis.md) — barks comme feedback.
- [Aléatoire et procédural](../systemes/aleatoire-et-procedural.md) — événements générés.
- [UI, UX et HUD](../interface/ui-ux-hud.md), [Audio](../interface/audio.md), [Accessibilité](../interface/accessibilite.md).
- [Principes de conception](../fondamentaux/principes-de-conception.md) — agence.
- [RPG](../genres/rpg.md).

## Sources

- Henry Jenkins, « Game Design as Narrative Architecture », in *First Person*, MIT Press, 2004.
- Harvey Smith & Matthias Worch, « What Happened Here? Environmental Storytelling », GDC 2010.
- Clint Hocking, « Ludonarrative Dissonance in Bioshock », blog *Click Nothing*, 2007.
- Emily Short, « Beyond Branching: Quality-Based, Salience-Based, and Waypoint Narrative Structures », 2016 — https://emshort.blog/
- Sam Kabo Ashwell, « Standard Patterns in Choice-Based Games », 2015 — https://heterogenoustasks.wordpress.com/
- Elan Ruskin, « AI-driven Dynamic Dialog through Fuzzy Pattern Matching », GDC 2012.
- Tynan Sylvester, *Designing Games: A Guide to Engineering Experiences*, O'Reilly, 2013.
- Jesse Schell, *The Art of Game Design: A Book of Lenses*, 3e éd., CRC Press, 2019 (chapitres sur l'histoire et le monde).
