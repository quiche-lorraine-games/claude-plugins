# uthana

Plugin Claude Code qui donne à un agent **l'API d'[Uthana](https://uthana.com/docs/api)** (animation 3D de personnages par IA), puis lui fait ranger les animations dans un projet Godot : brief, prompt, génération, contrôle du résultat, import dans Godot et vérification de l'import en headless.

Ce que l'agent peut faire :
- **animer depuis une description** : Text-to-Motion 3.0, 3.0 Lite et 3.0 Mini (4 à 10 s), et les modèles 1.0 et 2.0 ;
- **animer depuis une vidéo** d'une personne (Video-to-Motion 3.0) ;
- **produire de la locomotion** : marche ou course dans une direction, à une vitesse et dans un style donnés, faite pour boucler et pour un contrôleur de personnage ;
- **boucler et enchaîner** des animations ;
- **importer un personnage** FBX ou GLB, par exemple généré avec le plugin `tripo`, avec rigging automatique, et changer son squelette (Mixamo par défaut, UE5, Roblox R15) ;
- **télécharger** chaque animation retargetée sur le personnage voulu, en GLB, FBX ou BVH, à 24, 30 ou 60 i/s, avec ou sans maillage, sur place ou avec déplacement ;
- **suivre le compte** : solde, barème, dépenses, tâches et animations existantes.

Le plugin contient :
- **le skill `uthana:animer`** : quand utiliser Uthana et quand l'éviter, le déroulé en six étapes, le chemin depuis un personnage Tripo, les règles de coût, l'import dans Godot (bibliothèque d'animations, boucle, root motion), les erreurs, les droits et la sécurité de la clé ;
- **le script `skills/animer/scripts/uthana.py`** : client de l'API GraphQL d'Uthana en Python 3, bibliothèque standard uniquement. Une sous-commande par capacité, listées dans [`skills/animer/commandes.md`](skills/animer/commandes.md), et une commande `brut` pour toute autre opération. Chaque animation téléchargée reçoit une fiche `.uthana.json` (prompt, modèle, `motion_id`, `character_id`, débit, contrôle) ;
- **un hook de démarrage**, sans appel réseau, qui ne dit rien si `UTHANA_API_KEY` est définie, et signale en une ligne son absence ;
- **un gabarit de conventions** ([`skills/animer/conventions-exemple.md`](skills/animer/conventions-exemple.md)) à copier dans le projet du jeu, en `.claude/uthana.md`.

## Activer le plugin dans un projet

Dans le `.claude/settings.json` du projet :

```json
{
  "extraKnownMarketplaces": {
    "quiche-lorraine-games": {
      "source": { "source": "github", "repo": "quiche-lorraine-games/claude-plugins" }
    }
  },
  "enabledPlugins": {
    "uthana@quiche-lorraine-games": true
  }
}
```

En local, chaque personne l'installe une fois avec `claude plugin install uthana@quiche-lorraine-games --scope project`. Dans le cloud, ce réglage est ignoré : activer le plugin dans les réglages du Project ou de l'organisation (voir le [README de la marketplace](../../README.md)).

Pour l'installer sur une machine :

```bash
claude plugin marketplace add quiche-lorraine-games/claude-plugins
claude plugin install uthana@quiche-lorraine-games
```

## Prérequis

1. **Compte et paiement à l'usage** : créer un compte sur uthana.com (5 $ de crédit offerts), puis activer le paiement à l'usage dans `uthana.com/app/account`, rubrique *Billing*. Sans lui, l'API ne génère rien ; `verifier` le signale.
2. **Clé API** : la créer dans `uthana.com/app/account`.
3. **Environnement cloud** (menu de l'environnement dans la barre de titre de la session, puis *Edit*) :
   - **accès réseau** : ajouter **`uthana.com`** aux domaines autorisés. C'est le seul hôte utilisé : l'API (`/graphql`) et les téléchargements (`/motion/…`) y sont tous les deux ;
   - **clé** : l'enregistrer en variable d'environnement **`UTHANA_API_KEY`**, puis ouvrir une nouvelle session. Ne jamais la coller dans le chat ni la commiter.
   - Un *Network secret* ne convient pas : Uthana attend la clé en authentification Basic avec un mot de passe vide, que le formulaire des secrets refuse, et un secret enregistré en jeton *Bearer* est refusé par Uthana (`invalid_token`), qui réserve ce format aux connexions OAuth (constaté le 23/11/2026).
4. Vérifier :

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/animer/scripts/uthana.py" verifier
   ```

Pour la vérification de l'import, Godot doit être installé dans l'environnement.

## Coût

Paiement à l'usage, en dollars, sans abonnement ni minimum ; un seul solde pour l'application web et l'API ; les crédits achetés n'expirent pas. Uthana a arrêté les nouveaux abonnements en août 2026.

Barème relevé le 23/11/2026 sur [uthana.com/pricing](https://uthana.com/pricing) :

| Opération | Prix |
|---|---|
| Text-to-Motion 3.0 et 3.0 Lite | 0,10 $ / s |
| Text-to-Motion 3.0 Mini | 0,075 $ / s |
| Text-to-Motion 2.0 / 1.0 | 0,03 / 0,02 $ / s |
| Video-to-Motion 3.0 (2.0, 2.1) | 0,06 $ / s (0,05 $) |
| Locomotion | 0,02 $ / s |
| Boucle et enchaînement | 0,01 $ / s |
| Recherche dans la bibliothèque | 0,10 $ / s (non couverte par le script, accessible par `brut`) |
| Rigging automatique | 0,15 $ par personnage |
| Génération de personnage | 0,75 $ (non couverte par le script) |
| Téléchargements | gratuits et illimités |

Les coûts sont réservés à l'acceptation d'une tâche et débités sur la durée réellement produite ; une tâche échouée n'est pas facturée. Le skill impose à l'agent d'annoncer le coût, d'attendre l'accord avant une série, et de ne jamais relancer en boucle.

Limites : sans moyen de paiement enregistré, 4 tâches simultanées par type (HTTP 429 `job_limit_exceeded`, sans rien accepter ni facturer).

## Droits sur les animations : ce que disent les conditions

D'après les [conditions d'utilisation](https://uthana.com/terms) (version 2.0.0, en vigueur le 09/11/2026), lues directement :

- **§ 4.2, après un premier achat de crédit** : les animations peuvent être reproduites, modifiées, distribuées et utilisées commercialement dans des jeux, des films et des projets clients, et vendues comme packs d'animations. **Aucune mention d'Uthana n'est requise.** Ce régime s'applique aussi, rétroactivement, aux animations faites avant avec les crédits gratuits du même compte, et ne s'arrête pas quand le solde tombe à zéro ou que le compte est fermé.
- **§ 4.3, avant tout achat** : usage commercial permis à condition d'une mention visible, dans les crédits ou la documentation : « Animation generated with Uthana (uthana.com) ».
- **§ 5** : interdit, sans accord écrit, d'utiliser les animations pour entraîner un modèle de génération ou d'extraction de mouvement concurrent d'Uthana, ou de les vendre comme jeu de données d'entraînement.
- **§ 6.2 et § 7.2, ce qu'Uthana fait des données** : par défaut, Uthana peut utiliser les personnages, vidéos et animations du compte pour entraîner ses modèles, et inclure les animations générées depuis un texte dans des jeux de données qu'il vend à des tiers. Les fichiers supprimés en sont retirés sous 30 jours. Un refus d'entraînement demande un accord écrit séparé ; payer ne suffit pas. **À savoir avant d'envoyer le personnage d'un jeu non annoncé.**

À faire avant de mettre une animation dans le jeu :
1. Acheter du crédit une fois (ou garder la mention dans les crédits du jeu).
2. Garder les `.uthana.json` (date, `motion_id`) comme trace de production.
3. Pour un contenu confidentiel, lire les § 6 et 7 en vigueur et, au besoin, demander un accord à Uthana.

## Alternatives : les serveurs MCP d'Uthana

Uthana publie un serveur MCP hébergé (`https://mcp.uthana.com/mcp`, connexion par compte Uthana, sans clé) et un serveur local open source ([uthana-mcp](https://github.com/Uthana/uthana-mcp), avec une clé). Ce plugin n'en déclare aucun :
- le serveur hébergé demande une connexion par navigateur, peu pratique dans une session cloud, et Uthana indique que Claude ne peut pas y récupérer les fichiers exportés sans régler son accès réseau ;
- le script donne la fiche de traçabilité, le contrôle du GLB et l'import dans Godot, et se lit en entier : on voit ce qui part vers l'API et où va la clé.

On peut ajouter un de ces serveurs soi-même ; les règles de coût et de droits du skill restent valables.

## Tests

```bash
python3 -m unittest discover -s plugins/uthana/tests -v
```

Les tests lancent le script contre un faux serveur HTTP local qui imite l'API GraphQL et les téléchargements, et contre un faux proxy qui refuse les connexions. L'URL de base se règle par `--api` ou `UTHANA_API_BASE`. Ils couvrent chaque sous-commande (opération, variables, envoi multipart, URL de téléchargement), le suivi des tâches, les validations locales, chaque code d'erreur, les nouveaux essais sur 429 `job_limit_exceeded` et l'absence de nouvel essai sur une opération incertaine, l'analyse des GLB, l'absence de la clé (en clair et encodée) dans toutes les sorties et fiches, et le hook.

## Documentation de l'API utilisée

Le script vise `https://uthana.com/graphql`, en authentification Basic (clé en nom d'utilisateur, mot de passe vide). Il s'appuie sur :
- la [documentation de l'API](https://uthana.com/docs/api), lue le 23/11/2026 : capacités (texte, vidéo, locomotion, retargeting, boucle et enchaînement, personnages, téléchargement), limites, tarifs, changelog ;
- le **schéma GraphQL**, lu par introspection (ouverte sans clé) le 23/11/2026 : arguments et types exacts de chaque opération ;
- le [client Python officiel](https://github.com/Uthana/uthana-python-client) : noms d'API des modèles 1.0 et 2.0 (`text-to-motion`, `text-to-motion-bucmd`), identifiants des personnages fournis, forme de l'URL de téléchargement, extraction du `motion_id` d'une tâche (`result.result.id`).

Ce qui reste incertain :
- **Appels réels** : le script n'a pas encore été validé par un appel réel, gratuit ou payant.
- **Erreurs de solde** : leur forme exacte n'est pas documentée ; le script les reconnaît par mots-clés (`insufficient`, `balance`…) et par le statut 402.
- **Débit réel** : déduit du solde avant et après l'opération ; il inclut les autres opérations en cours sur le compte au même moment. `depenses` donne le détail exact.
- **Nom des animations dans le GLB** : choisi par Uthana ; `inspecter` l'affiche.
