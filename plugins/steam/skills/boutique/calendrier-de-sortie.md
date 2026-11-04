# Calendrier de sortie

> **En bref** : les étapes et les délais imposés entre l'inscription à Steam Direct et le clic sur « Release App » : paiement, documents, revue de la page puis du build, page Coming Soon, date de sortie, permissions. Relevé le 04/11/2026 sur la documentation Steamworks. Le rétroplanning complet est dans [gabarits/plan-de-sortie.md](gabarits/plan-de-sortie.md).

## Quand consulter cette fiche

- Tu fixes ou déplaces une date de sortie.
- Tu planifies l'annonce du jeu et la publication de sa page.
- Le studio n'a pas encore de compte Steamworks, ou crée un nouveau jeu.
- La date approche et tu vérifies que rien ne bloque.

---

## 1. Délais imposés par Valve

| Étape | Délai | Source |
|---|---|---|
| Documents (banque, fiscalité, identité) | **15 à 30 jours** pour un nouveau compte | Steam Direct |
| Attente entre le paiement des frais et la première sortie possible | **21 jours** | Steam Direct |
| Revue de la page boutique | 3 à 5 jours ouvrés en général ; soumettre **au moins 7 jours ouvrés** avant la mise en ligne voulue | Review Process |
| Revue du build | 3 à 5 jours ouvrés en général ; prévoir **au moins 7 jours ouvrés** | Review Process |
| Page Coming Soon publique avant la sortie | **au moins 2 semaines** | Coming Soon, Release Process |
| Changement de la date de sortie | possible jusqu'à **2 semaines** avant la date prévue, plus ensuite | Release Dates |
| Validation d'une proposition de prix | 1 à 2 jours ouvrés en général | Pricing |
| Contenu pour adultes (sexualité) | revue plus longue ; page et build soumis ensemble | Review Process |

La page de Steam Direct parle d'une revue de 1 à 5 jours ; la page *Review Process* donne 3 à 5 jours ouvrés et demande 7 jours ouvrés de marge : planifie avec la seconde.

**Les frais Steam Direct** : 100 $ par jeu (hors portefeuille Steam), non remboursables, rendus dans le versement qui suit 1 000 $ de revenu brut ajusté. Seul un administrateur du compte partenaire peut les payer, et le crédit d'application reste attaché au compte Steam de la personne qui a payé.

## 2. L'ordre des étapes

1. **Créer l'application** (un crédit Steam Direct par jeu) et remplir la checklist « Store Presence ».
2. **Soumettre la page à la revue** (*Mark as ready for review*). La page passe **avant** le build : on ne peut pas soumettre le build tant que la page n'est pas soumise.
3. Une fois la page approuvée, cliquer sur **Post as Coming Soon** : la page devient publique, la communauté (*Community Hub*) s'ouvre et les joueurs peuvent ajouter le jeu à leur liste de souhaits.
4. **Envoyer un build presque final** sur la branche `default`, avec toutes les fonctionnalités annoncées sur la page, puis le soumettre à la revue.
5. **Proposer les prix** dans toutes les devises (voir [prix-et-reductions.md](prix-et-reductions.md)) et, si voulue, la réduction de lancement.
6. Le jour J, quand la page est approuvée, publique depuis au moins deux semaines, et le build approuvé : cliquer sur **Release App**, puis **Publish Now** et **Release Now**. **Le jeu ne sort jamais tout seul.** Le bouton publie le paquet, applique la réduction de lancement, rend le jeu jouable et date la sortie à l'instant du clic.

Une fois la revue passée, il n'y en a plus : le jeu se met à jour librement.

**Permissions** : publier la page Coming Soon ou sortir le jeu demande deux permissions Steamworks, *Publish app changes to Steam* et *Manage pricing and discounts*. Vérifie bien avant le jour J que la personne qui cliquera les a.

## 3. La page Coming Soon

- Valve conseille de la publier **dès qu'on est prêt à parler du jeu en public**. Selon Valve, une page en ligne longtemps avant la sortie n'a pas d'inconvénient net, sauf si le jeu change beaucoup entre-temps. Un joueur qui a mis le jeu dans sa liste deux ans avant la sortie l'achète aussi volontiers qu'un joueur qui l'a fait deux semaines avant.
- Il faut au minimum les visuels de marque, des captures, une description et, idéalement, une bande-annonce de gameplay.
- **Attention aux fuites** : publier la page rend public tout son contenu (captures, vidéos, visuels de bibliothèque), même si le jeu est caché. Il en va de même quand le jeu passe en préchargement ou sort.

## 4. La date de sortie

- Il faut fixer une **date précise** dans Steamworks, même si elle n'est pas affichée.
- L'affichage public a cinq formats : date exacte, mois et année, trimestre, année, ou « Coming Soon ».
- Dans les listes de jeux à venir, le jeu est classé au **dernier jour** de la période affichée (dernier jour du mois, du trimestre…). Avec « Coming Soon », il passe derrière tous les jeux qui affichent une date.
- La date se modifie jusqu'à deux semaines avant ; ensuite, le jeu apparaît davantage dans les listes de sorties à venir et la date est figée. Valve envoie un rappel avant cette échéance.
- Le sélecteur de date masque les week-ends. Une sortie le week-end reste possible avec le bouton, mais Valve la déconseille : son équipe n'est pas là pour aider en cas de problème.
- La date sert aussi à Valve pour les invitations (Next Fest) et les rappels de revue.

## 5. Avant d'annoncer une date au public

Compte à rebours, à partir de la date de sortie voulue, avec les délais minimum de Valve :
- J − 2 semaines au plus tard : page Coming Soon publique, date figée ;
- J − 2 semaines − 7 jours ouvrés : page soumise à la revue ;
- build soumis au moins 7 jours ouvrés avant J ;
- pour un nouveau compte : 21 jours entre le paiement et J, et 15 à 30 jours de documents avant même d'accéder à Steamworks.

Ces délais sont des minimums. Pour une sortie qui compte sur les wishlists, la page doit être en ligne des mois avant (voir [visibilite-et-wishlists.md](visibilite-et-wishlists.md)), et une Next Fest se prépare plusieurs mois à l'avance (voir [demo-playtest-next-fest.md](demo-playtest-next-fest.md)).

---

## Pièges

- Annoncer une date à la presse avant d'avoir le compte Steamworks, les documents et les 21 jours d'attente.
- Soumettre le build sans avoir soumis la page : impossible.
- Laisser la bande-annonce s'encoder le jour J : la sortie est bloquée tant qu'une vidéo est en cours de conversion.
- Une date à moins de deux semaines qu'on veut encore déplacer.
- Personne de disponible avec les bonnes permissions au moment de cliquer.
- Sortir dans la même fenêtre que la Next Fest à laquelle le jeu est inscrit : il devient inéligible.
- Vouloir changer le nom du jeu après la revue de pré-sortie : Steamworks ne le permet plus (voir la page *Changing Your Game's Name* de la documentation). Fixe le nom définitif avant de soumettre la page.

## Checklist

- [ ] Compte Steamworks actif (documents validés), frais payés depuis au moins 21 jours le jour J
- [ ] Page soumise à la revue au moins 7 jours ouvrés avant sa mise en ligne voulue
- [ ] Page Coming Soon publique au moins 2 semaines avant J (des mois avant, de préférence)
- [ ] Date précise saisie ; format d'affichage choisi ; date figée 2 semaines avant
- [ ] Build presque final sur `default`, soumis au moins 7 jours ouvrés avant J, toutes les fonctionnalités annoncées présentes
- [ ] Prix proposés dans toutes les devises, réduction de lancement réglée avant la sortie
- [ ] Bandes-annonces encodées
- [ ] Une personne avec les permissions *Publish app changes* et *Manage pricing and discounts* disponible le jour J, en semaine
- [ ] Annonce communautaire prête pour la sortie

## Pistes d'implémentation

- Garde le calendrier dans le repo du jeu, à partir de [gabarits/plan-de-sortie.md](gabarits/plan-de-sortie.md), avec les dates réelles de chaque étape.
- Pour calculer « 7 jours ouvrés avant », compte en jours ouvrés américains (Valve est à Bellevue, États-Unis) et garde une marge pour les jours fériés de fin d'année.

## Voir aussi

- [gabarits/plan-de-sortie.md](gabarits/plan-de-sortie.md) : rétroplanning complet.
- [page-boutique.md](page-boutique.md) : ce que vérifie la revue.
- [prix-et-reductions.md](prix-et-reductions.md) : réduction de lancement.
- [acces-anticipe.md](acces-anticipe.md) : sortie en accès anticipé.

## Sources

- [Steam Direct](https://partner.steamgames.com/steamdirect)
- [Steam Direct Fee](https://partner.steamgames.com/doc/gettingstarted/appfee)
- [Review Process](https://partner.steamgames.com/doc/store/review_process)
- [Coming Soon](https://partner.steamgames.com/doc/store/coming_soon)
- [Release Process](https://partner.steamgames.com/doc/store/releasing)
- [Release Dates](https://partner.steamgames.com/doc/store/release_dates)
- [Store Page, Building and Editing](https://partner.steamgames.com/doc/store/page)
- [Trailers](https://partner.steamgames.com/doc/store/trailer)
