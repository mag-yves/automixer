# Mémoire de projet — AutomMixer

> État **courant** et **prochaines actions**, à lire en début de session et à mettre à jour
> après tout changement significatif. Règles, structure et commandes : `AGENTS.md` ; détail
> fonctionnel : `docs/cahier des charges.md`. **Ne rien dupliquer ici.**
> Plafond : ~40 lignes / 2 Ko.

## État courant

- Outil **Python local** (stdlib + FFmpeg) de montage par lot : remplacement de la piste
  audio des vidéos de `videosource/` par un son aléatoire de `soundsource/`. Les **7 phases**
  du CDC sont livrées (validation, sélection, coupe à la durée vidéo, export incrémental
  `_snd_<n>.mp4`, log `<dossier>_sound_<n>.txt`, garde-fous).
- Utilitaires : `update-usage.sh` (reconstruction du journal), `show-usage.sh` (dashboard),
  `start.sh` (menu). Sélection **uniforme** (commit `96f13bd`) : le journal d'usage est
  purement statistique et ne pèse plus sur le tirage.
- **29 tests** `unittest` verts (`python3 -m unittest discover -s tests`), FFmpeg 8.x.

## Dette / points d'attention

- **`docs/USAGE.md` obsolète** : décrit la sélection pondérée (retirée) et une reconstruction
  depuis `*_sound*.txt`, alors que le code lit les `_metadata.json`. À réaligner (🔴).
- **Risque `-shortest`** : un son plus court que la vidéo risque de tronquer la vidéo à la
  durée du son (non testé). À vérifier / corriger (🟠).
- **CDC partiellement non couvert** : §7.8 bilan global, §7.9 dry-run, §7.12 vérification
  post-export du flux audio — absents du code.
- **Nettoyage** : détection de durée dupliquée (`media_selector` / `audio_processor`), import
  `random` inutilisé (`orchestrator.py:3`), logs via `print` plutôt que `logging`.
- Dépendance implicite à `ffmpeg`/`ffprobe` (aucun venv/requirements) ; suivi du temps
  **non configuré** (`devtime`).

## Prochaines actions

- 🔴 Réaligner `docs/USAGE.md` sur le comportement réel (sélection uniforme, metadata).
- 🟠 Vérifier `-shortest` sur un son plus court que la vidéo (+ test).
- 🔵 Trancher les manques CDC (§7.8 / §7.9 / §7.12) et nettoyer les doublons.
- 🔵 Initialiser le suivi du temps (`devtime init` + commandes `/time-*`).
