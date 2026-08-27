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

    def test_choose_audio_prefers_least_used_sounds_when_more_than_pool_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sounds = root / "sounds"
            sounds.mkdir()

            fresh_candidates = []
            usage_counts = {}
            for index in range(20):
                path = sounds / f"fresh{index}.mp3"
                path.write_bytes(b"a")
                fresh_candidates.append(path)
                usage_counts[path.name] = 0

            overused = sounds / "overused.mp3"
            overused.write_bytes(b"a")
            usage_counts["overused.mp3"] = 999

            all_candidates = fresh_candidates + [overused]

            for _ in range(30):
                selected = choose_audio_for_video(
                    overused, all_candidates, previous_audio=None, usage_counts=usage_counts
                )
                self.assertNotEqual(selected, overused)

    def test_choose_audio_limits_pool_to_20_least_used_sounds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sounds = root / "sounds"
            sounds.mkdir()

            candidates = []
            usage_counts = {}
            for index in range(25):
                path = sounds / f"intro{index}.mp3"
                path.write_bytes(b"a")
                candidates.append(path)
                usage_counts[path.name] = index

            overused_names = {path.name for path in candidates[20:]}

            selected = choose_audio_for_video(
                candidates[0], candidates, previous_audio=None, usage_counts=usage_counts
            )

            self.assertNotIn(selected.name, overused_names)


if __name__ == "__main__":
    unittest.main()
