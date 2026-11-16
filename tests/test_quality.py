import unittest
import numpy as np
from eeg_quality import scan


class QualityTests(unittest.TestCase):
    def test_clean_sinusoid(self):
        x = 20 * np.sin(np.arange(3000) * 0.2)
        self.assertEqual(scan(x, 100)["flagged_percent"], 0)

    def test_flat_and_nonfinite(self):
        self.assertEqual(scan(np.zeros(3000), 100)["flat_windows"], 1)
        r = scan(np.full(3000, np.nan), 100)
        self.assertEqual(r["nonfinite_samples"], 3000)
        self.assertEqual(r["flagged_percent"], 100)

    def test_partial_window_duration_weighted(self):
        x = np.r_[20 * np.sin(np.arange(3000) * .2), np.zeros(1000)]
        self.assertEqual(scan(x, 100)["flagged_percent"], 25)

    def test_spike_marked(self):
        x = 20 * np.sin(np.arange(3000) * .2)
        x[50] = -201
        self.assertEqual(scan(x, 100)["high_amplitude_windows"], 1)

    def test_invalid_input(self):
        for values, sfreq in [([], 100), ([1], 0), ([1], float("nan")), ([[1]], 100)]:
            with self.subTest(values=values), self.assertRaises(ValueError):
                scan(values, sfreq)
