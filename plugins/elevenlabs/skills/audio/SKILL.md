---
name: audio
description: Pilote l'API ElevenLabs et range les sons produits dans un projet Godot. À charger quand on veut produire de l'audio de jeu par IA - répliques et dialogues de PNJ (synthèse vocale, plusieurs voix, voix expressives eleven_v3), voix de personnage à concevoir depuis une description, à remixer ou à cloner avec consentement, bruitages et effets sonores (bouclables ou non), musiques d'ambiance ou de combat, voix d'un enregistrement rejouée par une autre voix, voix isolée du bruit, morceau séparé en pistes, transcription et sous-titres SRT, alignement texte-audio pour sous-titres ou lip sync ; puis contrôler durée, format et niveaux, importer dans Godot et vérifier l'import en headless. Couvre aussi le casting des voix du projet, les crédits, la clé ELEVENLABS_API_KEY et ses permissions, l'historique pour récupérer un audio, et les erreurs (réseau bloqué, clé refusée, permission manquante, crédits épuisés, délai dépassé, contenu refusé). Ne convient pas au doublage d'acteurs réels sans leur accord, ni à l'audio en temps réel dans le jeu (agents conversationnels, streaming).
---

# Produire l'audio du jeu avec ElevenLabs

Ce skill pilote l'API REST d'ElevenLabs (`https://api.elevenlabs.io`) avec le script `scripts/elevenlabs.py`, rangé dans le même dossier que ce fichier. Le script n'utilise que la bibliothèque standard de Python 3. Il lit la clé dans `ELEVENLABS_API_KEY`.

```bash
ELEVEN="${CLAUDE_PLUGIN_ROOT}/skills/audio/scripts/elevenlabs.py"
python3 "$ELEVEN" --help
```

Le script a une sous-commande par capacité utile à un jeu. Toutes sont décrites dans [commandes.md](commandes.md) : options, endpoints, enchaînements. Ce fichier-ci donne les règles communes et le déroulé.

Le projet prime : ses conventions (dossier, nommage, format, casting des voix, style) l'emportent sur les valeurs par défaut de ce skill.

## Quand s'en servir

**Oui** :
- répliques de PNJ, annonces, narration, voix de tutoriel ; dialogues à plusieurs voix ;
- voix temporaires (*placeholder*) pour tester le rythme d'une scène avant l'enregistrement final ;
- bruitages : impacts, pas, portes, ambiances, interfaces, créatures, boucles d'ambiance ;
- musiques d'ambiance, de menu, de combat ; plan de composition à relire avant de payer ;
- retravailler un enregistrement : changer la voix, isoler la voix du bruit, séparer un morceau en pistes ;
- sous-titres et lip sync : transcription avec SRT, temps de chaque mot.

**Non**, propose une autre voie :
- cloner ou imiter la voix d'une personne réelle sans son accord écrit (acteur, célébrité, proche) ;
- audio généré pendant la partie, en temps réel (agents conversationnels, streaming) : hors du champ de ce skill ;
- une musique ou une voix qui doit ressembler à une œuvre ou un artiste précis ;
- un son dont le timing doit tomber à l'image près sur une animation : génère-le, puis cale-le à la main.

## Avant tout : vérifier l'accès

```bash
python3 "$ELEVEN" verifier
```

Le script vérifie que la clé est présente, sans l'afficher, teste l'accès réseau à l'API, puis lit l'offre et le solde de crédits. Il liste aussi les permissions de lecture absentes de la clé (une clé ElevenLabs peut être restreinte endpoint par endpoint). S'il échoue, consulte la section « Erreurs » et arrête-toi là : ne contourne rien.

## Conventions du projet

Avant la première génération, cherche les conventions audio du projet :
1. `.claude/elevenlabs.md`, le fichier dédié s'il existe ([gabarit](conventions-exemple.md)) ;
2. le `CLAUDE.md` du projet, puis le GDD (section audio, voix, casting) ;
3. les sons déjà présents : dossier, nommage, format, présence de `.elevenlabs.json`.

Il te faut au minimum :
- le dossier de destination et la règle de nommage ;
- le format : `.wav` pour les bruitages courts, `.mp3` pour voix et musiques, sauf mention contraire ;
- la langue des voix ;
- le **casting** : quelle voix (`voice_id`), quel modèle et quels réglages pour chaque personnage ;
- le style sonore (réaliste, rétro, cartoon…).

**S'il manque une de ces informations, demande-la à l'utilisateur au lieu de deviner.** Propose-lui ensuite d'écrire ses réponses dans `.claude/elevenlabs.md` à partir du gabarit.

**Un personnage garde toujours la même voix**, avec le même modèle et les mêmes réglages. Ne choisis jamais une voix au hasard pour un personnage déjà casté. Pour un nouveau personnage, propose 2 ou 3 voix (voir « Casting ») et laisse l'utilisateur choisir, puis note le choix dans le casting.

## Choisir la commande

| Besoin | Commande |
|---|---|
| Une réplique d'un personnage | `parole` |
| Plusieurs personnages qui se répondent | `dialogue` (`eleven_v3`) ou une `parole` par réplique |
| Sous-titres ou lip sync d'une réplique générée | `parole --horodatage` |
| Une voix pour un nouveau personnage | `voix`, `bibliotheque`, ou `concevoir-voix` puis `creer-voix` |
| Une variante d'une voix (plus âgée, plus rauque) | `remixer-voix` puis `creer-voix` |
| La voix d'une personne qui a donné son accord écrit | `cloner --consentement` |
| Un bruitage, une boucle d'ambiance | `bruitage` (`--boucle`) |
| Une musique | `plan-musique` (à relire), puis `musique --plan` ; `musique "prompt"` pour un premier jet |
| Rejouer une prise avec une autre voix | `changer-voix` |
| Nettoyer une prise | `isoler` |
| Séparer voix, batterie, basse… | `separer-pistes` |
| Transcrire, sous-titres SRT | `transcrire --srt` |
| Temps de chaque mot d'un texte déjà enregistré | `aligner` |
| Retrouver un audio de parole déjà payé | `historique`, puis `recuperer` |
| Endpoint que le script ne connaît pas | `brut` |

## Coût

ElevenLabs décompte des **crédits**, inclus dans l'abonnement mensuel du compte (et, selon l'offre, un dépassement facturé). Le solde se lit avec `verifier`.

Barème indicatif (octobre 2026), à vérifier sur la [page de prix de l'API](https://elevenlabs.io/pricing/api) :

| Commande | Crédits |
|---|---|
| `parole`, `dialogue` (`eleven_multilingual_v2`, `eleven_v3`) | 1 par caractère |
| `parole` avec `eleven_flash_v2_5` ou `eleven_turbo_v2_5` | 0,5 par caractère |
| `bruitage` | environ 200 par génération (source secondaire) |
| `musique` | environ 900 par minute (source secondaire) |
| `transcrire`, `changer-voix`, `isoler`, `separer-pistes`, `aligner`, `concevoir-voix`, `remixer-voix` | non vérifié : lis la page de prix |
| `verifier`, `modeles`, `consommation`, `historique`, `recuperer`, `voix`, `voix-info`, `bibliotheque`, `inspecter` | gratuit |

Le script estime le coût des commandes de parole avant l'envoi (nombre de caractères × facteur du modèle). Après chaque génération, il recopie le coût réel dans le champ `credits` de la fiche quand l'API le donne (en-tête `character-cost`). `consommation` donne les crédits consommés par jour.

Règles :
- **Une génération demandée explicitement** : annonce son coût en une ligne (ex. « parole, 120 caractères, multilingual v2 : ≈ 120 crédits »), puis lance-la, sauf si les conventions exigent un accord à chaque fois.
- **Avant une série** (2 générations payantes ou plus : toutes les répliques d'une scène, 5 variantes d'un bruitage), une musique, ou une variante non demandée : annonce le nombre de générations et le total estimé. **Attends l'accord.**
- **Ne relance jamais en boucle pour « améliorer ».** Après un résultat décevant, fais-le écouter (ou décris le contrôle), dis ce qui ne va pas, propose un prompt ou des réglages corrigés et leur coût, et laisse l'utilisateur décider.
- Pour un premier jet de voix, propose `eleven_flash_v2_5` (moitié prix) ; garde le modèle du casting pour la version finale.
- Pour montrer la requête sans rien dépenser, ajoute `--a-blanc`.

**Une requête à la fois.** Le nombre de requêtes simultanées dépend de l'offre (2 en gratuit). Lance les générations d'une série l'une après l'autre, jamais en parallèle. Sur un 429, le script attend et réessaie pendant environ 5 minutes ; un refus pour limite n'est pas facturé.

**Les requêtes sont synchrones**, il n'y a pas de tâche à reprendre. Une génération coupée (délai dépassé, erreur 5xx) a pu aboutir et être facturée. Pour la parole, le dialogue et le changement de voix, regarde `historique` et récupère l'audio avec `recuperer` (gratuit) avant toute relance. Les bruitages et la musique n'apparaissent pas dans l'historique de l'API : demande l'accord avant de relancer.

## Casting

Pour trouver une voix à un personnage :
1. `voix --recherche <mot>` : voix déjà dans le compte (voix par défaut d'ElevenLabs et voix du studio) ;
2. `bibliotheque --langue fr --genre male --age old --usage characters_animation` : voix partagées par la communauté, à ajouter avec `ajouter-voix` ;
3. `concevoir-voix "<description>"` : 3 aperçus créés depuis une description (âge, timbre, accent, attitude, contexte). Fais-les écouter, puis garde le bon avec `creer-voix <generated_voice_id> --nom … --description …`.

Pour les personnages principaux, préfère une voix conçue (`concevoir-voix`) ou une voix par défaut : le propriétaire d'une voix de la bibliothèque peut la retirer (après un préavis indiqué sur sa fiche), et l'on ne pourrait plus générer de nouvelles répliques avec elle.

Une fois la voix choisie, note dans le casting du projet : personnage, `voice_id`, nom, modèle, réglages (`--stabilite`, `--similarite`, `--style`, `--vitesse`) et graine éventuelle.

**Clonage** (`cloner`) : uniquement avec l'**accord écrit** de la personne enregistrée, pour l'usage prévu. Le script refuse sans `--consentement`. Ne clone jamais une voix trouvée en ligne, dans un film ou un autre jeu, même « pour tester ».

## Déroulé

### 1. Brief

Avant d'écrire le texte ou le prompt, établis avec l'utilisateur, ou à partir du GDD :
- **quoi** : la réplique et son contexte (qui parle, à qui, dans quel état), ou le son et l'action qui le déclenche ;
- **durée** voulue (bruitage, musique) et si le son **boucle** ;
- **voix** : celle du casting ;
- **nom et dossier** de destination, selon les conventions.

Si le brief couvre plusieurs sons, c'est une série : applique la règle de coût.

### 2. Texte ou prompt

**Parole** :
- écris le texte tel qu'il doit être dit, ponctuation comprise : la ponctuation guide l'intonation (« … », « ! », « ? ») ;
- écris les nombres, sigles et noms inventés comme ils se prononcent, ou passe `--normalisation on` ;
- avec `eleven_v3`, des balises d'interprétation entre crochets en anglais : `[whispers]`, `[laughs]`, `[sighs]`, `[shouts]`, `[angry]`… ; avec les autres modèles, joue sur `--stabilite` (bas : plus expressif, plus variable) ;
- pour un texte découpé en plusieurs fichiers, passe `--texte-avant` et `--texte-apres` pour garder la continuité de l'intonation ;
- longueur maximale par requête : 5 000 caractères pour `eleven_v3`, 10 000 pour `eleven_multilingual_v2`, 40 000 pour `eleven_flash_v2_5`.

**Bruitage** : décris le son concrètement, en anglais de préférence : source, matière, action, espace, distance. Ex. « heavy wooden door creaking open slowly, old iron hinges, small stone room ». Un seul son par prompt. Passe `--duree` si elle compte ; `--boucle` pour une ambiance.

**Musique** : genre, ambiance, instruments, tempo, usage dans le jeu. Ex. « calm medieval tavern music, lute and flute, 90 bpm, loopable background ». `--instrumental` pour garantir l'absence de voix. Pour une musique de plus de 30 s ou structurée, passe d'abord par `plan-musique`, relis le plan avec l'utilisateur, puis `musique --plan`.

Montre le texte ou le prompt à l'utilisateur avant une série.

### 3. Génération

```bash
python3 "$ELEVEN" parole JBFqnCBsd6RMkjVDRZzb "Halte ! Qui va là ?" \
  --sortie assets/audio/voix/garde/garde_halte_01.mp3 --stabilite 0.4

python3 "$ELEVEN" bruitage "heavy wooden door creaking open, iron hinges" --duree 2 \
  --sortie assets/audio/sfx/portes/porte_bois_ouvre_01.wav
```

Le script envoie la requête, écrit le fichier, puis la fiche `garde_halte_01.elevenlabs.json` à côté, et affiche le contrôle du résultat et les crédits débités.

Options principales (liste complète dans [commandes.md](commandes.md)) :

| Option | Effet |
|---|---|
| `--sortie` | fichier à écrire (obligatoire) ; refuse d'écraser sans `--ecraser` |
| `--format` | `output_format` de l'API ; par défaut selon l'extension : `.mp3` → `mp3_44100_128`, `.wav` → `pcm_44100` enveloppé en WAV |
| `--modele` | modèle ElevenLabs (voir `modeles`) |
| `--langue` | langue imposée (code ISO 639-1, ex. `fr`) |
| `--stabilite`, `--similarite`, `--style`, `--vitesse` | réglages de la voix pour cette requête |
| `--graine N` | graine, pour refaire un résultat proche |
| `--param CLE=VALEUR` | champ de l'API sans option dédiée, envoyé tel quel |
| `--delai S` | délai de réponse maximal |
| `--a-blanc` | affiche la requête sans l'envoyer |

Certains formats (`pcm_44100`, `mp3_44100_192`…) sont réservés à des offres supérieures : si l'API les refuse, passe `--format pcm_22050` ou une sortie `.mp3`.

### 4. Contrôle du résultat

Le script affiche, et range dans le champ `controle` de la fiche :
- format, fréquence d'échantillonnage, canaux, débit (MP3) ;
- durée ;
- pour un WAV : crête et RMS en dBFS.

Pour un fichier déjà présent : `python3 "$ELEVEN" inspecter <fichier>`.

Compare ces valeurs au brief et aux conventions :
- **durée** : un bruitage très éloigné de `--duree` est signalé ; une réplique anormalement longue ou courte pour son texte trahit souvent une hallucination (mots répétés, silence) : signale-le ;
- **niveau** : une crête à 0 dBFS sature ; un RMS très bas (sous −35 dBFS) est presque inaudible à côté du reste. Le mixage final se fait dans Godot (bus audio), ne régénère pas pour une question de volume ;
- **format** : Godot importe le WAV, le MP3 et l'Ogg Vorbis, pas l'Opus ni le PCM brut ;
- **contenu** : tu ne peux pas écouter. Pour une réplique, propose une vérification par `transcrire` (payant) si le texte compte, ou demande à l'utilisateur d'écouter. Ne présente jamais un son comme validé sur la seule foi du contrôle.

Décris le résultat à l'utilisateur en une ou deux lignes (valeurs et écarts).

### 5. Import dans Godot

- Le fichier doit être sous la racine du projet Godot (celle qui contient `project.godot`), dans le dossier prévu par les conventions. Passe directement le bon chemin à `--sortie`.
- Garde la fiche `.elevenlabs.json` à côté du son et commite les deux, avec le `.import` que Godot va créer. Ne commite jamais `.godot/`.
- **Boucle** : un son généré avec `--boucle` ne boucle dans Godot que si l'import le dit. Dans le `.import` : pour un WAV, `edit/loop_mode=1` (boucle avant) ; pour un MP3 ou un Ogg, `loop=true`. Ou dans le dock Import de l'éditeur.
- Voix et musiques : préfère le MP3 (léger). Bruitages courts et fréquents : le WAV (pas de décodage, latence minimale).
- Les réglages d'import propres au projet (compression, bus, normalisation) viennent de ses conventions.

### 6. Vérification de l'import en headless

Lance l'import sans éditeur graphique. Le binaire vient des conventions du projet : `godot`, `godot4` ou la variable `$GODOT`.

```bash
godot --headless --path <racine_du_projet> --import 2>&1 | tee /tmp/import-godot.log
```

`--import` existe depuis Godot 4.3. Sur une version plus ancienne : `godot --headless --path <racine> --editor --quit`.

Puis vérifie :
1. `grep -n "ERROR" /tmp/import-godot.log` ne cite pas le nouveau fichier ;
2. le fichier `<son>.import` existe et ne contient pas `valid=false` ;
3. le fichier importé existe dans `.godot/imported/`.

Si Godot n'est pas installé dans l'environnement, dis-le clairement : le son est livré, mais l'import n'a pas été vérifié.

## Fiche `.elevenlabs.json`

Chaque résultat a une fiche, à côté de lui (`garde_halte_01.mp3` → `garde_halte_01.elevenlabs.json`). Elle permet de retrouver et de refaire le son. Elle contient :
- l'opération (endpoint), le texte ou le prompt ;
- la voix (`voice_id` et nom), le modèle, le format ;
- les paramètres envoyés (réglages de voix, graine, durée…) ;
- les entrées : fichiers (chemin relatif au dossier de la fiche, taille, empreinte SHA-256) ; un fichier pris hors du projet ne garde que son nom et son empreinte ;
- la date, le `request_id`, le `history_item_id` (parole), le `song_id` (musique) ;
- les crédits débités, si l'API les donne ;
- la liste des fichiers écrits, relatifs au dossier de la fiche ;
- le contrôle.

Ne la modifie pas à la main. Pour refaire un son, relis-la et relance avec les mêmes texte, voix, modèle, réglages et graine, après accord sur le coût. Le résultat sera proche, pas identique : la graine n'est qu'un « meilleur effort ».

## Erreurs et ce qu'il faut dire

Le script écrit sur la sortie d'erreur un message court qui donne l'action à faire, et sort avec un code distinct selon le cas. Transmets l'essentiel à l'utilisateur et arrête-toi : ne contourne jamais une erreur de réseau, de clé ou de permission.

| Code | Cas | Ce que tu dis à l'utilisateur |
|---|---|---|
| 0 | succès | résumé du contrôle et chemin du fichier |
| 1 | erreur API inattendue, voix introuvable, réponse illisible | le message du script. Après une erreur 5xx sur une génération, regarde `historique` avant de relancer |
| 2 | argument invalide, refusé par le script ou par la validation de l'API (422) | corrige l'appel toi-même, sans rien demander |
| 3 | clé absente ou refusée (401) | « La clé ElevenLabs manque ou est refusée. Ajoute ou corrige `ELEVENLABS_API_KEY` dans les secrets de l'environnement, puis ouvre une nouvelle session. » Ne demande jamais la clé dans le chat |
| 4 | crédits épuisés (`quota_exceeded`) | « Le compte ElevenLabs n'a plus assez de crédits ; rien n'a été généré. Recharge ou change d'offre. » |
| 5 | domaine bloqué par la politique réseau (403 du proxy) ou injoignable | « Le domaine `<hôte>` est bloqué. Ajoute-le aux domaines autorisés de l'environnement. » Donne l'hôte exact cité par le script |
| 6 | permission manquante sur la clé (`missing_permissions`) | « La clé n'a pas la permission `<nom>`. Ajoute-la à la clé dans les réglages ElevenLabs (Developers, API Keys). » La valeur de la clé ne change pas : pas besoin de toucher au secret |
| 7 | délai dépassé | « ElevenLabs n'a pas répondu à temps ; la génération a pu être facturée. » Regarde `historique` et `recuperer` pour la parole ; pour un bruitage ou une musique, demande l'accord avant de relancer, avec un `--delai` plus long |
| 8 | contenu refusé par la modération | dis-le, et propose une reformulation |
| 9 | trop de requêtes simultanées (429), malgré environ 5 minutes de nouveaux essais | rien n'a été facturé. Attends la fin des requêtes en cours, puis relance une seule requête à la fois |

## Droits et sécurité

- **Licence** : l'audio produit avec une offre gratuite ne peut pas servir commercialement. Avant de mettre un son dans un jeu destiné à la vente, vérifie que le compte a une offre payante (`verifier` affiche l'offre). Voir le README du plugin.
- **Voix réelles** : jamais de clonage sans accord écrit ; jamais d'imitation d'une personne identifiable par la description d'une voix conçue.
- **Clé** : ne demande **jamais** la clé dans le chat. Si l'utilisateur la colle quand même, ne la réutilise pas, ne la recopie nulle part, et conseille-lui de la révoquer dans les réglages ElevenLabs et d'en créer une autre, à mettre en secret de l'environnement.
- Ne l'affiche pas : pas de `echo $ELEVENLABS_API_KEY`, pas de `env` ni de `printenv` non filtrés, pas de `set -x` autour des appels.
- Ne la mets dans aucun fichier, log, commit, fiche ou message de PR. Le script masque la clé dans tout ce qu'il écrit et ne l'envoie qu'à l'API.
- Pour tester sa présence : `python3 "$ELEVEN" verifier`, jamais un affichage de la variable.
