#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from automixer.usage_dashboard import print_dashboard
from config.settings import SOUND_USAGE_LOG


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Affiche un dashboard résumant l'usage des sons à partir de sound_usage_log.json."
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=SOUND_USAGE_LOG,
        help="Chemin du journal JSON à analyser (défaut: sound_usage_log.json).",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Nombre de sons à afficher dans chaque classement (défaut: 10).",
    )
    args = parser.parse_args()

    print_dashboard(args.log, top_n=args.top)


if __name__ == "__main__":
    main()
