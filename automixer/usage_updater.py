from __future__ import annotations

import json
import re
from pathlib import Path

from automixer.sound_usage import load_usage_counts, save_usage_counts
from automixer.source_validator import SUPPORTED_AUDIO_EXTENSIONS, collect_supported_files

# nnnnnnnn_metadata.json
METADATA_FILE_PATTERN = re.compile(r"^\d+_metadata\.json$")


def find_metadata_files(root: Path) -> list[Path]:
    """Retourne tous les fichiers metadata trouvés récursivement sous root."""
    return sorted(
        path
        for path in root.rglob("*.json")
        if path.is_file() and METADATA_FILE_PATTERN.match(path.name)
    )


def extract_audio_name(metadata_path: Path) -> str | None:
    """Extrait le nom du son référencé par la clé "audio" d'un fichier metadata, si présente."""
    try:
        data = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(data, dict):
        return None

    audio = data.get("audio")
    if isinstance(audio, str) and audio.strip():
        return audio.strip()
    return None


def count_usages(root: Path) -> dict[str, int]:
    """Compte les utilisations de chaque son à partir des fichiers metadata."""
    counts: dict[str, int] = {}
    for metadata_path in find_metadata_files(root):
        name = extract_audio_name(metadata_path)
        if name:
            counts[name] = counts.get(name, 0) + 1
    return counts


def update_usage_log(root: Path, log_path: Path, sounds_root: Path | None = None) -> dict[str, int]:
    """Reconstruit le journal d'utilisation à partir des fichiers metadata trouvés sous root."""
    scanned = count_usages(root)
    # Les sons déjà connus mais non trouvés sont conservés avec un compteur à zéro.
    usage_counts = {name: 0 for name in load_usage_counts(log_path)}
    if sounds_root is not None:
        # La bibliothèque de sons est référencée intégralement, même les sons jamais utilisés.
        for path in collect_supported_files(sounds_root, SUPPORTED_AUDIO_EXTENSIONS):
            usage_counts.setdefault(path.name, 0)
    usage_counts.update(scanned)
    save_usage_counts(log_path, usage_counts)
    return usage_counts
