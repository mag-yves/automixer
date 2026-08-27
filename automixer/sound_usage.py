from __future__ import annotations

import json
from pathlib import Path


def load_usage_counts(path: Path) -> dict[str, int]:
    """Charge le journal d'utilisation des sons, ou un journal vide si absent/invalide."""
    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(data, dict):
        return {}

    return {str(name): int(count) for name, count in data.items()}


def save_usage_counts(path: Path, usage_counts: dict[str, int]) -> None:
    """Persiste le journal d'utilisation des sons sur disque."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(usage_counts, handle, indent=2, sort_keys=True, ensure_ascii=False)


def increment_usage(usage_counts: dict[str, int], audio_path: Path) -> None:
    """Incrémente le compteur d'utilisation d'un son."""
    usage_counts[audio_path.name] = usage_counts.get(audio_path.name, 0) + 1
