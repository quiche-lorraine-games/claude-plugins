# Visibilité et wishlists

> **En bref** : comment Steam montre un jeu, ce qui compte et ce qui ne compte pas d'après Valve, et comment fonctionnent les listes de souhaits (*wishlists*) et leurs notifications. Relevé le 04/11/2026 sur la documentation Steamworks.

## Quand consulter cette fiche

- Tu bâtis la stratégie de lancement ou d'annonce.
- Tu te demandes si la note des avis, le trafic ou le taux de conversion pèsent sur la visibilité.
- Tu veux savoir quand les joueurs qui ont le jeu en liste de souhaits sont prévenus.
- Tu lis les chiffres de wishlists ou de trafic.

---

## 1. Ce qui compte, d'après Valve

| Facteur | Effet sur la visibilité algorithmique |
|---|---|
| **Achats et parties** | le signal fort : un jeu acheté et joué est montré à plus de monde |
| **Langues du jeu** | Steam montre davantage le jeu aux joueurs qui parlent une de ses langues |
| **Tags** | décident des pages de genre, des recommandations et de « Plus comme ça » (voir [page-boutique.md](page-boutique.md)) |
| Wishlists | **pas un facteur**, sauf exceptions comme l'onglet *Popular Upcoming* ; elles comptent par les notifications |
| Trafic de la page | **pas un facteur** en soi |
| Taux de conversion visite → achat | **pas un facteur** |
| Note des avis | **pas un facteur** tant qu'elle reste à 40 % ou plus (« Moyennes ») ; en dessous (« Plutôt négatives »), le jeu est moins mis en avant |

Il n'existe **aucune publicité payante** sur Steam, ni pour la Next Fest.

## 2. Visibilité à la sortie

À la sortie complète (pas en accès anticipé), le jeu :
- entre dans une **file des nouveautés** (*New Releases Queue*) : les jeux qui ont reçu le moins de vues depuis leur sortie passent en premier, selon les préférences de chaque joueur. C'est une base de visibilité qui sert à mesurer l'intérêt ;
- apparaît dans la liste de toutes les nouveautés ;
- déclenche un e-mail aux joueurs qui l'ont dans leur liste de souhaits.

Ensuite, s'il marche : recommandations personnalisées, « Nouveautés populaires » (*New and Trending*, d'où un jeu peut vite sortir si beaucoup de jeux populaires sortent en même temps), meilleures ventes, puis éventuellement la capsule principale de l'accueil. La capsule principale est personnalisée pour chaque joueur, selon ce que lui et ses amis jouent et achètent.

L'accès anticipé a une visibilité plus réduite ; la sortie de l'accès anticipé est traitée comme une première sortie complète (voir [acces-anticipe.md](acces-anticipe.md)).

Valve rappelle que la boutique ne suffit pas : un joueur peut avoir besoin de voir un jeu des dizaines de fois avant d'y prêter attention. L'annonce, la page Coming Soon tôt et la communication extérieure restent nécessaires.

## 3. Les wishlists

Dès que la page est publique, les joueurs peuvent ajouter le jeu à leur liste de souhaits. Ils reçoivent un e-mail ou une notification mobile :

| Déclencheur | Condition |
|---|---|
| Sortie (accès anticipé ou complète) | automatique ; une deuxième fois à la sortie de l'accès anticipé |
| Réduction | **20 % ou plus**, sur au moins le paquet le moins cher, pendant **plus de 8 heures** |
| Sortie d'une démo | bouton à presser soi-même, **une seule fois**, dans les **14 jours** après la première sortie de la démo |

**Délai entre deux notifications** : un joueur prévenu au sujet d'un jeu ne l'est plus pendant **2 semaines**, quel que soit le déclencheur (délai qui peut s'allonger pendant les soldes saisonnières). Espace donc la sortie de la démo, la sortie du jeu et les réductions d'au moins deux semaines pour que chacune touche tout le monde.

Seuls les joueurs dont l'e-mail est vérifié, et qui n'ont pas refusé ces messages, les reçoivent. Un e-mail bloqué plus d'une semaine n'est plus envoyé.

Selon Valve, aucun nombre minimum de wishlists ne déclenche la visibilité, et aucune formule ne prédit les ventes à partir d'eux.

## 4. Mesurer

- **Wishlists** : section *Wishlists* du rapport de ventes (ajouts, achats, suppressions), répartition par pays dans le rapport régional ; mise à jour une fois par jour, pour la veille.
- **Trafic** : onglet *Traffic Breakdown* de *Marketing & Visibility* : où le jeu a été montré, combien de fois, et combien de clics vers la page. On y voit aussi l'effet des e-mails de wishlists.
- Après chaque annonce, festival ou réduction, compare la courbe des wishlists pour savoir ce qui a marché.

---

## Pièges

- Lancer une réduction de 15 % en pensant prévenir les wishlists : il faut 20 %.
- Sortir la démo une semaine avant le jeu : le joueur prévenu pour la démo ne le sera pas pour la sortie.
- Se fier au trafic ou au taux de conversion comme levier de visibilité : Valve dit qu'ils ne comptent pas.
- Croire qu'une note « Moyennes » pénalise : seule la chute sous 40 % le fait.
- Oublier le bouton de notification de la démo, ou le presser des mois avant la Next Fest : il n'y en a qu'un.

## Checklist

- [ ] Page Coming Soon publique dès que le jeu peut être montré
- [ ] Langues du jeu choisies en tenant compte de la visibilité
- [ ] Tags complets et précis
- [ ] Démo, sortie et réductions espacées d'au moins deux semaines
- [ ] Première réduction après la sortie à 20 % ou plus si elle doit prévenir les wishlists
- [ ] Bouton de notification de la démo pressé au bon moment (dans les 14 jours)
- [ ] Suivi régulier des wishlists et du trafic, noté dans le plan de sortie

## Pistes d'implémentation

- Garde un tableau daté des wishlists (ajouts nets par semaine) et des événements (annonce, bande-annonce, festival, démo) dans le repo du jeu : c'est la seule façon de relier une action à son effet.

## Voir aussi

- [calendrier-de-sortie.md](calendrier-de-sortie.md)
- [prix-et-reductions.md](prix-et-reductions.md)
- [demo-playtest-next-fest.md](demo-playtest-next-fest.md)
- [apres-la-sortie.md](apres-la-sortie.md) : *Update Visibility Rounds*.

## Sources

- [Visibility on Steam](https://partner.steamgames.com/doc/marketing/visibility)
- [Wishlists](https://partner.steamgames.com/doc/marketing/wishlist)
- [Demos](https://partner.steamgames.com/doc/store/application/demos) (notification de sortie de démo)
- [Steam Next Fest](https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest) (pas de publicité payante)
