import tempfile
import unittest
from pathlib import Path

from automixer.output_manager import append_sound_log, get_next_output_path


class OutputManagerTests(unittest.TestCase):
    def test_get_next_output_path_increments_suffix(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = root / "video.mp4"
            original.write_bytes(b"video")
            (root / "video_snd_1.mp4").write_bytes(b"output1")
            (root / "video_snd_2.mp4").write_bytes(b"output2")

            target = get_next_output_path(original)

            self.assertEqual(target.name, "video_snd_3.mp4")

    def test_get_next_output_path_does_not_duplicate_suffix_on_processed_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            processed = root / "video_snd_1.mp4"
            processed.write_bytes(b"output")

            target = get_next_output_path(processed)

            self.assertEqual(target.name, "video_snd_2.mp4")

    def test_append_sound_log_records_audio_and_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            video = root / "video.mp4"
            audio = root / "intro.mp3"
            output = root / "video_snd_1.mp4"
            video.write_bytes(b"video")
            audio.write_bytes(b"audio")
            output.write_bytes(b"output")

            log_path = append_sound_log(root, video, audio, output)

            self.assertTrue(log_path.exists())
            self.assertEqual(log_path.name, f"{root.name}_sound_1.txt")
            content = log_path.read_text(encoding="utf-8")
            self.assertIn("video.mp4", content)
            self.assertIn("intro.mp3", content)
            self.assertIn("video_snd_1.mp4", content)
            self.assertIn("[", content)

    def test_append_sound_log_uses_output_iteration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            video = root / "video.mp4"
            audio = root / "intro.mp3"
            output = root / "video_snd_2.mp4"

            log_path = append_sound_log(root, video, audio, output)

            self.assertEqual(log_path.name, f"{root.name}_sound_2.txt")


if __name__ == "__main__":
    unittest.main()
