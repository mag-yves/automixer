import tempfile
import unittest
from pathlib import Path

from automixer.sound_usage import increment_usage, load_usage_counts, save_usage_counts


class SoundUsageTests(unittest.TestCase):
    def test_load_usage_counts_returns_empty_dict_when_missing(self):
        missing = Path("/tmp/this-usage-log-should-not-exist.json")
        self.assertEqual(load_usage_counts(missing), {})

    def test_save_and_load_usage_counts_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "usage.json"
            counts = {"intro1.mp3": 3, "intro2.mp3": 0}

            save_usage_counts(log_path, counts)
            loaded = load_usage_counts(log_path)

            self.assertEqual(loaded, counts)

    def test_increment_usage_creates_and_increments_counter(self):
        counts: dict[str, int] = {}
        audio = Path("intro1.mp3")

        increment_usage(counts, audio)
        increment_usage(counts, audio)

        self.assertEqual(counts["intro1.mp3"], 2)

    def test_load_usage_counts_ignores_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "usage.json"
            log_path.write_text("not valid json", encoding="utf-8")

            self.assertEqual(load_usage_counts(log_path), {})


if __name__ == "__main__":
    unittest.main()
