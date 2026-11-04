# Visuels de la boutique et de la bibliothèque

> **En bref** : toutes les images que Valve demande pour la page boutique, la bibliothèque, la communauté et les événements, avec leurs tailles exactes, leurs formats et les règles de contenu. Relevé le 04/11/2026 sur la documentation Steamworks ; les tailles ont changé en août 2024 et les anciennes ne sont plus acceptées.

## Quand consulter cette fiche

- Tu prépares ou commandes les visuels d'une page Steam.
- Tu vérifies une capsule avant de l'envoyer : taille, lisibilité du logo, texte autorisé.
- Tu veux annoncer une mise à jour ou un événement sur les capsules.
- Tu génères un visuel (par IA ou à la main) et tu dois l'exporter aux bonnes dimensions.

---

## 1. Tailles exactes

Règle de Valve : les dimensions doivent être exactes. Les gabarits officiels (*templates*) se téléchargent depuis la page [Store Graphical Assets](https://partner.steamgames.com/doc/store/assets/standard) ; ils montrent aussi les zones de texte.

### Boutique

| Visuel | Obligatoire | Taille | Où il apparaît |
|---|---|---|---|
| *Header capsule* (capsule d'en-tête) | oui | 920 × 430 | haut de la page, « Recommandé pour vous », Big Picture, offres du jour |
| *Small capsule* (petite capsule) | oui | 462 × 174 | listes : recherche, meilleures ventes, nouveautés. Réduite automatiquement en 184 × 69 et 120 × 45 |
| *Main capsule* (capsule principale) | oui | 1232 × 706 | carrousel en haut de l'accueil |
| *Vertical capsule* (capsule verticale) | oui | 748 × 896 | haut de l'accueil pendant les soldes saisonnières, pages de soldes |
| Captures d'écran | oui, **5 au minimum** | 1920 × 1080 au minimum, 16:9 | page boutique, accueil |
| *Page background* (arrière-plan) | non | 1438 × 810 | fond de la page ; sans lui, Steam en tire un de la dernière capture |
| *Bundle header* | si lot | 707 × 232 | haut de la page d'un lot |

### Communauté et client

| Visuel | Obligatoire | Taille | Format |
|---|---|---|---|
| *Shortcut icon* (icône de raccourci) | oui | 256 × 256 | .ico ou .png (Steam génère le .ico depuis un .png) |
| *App icon* (icône de l'application) | oui | 184 × 184 | .jpg |

### Bibliothèque

| Visuel | Obligatoire | Taille | Contenu |
|---|---|---|---|
| *Library capsule* | oui | 600 × 900 | illustration et logo ; demi-taille générée automatiquement |
| *Library header* | oui | 920 × 430 | comme la capsule d'en-tête ; sans lui, Steam reprend celle de la boutique |
| *Library hero* | oui | 3840 × 1240, .png | **illustration seule, aucun texte**. Zone sûre de 860 × 380 au centre, jamais rognée |
| *Library logo* | oui | 1280 de large et/ou 720 de haut, .png transparent | le logo seul, posé sur le *hero* |

Les visuels de bibliothèque ne s'affichent qu'une fois la page boutique publiée. Après l'envoi du logo, un outil d'aperçu permet de le placer : en bas à gauche, en haut au centre, au centre, en bas au centre.

### Événements et annonces

| Visuel | Obligatoire | Taille |
|---|---|---|
| *Event cover* (couverture) | oui pour chaque événement | 800 × 450 |
| *Event header* (en-tête) | non | 1920 × 622 (voir le gabarit pour le rognage) |

Les images insérées dans le corps d'une annonce s'affichent sur 800 px de large au plus.

---

## 2. Règles de contenu des capsules

Règles de Valve, en vigueur depuis le 1er septembre 2022 ([Graphical Asset Rules](https://partner.steamgames.com/doc/store/assets/rules)). Sur les capsules de base, **uniquement l'illustration du jeu, son nom et un sous-titre officiel**. Donc :

- aucune note de critique ou d'avis, ni Steam ni presse ;
- aucun nom, symbole ou logo de récompense ;
- aucun texte de réduction (« En promo », « −90 % ») ;
- aucun appel à l'action (« Précommandez », « Ajoutez à votre liste de souhaits ») ;
- rien qui fasse la promotion d'un autre produit, suite comprise ;
- aucun autre texte.

Pour toutes les capsules, boutique et bibliothèque :
- un logo ou un nom de produit **lisible** ;
- des dimensions exactes ;
- une illustration adaptée à un public PG-13.

Un jeu qui ne respecte pas ces règles peut perdre de la visibilité et n'est pas éligible aux soldes et événements officiels.

**Exception : les *Artwork Overrides*** (visuels temporaires). Pour annoncer une grosse mise à jour, un DLC ou un événement en cours :
- obligatoirement par l'outil *Artwork Overrides*, pour **un mois au plus** ;
- texte traduit dans au moins toutes les langues du jeu ;
- uniquement pour du contenu **déjà disponible** (« Mise à jour majeure disponible », « Nouveau DLC ») ; jamais « Ajoutez-le à votre liste de souhaits », « Précommandez » ou une date.

Les citations de presse, notes et récompenses ont leurs propres emplacements sur la page (*Store Page Accolades*, voir [page-boutique.md](page-boutique.md)).

---

## 3. Conseils de Valve pour la composition

- Reprends l'illustration principale et le logo du marketing (boîte, affiche) : l'image doit dire tout de suite quelque chose d'important sur le jeu et donner une idée du gameplay.
- **Petite capsule** : le logo doit rester lisible à 120 × 45 ; en pratique, il remplit presque toute la capsule. Son illustration peut différer des autres capsules.
- **Library hero** : place ce qui compte (visage du personnage, par exemple) dans la zone sûre de 860 × 380, et étends l'illustration sur tout le cadre.
- **Library logo** : le logotype seul (titre dans sa typographie), éventuellement un pictogramme à côté, sur fond transparent, sans autre mot.
- **Arrière-plan** : discret, peu lumineux, pour ne pas concurrencer le contenu.
- En règle générale, les capsules ne changent pas ; les visuels temporaires servent aux événements.

---

## 4. Pièges

- Exporter aux tailles d'avant août 2024 (par exemple 460 × 215 pour la capsule d'en-tête, taille que citent encore de vieux guides) : elles sont refusées. L'offre du jour (*Daily Deal*) réutilise automatiquement la capsule d'en-tête.
- Un logo fin ou détaillé, illisible à 120 × 45 dans la petite capsule.
- Du texte dans le *library hero*.
- Un logo de bibliothèque sur fond opaque.
- Mettre la date de sortie, « Démo disponible » ou un laurier de festival sur une capsule.
- Publier la page avec des visuels d'un projet non annoncé : publier envoie toutes les images sur les serveurs publics, où des sites tiers peuvent les récupérer, même si le jeu est caché.

---

## Checklist

- [ ] Capsule d'en-tête 920 × 430, petite 462 × 174, principale 1232 × 706, verticale 748 × 896
- [ ] Logo lisible sur la petite capsule réduite à 120 × 45 (vérifier en réduisant l'image)
- [ ] Aucun texte sur les capsules hors titre et sous-titre officiel
- [ ] Au moins 5 captures de gameplay, 1920 × 1080 minimum, 16:9
- [ ] Icône de raccourci 256 × 256 (.png ou .ico) et icône d'application 184 × 184 (.jpg)
- [ ] Capsule de bibliothèque 600 × 900 et en-tête de bibliothèque 920 × 430
- [ ] *Hero* 3840 × 1240 .png sans texte, l'essentiel dans les 860 × 380 du centre
- [ ] Logo de bibliothèque .png transparent, 1280 de large ou 720 de haut
- [ ] Couverture d'événement 800 × 450 prête pour la première annonce
- [ ] Illustrations adaptées à un public PG-13

## Pistes d'implémentation

- **Vérifier une image** avant de la livrer : `python3 -c "import struct,sys; d=open(sys.argv[1],'rb').read(24); print(struct.unpack('>II', d[16:24]))" capsule.png` donne largeur et hauteur d'un PNG ; ou `file capsule.png`, ou `identify` d'ImageMagick s'il est installé.
- **Captures depuis Godot** : `get_viewport().get_texture().get_image().save_png("user://capture.png")` dans un script de debug, avec une fenêtre en 1920 × 1080 (ou plus) et une interface masquable. Valve conseille de garder l'interface du jeu visible sur certaines captures : elle aide le joueur à comprendre comment il joue.
- **Captures localisées** : déposer la version traduite sur la miniature de la capture d'origine dans Steamworks ; un suffixe de langue dans le nom (ex. `combat_french.jpg`) aide l'outil.
- Garder les fichiers sources (calques, logo vectoriel) dans le repo du jeu, avec un dossier par taille exportée.

## Voir aussi

- [page-boutique.md](page-boutique.md) : captures, bande-annonce, description, tags.
- [apres-la-sortie.md](apres-la-sortie.md) : visuels temporaires pour une mise à jour.
- [demo-playtest-next-fest.md](demo-playtest-next-fest.md) : visuels d'une démo et d'un Playtest.

## Sources

- [Graphical Assets - Overview](https://partner.steamgames.com/doc/store/assets)
- [Store Graphical Assets](https://partner.steamgames.com/doc/store/assets/standard)
- [Library Assets](https://partner.steamgames.com/doc/store/assets/libraryassets)
- [Graphical Asset Rules](https://partner.steamgames.com/doc/store/assets/rules)
- [Events and Announcements Tools](https://partner.steamgames.com/doc/marketing/event_tools)
- [Store Page, Building and Editing](https://partner.steamgames.com/doc/store/page)
