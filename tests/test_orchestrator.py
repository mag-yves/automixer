import subprocess
import tempfile
import unittest
import json
from pathlib import Path

from automixer.orchestrator import process_videos


class OrchestratorTests(unittest.TestCase):
    def test_process_videos_creates_output_and_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos_root = root / "videosource"
            sounds_root = root / "soundsource"
            videos_root.mkdir()
            sounds_root.mkdir()

            video_path = videos_root / "clip.mp4"
            audio_path = sounds_root / "intro.mp3"

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "testsrc=size=640x360:rate=30:duration=2",
                    "-pix_fmt",
                    "yuv420p",
                    str(video_path),
                ],
                capture_output=True,
                check=True,
            )

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "sine=frequency=800:duration=5",
                    "-q:a",
                    "9",
                    str(audio_path),
                ],
                capture_output=True,
                check=True,
            )

            outputs = process_videos(videos_root, sounds_root, usage_log_path=root / "sound_usage_log.json")

            self.assertEqual(len(outputs), 1)
            self.assertTrue(outputs[0].exists())
            self.assertTrue((videos_root / f"{videos_root.name}_sound_1.txt").exists())
            content = (videos_root / f"{videos_root.name}_sound_1.txt").read_text(encoding="utf-8")
            self.assertIn("intro.mp3", content)
            self.assertIn("clip", content)

    def test_process_videos_does_not_update_usage_counter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos_root = root / "videosource"
            sounds_root = root / "soundsource"
            videos_root.mkdir()
            sounds_root.mkdir()

            video_path = videos_root / "clip.mp4"
            audio_path = sounds_root / "intro.mp3"
            usage_log_path = root / "sound_usage_log.json"
            usage_log_path.write_text(json.dumps({"intro.mp3": 7}), encoding="utf-8")

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "testsrc=size=640x360:rate=30:duration=2",
                    "-pix_fmt",
                    "yuv420p",
                    str(video_path),
                ],
                capture_output=True,
                check=True,
            )

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "sine=frequency=800:duration=5",
                    "-q:a",
                    "9",
                    str(audio_path),
                ],
                capture_output=True,
                check=True,
            )

            outputs = process_videos(videos_root, sounds_root, usage_log_path=usage_log_path)

            self.assertEqual(len(outputs), 1)
            self.assertEqual(json.loads(usage_log_path.read_text(encoding="utf-8")), {"intro.mp3": 7})


if __name__ == "__main__":
    unittest.main()
