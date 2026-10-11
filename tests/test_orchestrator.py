import re
import subprocess
import tempfile
import unittest
import json
from pathlib import Path

from automixer.orchestrator import process_videos
from config.settings import ASSIGNMENTS_PER_VIDEO


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

            outputs = process_videos(
                videos_root,
                sounds_root,
                usage_log_path=root / "sound_usage_log.json",
                assignments_per_video=1,
            )

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

            outputs = process_videos(
                videos_root,
                sounds_root,
                usage_log_path=usage_log_path,
                assignments_per_video=1,
            )

            self.assertEqual(len(outputs), 1)
            self.assertEqual(json.loads(usage_log_path.read_text(encoding="utf-8")), {"intro.mp3": 7})

    def _make_video(self, path: Path) -> None:
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
                str(path),
            ],
            capture_output=True,
            check=True,
        )

    def _make_audio(self, path: Path, index: int) -> None:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                f"sine=frequency={200 + index * 100}:duration=5",
                "-q:a",
                "9",
                str(path),
            ],
            capture_output=True,
            check=True,
        )

    def test_process_videos_produces_assignments_per_video_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos_root = root / "videosource"
            sounds_root = root / "soundsource"
            videos_root.mkdir()
            sounds_root.mkdir()

            self._make_video(videos_root / "clip.mp4")
            for idx in range(1, 4):
                self._make_audio(sounds_root / f"intro_{idx}.mp3", idx)

            outputs = process_videos(
                videos_root,
                sounds_root,
                usage_log_path=root / "sound_usage_log.json",
                assignments_per_video=3,
            )

            self.assertEqual(len(outputs), 3)
            self.assertEqual(
                sorted(path.name for path in outputs),
                ["clip_snd_1.mp4", "clip_snd_2.mp4", "clip_snd_3.mp4"],
            )

            chosen: list[str] = []
            for iteration in range(1, 4):
                log_file = videos_root / f"{videos_root.name}_sound_{iteration}.txt"
                self.assertTrue(log_file.exists())
                match = re.search(r"audio=([^\s|]+)", log_file.read_text(encoding="utf-8"))
                self.assertIsNotNone(match)
                chosen.append(match.group(1))

            # La règle anti-répétition évite que le même son soit repris d'affilée.
            for first, second in zip(chosen, chosen[1:]):
                self.assertNotEqual(first, second)

    def test_process_videos_uses_configured_assignments_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos_root = root / "videosource"
            sounds_root = root / "soundsource"
            videos_root.mkdir()
            sounds_root.mkdir()

            self._make_video(videos_root / "clip.mp4")
            for idx in range(1, ASSIGNMENTS_PER_VIDEO + 1):
                self._make_audio(sounds_root / f"intro_{idx}.mp3", idx)

            outputs = process_videos(
                videos_root, sounds_root, usage_log_path=root / "sound_usage_log.json"
            )

            self.assertEqual(len(outputs), ASSIGNMENTS_PER_VIDEO)


if __name__ == "__main__":
    unittest.main()
