# AGENTS.md — AutomMixer

Outil **Python local** (bibliothèque standard uniquement) qui automatise le montage de
vidéos courtes : il remplace la piste audio de chaque vidéo de `videosource/` par un son
tiré au hasard dans `soundsource/`, en adaptant la durée du son à celle de la vidéo.
Traitement **par lot**, sorties incrémentales sans écrasement, journalisation par dossier.
Documentation et messages de commit **en français**.

Développement **solo**, usage privé : versionner sur `master` avec des commits clairs par
étape logique (format `type(scope): description`). Pas de politique de branches / PR / release.

Sources de vérité :

- `docs/cahier des charges.md` — spécification fonctionnelle (phases, règles, critères).
- `docs/USAGE.md` — guide d'utilisation (⚠️ **partiellement désynchronisé**, cf. Pièges).

Dépendance externe : **FFmpeg** (`ffmpeg`, `ffprobe`) doit être dans le `PATH`. Aucun paquet
Python ni venv : tout repose sur la bibliothèque standard.

## Commandes

```bash
python3 -m unittest discover -s tests -v   # suite de tests (29 tests, requiert ffmpeg)
python3 run_automixer.py                   # équivaut à ./generate.sh : attribue les sons
./start.sh                                 # menu interactif (1 générer, 2 maj, 3 dashboard)

./update-usage.sh [dossier]                # reconstruit sound_usage_log.json (défaut videostorage)
./show-usage.sh --top 20                   # dashboard texte de l'usage des sons
python3 automixer/source_validator.py      # vérifie videosource / soundsource
```

`generate.sh`, `update-usage.sh` et `show-usage.sh` se placent d'abord à la racine du projet.

## Règles du projet (à respecter)

- **CDC d'abord** : tout écart fonctionnel est validé dans `docs/cahier des charges.md`
  **avant** de coder.
- **Aucun écrasement** : les sorties suivent `<nom>_snd_<n>.mp4` et prennent le prochain
  numéro libre ; `_base_name_for_output` neutralise les suffixes déjà présents pour ne pas
  les empiler.
- **Sélection audio uniforme** : tirage uniforme sur **tous** les sons présents (seule
  règle : éviter la répétition immédiate du son précédent). `sound_usage_log.json` est
  **statistique uniquement** et n'influence jamais le tirage ; il n'est **pas** mis à jour
  pendant le run (reconstruction manuelle via `update-usage.sh`).
- **Attributions multiples** : chaque vidéo reçoit `ASSIGNMENTS_PER_VIDEO` sorties
  (`config/settings.py`, défaut 2). Un tirage aléatoire **frais** est refait avant chaque
  attribution ; `process_videos(..., assignments_per_video=N)` surcharge le réglage (tests).
- **La durée de la vidéo est la référence** : le son est coupé s'il est plus long ; aucun
  bouclage.
- **Robustesse** : une erreur sur une vidéo n'interrompt pas le lot (`ERREUR TRAITEMENT`
  puis `continue`, `automixer/orchestrator.py:68`).
- **Logs horodatés** : toute étape passe par `log_phase` au format `[YYYY-MM-DD HH:MM:SS] …`.
- **Tests isolés sur données jetables** : chaque test crée un `TemporaryDirectory` et des
  médias factices (`ffmpeg -f lavfi`) ; ne jamais pointer les tests sur les liens réels.

## Pièges à connaître

- **Liens symboliques non versionnés** (`.gitignore`) : `videosource` →
  `../../iadata/autogen/short`, `soundsource` → `../../iadata/creations/musiques/Intro Short/`,
  `videostorage` → `../../iadata/autogen/to-publish/`. À recréer après un clone.
- **`docs/USAGE.md` obsolète** : il décrit encore une sélection pondérée vers les 20 sons les
  moins utilisés (retirée par le CDC §7.3) et une mise à jour des usages depuis
  `*_sound*.txt`, alors que `usage_updater.py` ne lit que `<n...>_metadata.json` (clé `audio`).
- **Dossier de log = dossier de la vidéo** : le nom du fichier `<dossier>_sound_<n>.txt` vient
  du nom du dossier parent et du numéro du fichier de sortie (`output_manager.py:31`).
- **`update-usage.sh` passe `--sounds soundsource`** : l'option `--sounds` sert à référencer
  intégralement la bibliothèque (sons à `0`), pas à restreindre le scan (qui part de
  `videostorage`).
- **Détection de durée dupliquée** : `media_selector.get_media_duration` et
  `audio_processor._get_duration` font la même chose via `ffprobe`.
- **Son plus court que la vidéo** : `-shortest` combiné à `-t <durée vidéo>` risque de
  tronquer la vidéo à la durée du son ; cas non couvert par les tests (cf. `memory.md`).

## Structure

- `run_automixer.py` — point d'entrée CLI (appelle `process_videos`).
- `automixer/orchestrator.py` — boucle par lot, `log_phase`, `process_videos`.
- `automixer/source_validator.py` — validation des sources, collecte `.mp4`/`.mp3`, exclusion
  des sorties déjà générées (`_snd_`).
- `automixer/media_selector.py` — durée média (`ffprobe`) + choix aléatoire du son.
- `automixer/audio_processor.py` — remplacement audio `ffmpeg` (vidéo copiée, audio AAC).
- `automixer/output_manager.py` — nommage incrémental + fichier `<dossier>_sound_<n>.txt`.
- `automixer/sound_usage.py` — lecture / écriture du journal JSON d'usage.
- `automixer/usage_updater.py` — reconstruction du journal depuis les metadata.
- `automixer/usage_dashboard.py` — dashboard texte de l'usage.
- `config/settings.py` — chemins (racine projet : `videosource`, `soundsource`,
  `videostorage`, `sound_usage_log.json`).
- `tests/` — tests `unittest` (logique métier + intégration ffmpeg).
- `docs/` — cahier des charges + guide d'utilisation.

## Mémoire de projet

- **Rôle** : `memory.md` porte l'**état volatile** (où on en est, dette, prochaines actions) ;
  les règles stables vivent ici et dans `docs/cahier des charges.md`.
- **Lecture** : au début de chaque session, lire `memory.md` avant de commencer.
- **Mise à jour** : après tout changement significatif, actualiser `memory.md`.
- **Plafond** : ~40 lignes / 2 Ko. Au-delà, compresser : les détails vont dans le CDC ou
  l'historique git, `memory.md` ne garde qu'une synthèse.
