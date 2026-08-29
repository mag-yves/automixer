from __future__ import annotations

import random
from datetime import datetime
from pathlib import Path

from automixer.audio_processor import replace_audio_in_video
from automixer.media_selector import choose_audio_for_video, get_media_duration
from automixer.output_manager import append_sound_log, get_next_output_path
from automixer.sound_usage import load_usage_counts
from automixer.source_validator import validate_sources
from config.settings import SOUND_USAGE_LOG


def log_phase(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def process_videos(
    videos_root: Path | str,
    sounds_root: Path | str,
    usage_log_path: Path | str | None = None,
) -> list[Path]:
    videos_root = Path(videos_root)
    sounds_root = Path(sounds_root)
    usage_log_path = Path(usage_log_path) if usage_log_path is not None else SOUND_USAGE_LOG

    log_phase("Début du traitement")
    validation = validate_sources(videos_root, sounds_root)
    if not validation.valid:
        for error in validation.errors:
            log_phase(f"ERREUR: {error}")
        raise FileNotFoundError("Validation des sources échouée.")

    if not validation.audio_files:
        raise FileNotFoundError(f"Aucun fichier audio .mp3 trouvé dans {sounds_root}")

    usage_counts = load_usage_counts(usage_log_path)
    handled: list[Path] = []
    previous_audio: Path | None = None

    for video_path in validation.video_files:
        try:
            log_phase(f"Traitement de la vidéo: {video_path}")

            video_duration = get_media_duration(video_path)
            if video_duration is None:
                raise ValueError(f"Impossible de lire la durée de la vidéo : {video_path}")

            output_path = get_next_output_path(video_path)
            audio_file = choose_audio_for_video(video_path, validation.audio_files, previous_audio, usage_counts)
            previous_audio = audio_file

            log_phase(f"Son choisi: {audio_file.name}")

            audio_duration = get_media_duration(audio_file)
            log_phase(
                f"Durée vidéo: {video_duration}s | Durée son: {audio_duration}s"
            )

            processed_path = replace_audio_in_video(video_path, audio_file, output_path)
            log_phase(f"Sortie exportée: {processed_path.name}")

            log_path = append_sound_log(video_path.parent, video_path, audio_file, processed_path)
            log_phase(f"Log ajouté: {log_path}")

            handled.append(processed_path)
        except Exception as exc:  # pragma: no cover - guard de robustesse
            log_phase(f"ERREUR TRAITEMENT: {video_path} -> {exc}")
            continue

    log_phase("Traitement terminé")
    return handled
