from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from config.settings import SOUNDS_SOURCE, VIDEOS_SOURCE

SUPPORTED_AUDIO_EXTENSIONS = {".mp3"}
SUPPORTED_VIDEO_EXTENSIONS = {".mp4"}


@dataclass
class SourceValidationResult:
    videos_root: Path
    sounds_root: Path
    video_files: list[Path] = field(default_factory=list)
    audio_files: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors


def is_generated_output_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() == ".mp4" and "_snd_" in path.stem


def collect_supported_files(root: Path, extensions: set[str]) -> list[Path]:
    if not root.exists():
        return []

    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in extensions and not is_generated_output_file(path):
            files.append(path)
    return files


def validate_sources(videos_root: Path, sounds_root: Path) -> SourceValidationResult:
    result = SourceValidationResult(videos_root=Path(videos_root), sounds_root=Path(sounds_root))

    if not result.videos_root.exists():
        result.errors.append(f"Dossier vidéo introuvable : {result.videos_root}")
    if not result.sounds_root.exists():
        result.errors.append(f"Dossier audio introuvable : {result.sounds_root}")

    if result.errors:
        return result

    result.video_files = collect_supported_files(result.videos_root, SUPPORTED_VIDEO_EXTENSIONS)
    result.audio_files = collect_supported_files(result.sounds_root, SUPPORTED_AUDIO_EXTENSIONS)

    if not result.video_files:
        result.warnings.append(f"Aucune vidéo .mp4 trouvée dans : {result.videos_root}")
    if not result.audio_files:
        result.warnings.append(f"Aucun fichier audio .mp3 trouvé dans : {result.sounds_root}")

    return result


def main() -> None:
    report = validate_sources(VIDEOS_SOURCE, SOUNDS_SOURCE)

    print(f"[{__name__}] Vérification des sources")
    print(f"Vidéos: {len(report.video_files)}")
    print(f"Audio: {len(report.audio_files)}")

    if report.errors:
        for error in report.errors:
            print(f"ERREUR: {error}")
        raise SystemExit(1)

    for warning in report.warnings:
        print(f"ATTENTION: {warning}")

    print("Validation des sources OK.")


if __name__ == "__main__":
    main()
