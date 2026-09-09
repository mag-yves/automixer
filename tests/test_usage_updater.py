import json
import tempfile
import unittest
from pathlib import Path

from automixer.usage_updater import count_usages, update_usage_log


class UsageUpdaterTests(unittest.TestCase):
    def test_count_usages_reads_audio_field_from_metadata_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder_a = root / "batch_01" / "clip_a"
            folder_b = root / "batch_02" / "clip_b"
            folder_a.mkdir(parents=True)
            folder_b.mkdir(parents=True)

            (folder_a / "20260101_metadata.json").write_text(
                json.dumps({"audio": "intro001.mp3"}), encoding="utf-8"
            )
            (folder_b / "20260102_metadata.json").write_text(
                json.dumps({"audio": "intro001.mp3"}), encoding="utf-8"
            )
            # Clé "audio" absente : ne doit pas planter ni compter.
            (folder_b / "20260103_metadata.json").write_text(
                json.dumps({"video_file": "clip.mp4"}), encoding="utf-8"
            )

            counts = count_usages(root)

            self.assertEqual(counts, {"intro001.mp3": 2})

    def test_count_usages_ignores_non_metadata_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sound.txt").write_text("audio=intro001.mp3", encoding="utf-8")
            (root / "notes_metadata.json").write_text(
                json.dumps({"audio": "intro002.mp3"}), encoding="utf-8"
            )

            counts = count_usages(root)

            self.assertEqual(counts, {})

    def test_update_usage_log_keeps_known_sounds_not_found_at_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log_path = root / "sound_usage_log.json"
            log_path.write_text(json.dumps({"intro001.mp3": 5, "intro002.mp3": 3}), encoding="utf-8")

            folder = root / "clip"
            folder.mkdir()
            (folder / "20260101_metadata.json").write_text(
                json.dumps({"audio": "intro001.mp3"}), encoding="utf-8"
            )

            counts = update_usage_log(root, log_path)

            self.assertEqual(counts, {"intro001.mp3": 1, "intro002.mp3": 0})
            self.assertEqual(json.loads(log_path.read_text(encoding="utf-8")), counts)

    def test_update_usage_log_seeds_all_sounds_from_library(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log_path = root / "sound_usage_log.json"
            sounds_root = root / "soundsource"
            sounds_root.mkdir()
            for name in ("intro001.mp3", "intro002.mp3", "intro003.mp3"):
                (sounds_root / name).write_bytes(b"a")

            folder = root / "clip"
            folder.mkdir()
            (folder / "20260101_metadata.json").write_text(
                json.dumps({"audio": "intro001.mp3"}), encoding="utf-8"
            )

            counts = update_usage_log(root, log_path, sounds_root=sounds_root)

            self.assertEqual(counts, {"intro001.mp3": 1, "intro002.mp3": 0, "intro003.mp3": 0})


if __name__ == "__main__":
    unittest.main()
