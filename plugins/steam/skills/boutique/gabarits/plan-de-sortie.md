# Plan de sortie Steam — gabarit

Gabarit à copier dans le repo du jeu (ex. `docs/steam/plan-de-sortie.md`), puis à remplir. Les délais minimum viennent de la documentation Steamworks relevée le 04/11/2026 (voir les fiches du skill `steam:boutique`) ; vérifie-les avant de fixer une date. Les durées marquées « conseil » sont des points de départ, pas des règles.

```markdown
# Plan de sortie Steam : <nom du jeu>

## Identité
- App ID du jeu : <…>        App ID de la démo : <…>        App ID du playtest : <…>
- Nom définitif (ne change plus après la revue) : <…>
- Personne qui cliquera sur « Release App » (permissions Publish app changes et
  Manage pricing and discounts vérifiées) : <…>

## Dates clés
| Étape | Date prévue | Date réelle | Règle ou conseil |
|---|---|---|---|
| Paiement Steam Direct (100 $) | | | règle : au moins 21 jours avant la sortie |
| Documents banque, fiscalité, identité validés | | | règle : 15 à 30 jours |
| Page soumise à la revue | | | règle : 7 jours ouvrés avant la mise en ligne voulue |
| Page Coming Soon publique (annonce) | | | règle : au moins 2 semaines avant la sortie ; conseil : des mois avant |
| Démo soumise à la revue | | | règle : 7 jours ouvrés ; Next Fest : 3 semaines avant (5 pour l'aperçu presse) |
| Démo en ligne + notification aux wishlists | | | règle : notification dans les 14 jours, une seule fois |
| Inscription Next Fest | | | règle : une seule Next Fest par jeu |
| Next Fest | | | règle : sortie du jeu après la fin |
| Prix proposés (37 devises) | | | conseil : quelques jours avant la sortie |
| Réduction de lancement réglée | | | règle : avant la sortie ; 10–40 %, 7–14 jours |
| Build soumis à la revue | | | règle : 7 jours ouvrés avant la sortie |
| Bandes-annonces encodées | | | règle : pas de sortie pendant un encodage |
| Date de sortie figée | | | règle : 2 semaines avant la sortie |
| Sortie (en semaine) | | | conseil de Valve : pas le week-end |
| Première réduction possible | | | règle : 30 jours après la sortie ou la fin de la réduction de lancement |
| Premières soldes saisonnières possibles | | | règle : jeu sorti depuis au moins 30 jours |

Espacer d'au moins 2 semaines la notification de démo, la sortie et la première
réduction à 20 % ou plus : un joueur n'est prévenu qu'une fois toutes les 2 semaines.

## Page boutique
- [ ] Capsules : en-tête 920×430, petite 462×174, principale 1232×706, verticale 748×896
- [ ] Bibliothèque : capsule 600×900, en-tête 920×430, hero 3840×1240, logo 1280 de large ou 720 de haut
- [ ] Icônes : raccourci 256×256, application 184×184
- [ ] 5 captures de gameplay ou plus, 1920×1080 ou plus, dont 4 « tous âges »
- [ ] Bande-annonce de gameplay en premier
- [ ] Description courte (texte brut, sans date) et « À propos » relues, par langue
- [ ] 20 tags, les 5 premiers précis
- [ ] Langues déclarées : interface / sous-titres / audio
- [ ] Fonctionnalités cochées = fonctionnalités présentes dans le build

## Build
- [ ] Se lance sur chaque système annoncé
- [ ] Succès, Steam Cloud, manette : présents s'ils sont cochés
- [ ] Pas de steam_appid.txt dans le build envoyé
- [ ] Testé depuis Steam, sur la branche default

## Steam Deck (si visé)
- [ ] Manette par défaut complète, glyphes corrects, clavier virtuel
- [ ] 30 i/s et texte d'au moins 9 px (12 visés) en 1280×800

## Suivi
| Date | Événement (annonce, bande-annonce, festival, démo, réduction) | Wishlists nettes de la semaine |
|---|---|---|
```
