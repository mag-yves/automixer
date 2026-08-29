# AutomMixer - Guide d'utilisation

## Prérequis

- Python 3.10 ou plus
- FFmpeg installé et disponible dans le PATH
- Les dossiers sources présents dans le projet :
  - `videosource/`
  - `soundsource/`

## Structure du projet

- `automixer/` : modules Python du projet
- `config/` : paramètres et chemins du projet
- `docs/` : documentation
- `videosource/` : vidéos à traiter
- `soundsource/` : fichiers audio de remplacement
- `videostorage/` : archives des vidéos déjà traitées (analysées par `update-usage.sh`)
- `tests/` : tests unitaires

## Lancement du script

Le plus simple est d'utiliser le menu interactif :

```bash
./start.sh
```

Il propose :
- `1` : démarrer l'attribution des sons (`generate.sh`)
- `2` : mettre à jour les usages (`update-usage.sh`)
- `Q` : quitter

Le point d’entrée le plus simple est le script racine :

```bash
python3 run_automixer.py
```

Autre option, en appelant directement le module :

```bash
python3 -m automixer.orchestrator
```

ou, si vous préférez lancer directement une fonction depuis un terminal Python :

```bash
python3 - <<'PY'
from pathlib import Path
from automixer.orchestrator import process_videos

process_videos(Path('videosource'), Path('soundsource'))
PY
```

## Comportement

Pour chaque vidéo détectée dans `videosource` :
- un fichier son est choisi aléatoirement dans `soundsource`, en privilégiant les 20 sons les moins utilisés (compteur tenu dans `sound_usage_log.json`)
- la piste audio de la vidéo est remplacée
- le son est coupé pour correspondre à la durée de la vidéo
- la sortie est enregistrée sous le format :
  - `nom_video_snd_1.mp4`
  - `nom_video_snd_2.mp4`
  - etc.
- un fichier `<nom_du_sous-dossier>_sound_<n>.txt` est ajouté dans le dossier de la vidéo avec le nom du son utilisé et l’horodatage

## Mise à jour manuelle du journal d'utilisation

Le journal `sound_usage_log.json` peut être reconstruit à tout moment à partir des fichiers de log présents sur le disque :

```bash
./update-usage.sh
```

ou directement :

```bash
python3 update_usage.py [dossier_racine] [--log chemin/sound_usage_log.json]
```

Comportement :
- exploration récursive du dossier racine (par défaut `videostorage/`)
- prise en compte des fichiers `sound.txt`, `<n...>_sound.txt`, `<n...>_<n...>_sound.txt` et `<n...>_<n...>_sound_<n>.txt`
- extraction de chaque valeur `audio=` : une occurrence = une utilisation
- réécriture des compteurs de `sound_usage_log.json` à partir des valeurs comptées ; les sons déjà présents dans le journal mais absents du scan sont conservés avec un compteur à `0`

Utile après un déplacement de vidéos, une perte du journal ou un traitement effectué hors du script.

## Remarques importantes

- Les sorties sont incrémentées pour éviter d’écraser les précédents résultats.
- Les dossiers `videosource/` et `soundsource/` sont exclus du dépôt Git via `.gitignore`.
- Le journal `sound_usage_log.json` (à la racine du projet) est également exclu du dépôt Git car il s’agit de données locales générées.
- Les logs du traitement s’affichent dans le terminal avec horodatage.

## Tests

Pour exécuter les tests du projet :

```bash
python3 -m unittest discover -s tests -v
```
