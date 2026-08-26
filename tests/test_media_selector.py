import tempfile
import unittest
from pathlib import Path

from automixer.media_selector import choose_audio_for_video, get_media_duration


class MediaSelectorTests(unittest.TestCase):
    def test_choose_audio_avoids_previous_audio_when_possible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sounds = root / "sounds"
            sounds.mkdir()
            first = sounds / "intro1.mp3"
            second = sounds / "intro2.mp3"
            first.write_bytes(b"a")
            second.write_bytes(b"b")

            selected = choose_audio_for_video(first, [first, second], previous_audio=first)
            self.assertEqual(selected, second)

    def test_choose_audio_returns_single_file_when_only_one_available(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sounds = root / "sounds"
            sounds.mkdir()
            only = sounds / "intro1.mp3"
            only.write_bytes(b"a")

            selected = choose_audio_for_video(only, [only], previous_audio=only)
            self.assertEqual(selected, only)

    def test_get_media_duration_handles_missing_file(self):
        missing = Path("/tmp/this-file-should-not-exist.mp3")
        self.assertIsNone(get_media_duration(missing))


if __name__ == "__main__":
    unittest.main()
