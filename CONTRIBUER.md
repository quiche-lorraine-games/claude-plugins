# Contribuer au référentiel

Règles pour ajouter ou modifier une fiche, qu'on soit humain ou agent.

## Format d'une fiche

1. `# Titre`
2. `> **En bref** : …` en 2 ou 3 phrases : ce que couvre la fiche.
3. `## Quand consulter cette fiche` : situations concrètes (« tu implémentes un saut », « les joueurs se plaignent que… »).
4. Corps : principes → règles concrètes et valeurs de départ chiffrées (les tableaux sont bienvenus) → patterns → anti-patterns et pièges.
5. `## Checklist` : cases `- [ ]` actionnables.
6. `## Pistes d'implémentation` : agnostique moteur d'abord (pseudo-code court si utile), puis notes UE5 / Godot / Unity seulement si elles apportent quelque chose.
7. `## Voir aussi` : liens relatifs vers les autres fiches.
8. `## Sources` : références réelles uniquement.

## Règles de rédaction

- **Français.** Les termes techniques anglais standards restent en italique, avec la traduction quand elle existe : *core loop* (boucle centrale), *coyote time*.
- **Dense et actionnable.** Pas d'introduction historique ni de remplissage. Entre 120 et 350 lignes par fiche thématique ; les fiches genres et les gabarits peuvent être plus courts.
- **Écrire pour un agent** : formulations impératives (« Toujours… », « Éviter… », « Si X alors Y »), questions de diagnostic, arbres de décision simples.
- **Chiffres** : uniquement des valeurs établies, ou présentées explicitement comme « point de départ » ou « règle empirique ». Ne jamais inventer de statistique, de citation ou de source.
- **Gameplay ou présentation** : toujours préciser si un élément change la logique de jeu ou seulement son rendu.
- Pas d'emoji. Markdown GitHub standard.

## Après un ajout

- Ajouter la fiche à la table de routage de [CLAUDE.md](CLAUDE.md) et à l'arborescence du [README.md](README.md).
- Ajouter les nouveaux termes à [glossaire.md](glossaire.md) et les nouvelles références à [sources.md](sources.md).
- Vérifier que les liens relatifs fonctionnent.
