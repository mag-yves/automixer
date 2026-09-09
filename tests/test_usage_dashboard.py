import unittest

from automixer.usage_dashboard import build_dashboard_lines


class UsageDashboardTests(unittest.TestCase):
    def test_build_dashboard_lines_reports_totals(self):
        usage_counts = {"a.mp3": 5, "b.mp3": 2, "c.mp3": 0, "d.mp3": 0}

        lines = build_dashboard_lines(usage_counts, top_n=10)
        text = "\n".join(lines)

        self.assertIn("Sons référencés     : 4", text)
        self.assertIn("Utilisations totales: 7", text)
        self.assertIn("Sons jamais utilisés: 2", text)
        self.assertIn("Sons déjà utilisés  : 2", text)
        self.assertIn("a.mp3", text)
        self.assertIn("c.mp3", text)

    def test_build_dashboard_lines_handles_no_usage_at_all(self):
        usage_counts = {"a.mp3": 0, "b.mp3": 0}

        lines = build_dashboard_lines(usage_counts, top_n=10)
        text = "\n".join(lines)

        self.assertIn("Sons référencés     : 2", text)
        self.assertIn("Utilisations totales: 0", text)
        self.assertNotIn("les plus utilisés", text)

    def test_build_dashboard_lines_limits_to_top_n(self):
        usage_counts = {f"sound{i}.mp3": i + 1 for i in range(15)}

        lines = build_dashboard_lines(usage_counts, top_n=5)
        text = "\n".join(lines)

        self.assertIn("Top 5 des sons les plus utilisés", text)
        self.assertIn("Top 5 des sons les moins utilisés", text)


if __name__ == "__main__":
    unittest.main()
