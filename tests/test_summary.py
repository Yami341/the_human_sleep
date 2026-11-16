import unittest
from sleep_summary import summarize


def epoch(start, stage="N2", duration=30):
    return {"start_seconds": start, "duration_seconds": duration, "stage": stage}


class SummaryTests(unittest.TestCase):
    def test_unknown_not_counted_as_wake(self):
        result = summarize([epoch(0, "W"), epoch(30), epoch(60, "UNKNOWN")])
        self.assertEqual(result["observed_minutes"], 1.5)
        self.assertEqual(result["scored_minutes"], 1)
        self.assertEqual(result["annotated_sleep_minutes"], 0.5)
        self.assertEqual(result["annotated_sleep_fraction_of_scored"], 0.5)

    def test_all_unknown_has_no_scored_fraction(self):
        result = summarize([epoch(0, "UNKNOWN")])
        self.assertIsNone(result["annotated_sleep_fraction_of_scored"])

    def test_variable_durations(self):
        result = summarize([epoch(10, "W", 10), epoch(20, "REM", 50)])
        self.assertAlmostEqual(result["annotated_sleep_minutes"], 50 / 60)
        self.assertEqual(result["observed_minutes"], 1)

    def test_invalid_time_and_stage(self):
        for row in [epoch(-1), epoch(float("nan")), epoch(float("inf")),
                    epoch(0, duration=0), epoch(0, duration=-30),
                    epoch(0, duration=float("inf")), epoch(0, "N4"), {}]:
            with self.subTest(row=row), self.assertRaises(ValueError):
                summarize([row])

    def test_gap_overlap_and_out_of_order_rejected(self):
        for start in (29, 31, 0):
            with self.subTest(start=start), self.assertRaises(ValueError):
                summarize([epoch(0), epoch(start)])

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            summarize([])


if __name__ == "__main__":
    unittest.main()
