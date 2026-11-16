"""Exploratory signal flags, not validated clinical artifact detection."""
import numpy as np

WINDOW_SECONDS = 30
FLAT_RANGE_UV = 1.0
HIGH_ABSOLUTE_UV = 200.0


def scan(values_uv, sfreq):
    values = np.asarray(values_uv, dtype=float)
    if values.ndim != 1 or not values.size or not np.isfinite(sfreq) or sfreq <= 0:
        raise ValueError("Expected nonempty 1D signal and positive finite sampling rate")
    size = round(WINDOW_SECONDS * sfreq)
    if size < 1:
        raise ValueError("Sampling rate too small")
    windows = []
    for start in range(0, len(values), size):
        chunk = values[start:start + size]
        finite = np.isfinite(chunk)
        good = chunk[finite]
        flat = bool(finite.all() and np.ptp(chunk) < FLAT_RANGE_UV)
        high = bool(good.size and np.max(np.abs(good)) > HIGH_ABSOLUTE_UV)
        missing = not bool(finite.all())
        windows.append({"start_seconds": start / sfreq, "duration_seconds": len(chunk) / sfreq,
                        "nonfinite_samples": int((~finite).sum()), "flat": flat,
                        "high_amplitude": high, "nonfinite": missing,
                        "flagged": flat or high or missing})
    duration = len(values) / sfreq
    return {"duration_seconds": duration, "windows": windows,
            "flagged_percent": 100 * sum(w["duration_seconds"] for w in windows if w["flagged"]) / duration,
            "nonfinite_samples": sum(w["nonfinite_samples"] for w in windows),
            "flat_windows": sum(w["flat"] for w in windows),
            "high_amplitude_windows": sum(w["high_amplitude"] for w in windows)}
