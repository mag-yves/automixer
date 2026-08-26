#!/usr/bin/env python3

from pathlib import Path

from automixer.orchestrator import process_videos


if __name__ == "__main__":
    process_videos(Path("videosource"), Path("soundsource"))
