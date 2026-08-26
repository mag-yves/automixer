import tempfile
import unittest
from pathlib import Path

from automixer.output_manager import append_sound_log


class Phase5LoggingTests(unittest.TestCase):
    def test_sound_log_contains_timestamp_and_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            video = root / "clip.mp4"
            audio = root / "intro.mp3"
            output = root / "clip_snd_1.mp4"

            video.write_bytes(b"video")
            audio.write_bytes(b"audio")
            output.write_bytes(b"output")

            log_path = append_sound_log(root, video, audio, output)
            content = log_path.read_text(encoding="utf-8")

            self.assertIn("video=clip.mp4", content)
            self.assertIn("audio=intro.mp3", content)
            self.assertIn("output=clip_snd_1.mp4", content)
            self.assertRegex(content, r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]")


if __name__ == "__main__":
    unittest.main()
