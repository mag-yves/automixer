from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


def _base_name_for_output(path: Path) -> str:
    stem = path.stem
    match = re.match(r"^(.*?)(?:_snd_\d+)+$", stem)
    if match:
        return match.group(1)
    if stem.endswith("_snd"):
        return stem[:-4]
    return stem


def get_next_output_path(video_path: Path) -> Path:
    """Retourne le prochain chemin de sortie libre avec suffixe incrémental."""
    parent = video_path.parent
    stem = _base_name_for_output(video_path)
    counter = 1

    while True:
        candidate = parent / f"{stem}_snd_{counter}.mp4"
        if not candidate.exists():
            return candidate
        counter += 1


def append_sound_log(log_dir: Path, video_path: Path, audio_path: Path, output_path: Path) -> Path:
    """Ajoute une ligne de log horodatée dans un fichier d'itération."""
    subfolder_name = log_dir.name
    match = re.search(r"_snd_(\d+)$", output_path.stem)
    iteration = match.group(1) if match else "1"
    log_path = log_dir / f"{subfolder_name}_sound_{iteration}.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = (
        f"[{timestamp}] video={video_path.name} | "
        f"audio={audio_path.name} | output={output_path.name}\n"
    )
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(line)
    return log_path
