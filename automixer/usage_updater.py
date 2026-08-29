from __future__ import annotations

import re
from pathlib import Path

from automixer.sound_usage import load_usage_counts, save_usage_counts

# nnnnnn_nnnnnn_sound_n.txt, nnnnnn_nnnnnn_sound.txt, nnnnnn_sound.txt, sound.txt
LOG_FILE_PATTERN = re.compile(r"^(?:\d+_)*sound(?:_\d+)?\.txt$")
AUDIO_FIELD_PATTERN = re.compile(r"audio=([^|\n\r]+)")


def find_sound_log_files(root: Path) -> list[Path]:
    """Retourne tous les fichiers de log de son trouvés récursivement sous root."""
    return sorted(
        path
        for path in root.rglob("*.txt")
        if path.is_file() and LOG_FILE_PATTERN.match(path.name)
    )


def extract_audio_names(log_path: Path) -> list[str]:
    """Extrait les valeurs de audio= contenues dans un fichier de log."""
    try:
        content = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    names = []
    for match in AUDIO_FIELD_PATTERN.finditer(content):
        name = match.group(1).strip()
        if name:
            names.append(name)
    return names


def count_usages(root: Path) -> dict[str, int]:
    """Compte les utilisations de chaque son à partir des fichiers de log."""
    counts: dict[str, int] = {}
    for log_path in find_sound_log_files(root):
        for name in extract_audio_names(log_path):
            counts[name] = counts.get(name, 0) + 1
    return counts


def update_usage_log(root: Path, log_path: Path) -> dict[str, int]:
    """Reconstruit le journal d'utilisation à partir des fichiers de log trouvés sous root."""
    scanned = count_usages(root)
    # Les sons déjà connus mais non trouvés sont conservés avec un compteur à zéro.
    usage_counts = {name: 0 for name in load_usage_counts(log_path)}
    usage_counts.update(scanned)
    save_usage_counts(log_path, usage_counts)
    return usage_counts
