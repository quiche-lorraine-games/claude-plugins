# Économie de jeu

> **En bref** : comment les ressources entrent dans le jeu, circulent, se transforment et en sortent. Couvre les sources et les puits (*faucets & sinks*), les conversions, l'inflation, les monnaies multiples, les tables de butin pondérées, la rareté, le prix et la valeur perçue, le crafting, l'économie entre joueurs, ainsi que les modèles de monétisation et les *dark patterns* à éviter.

## Quand consulter cette fiche

- Tu ajoutes une monnaie, une boutique, un système de crafting ou de butin.
- Les joueurs accumulent des ressources sans savoir quoi en faire (ou en manquent toujours).
- Les prix d'un marché entre joueurs explosent.
- Tu écris une table de butin et dois choisir des poids de rareté.
- Tu dois décider d'un modèle de monétisation ou évaluer une mécanique payante.

---

## 1. Modèle de base : sources, réservoirs, conversions, puits

Toute économie de jeu peut se décrire comme un graphe de flux (formalisé par Joris Dormans avec l'outil *Machinations*) :

| Élément | Rôle | Exemples |
|---|---|---|
| **Source** (*faucet*) | Crée une ressource à partir de rien | Ennemi qui lâche de l'or, récolte, récompense de quête, revenu passif |
| **Réservoir** (*pool*) | Stocke une ressource | Inventaire, porte-monnaie, banque |
| **Convertisseur** (*converter*) | Transforme une ressource en une autre | Crafting, boutique (or → épée), fonderie (minerai → lingot) |
| **Échangeur** (*trader*) | Transfert entre acteurs sans création | Commerce entre joueurs, enchères |
| **Puits** (*sink* / *drain*) | Détruit une ressource | Achat à un PNJ, réparation, taxe, consommable utilisé, mort |

**Règle d'or** : à long terme, `somme des sources ≈ somme des puits` pour chaque ressource. Sinon :
- **Sources > puits** → accumulation, inflation, la ressource perd tout sens.
- **Puits > sources** → pénurie, frustration, *grind*.

### Diagnostic d'une économie

1. Lister chaque ressource.
2. Pour chacune, lister **toutes** les sources et **tous** les puits, avec un débit estimé (par minute de jeu ou par session).
3. Tracer la **quantité détenue par un joueur typique** au cours du temps (tableur ou simulation).
4. Vérifier qu'à chaque phase du jeu, le joueur a **quelque chose d'intéressant à acheter** et **pas assez pour tout acheter**.

## 2. Ressources et conversion

- **Chaque ressource doit avoir une raison d'exister** : un rôle distinct (temps, risque, rareté, spécialisation). Deux ressources qui servent au même usage doivent être fusionnées.
- **Chaînes de valeur** (*value chains*, Daniel Cook) : une ressource brute gagne de la valeur en passant par des conversions (minerai → lingot → épée). Chaque étape doit offrir un choix ou un effort, sinon c'est un clic de plus pour rien.
- **Taux de conversion** : à garder simples et stables (1:1, 2:1, 5:1, 10:1). Des taux complexes rendent l'économie illisible.
- **Pertes à la conversion** : une conversion qui détruit une partie de la valeur (revendre à 25–50 % du prix d'achat) agit comme un puits et empêche les boucles d'arbitrage infinies.
- **Tester les boucles d'arbitrage** : acheter A, le convertir en B, revendre B plus cher que A = argent infini. Vérifier systématiquement chaque cycle du graphe.

## 3. Monnaies multiples

| Monnaie | Fonction typique |
|---|---|
| **Douce** (*soft currency*) | Gagnée en jouant, abondante, sert aux achats courants |
| **Dure** (*hard / premium currency*) | Rare, souvent achetable avec de l'argent réel |
| **Spécialisée** (jetons, fragments) | Liée à un mode, un événement ou un type d'objet |
| **Ressource de progression** (points de compétence) | Ne s'échange pas, mesure l'avancement |

Règles :
- **Le moins de monnaies possible.** Chaque monnaie supplémentaire ajoute un coût de compréhension. Un jeu solo premium s'en sort généralement avec une ou deux.
- Une monnaie spécialisée sert à **isoler** un sous-système (un événement ne doit pas déséquilibrer l'économie principale).
- **Afficher les soldes** là où on en a besoin (boutique, écran de crafting), pas en permanence dans le HUD si elles ne servent pas en jeu.
- Les monnaies premium qui ne correspondent pas à un multiple clair des prix (packs de 500 pour des objets à 800) sont un *dark pattern* reconnu (voir § 9).

## 4. Inflation

L'inflation apparaît quand la masse monétaire des joueurs grandit plus vite que les puits. Elle est critique dans les jeux persistants (MMO) où l'argent s'accumule sur des mois.

Symptômes : prix des marchés joueurs qui montent, nouveaux joueurs incapables d'acheter quoi que ce soit, monnaie douce ignorée au profit d'objets troqués.

Contre-mesures :
- **Puits proportionnels** à la richesse : taxe en pourcentage sur les transactions, coût de réparation proportionnel à la valeur de l'objet.
- **Puits désirables** : cosmétiques, logements, montures, confort — des dépenses que les joueurs riches **veulent** faire.
- **Objets consommables** : potions, munitions, enchantements temporaires détruisent de la valeur en continu.
- **Plafonds** de détention ou de gain par période.
- **Sources liées au temps plutôt qu'à l'action répétable** pour limiter l'exploitation par les bots.
- **Surveiller** : télémétrie de la masse monétaire totale et des prix médians (voir [Playtest et métriques](../production/playtest-et-metriques.md)).

En **solo**, l'inflation se traduit par « j'ai 50 000 pièces et rien à acheter » : prévoir des puits de fin de jeu (améliorations coûteuses, objets de collection).

## 5. Loot tables et rareté

### Table pondérée

Chaque entrée a un **poids** ; la probabilité d'une entrée = poids / somme des poids.

```
table "coffre_niveau_1":
    pièces (20–40)        poids 50
    potion de soin         poids 30
    arme commune           poids 15
    arme rare              poids 4
    arme légendaire        poids 1
```

### Paliers de rareté — point de départ

Valeurs indicatives à ajuster selon le rythme voulu, pas un standard de l'industrie :

| Rareté | Poids indicatif | Couleur conventionnelle |
|---|---|---|
| Commun | 60 | blanc / gris |
| Peu commun | 25 | vert |
| Rare | 10 | bleu |
| Épique | 4 | violet |
| Légendaire | 1 | orange / doré |

Les couleurs blanc → vert → bleu → violet → orange sont une convention largement partagée depuis *Diablo* et *World of Warcraft* : la réutiliser évite d'avoir à l'enseigner. Ne pas porter l'information par la couleur seule (icône, nom, cadre — voir [Accessibilité](../interface/accessibilite.md)).

### Techniques

- **Tables imbriquées** : une entrée « arme rare » pointe vers une sous-table d'armes rares. Plus facile à maintenir.
- **Tirage garanti + tirage aléatoire** : un boss lâche toujours son objet signature + un tirage dans une table.
- **Protection contre la malchance** (*pity*, *bad luck protection*) : augmenter la probabilité d'un objet rare à chaque échec, ou le garantir après N tirages. Avec une probabilité `p` par tirage, le nombre de tirages pour obtenir l'objet suit une loi géométrique : en moyenne `1/p`, mais une part non négligeable des joueurs attendra bien plus (à `p = 1 %`, environ 37 % des joueurs n'ont toujours rien après 100 tirages, car `0,99^100 ≈ 0,366`). La garantie élimine cette queue de distribution.
- **Éviter les doublons inutiles** : retirer les objets déjà possédés du pool, ou convertir les doublons en ressource.
- **Butin adapté** (*smart loot*) : biaiser les tirages vers la classe ou le build du joueur.
- **Afficher les probabilités** quand le tirage est payant ; c'est une obligation dans plusieurs juridictions et sur certaines plateformes.

Pour les techniques d'aléatoire contrôlé (sacs mélangés, distribution pseudo-aléatoire), voir [Aléatoire et procédural](aleatoire-et-procedural.md).

## 6. Prix et valeur perçue

- **Prix de référence** : définir une unité de valeur (ex. « 1 minute de jeu ≈ 10 pièces ») et exprimer chaque prix en temps de jeu. Un objet à 1 000 pièces = 100 minutes de jeu : est-ce que l'objet le vaut ?
- **Prix croissants par palier** : améliorations successives au coût croissant (souvent ×1,5 à ×2 par niveau, point de départ) pour équilibrer avec la courbe de gains (voir [Progression](progression.md)).
- **Ancrage** : le premier prix vu sert de référence ; une boutique qui montre d'abord un objet cher fait paraître les autres abordables. À utiliser pour la lisibilité, pas pour manipuler.
- **Valeur perçue > valeur statistique** : un objet unique, nommé, avec une apparence distincte est perçu comme plus précieux qu'un objet statistiquement meilleur mais générique.
- **Toujours montrer la comparaison** avec l'équipement actuel avant achat (flèches vertes/rouges, delta chiffré).
- **Revente** : prix de revente nettement inférieur au prix d'achat (point de départ 25–50 %) pour éviter l'arbitrage et rendre l'achat significatif.

## 7. Crafting

Le crafting est un convertisseur. Il est intéressant quand il offre des **choix** :

| Type | Description | Intérêt |
|---|---|---|
| **Recette fixe** | A + B → C | Simple, lisible ; risque de corvée |
| **Découverte** | Expérimenter pour trouver les recettes | Exploration, surprise ; frustrant sans indices |
| **Modulaire** | Assembler des composants aux propriétés combinées | Expression, builds ; difficile à équilibrer |
| **Amélioration** | Investir des ressources dans un objet existant | Attachement à l'objet |

Règles :
- **Le crafting ne doit pas être une simple file d'attente de clics.** Si toutes les recettes sont évidentes et sans alternative, les remplacer par un achat direct.
- **Réduire la friction** : afficher les ingrédients manquants et où les trouver, permettre de crafter depuis le stockage, crafter en lot.
- **Lier le crafting à l'exploration** : les ingrédients rares viennent de zones dangereuses → risque/récompense.
- Voir aussi [Survie et crafting](../genres/survie-crafting.md).

## 8. Économie entre joueurs

Dès que les joueurs échangent, l'économie devient un système réel avec spéculation, monopoles et fraude.

- **Les joueurs optimisent** : ils trouveront la boucle la plus rentable, quelle que soit l'intention du design.
- **Bots et farming** : toute source répétable et échangeable sera automatisée. Lier les meilleures récompenses au compte (*bind on pickup*) limite le problème.
- **Commerce réel non officiel** (*RMT*, *real money trading*) : apparaît dès qu'une ressource échangeable a de la valeur. Le décider en amont (interdire, tolérer, encadrer).
- **Taxes de marché** : puits efficace et naturel.
- **Marché centralisé (hôtel des ventes) vs troc direct** : le marché centralisé rend les prix transparents et l'économie plus efficiente, mais réduit les interactions sociales.
- **Ne pas lancer d'économie joueur sans télémétrie.**

## 9. Monétisation et dark patterns

### Modèles

| Modèle | Principe | Points d'attention |
|---|---|---|
| **Premium** | Achat unique | Aucun conflit entre design et revenus |
| **Premium + DLC / extensions** | Contenu additionnel payant | Le jeu de base doit rester complet |
| **Free-to-play cosmétique** | Achats sans effet sur le gameplay | Modèle le plus sain en F2P |
| **Free-to-play avec avantages** | Achats de puissance ou de temps | Risque de *pay-to-win* ; tension design/revenus |
| **Passe de saison** (*battle pass*) | Piste de récompenses sur une durée limitée | Peut créer de l'obligation et de la peur de manquer |
| **Abonnement** | Accès payé par période | Pousse à allonger artificiellement le temps de jeu |
| **Tirages aléatoires payants** (*loot boxes*, *gacha*) | Payer pour un tirage aléatoire | Proche du jeu d'argent ; réglementé ou interdit dans certains pays |

Contexte réglementaire (à vérifier au moment de la sortie, il évolue) : la Commission belge des jeux de hasard a qualifié en 2018 certaines *loot boxes* payantes de jeux de hasard ; PEGI et l'ESRB signalent depuis 2020 les achats incluant des éléments aléatoires ; plusieurs plateformes et pays imposent la publication des probabilités.

### Dark patterns à éviter

Classement inspiré de Zagal, Björk et Lewis (2013) :

| Catégorie | Exemples | Alternative saine |
|---|---|---|
| **Temporels** | Récompenses perdues si on ne se connecte pas, minuteurs d'attente contournables en payant, rendez-vous obligatoires | Rattrapage possible, attente sans option payante, contenu qui reste disponible |
| **Monétaires** | Monnaie premium qui masque le prix réel, packs qui ne correspondent jamais aux prix, achats pendant un moment de frustration | Prix en monnaie réelle visibles, packs aux multiples cohérents |
| **Sociaux** | Obligation d'inviter des amis, pression de groupe pour se connecter | Social optionnel et récompensé positivement |
| **Psychologiques** | Peur de manquer (*FOMO*), coûts irrécupérables exploités, aléatoire payant opaque | Offres permanentes, probabilités affichées, garantie après N tirages |

Règle pour un agent : **si une mécanique ne fonctionne que parce que le joueur ne comprend pas ce qu'il paie ou se sent puni de partir, ne pas l'implémenter sans le signaler explicitement à l'auteur.**

---

## Anti-patterns et pièges

- **Monnaie sans puits** : au bout de quelques heures, elle ne vaut plus rien.
- **Trop de monnaies** : le joueur ne sait plus ce qui est précieux.
- **Boucle d'arbitrage** non détectée : richesse infinie.
- **Rareté sans protection** : une partie des joueurs ne verra jamais l'objet visé.
- **Crafting corvée** : dix étapes sans choix.
- **Économie rééquilibrée sans télémétrie** : on corrige au hasard.
- **Prix fixés « au feeling »** sans unité de référence en temps de jeu.

## Checklist

- [ ] Chaque ressource a un rôle unique et documenté.
- [ ] Pour chaque ressource, toutes les sources et tous les puits sont listés avec un débit estimé.
- [ ] Une simulation (tableur) montre le solde typique du joueur au fil du temps.
- [ ] Chaque cycle de conversion a été vérifié contre l'arbitrage infini.
- [ ] Les prix sont exprimés dans une unité de référence (temps de jeu).
- [ ] Les tables de butin sont des données externes, avec poids lisibles.
- [ ] Les objets rares ont une protection contre la malchance.
- [ ] La couleur de rareté est doublée d'un autre signal (icône, nom).
- [ ] Il existe des puits désirables pour les joueurs riches.
- [ ] Si multijoueur : taxes, liaison au compte, télémétrie de la masse monétaire.
- [ ] Aucun *dark pattern* de la liste § 9 ; toute mécanique de monétisation ambiguë est signalée à l'auteur.

## Pistes d'implémentation

Tirage pondéré avec garantie (*pity*) :

```
function roll(table, rng, state):
    total = sum(e.weight for e in table.entries)
    r = rng.range(0, total)
    for e in table.entries:
        if r < e.weight:
            result = e
            break
        r -= e.weight
    // pity : garantie de rare après N échecs
    if result.rarity >= RARE: state.failCount = 0
    else:
        state.failCount += 1
        if state.failCount >= table.pityThreshold:
            result = rollFrom(table.subtable(RARE), rng)
            state.failCount = 0
    if result.isTable: return roll(result.table, rng, state)  // tables imbriquées
    return result
```

- **RNG injectable et à graine** (*seed*) pour reproduire un tirage en test.
- Écrire un **test de distribution** : 100 000 tirages, vérifier que les fréquences observées collent aux poids.
- **Toutes les transactions passent par un service unique** (ajouter/retirer/convertir) qui journalise : facilite la télémétrie et la détection des boucles.
- **UE5** : `UDataTable` pour les tables de butin, `UPrimaryDataAsset` pour les définitions d'objets ; en multijoueur, transactions uniquement côté serveur.
- **Godot** : tables en `Resource` ; `RandomNumberGenerator` avec `seed`.
- **Unity** : `ScriptableObject` ; `System.Random` instancié avec graine plutôt que `UnityEngine.Random` global pour la reproductibilité.

## Voir aussi

- [Progression](progression.md) — courbes de gains, programmes de renforcement.
- [Aléatoire et procédural](aleatoire-et-procedural.md) — aléatoire contrôlé, sacs mélangés.
- [Équilibrage et difficulté](equilibrage-et-difficulte.md) — courbes de coût.
- [Multijoueur](multijoueur.md) — autorité serveur, triche.
- [Survie et crafting](../genres/survie-crafting.md), [RPG](../genres/rpg.md), [Deckbuilder et cartes](../genres/deckbuilder-cartes.md).
- [Playtest et métriques](../production/playtest-et-metriques.md) — télémétrie.

## Sources

- Ernest Adams & Joris Dormans, *Game Mechanics: Advanced Game Design*, New Riders, 2012 (sources, puits, convertisseurs, Machinations).
- Ian Schreiber & Brenda Romero, *Game Balance*, CRC Press, 2021.
- Daniel Cook, « Value chains », Lostgarden, 2021 — https://lostgarden.com/
- José P. Zagal, Staffan Björk & Chris Lewis, « Dark Patterns in the Design of Games », *Foundations of Digital Games*, 2013.
- Edward Castronova, *Synthetic Worlds: The Business and Culture of Online Games*, University of Chicago Press, 2005.
- Commission des jeux de hasard (Belgique), rapport sur les *loot boxes*, 2018.
- Base communautaire des dark patterns — https://www.darkpattern.games/
