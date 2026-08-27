import subprocess
import tempfile
import unittest
from pathlib import Path

from automixer.orchestrator import process_videos


class Phase7StabilizationTests(unittest.TestCase):
    def test_process_videos_skips_invalid_video_and_keeps_valid_ones(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos_root = root / "videosource"
            sounds_root = root / "soundsource"
            videos_root.mkdir()
            sounds_root.mkdir()

            valid_video = videos_root / "valid.mp4"
            invalid_video = videos_root / "invalid.mp4"

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    "testsrc=size=320x240:rate=15:duration=2",
                    "-pix_fmt",
                    "yuv420p",
                    str(valid_video),
                ],
                capture_output=True,
                check=True,
            )
            invalid_video.write_bytes(b"not a valid mp4")

            for idx in range(1, 3):
                audio_path = sounds_root / f"intro_{idx}.mp3"
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-f",
                        "lavfi",
                        "-i",
                        f"sine=frequency={200 + idx * 100}:duration=5",
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
            self.assertTrue(outputs[0].name.startswith("valid_snd_"))


if __name__ == "__main__":
    unittest.main()
