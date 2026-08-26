from __future__ import annotations

import random
from pathlib import Path

from config.settings import SOUNDS_SOURCE


def get_media_duration(file_path: Path) -> float | None:
    """Retourne la durée en secondes d'un média si elle peut être lue."""
    if not file_path.exists():
        return None

    try:
        import subprocess

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(file_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0 or not result.stdout.strip():
            return None

        return float(result.stdout.strip())
    except (OSError, ValueError):
        return None


def choose_audio_for_video(video_path: Path, audio_files: list[Path], previous_audio: Path | None = None) -> Path:
    """Choisit un fichier audio aléatoire en évitant, si possible, le précédent son."""
    candidates = [path for path in audio_files if path.exists()]
    if not candidates:
        raise FileNotFoundError(f"Aucun fichier audio disponible pour {video_path}")

    if len(candidates) == 1:
        return candidates[0]

    if previous_audio is not None and previous_audio in candidates:
        available = [path for path in candidates if path != previous_audio]
        if available:
            return random.choice(available)

    return random.choice(candidates)
