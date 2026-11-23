# Référence des commandes de `uthana.py`

Les capacités de l'API Uthana utiles à un jeu, une sous-commande par opération. Ce fichier complète [SKILL.md](SKILL.md) : les règles de coût, de conventions, de droits et de sécurité y restent valables. `python3 "$UTHANA" <commande> --help` donne toutes les options.

## Options communes

**Personnage** (`--personnage`) : un `character_id` Uthana, ou le nom d'un personnage fourni à tous les comptes : `tar` (défaut), `ava`, `manny`, `quinn`.

**Téléchargement** (toutes les commandes qui produisent une animation, et `telecharger`, `statut`) :

| Option | Paramètre Uthana | Effet |
|---|---|---|
| `--sortie F` | format d'après l'extension | `.glb` (conseillé pour Godot), `.fbx` ou `.bvh` ; obligatoire ; refuse d'écraser sans `--ecraser` |
| `--fps 24\|30\|60` | `fps` | images par seconde, 30 par défaut |
| `--sans-maillage` | `no_mesh=true` | squelette et animation seulement |
| `--sur-place` | `in_place=true` | sans déplacement horizontal de la racine |
| `--torse` | `torso_only=true` | bas du corps immobile |
| `--vitesse-lecture X` | `speed_multiplier` | de 0 (exclu) à 2 |

Le téléchargement passe par `https://uthana.com/motion/file/motion_viewer/<character_id>/<motion_id>/<format>/…`, avec la même authentification. Il est gratuit et illimité en paiement à l'usage ; il retarget l'animation sur le personnage demandé.

**Autres** : `--a-blanc` (commandes payantes) affiche la requête sans l'envoyer ; `--delai S` règle le délai de réponse HTTP (300 s).

## Compte (gratuit)

| Commande | Opération GraphQL |
|---|---|
| `verifier` | `org` : nom, paiement à l'usage, solde |
| `prix` | `payg_prices` : barème par modèle |
| `depenses [--limite N]` | `payg_ledger` : débits, recharges |

## Personnages

| Commande | Opération | Coût |
|---|---|---|
| `personnages` | `characters` | gratuit |
| `importer FICHIER [--nom N] [--sortie F]` | `create_character` (envoi multipart) | 0,15 $ si rigging, sinon gratuit |
| `telecharger-personnage ID --sortie F` | `/motion/bundle/<id>/character.<glb\|fbx>` | gratuit |

Options d'`importer` :
- `--sans-rig` : le fichier a déjà un squelette (plus rapide, gratuit) ;
- `--squelette ue5|r15` : refaire le squelette au format Unreal Engine 5 ou Roblox R15 (sinon, squelette compatible Mixamo) ;
- `--sans-doigts` : sans os de doigts (mieux pour une main à la géométrie simplifiée) ;
- `--pieds-au-sol` : pieds au sol dans la pose de repos (sinon, hanches à l'origine) ;
- `--sans-prefixe` : os sans préfixe `mixamorig:` ;
- `--sans-face-avant` : ne pas tourner le personnage vers l'avant ;
- `--sortie perso_rig.glb` : télécharge aussi le personnage rigué.

Le rigging prend en général 30 à 60 s. La réponse donne une confiance de 0 à 1 ; sous 0,5, le script avertit. Erreurs connues : fichier de plus de 30 Mo, format autre que FBX ou GLB, « Essential joints missing » (squelette sans bassin, épaules ou hanches), personnage non humanoïde.

## Animations

### `texte "prompt" --sortie F`

- `--modele 3.0` (défaut), `3.0-lite`, `3.0-mini` : `create_text_to_motion_job`, tâche suivie toutes les 5 à 15 s. Durée `--duree` : 4 à 10 s pour 3.0 (4 par défaut), 5 à 10 s pour Lite et Mini (5 par défaut). `--sans-reecriture` garde le prompt tel quel ; `--rapide` utilise la variante rapide. `--sans-attendre` crée la tâche et rend la main ; `--attente S` (600 s).
- `--modele 2.0` ou `1.0` : `create_text_to_motion`, réponse immédiate ; `--duree` de 0,25 à 10 s, `--graine`, `--ik-pieds`.

### `video FICHIER --sortie F`

`create_video_to_motion` (envoi multipart), tâche suivie. `--modele video-to-motion-3.0` (défaut), `-2.1`, `-2.0` ; `--mains` pour des mains plus fines ; `--nom`. Vidéo : une personne, plan fixe, corps entier, 2 à 60 s, 24 à 120 i/s, 300 à 4 096 px, MP4, MOV, AVI ou WebM de 128 Mo au plus. Une même vidéo renvoyée pendant que sa tâche tourne (ou dans les 24 h après succès) renvoie la tâche existante. Limite de 10 minutes de traitement ; une vidéo qui fait échouer la tâche par manque de mémoire est bloquée jusqu'à vérification par Uthana.

### `locomotion --sortie F`

`create_locomotion`, réponse immédiate. Pour un contrôleur de personnage : une animation par direction, vitesse et style.
- `--angle` : direction en degrés, 0 avant, 90 droite, −90 gauche, 180 arrière ;
- `--vitesse` : m/s (1,2 par défaut ; 0,25 à 8, conseillé jusqu'à 6) ;
- `--foulees` : paires de pas, 1 à 5 (4 par défaut) ;
- `--style` : voir `styles` (`neutral_male_a` par défaut).

Avec `--sur-place`, le code du jeu déplace le personnage dans la direction de l'animation jouée.

### `boucler MOTION_ID --sortie F`

`create_looped_motion`. `--mode closed` (défaut : le personnage revient à son point de départ, pour un idle ou une course sur place) ou `open` (il avance à chaque cycle, pour une marche avec root motion). `--debut` et `--fin` (fractions 0–1) recadrent l'animation ; `--zone` règle la durée de la zone de raccord (2 s) ; `--zone-mode modify` (garde la durée) ou `extend` (l'allonge).

### `enchainer PREMIER SECOND --sortie F`

`stitch` : enchaîne deux animations sur un personnage. `--transition` : 0,1 à 3 s (1 par défaut). API en aperçu chez Uthana, susceptible de changer. Les découpes et le placement fins se font avec `brut`.

### `styles`

`locomotion_styles` : styles acceptés par `locomotion`.

## Reprise (gratuit)

| Commande | Usage |
|---|---|
| `telecharger MOTION_ID --personnage ID --sortie F` | refaire un fichier, pour un autre personnage, format ou option |
| `statut JOB_ID [--sortie F]` | état d'une tâche ; avec `--sortie`, télécharge si elle est finie |
| `taches [--methode TextToMotion]` | tâches du compte |
| `animations [--recherche T] [--source mine\|uthana\|all]` | animations du compte (ou de la bibliothèque d'exemples d'Uthana) |

## Divers

`brut "query ou mutation" [--variables JSON]` exécute une opération GraphQL que le script ne connaît pas (le schéma complet s'explore par introspection, sans clé). Une mutation est traitée comme payante : jamais de nouvel essai automatique.

`inspecter F.glb` : animations, durées, images par seconde, os et maillages d'un GLB local.

## Enchaînements utiles

**Animer un personnage de Tripo :**
```bash
python3 "$UTHANA" importer assets/persos/garde.glb --nom Garde --pieds-au-sol --sortie assets/persos/garde_rig.glb
# noter le character_id affiché dans .claude/uthana.md
python3 "$UTHANA" texte "a guard salutes, then returns to attention" --personnage <character_id> \
  --sortie assets/anims/garde/garde_salut.glb --sans-maillage
```

**Jeu de locomotion sur place** (série : annoncer le total et attendre l'accord) :
```bash
for a in 0 90 180 -90; do
  python3 "$UTHANA" locomotion --personnage <character_id> --angle $a --vitesse 1.4 --sur-place \
    --sans-maillage --sortie "assets/anims/garde/garde_marche_${a}.glb"
done
```
Lance ces commandes l'une après l'autre, jamais en parallèle.
