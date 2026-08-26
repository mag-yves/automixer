from __future__ import annotations

import subprocess
from pathlib import Path


def replace_audio_in_video(video_path: Path, audio_path: Path, output_path: Path) -> Path:
    """Remplace la piste audio d'une vidéo par un fichier audio coupé à la durée de la vidéo."""
    if not video_path.exists():
        raise FileNotFoundError(f"Vidéo introuvable : {video_path}")
    if not audio_path.exists():
        raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")

    video_duration = _get_duration(video_path)
    if video_duration is None:
        raise ValueError(f"Impossible de lire la durée de la vidéo : {video_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-shortest",
        "-t",
        str(video_duration),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        str(output_path),
    ]

    subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=True)
    return output_path


def _get_duration(file_path: Path) -> float | None:
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
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None
