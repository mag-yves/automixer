import tempfile
import unittest
from pathlib import Path

from automixer.source_validator import validate_sources


class ValidateSourcesTests(unittest.TestCase):
    def test_valid_sources_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos = root / "videosource"
            sounds = root / "soundsource"
            videos.mkdir()
            sounds.mkdir()

            (videos / "clip1.mp4").write_bytes(b"video")
            (videos / "subdir").mkdir()
            (videos / "subdir" / "clip2.mp4").write_bytes(b"video")
            (sounds / "intro1.mp3").write_bytes(b"audio")

            report = validate_sources(videos, sounds)

            self.assertTrue(report.valid)
            self.assertEqual(len(report.video_files), 2)
            self.assertEqual(len(report.audio_files), 1)
            self.assertFalse(report.errors)

    def test_missing_video_folder_reports_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos = root / "videosource"
            sounds = root / "soundsource"
            sounds.mkdir()
            (sounds / "intro1.mp3").write_bytes(b"audio")

            report = validate_sources(videos, sounds)

            self.assertFalse(report.valid)
            self.assertIn("Dossier vidéo introuvable", report.errors[0])

    def test_no_supported_files_are_reported_as_warnings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos = root / "videosource"
            sounds = root / "soundsource"
            videos.mkdir()
            sounds.mkdir()

            (videos / "clip.txt").write_text("not video")
            (sounds / "intro.wav").write_bytes(b"audio")

            report = validate_sources(videos, sounds)

            self.assertTrue(report.valid)
            self.assertEqual(len(report.video_files), 0)
            self.assertEqual(len(report.audio_files), 0)
            self.assertTrue(report.warnings)

    def test_processed_output_files_are_excluded_from_source_scan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            videos = root / "videosource"
            sounds = root / "soundsource"
            videos.mkdir()
            sounds.mkdir()

            original = videos / "movie.mp4"
            original.write_bytes(b"video")
            processed = videos / "movie_snd_1.mp4"
            processed.write_bytes(b"processed")
            (sounds / "intro1.mp3").write_bytes(b"audio")

            report = validate_sources(videos, sounds)

            self.assertEqual(len(report.video_files), 1)
            self.assertEqual(report.video_files[0].name, "movie.mp4")


if __name__ == "__main__":
    unittest.main()
