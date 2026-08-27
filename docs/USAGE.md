# AutomMixer - Guide d'utilisation

## Prérequis

- Python 3.10 ou plus
- FFmpeg installé et disponible dans le PATH
- Les dossiers sources présents dans le projet :
  - `videosource/`
  - `soundsource/`

## Structure du projet

- `automixer/` : modules Python du projet
- `docs/` : documentation
- `videosource/` : vidéos à traiter
- `soundsource/` : fichiers audio de remplacement
- `tests/` : tests unitaires

## Lancement du script

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
- un fichier son est choisi aléatoirement dans `soundsource`
- la piste audio de la vidéo est remplacée
- le son est coupé pour correspondre à la durée de la vidéo
- la sortie est enregistrée sous le format :
  - `nom_video_snd_1.mp4`
  - `nom_video_snd_2.mp4`
  - etc.
- un fichier `<nom_du_sous-dossier>_sound_<n>.txt` est ajouté dans le dossier de la vidéo avec le nom du son utilisé et l’horodatage

## Remarques importantes

- Les sorties sont incrémentées pour éviter d’écraser les précédents résultats.
- Les dossiers `videosource/` et `soundsource/` sont exclus du dépôt Git via `.gitignore`.
- Les logs du traitement s’affichent dans le terminal avec horodatage.

## Tests

Pour exécuter les tests du projet :

```bash
python3 -m unittest discover -s tests -v
```
