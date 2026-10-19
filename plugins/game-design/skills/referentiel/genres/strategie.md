# Stratégie

> **En bref** : point d'entrée pour les jeux de stratégie — 4X, RTS (temps réel), tactique au tour par tour, *tower defense*. Ce qui fait la qualité du genre : des décisions intéressantes sous contrainte, une économie qui crée des arbitrages, une information gérée avec soin et des contre-jeux pour chaque stratégie.

## Quand consulter cette fiche

- Tu conçois un jeu où le joueur gère des unités, des ressources ou un territoire.
- Une stratégie ou une unité domine toutes les autres.
- La fin de partie traîne ou est jouée d'avance.
- Tu dois choisir quelle information montrer ou cacher (brouillard de guerre, intentions ennemies).

## Boucle centrale typique

```
Lire la situation → Décider (construire, déplacer, attaquer, rechercher)
       ↑                                   ↓
 Nouvelle situation ← Résolution (combat, production) ← Dépenser des ressources
```

Sid Meier : un jeu est « une série de choix intéressants ». En stratégie, c'est littéralement le contenu. Un choix est intéressant s'il n'a pas de réponse évidente, s'il a des conséquences et si le joueur a l'information pour raisonner. Voir [Principes de conception](../fondamentaux/principes-de-conception.md).

## Piliers transverses

1. **Arbitrages économiques** : chaque ressource dépensée ici ne l'est pas ailleurs (économie vs armée vs technologie). Voir [Économie](../systemes/economie.md).
2. **Contre-jeu** : toute stratégie a une réponse. Relations de type pierre-feuille-ciseaux entre unités, souples plutôt que absolues.
3. **Gestion de l'information** : ce qui est connu, caché, estimable.
4. **Lisibilité à grande échelle** : l'état du jeu se comprend d'un coup d'œil malgré de nombreuses unités.

## Sous-genre : 4X (*eXplore, eXpand, eXploit, eXterminate*)

- Terme proposé par Alan Emrich (1993) à propos de *Master of Orion*.
- Boucle longue : villes / colonies → production → expansion → conflit ou victoire alternative.
- Plusieurs **conditions de victoire** (militaire, scientifique, culturelle, diplomatique) = plusieurs styles de jeu.
- Problème connu : la **fin de partie** (*late game*) devient une gestion fastidieuse et l'issue est décidée longtemps avant la fin. Remèdes : automatisation, crises de fin de partie, victoire anticipée quand l'avance est écrasante, réduction du nombre d'unités à gérer.
- Références : *Civilization* (série), *Master of Orion II*, *Stellaris*, *Humankind*.

## Sous-genre : RTS (temps réel)

- **Macro** (économie, production, expansion) vs **micro** (contrôle fin des unités au combat).
- **APM** (actions par minute) : en compétition élevée, la vitesse d'exécution devient une compétence. Pour un public large, réduire l'exigence d'APM : files de production, contrôle de groupe, automatisation, unités moins nombreuses mais plus importantes.
- Brouillard de guerre et **éclaireurs** : l'information se gagne.
- Ordres de construction (*build orders*) : les ouvertures se codifient, prévoir des contres.
- Références : *StarCraft* / *StarCraft II* (asymétrie de factions), *Age of Empires II*, *Company of Heroes* (couvert, escouades), *Northgard* (rythme lent).

## Sous-genre : tactique au tour par tour

- Peu d'unités, chacune importante ; positionnement, couvert, portée, ligne de vue.
- **Probabilités affichées** : le pourcentage affiché doit être honnête. Les joueurs perçoivent mal les probabilités (un 95 % raté paraît injuste). Options : afficher et assumer, réduire l'aléatoire, ou tricher en faveur du joueur de façon documentée.
- **Information parfaite** comme alternative : *Into the Breach* montre toutes les attaques ennemies du tour suivant ; le jeu devient un puzzle de contre-mesures.
- Références : *XCOM: Enemy Unknown* / *XCOM 2*, *Into the Breach*, *Fire Emblem*, *Final Fantasy Tactics*.

## Sous-genre : *tower defense*

- Boucle : vague d'ennemis → récompense → placement / amélioration de tours → vague suivante.
- Diversité d'ennemis qui **teste** différentes faiblesses (rapides, blindés, volants, nombreux).
- Tours aux **rôles complémentaires** (zone, cible unique, ralentissement, anti-aérien).
- Laisser le joueur influencer le chemin (labyrinthe) ou fixer le chemin et varier les emplacements.
- Accélération ×2/×3 pour les vagues faciles.
- Références : *Kingdom Rush*, *Bloons TD 6*, *Plants vs. Zombies*.

## Mécaniques transverses

| Mécanique | Conseil |
|---|---|
| Effet boule de neige | Un avantage précoce qui s'amplifie rend la fin jouée d'avance. Ajouter des freins (coût d'entretien croissant, rendements décroissants) sans punir le gagnant. |
| Rattrapage (*catch-up*) | Aider discrètement le joueur en retard (bonus d'objectif, coûts réduits). Rester discret pour ne pas annuler le mérite. |
| Arbre technologique | Embranchements exclusifs ou coûts élevés = choix ; arbre complet obtenable = simple ordre. |
| Asymétrie de factions | Forte identité, mais équilibrage coûteux. Commencer symétrique, puis différencier. |
| IA adverse | Elle doit **paraître** intelligente et lisible ; tricher (bonus de ressources) aux niveaux élevés est courant et acceptable si annoncé. Voir [IA et ennemis](../systemes/ia-ennemis.md). |

## Pièges fréquents

- Stratégie dominante (une unité ou une ouverture bat tout) : surveiller les taux de victoire.
- Micro-gestion fastidieuse qui masque les vraies décisions.
- Information cachée frustrante (perte sans comprendre pourquoi).
- Fin de partie interminable.
- Interface qui demande trop de clics pour des actions fréquentes.
- Probabilités affichées perçues comme mensongères.

## Checklist

- [ ] Chaque ressource force un arbitrage.
- [ ] Chaque unité / stratégie a au moins un contre.
- [ ] Le joueur sait pourquoi il a gagné ou perdu une bataille.
- [ ] Un mécanisme limite l'effet boule de neige.
- [ ] La fin de partie a été testée et ne traîne pas.
- [ ] Les actions fréquentes sont accessibles en un raccourci.
- [ ] La lisibilité tient avec le nombre maximal d'unités à l'écran.
- [ ] Les probabilités affichées sont exactes ou la triche est documentée.

## Pistes d'implémentation

- Simulation **déterministe** séparée du rendu : facilite rejeu, sauvegarde et multijoueur en *lockstep* (voir [Multijoueur](../systemes/multijoueur.md)).
- Données d'unités dans un tableur (coût, PV, dégâts, portée, cible) ; calculer le coût-efficacité de chaque unité.
- Pathfinding : A* sur grille ou navmesh ; *flow fields* pour de grandes foules.

## Voir aussi

- [Économie](../systemes/economie.md)
- [Équilibrage et difficulté](../systemes/equilibrage-et-difficulte.md)
- [IA et ennemis](../systemes/ia-ennemis.md)
- [Multijoueur](../systemes/multijoueur.md)
- [UI, UX et HUD](../interface/ui-ux-hud.md)
- [Principes de conception](../fondamentaux/principes-de-conception.md)

## Sources

- Sid Meier, « Interesting Decisions », GDC 2012.
- Alan Emrich, « MicroProse' Strategic Space Opera is Rated XXXX », *Computer Gaming World*, 1993 (origine du terme 4X).
- Ian Schreiber et Brenda Romero, *Game Balance*, CRC Press, 2021.
- Matthew Davis et Justin Ma (Subset Games), « Into the Breach Design Postmortem », GDC 2019.
