import subprocess
import tempfile
import unittest
from pathlib import Path

from automixer.audio_processor import replace_audio_in_video


class AudioProcessorTests(unittest.TestCase):
    def test_replace_audio_in_video_reduces_audio_to_video_length(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            video_path = root / "video.mp4"
            audio_path = root / "intro.mp3"
            output_path = root / "video_with_audio.mp4"

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
                    "sine=frequency=1000:duration=5",
                    "-q:a",
                    "9",
                    str(audio_path),
                ],
                capture_output=True,
                check=True,
            )

            result_path = replace_audio_in_video(video_path, audio_path, output_path)

            self.assertTrue(result_path.exists())
            self.assertEqual(result_path, output_path)

            duration = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    str(result_path),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertLess(float(duration.stdout.strip()), 2.5)


if __name__ == "__main__":
    unittest.main()
