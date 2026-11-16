"""Descriptive summary of contiguous, pre-scored epochs; not a classifier."""
import argparse
import csv
import json
import math
from pathlib import Path

STAGES = ("W", "N1", "N2", "N3", "REM", "UNKNOWN")


def summarize(rows):
    """One session, seconds relative to its start; no gaps or overlap allowed."""
    seconds = dict.fromkeys(STAGES, 0.0)
    previous_end = None
    first_start = None
    count = 0
    for row in rows:
        try:
            start = float(row["start_seconds"])
            duration = float(row["duration_seconds"])
            stage = row["stage"]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Expected start_seconds, duration_seconds, stage") from exc
        if not math.isfinite(start) or not math.isfinite(duration):
            raise ValueError("Times must be finite")
        if start < 0 or duration <= 0 or stage not in STAGES:
            raise ValueError("Invalid time or stage")
        end = start + duration
        if not math.isfinite(end) or end <= start:
            raise ValueError("Unrepresentable interval")
        if previous_end is not None and not math.isclose(
            start, previous_end, rel_tol=0, abs_tol=1e-6
        ):
            raise ValueError("Epochs must be ordered and contiguous, without overlap")
        if first_start is None:
            first_start = start
        previous_end = end
        seconds[stage] += duration
        count += 1
    if not count:
        raise ValueError("At least one epoch is required")
    total = sum(seconds.values())
    if not math.isfinite(total):
        raise ValueError("Total duration overflow")
    scored = total - seconds["UNKNOWN"]
    sleep = sum(seconds[s] for s in ("N1", "N2", "N3", "REM"))
    return {
        "purpose": "descriptive_research_only",
        "epochs": count,
        "start_seconds": first_start,
        "end_seconds": previous_end,
        "observed_minutes": total / 60,
        "scored_minutes": scored / 60,
        "unknown_minutes": seconds["UNKNOWN"] / 60,
        "annotated_sleep_minutes": sleep / 60,
        "stage_minutes": {s: value / 60 for s, value in seconds.items()},
        "annotated_sleep_fraction_of_scored": sleep / scored if scored else None,
        "note": "No diagnosis. Scored fraction is not sleep efficiency.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    args = parser.parse_args()
    try:
        with args.csv_path.open(encoding="utf-8", newline="") as handle:
            report = summarize(csv.DictReader(handle))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
