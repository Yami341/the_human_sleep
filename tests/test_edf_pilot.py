import unittest
from sleep_edf_pilot import normalize


class AnnotationTests(unittest.TestCase):
    def test_clip_map_and_preserve(self):
        rows = normalize([(-10, 30, "Sleep stage 3"), (20, 50, "Sleep stage 4")], 60)
        self.assertEqual([r["duration_seconds"] for r in rows], [20, 40])
        self.assertEqual([r["stage"] for r in rows], ["N3", "N3"])
        self.assertEqual(rows[1]["original_label"], "Sleep stage 4")

    def test_gaps_and_missing(self):
        rows = normalize([(10, 10, "Sleep stage R")], 30)
        self.assertEqual([r["stage"] for r in rows], ["UNKNOWN", "REM", "UNKNOWN"])
        self.assertEqual(normalize([], 30)[0]["duration_seconds"], 30)

    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            normalize([(0, 30, "Sleep stage W"), (20, 30, "Sleep stage R")], 60)

    def test_unknown_label_and_nonfinite_rejected(self):
        for item in [(0, 30, "unexpected"), (float("nan"), 30, "Sleep stage W")]:
            with self.subTest(item=item), self.assertRaises(ValueError):
                normalize([item], 60)
