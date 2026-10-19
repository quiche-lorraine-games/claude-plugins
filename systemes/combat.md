# Combat

> **En bref** : structure d'une attaque (anticipation, phase active, récupération), zones de collision, télégraphie, invulnérabilité, impact, formules de dégâts et rythme des affrontements. Le but : un combat lisible, juste et où chaque décision du joueur compte.

## Quand consulter cette fiche

- Tu implémentes une attaque (mêlée, tir, sort) pour le joueur ou un ennemi.
- Le combat est « mou », « confus » ou « injuste » d'après les retours de playtest.
- Tu choisis une formule de dégâts / d'armure ou tu règles des points de vie.
- Plusieurs ennemis attaquent en même temps et le joueur se fait submerger.
- Tu dois décider si une action peut en interrompre une autre (*cancel*).

---

## 1. Verbes de combat

Avant les chiffres, définir les **verbes** disponibles et leurs relations. Un combat intéressant naît des interactions entre verbes, pas de leur nombre.

| Verbe | Rôle | Contre-verbe typique |
|---|---|---|
| Attaquer (léger / lourd) | Infliger des dégâts, prendre l'initiative | Bloquer, esquiver, parer |
| Bloquer / garde | Réduire ou annuler un coup, au prix de mobilité ou d'endurance | Attaque qui brise la garde, saisie |
| Esquiver / dash | Éviter par le mouvement, souvent avec invulnérabilité courte | Attaque à zone large, attaque retardée |
| Parer | Fenêtre courte, haute récompense (contre-attaque, étourdissement) | Feinte, attaque à rythme irrégulier |
| Saisir / projeter | Battre une garde | Attaque rapide, esquive |
| Se repositionner | Contrôler la distance (*spacing*) | Projectile, attaque à allonge |

Règles :
- **Chaque verbe doit avoir un coût** (temps de récupération, endurance, ressource, exposition). Un verbe gratuit devient dominant.
- Viser des relations de type pierre-feuille-ciseaux entre options (voir [Équilibrage et difficulté](equilibrage-et-difficulte.md), section intransitif).
- Commencer avec 2–3 verbes solides ; en ajouter seulement si un playtest montre un manque de décisions.

## 2. Structure d'une attaque (frame data)

Toute action se découpe en trois phases. Les jeux de combat les mesurent en frames (1 frame = 1/60 s à 60 fps).

| Phase | Ce qui se passe | Ce que ça règle |
|---|---|---|
| **Anticipation** (*startup / windup*) | Pas encore de hitbox ; posture lisible | Réactivité, lisibilité, possibilité de réagir |
| **Active** (*active frames*) | Hitbox présente, peut toucher | Fenêtre de danger, tolérance du timing |
| **Récupération** (*recovery*) | Hitbox éteinte, personnage vulnérable | Punition d'une attaque ratée, engagement |

Valeurs de départ (règles empiriques, à ajuster au playtest) :

| Type d'action | Anticipation | Active | Récupération |
|---|---|---|---|
| Attaque légère du joueur | très courte (≈ 2–6 frames) | 2–4 frames | courte |
| Attaque lourde du joueur | longue, ressentie | 3–6 frames | longue (engagement) |
| Attaque d'ennemi standard | **toujours plus longue que le temps de réaction humain** (≈ 0,2–0,25 s minimum, plus pour un joueur occasionnel) | courte | assez longue pour punir |
| Attaque de boss signature | 0,5 s et plus, avec signal visuel + sonore | variable | fenêtre de punition claire |

Principes :
- **Joueur : anticipation courte** (réactivité). **Ennemi : anticipation longue** (lisibilité). Cette asymétrie est normale et souhaitable.
- **La récupération est le prix de l'attaque.** C'est elle qui crée le risque et la fenêtre de contre-attaque.
- **Engagement** (*commitment*) : plus une attaque est puissante, plus elle doit engager le joueur (récupération longue, mouvement bloqué). Un coup fort sans engagement devient spammable.
- Le **frame advantage** (qui récupère en premier après un échange) détermine qui a l'initiative ensuite. Bloquer une attaque devrait généralement laisser l'avantage au défenseur, sinon bloquer ne sert à rien.

## 3. Hitbox et hurtbox

- **Hitbox** : volume qui inflige des dégâts. **Hurtbox** : volume qui reçoit des dégâts. Toujours séparés de la capsule de collision physique.
- Les hitbox d'attaque peuvent **déborder légèrement** l'animation (indulgence pour le joueur). Les hitbox ennemies doivent **coller au visuel ou être plus petites** : un coup qui touche « dans le vide » est vécu comme une injustice.
- La hurtbox du joueur peut être **plus petite** que son sprite/mesh (classique en *bullet hell* : hitbox réduite au cœur du vaisseau).
- **Un coup = une touche par cible** : mémoriser les cibles déjà touchées pendant la phase active pour éviter les touches multiples involontaires.
- Prévoir un **affichage debug** des hitbox/hurtbox dès le début. Indispensable pour régler et diagnostiquer.

## 4. Télégraphie

Le joueur doit pouvoir **lire l'intention** d'un ennemi avant qu'elle se réalise.

Canaux à combiner (au moins deux pour les attaques dangereuses) :
- **Pose** : silhouette d'anticipation exagérée, distincte pour chaque attaque.
- **Visuel** : éclat, changement de couleur, zone au sol (*AoE marker*), ligne de visée laser.
- **Audio** : son d'annonce distinct par attaque (indispensable pour les menaces hors écran).
- **Temps** : délai fixe ou rythme reconnaissable.

Règles :
- **Plus une attaque fait mal, plus elle doit être télégraphiée.**
- Une attaque **non télégraphiée** n'est acceptable que si elle est faible ou évitable par un positionnement général.
- Les **feintes** et retards (*delayed attacks*) sont des outils avancés : à réserver aux ennemis d'élite et boss, et ils doivent rester apprenables (même délai à chaque fois).
- Signaler les menaces **hors champ** (indicateur directionnel, son spatialisé).

## 5. Invulnérabilité, impact, recul

| Mécanique | Usage | Valeur de départ | Nature |
|---|---|---|---|
| **i-frames** d'esquive | Rendre l'esquive fiable | une fraction de la durée du dash (souvent le début) | Gameplay |
| i-frames après dégât subi | Éviter les morts en chaîne (*stunlock*) | ≈ 0,5–1,5 s en plateforme/action 2D, avec clignotement | Gameplay |
| **Hit stop** (*hit pause*) | Donner du poids à l'impact | quelques frames (≈ 2–10), proportionnel à la puissance | Présentation (fige brièvement le temps) |
| **Hit stun** | La cible est interrompue | doit dépasser la récupération de l'attaquant si on veut des combos | Gameplay |
| **Knockback** (recul) | Séparer, repousser, utiliser l'environnement | impulsion + friction ; plus fort sur coup lourd | Gameplay |
| Super armor / poise | Certaines attaques ne sont pas interrompues | réservé aux ennemis lourds et coups lourds | Gameplay |

Notes :
- Le **hit stop** s'applique en général à l'attaquant **et** à la cible ; un léger tremblement de la cible pendant la pause renforce l'effet. Voir [Game feel / juice](../ressenti/game-feel-juice.md).
- Toujours afficher clairement l'**état invulnérable** (clignotement, transparence) : le joueur doit savoir quand il est protégé.
- Éviter le **stunlock** du joueur : plafonner le hit stun cumulé ou accorder des i-frames après un certain nombre de coups.

## 6. Annulations et priorités

- **Cancel window** : fenêtre pendant laquelle une action peut être interrompue par une autre (ex. annuler la récupération d'une attaque par une esquive).
- Définir explicitement une **table de priorités** : quelles actions annulent quelles autres, et dans quelle phase.

| Action en cours → | Esquive | Attaque suivante (combo) | Saut | Bloc |
|---|---|---|---|---|
| Anticipation | souvent oui | non | selon jeu | souvent oui |
| Active | non | non | non | non |
| Récupération (début) | selon le niveau d'engagement voulu | fenêtre de combo | non | non |
| Récupération (fin) | oui | oui | oui | oui |

- Combiner avec un **input buffer** (≈ 0,1–0,2 s) pour que les entrées faites un peu tôt ne soient pas perdues (voir [Contrôles et mouvement](../ressenti/controles-et-mouvement.md)).
- Trop d'annulations = le combat perd son engagement. Trop peu = sensation de lourdeur. C'est **le** réglage qui définit l'identité d'un système (réactif type character action vs engagé type Souls-like).

## 7. Formules de dégâts et d'armure

| Modèle | Formule | Avantages | Pièges |
|---|---|---|---|
| **Soustractive** | `dégâts = max(min_dmg, atk - def)` | Simple, intuitive, rend les petits coups inutiles contre les tanks | Très sensible : une petite variation de `def` change tout ; risque de 0 dégât → prévoir un plancher |
| **Pourcentage fixe** | `dégâts = atk × (1 - réduction)` avec réduction plafonnée | Lisible (« -30 % ») | Si on cumule des réductions additives, on atteint 100 % → toujours plafonner ou multiplier |
| **Ratio (rendements décroissants)** | `dégâts = atk × K / (K + def)` (ex. K = 100, modèle utilisé par League of Legends) | Jamais 0 ; chaque point de `def` augmente la survie effective de façon **linéaire** (`PV effectifs = PV × (1 + def/K)`) | Moins intuitif pour le joueur ; afficher la réduction calculée |
| **Multiplicateurs de type** | `dégâts × table[type_atk][type_def]` | Crée des matchups, du contre-jeu | Doit rester mémorisable ; afficher l'efficacité (« super efficace ») |

Recommandations :
- **Petits nombres** si le jeu est tactique et lisible (on peut compter les coups). **Grands nombres** si la progression est longue et cumulative (RPG, ARPG).
- Ordre de calcul à fixer **une fois pour toutes** et documenter : base → bonus additifs → multiplicateurs → réduction de la cible → critique → plancher/plafond → arrondi.
- Regrouper les bonus **additifs dans une même catégorie**, **multiplier entre catégories** : évite l'explosion exponentielle tout en gardant chaque catégorie utile.
- Le **critique** : chance × multiplicateur. Valeur moyenne = `1 + chance × (mult - 1)`. Un critique très fréquent et faible devient du bruit ; rare et fort crée des moments.

## 8. Rythme : DPS, TTK, temps pour mourir

- **DPS** = dégâts moyens par seconde, incluant précision, critique, rechargement et temps morts.
- **TTK** (*time to kill*) = PV de la cible / DPS effectif. **TTD** (*time to die*) = la même chose côté joueur.
- Le rapport TTK/TTD définit le genre :
  - TTK court + TTD court : tactique, tendu, punitif (shooter tactique).
  - TTK long + TTD long : duel d'endurance, place pour les décisions en combat (action-RPG, MOBA).
  - TTK court + TTD long : power fantasy (horde, beat'em all).
- **Compter en coups**, pas en PV : « un ennemi de base meurt en 3 coups légers », « le joueur survit à 4 coups d'ennemi de base ». Plus robuste à régler et à communiquer.
- Les **seuils de coups** comptent plus que la valeur exacte : passer de 3 à 2 coups pour tuer est un changement majeur ; passer de 104 à 110 dégâts peut ne rien changer.

## 9. Mêlée vs distance

| Aspect | Mêlée | Distance |
|---|---|---|
| Risque | Élevé (proximité) | Faible à moyen |
| Récompense attendue | Dégâts plus forts, contrôle (étourdissement, recul) | Sécurité, précision |
| Défi principal | Timing, spacing | Visée, gestion de munitions et de couverture |
| Aide à la visée | Magnétisme / *soft lock* vers la cible | Aim assist, friction de visée (manette) |

- Si les deux coexistent, **la mêlée doit être récompensée** (dégâts, ressources rendues comme dans DOOM (2016) avec ses *glory kills*) sinon le joueur restera à distance.
- Donner aux ennemis des moyens de **forcer le changement de distance** (rusher contre le sniper, zone contre le campeur).

## 10. Gestion des ennemis multiples : jetons d'attaque

Problème : si tous les ennemis à portée attaquent dès qu'ils peuvent, le joueur est submergé de façon illisible.

Solution standard : un **gestionnaire de jetons d'attaque** (*attack tokens*, souvent appelé *kung-fu circle*).
- Un pool limité de jetons (ex. 1–3 selon difficulté) ; un ennemi doit en obtenir un pour attaquer.
- Les autres **tournent autour**, se repositionnent, provoquent : ils restent menaçants mais n'attaquent pas.
- Attribuer en priorité aux ennemis **visibles à l'écran** et **devant** le joueur ; pénaliser ceux derrière la caméra.
- Poids différents : un ennemi lourd consomme plus de jetons.
- Rendre le jeton après un délai de récupération (pas immédiatement après l'attaque) pour garder un rythme.

```text
on_enemy_wants_attack(enemy):
    cost = enemy.attack_token_cost
    if tokens_available >= cost and enemy.is_on_screen:
        tokens_available -= cost
        enemy.start_attack()
        schedule(enemy.attack_duration + token_cooldown, release(cost))
    else:
        enemy.reposition_or_taunt()
```

La difficulté peut se régler presque entièrement par **le nombre de jetons** et **la durée d'anticipation**, sans toucher aux dégâts.

## 11. Contre-mesures et profondeur

- Chaque menace doit avoir **au moins une réponse** claire (esquive, blocage, interruption, positionnement).
- Chaque option du joueur doit avoir **au moins un contre** côté ennemis, sinon elle devient dominante.
- Varier les ennemis selon **la réponse qu'ils exigent** (voir [IA et ennemis](ia-ennemis.md)), pas seulement selon leurs stats.
- Récompenser la maîtrise : parade parfaite, esquive au dernier moment (*perfect dodge*), punition après récupération.

---

## Anti-patterns et pièges

- **Hitbox ennemie plus grande que le visuel** : sentiment d'injustice garanti.
- **Attaque instantanée et forte** sans télégraphie.
- **Ennemis qui attaquent tous ensemble** sans régulation.
- **Sac à PV** : augmenter les PV pour augmenter la difficulté rend le combat long, pas intéressant.
- **Option dominante** : une attaque sans coût ni contre (spam d'un coup sûr).
- **Stunlock** du joueur sans issue.
- **Absence de feedback** sur un coup qui touche ou qui est bloqué : le joueur ne sait pas ce qui fonctionne.
- **Formules opaques** : le joueur ne comprend pas pourquoi il fait peu de dégâts.

## Checklist

- [ ] Les verbes de combat et leurs contres sont listés et chacun a un coût.
- [ ] Chaque attaque a anticipation / active / récupération définies et réglables en données.
- [ ] Les attaques ennemies ont une anticipation supérieure au temps de réaction humain.
- [ ] Hitbox et hurtbox sont séparées de la collision et visualisables en debug.
- [ ] Une cible n'est touchée qu'une fois par attaque.
- [ ] Les attaques dangereuses ont au moins deux signaux (visuel + audio).
- [ ] Les i-frames (esquive, après dégât) sont visibles pour le joueur.
- [ ] Hit stop, flash et son d'impact sont en place (présentation).
- [ ] La table des annulations est explicite et un input buffer existe.
- [ ] L'ordre de calcul des dégâts est documenté, avec plancher et plafonds.
- [ ] Le nombre de coups pour tuer / pour mourir est fixé pour les cas de base.
- [ ] Un système de jetons limite les attaques simultanées.
- [ ] Le joueur ne peut pas être enchaîné sans issue (anti-stunlock).

## Pistes d'implémentation

- Décrire chaque attaque en **données** (DataAsset, Resource, ScriptableObject, JSON) : durées par phase, forme et décalage de hitbox, dégâts, recul, hit stop, flags d'annulation. Ne jamais coder les durées en dur.
- Piloter les phases par des **événements d'animation** (*anim notifies*) ou par un timer, mais garder une seule source de vérité.
- Exécuter la logique de combat à **pas de temps fixe** si la précision au frame près compte (jeu de combat, rollback).
- **UE5** : `AnimNotifyState` pour activer/désactiver les hitbox ; Gameplay Ability System (GAS) pour coûts, cooldowns, tags d'état (`State.Invulnerable`, `State.Stunned`) et Gameplay Effects pour les dégâts.
- **Godot** : `Area2D`/`Area3D` pour hitbox et hurtbox avec couches de collision dédiées ; `AnimationPlayer` pour activer les formes au bon moment.
- **Unity** : triggers sur couches dédiées + `Physics.OverlapBox` pendant la phase active ; événements d'animation pour les phases.

## Voir aussi

- [Game feel / juice](../ressenti/game-feel-juice.md)
- [Contrôles et mouvement](../ressenti/controles-et-mouvement.md)
- [IA et ennemis](ia-ennemis.md)
- [Équilibrage et difficulté](equilibrage-et-difficulte.md)
- [Audio](../interface/audio.md)
- [Accessibilité](../interface/accessibilite.md)

## Sources

- Steve Swink, *Game Feel: A Game Designer's Guide to Virtual Sensation*, Morgan Kaufmann, 2008.
- Ian Schreiber & Brenda Romero, *Game Balance*, CRC Press, 2021.
- Ian Schreiber, *Game Balance Concepts* (cours en ligne), 2010 — https://gamebalanceconcepts.wordpress.com/
- League of Legends Wiki, « Armor » (formule `100 / (100 + armure)`) — https://leagueoflegends.fandom.com/wiki/Armor
- Masahiro Sakurai, chaîne YouTube *Masahiro Sakurai on Creating Games* (2022–2024), épisodes sur le hit stop et l'anticipation.
- Infil, *Fighting Game Glossary* — https://glossary.infil.net/
