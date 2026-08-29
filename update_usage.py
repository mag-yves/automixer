#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from automixer.usage_updater import update_usage_log
from config.settings import SOUND_USAGE_LOG, VIDEO_STORAGE


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Met à jour sound_usage_log.json à partir des fichiers *_sound*.txt."
    )
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=VIDEO_STORAGE,
        help="Dossier racine à explorer récursivement (défaut: videostorage).",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=SOUND_USAGE_LOG,
        help="Chemin du journal JSON à mettre à jour.",
    )
    args = parser.parse_args()

    if not args.root.is_dir():
        parser.error(f"Dossier introuvable: {args.root}")

    usage_counts = update_usage_log(args.root, args.log)
    total = sum(usage_counts.values())
    print(f"{len(usage_counts)} sons référencés, {total} utilisations comptabilisées.")
    print(f"Journal mis à jour: {args.log}")


if __name__ == "__main__":
    main()
