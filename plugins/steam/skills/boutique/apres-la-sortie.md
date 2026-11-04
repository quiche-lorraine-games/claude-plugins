# Après la sortie : mises à jour, annonces, événements

> **En bref** : comment publier une mise à jour sans casser le jeu des joueurs, l'annoncer (annonces, visuels temporaires, *Update Visibility Rounds*, réduction), et les règles des annonces Steam. Relevé le 04/11/2026 sur la documentation Steamworks.

## Quand consulter cette fiche

- Tu publies un correctif ou une grosse mise à jour.
- Tu rédiges une annonce ou un événement Steam.
- Tu veux remettre le jeu en avant après la sortie.

---

## 1. Publier une mise à jour

- Après la sortie, les joueurs reçoivent le build de la branche **`default`**. Envoie d'abord le nouveau build sur une **branche de test protégée par mot de passe**, teste-le depuis Steam, puis passe-le sur `default`.
- Un nouveau dépôt (*depot*) doit être ajouté à **tous les paquets** (boutique et clés).
- Les mises à jour passent par Steam : n'impose pas de téléchargement de contenu dans le jeu.
- Chaque mise à jour est téléchargée par tous les joueurs avant de rejouer : attention à la taille.
- Contenu gratuit → dans le jeu de base ; petits contenus payants → achats en jeu (Steam Inventory, microtransactions Steam) ; gros contenus payants (cartes, modes, extension) → DLC.

## 2. Annoncer

| Outil | Usage | Règles |
|---|---|---|
| **Annonce ou événement** | toute nouvelle, avec notes de version | visible sur la page (les deux dernières), la communauté, la bibliothèque, le fil d'activité des abonnés, le flux RSS |
| **Visuels temporaires** (*Artwork Overrides*) | annoncer une mise à jour ou un DLC sur les capsules | un mois au plus, texte traduit dans toutes les langues du jeu, contenu déjà disponible seulement (voir [visuels.md](visuels.md)) |
| **Update Visibility Round** | place sur l'accueil (« Récemment mis à jour ») pour les joueurs qui ont le jeu ou l'ont en liste de souhaits | pour une mise à jour majeure ; il faut d'abord une annonce ; utilisable après la fin de la visibilité de lancement (deux semaines après une sortie en accès anticipé) ; pas de délai entre deux. Les DLC n'en ont pas : utiliser une de celles du jeu |
| **Réduction** | profiter de l'attention de la mise à jour | 20 % ou plus pour prévenir les wishlists ; règles des 30 jours (voir [prix-et-reductions.md](prix-et-reductions.md)) |

### Les annonces Steam

- Visuels : **couverture 800 × 450** obligatoire, en-tête 1920 × 622 facultatif ; images du corps en JPG, PNG ou GIF animé, affichées sur 800 px de large au plus ; vidéos YouTube intégrables.
- Choisis la **bonne catégorie** : elle décide où et à qui l'annonce s'affiche (notes de version, mise à jour majeure, diffusion, réduction en jeu…). Les événements datés (diffusion, offre limitée) ont une date de fin et sont archivés ensuite.
- On peut programmer une annonce, la traduire (import CSV possible), la cloner. Une publication peut mettre jusqu'à une heure à apparaître dans la bibliothèque (modération).
- On ne publie pas un événement dont le début est passé, et on ne déplace pas un début déjà passé.
- « Mise en avant pour les grands événements » : à réserver aux événements majeurs, espacés.
- Règles de Valve : contenu adapté au public du jeu et sans risque au travail ; une annonce sur un autre produit se marque *Cross Promotion* ; pas de promotion d'une meilleure version vendue ailleurs.
- Pour l'accès anticipé : une annonce de type mise à jour (majeure, régulière ou notes de version) au moins tous les 12 mois, sinon avertissement sur la page.

## 3. Conseils de Valve

- Corriger vite ce que signalent les joueurs, et l'annoncer : c'est la meilleure preuve d'écoute.
- Pour ses propres jeux, Valve sort une **grosse mise à jour tous les 1 à 2 mois au plus**, annoncée 3 ou 4 jours avant, en dévoilant les changements petit à petit.
- L'équipe qui fait le contenu lit aussi les retours des joueurs (sans passer ses journées sur le forum).
- Une annonce a un but ; sans raison de publier, ne publie pas : trop d'annonces lassent.
- Mettre en avant les créations des joueurs, reprendre les références de la communauté, teaser le contenu à venir.

---

## Pièges

- Envoyer un build directement sur `default` sans l'avoir lancé depuis Steam.
- Oublier d'ajouter un nouveau dépôt aux paquets de clés.
- Gaspiller un *Update Visibility Round* sur un petit correctif.
- Annoncer « Bientôt disponible » sur une capsule temporaire.
- Une annonce mal classée, qui n'atteint pas les joueurs visés.

## Checklist

- [ ] Build testé sur une branche protégée depuis Steam, puis passé sur `default`
- [ ] Nouveaux dépôts ajoutés à tous les paquets
- [ ] Annonce avec couverture 800 × 450, bonne catégorie, traduite
- [ ] Mise à jour majeure : *Update Visibility Round*, visuels temporaires traduits, réduction éventuelle à 20 % ou plus en respectant les délais
- [ ] Retours des joueurs suivis après la publication

## Pistes d'implémentation

- Garde les notes de version dans le repo du jeu (ex. `CHANGELOG.md`), et rédige l'annonce Steam à partir d'elles.
- Affiche le numéro de version dans le menu du jeu, pour que les joueurs puissent le citer dans leurs retours.

## Voir aussi

- [visuels.md](visuels.md) : visuels temporaires, visuels d'événement.
- [prix-et-reductions.md](prix-et-reductions.md)
- [visibilite-et-wishlists.md](visibilite-et-wishlists.md)

## Sources

- [Updating Your Game - Best Practices](https://partner.steamgames.com/doc/store/updates)
- [Events and Announcements Tools](https://partner.steamgames.com/doc/marketing/event_tools)
- [Visibility on Steam](https://partner.steamgames.com/doc/marketing/visibility) (*Update Visibility Rounds*)
- [Graphical Asset Rules](https://partner.steamgames.com/doc/store/assets/rules) (visuels temporaires)
- [Early Access](https://partner.steamgames.com/doc/store/earlyaccess)
