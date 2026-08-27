import subprocess
import tempfile
import unittest
from pathlib import Path

from automixer.orchestrator import process_videos


class Phase6ValidationTests(unittest.TestCase):
    def test_process_videos_handles_multiple_videos_and_writes_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos_root = root / "videosource"
            sounds_root = root / "soundsource"
            videos_root.mkdir()
            sounds_root.mkdir()

            first_dir = videos_root / "batch_01"
            second_dir = videos_root / "batch_02"
            first_dir.mkdir()
            second_dir.mkdir()

            video_files = [
                first_dir / "clip_a.mp4",
                first_dir / "clip_b.mp4",
                second_dir / "clip_c.mp4",
            ]

            for index, video_file in enumerate(video_files, start=1):
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-f",
                        "lavfi",
                        "-i",
                        f"testsrc=size=640x360:rate=30:duration={index/2 + 1}",
                        "-pix_fmt",
                        "yuv420p",
                        str(video_file),
                    ],
                    capture_output=True,
                    check=True,
                )

            for idx in range(1, 4):
                audio_file = sounds_root / f"intro_{idx}.mp3"
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-f",
                        "lavfi",
                        "-i",
                        f"sine=frequency={200 + idx * 100}:duration=6",
                        "-q:a",
                        "9",
                        str(audio_file),
                    ],
                    capture_output=True,
                    check=True,
                )

            outputs = process_videos(videos_root, sounds_root, usage_log_path=root / "sound_usage_log.json")

            self.assertEqual(len(outputs), 3)
            for output in outputs:
                self.assertTrue(output.exists())

            for folder in [first_dir, second_dir]:
                log_file = folder / f"{folder.name}_sound_1.txt"
                self.assertTrue(log_file.exists())
                self.assertIn("video=", log_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
