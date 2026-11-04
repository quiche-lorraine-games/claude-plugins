---
name: boutique
description: Référentiel en français pour préparer la sortie d'un jeu sur Steam, tiré de la documentation Steamworks. À charger quand on prépare ou critique une page boutique Steam (capsules et visuels aux tailles exactes, captures, bande-annonce, description courte et longue, tags, langues), qu'on planifie une sortie (Steam Direct, revue de Valve, page Coming Soon, date de sortie, wishlists, visibilité), qu'on décide d'un prix ou d'une réduction (réduction de lancement, délais de 30 jours, soldes saisonnières), qu'on prépare une démo, un Steam Playtest, une participation à la Steam Next Fest ou un accès anticipé, qu'on vise la compatibilité Steam Deck (Verified), qu'on intègre succès, Steam Cloud ou Steam Input dans un jeu Godot, ou qu'on prépare une mise à jour et son annonce. Contient aussi un gabarit de rétroplanning de sortie à copier dans le projet.
---

# Préparer la sortie sur Steam

Référentiel tiré de la documentation Steamworks de Valve, pour préparer et critiquer tout ce qui précède et accompagne la sortie d'un jeu sur Steam. Les fiches sont dans le même dossier que ce fichier.

## Comment s'en servir

1. **Le projet prime.** Le calendrier, le prix, les langues et les choix de sortie du projet (GDD, plan marketing, contrat d'éditeur) l'emportent sur ce référentiel.
2. **Lis la fiche avant d'agir.** Repère la fiche dans la table ci-dessous et lis au moins ses règles et sa checklist. Une ou deux fiches suffisent en général.
3. **Les règles de Valve changent.** Chaque fiche dit à quelle date elle a été relevée et cite ses pages sources. Avant une décision qui engage (date de sortie, prix, réduction, inscription à un festival), ouvre la page source pour vérifier qu'elle n'a pas changé. Si une page contredit la fiche, c'est la page qui a raison : dis-le à l'utilisateur.
4. **Distingue règle et conseil.** Les fiches séparent ce que Valve impose (« règle de Valve ») de ce qu'elle recommande et de ce qui n'est qu'un point de départ. Ne présente jamais un conseil comme une obligation.
5. **Tu n'as pas accès à Steamworks.** Le site partenaire (`partner.steamgames.com`, partie connectée) demande un compte du studio. Tu prépares les fichiers, les textes, les checklists et le calendrier ; l'humain les saisit et clique sur les boutons (revue, publication, sortie, prix).
6. **Ne publie rien à la place de l'humain.** Publier la page, lancer la sortie, changer un prix ou une réduction est irréversible ou presque (le nom du jeu, par exemple, ne change plus après la revue). Prépare, explique, puis laisse l'humain décider.
7. **Cite tes sources.** Quand une proposition s'appuie sur une fiche, mentionne-la (ex. « cf. `steam:boutique`, `prix-et-reductions.md`, délai de 30 jours après une hausse »).
8. **Les gabarits se copient dans le projet.** [gabarits/plan-de-sortie.md](gabarits/plan-de-sortie.md) se remplit dans le repo du jeu (ex. `docs/`), jamais ici.

## Table de routage

| Tu travailles sur… | Lis d'abord |
|---|---|
| Les capsules, l'icône, les images de la bibliothèque, l'arrière-plan | [visuels.md](visuels.md) |
| Les captures, la bande-annonce, la description, les tags, les langues de la page | [page-boutique.md](page-boutique.md) |
| Le calendrier de sortie : Steam Direct, revue, Coming Soon, date, bouton de sortie | [calendrier-de-sortie.md](calendrier-de-sortie.md) |
| Les wishlists et la visibilité dans la boutique | [visibilite-et-wishlists.md](visibilite-et-wishlists.md) |
| Le prix, le prix régional, la réduction de lancement, les soldes | [prix-et-reductions.md](prix-et-reductions.md) |
| Une démo, un Steam Playtest, la Steam Next Fest | [demo-playtest-next-fest.md](demo-playtest-next-fest.md) |
| L'accès anticipé (*Early Access*) | [acces-anticipe.md](acces-anticipe.md) |
| La compatibilité Steam Deck (Verified, Playable) | [steam-deck.md](steam-deck.md) |
| Succès, Steam Cloud, Steam Input, overlay, dans un jeu Godot | [fonctionnalites-steamworks.md](fonctionnalites-steamworks.md) |
| Une mise à jour, une annonce, un événement après la sortie | [apres-la-sortie.md](apres-la-sortie.md) |
| Le rétroplanning complet d'une sortie | [gabarits/plan-de-sortie.md](gabarits/plan-de-sortie.md) |
| Retrouver une page Steamworks citée | [sources.md](sources.md) |
| Écrire le code Steamworks d'un jeu Godot (GodotSteam) | le skill `steam:godotsteam` |

## Les règles à ne jamais oublier

Relevées le 04/11/2026 ; détails et sources dans les fiches.

- **21 jours** entre le paiement des 100 $ de Steam Direct et la première sortie possible.
- La revue de Valve prend en général 3 à 5 jours ouvrés, pour la page puis pour le build : soumets chacun **au moins 7 jours ouvrés** avant la date voulue. La page passe en revue avant le build.
- La page **Coming Soon** doit être publique **au moins deux semaines** avant la sortie.
- La date de sortie ne peut plus changer dans les **deux semaines** qui la précèdent.
- Le jeu ne sort pas tout seul : quelqu'un doit cliquer sur **Release App** le jour J.
- Aucune réduction pendant **30 jours** après la sortie (sauf la réduction de lancement, de 10 à 40 %, 7 à 14 jours, à prévoir avant la sortie), après une hausse de prix, ou entre deux réductions.
- **Une seule Next Fest** par jeu, avec une démo jouable et une page publique, et une sortie après la fin du festival.
- Capsules : uniquement l'illustration, le titre et un sous-titre officiel. Pas de note, de prix, de récompense, d'appel à l'action ni de « bientôt disponible ».
- Captures : du gameplay seulement, 1920×1080 au minimum, au moins 5.
