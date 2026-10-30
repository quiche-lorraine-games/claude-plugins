# Conventions audio ElevenLabs — gabarit

Gabarit à copier dans le projet du jeu, par exemple dans `.claude/elevenlabs.md`, puis à remplir. Le skill `elevenlabs:audio` lit ce fichier avant chaque génération. Les valeurs ci-dessous sont des exemples, pas des recommandations : seul le projet décide.

```markdown
# Conventions audio générées avec ElevenLabs

## Destination et nommage
- Voix : res://assets/audio/voix/<personnage>/<personnage>_<réplique>_<variante>.mp3
  (ex. garde_halte_01.mp3)
- Bruitages : res://assets/audio/sfx/<catégorie>/<objet>_<action>_<variante>.wav
  (ex. porte_bois_ouvre_01.wav)
- Musiques : res://assets/audio/musique/<lieu ou moment>_<variante>.mp3
- En minuscules et snake_case. La fiche .elevenlabs.json reste à côté du son et se commite avec lui.

## Formats
- Voix et musiques : .mp3 (mp3_44100_128)
- Bruitages : .wav (pcm_44100 ; pcm_22050 si l'offre refuse le 44,1 kHz)

## Langue
- Langue des voix : fr (passer --langue fr)

## Casting
| Personnage | voice_id | Nom de la voix | Modèle | Réglages |
|---|---|---|---|---|
| Garde | JBFqnCBsd6RMkjVDRZzb | George | eleven_multilingual_v2 | --stabilite 0.4 |
| Narratrice | (à choisir) | | eleven_v3 | --stabilite 0.5 |

Premiers jets : eleven_flash_v2_5 (moitié prix), puis le modèle du casting pour la version finale.

## Style sonore
- Bruitages : (une phrase, ex. « réaliste, sec, peu de réverbération ; mots à ajouter : close mic, dry »)
- Musique : (ex. « orchestral médiéval, instrumental, bouclable, 70–100 bpm »)

## Niveaux et boucles
- Le mixage se fait dans les bus audio de Godot ; ne pas régénérer pour une question de volume.
- Sons en boucle : générer avec --boucle, puis edit/loop_mode=1 (WAV) ou loop=true (MP3) dans le .import.

## Godot
- Binaire : godot   (ou chemin complet, ex. /opt/godot/godot)
- Version : 4.x

## Crédits
- Accord préalable : dès 2 générations ou une musique (règle par défaut du skill ;
  écrire « toujours » pour exiger un accord même pour une seule génération)
- Offre du compte : (ex. Creator, payante : usage commercial autorisé)
```
