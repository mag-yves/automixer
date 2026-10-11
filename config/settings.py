from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

VIDEOS_SOURCE = BASE_DIR / "videosource"
SOUNDS_SOURCE = BASE_DIR / "soundsource"
VIDEO_STORAGE = BASE_DIR / "videostorage"
SOUND_USAGE_LOG = BASE_DIR / "sound_usage_log.json"

# Nombre d'attributions de son (donc de sorties vidéo) à produire par vidéo.
ASSIGNMENTS_PER_VIDEO = 2
