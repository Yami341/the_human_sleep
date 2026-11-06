"""Fixed, checksum-verified Sleep-EDF pilot. Research visualization only."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import urllib.request

from sleep_summary import summarize

BASE = "https://physionet.org/files/sleep-edfx/1.0.0/"
FILES = ("SC4001E0-PSG.edf", "SC4001EC-Hypnogram.edf")
LICENSE = "https://physionet.org/content/sleep-edfx/view-license/1.0.0/"
MAP = {"Sleep stage W": "W", "Sleep stage 1": "N1",
       "Sleep stage 2": "N2", "Sleep stage 3": "N3",
       "Sleep stage 4": "N3", "Sleep stage R": "REM",
       "Sleep stage ?": "UNKNOWN", "Movement time": "UNKNOWN"}


def sha256(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def download(data_dir):
    data_dir.mkdir(parents=True, exist_ok=True)
    checksums = urllib.request.urlopen(BASE + "SHA256SUMS.txt", timeout=60).read()
    (data_dir / "SHA256SUMS.txt").write_bytes(checksums)
    (data_dir / "license.html").write_bytes(
        urllib.request.urlopen(LICENSE, timeout=60).read())
    expected = {}
    for line in checksums.decode().splitlines():
        digest, name = line.split(maxsplit=1)
        expected[name.lstrip("*").removeprefix("./")] = digest
    manifest = []
    for name in FILES:
        key = "sleep-cassette/" + name
        digest = expected[key]
        path = data_dir / name
        if not path.exists():
            part = path.with_suffix(".part")
            with urllib.request.urlopen(BASE + key, timeout=60) as src, part.open("wb") as dst:
                while chunk := src.read(1024 * 1024):
                    dst.write(chunk)
            if sha256(part) != digest:
                raise ValueError("Checksum mismatch: " + name)
            part.replace(path)
        if sha256(path) != digest:
            raise ValueError("Cached file checksum mismatch: " + name)
        manifest.append({"file": name, "url": BASE + key, "sha256": digest,
                         "bytes": path.stat().st_size})
    return manifest


def normalize(intervals, duration):
    """Clip to recording; preserve original labels, fill gaps as UNKNOWN."""
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Invalid recording duration")
    rows, cursor = [], 0.0
    for onset, length, label in intervals:
        if label not in MAP or not all(map(math.isfinite, (onset, length))) or length <= 0:
            raise ValueError("Invalid annotation")
        start, end = max(0.0, onset), min(duration, onset + length)
        if end <= start:
            continue
        if start < cursor:
            raise ValueError("Overlapping or unordered annotations")
        if start > cursor:
            rows.append(dict(start_seconds=cursor, duration_seconds=start-cursor,
                             stage="UNKNOWN", original_label="UNANNOTATED"))
        rows.append(dict(start_seconds=start, duration_seconds=end-start,
                         stage=MAP[label], original_label=label))
        cursor = end
    if cursor < duration:
        rows.append(dict(start_seconds=cursor, duration_seconds=duration-cursor,
                         stage="UNKNOWN", original_label="UNANNOTATED"))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    manifest = download(args.data_dir)
    import mne
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    raw = mne.io.read_raw_edf(args.data_dir / FILES[0], preload=False, verbose="ERROR")
    annotations = mne.read_annotations(args.data_dir / FILES[1])
    # MNE returns orig_time=None for these EDF+ annotations. Check the
    # source EDF date/time fields instead; onsets are relative to that start.
    with (args.data_dir / FILES[0]).open("rb") as psg, (args.data_dir / FILES[1]).open("rb") as hyp:
        psg.seek(168)
        hyp.seek(168)
        if psg.read(16) != hyp.read(16):
            raise ValueError("EDF clocks differ; manual alignment required")
    if annotations.orig_time is not None and annotations.orig_time != raw.info["meas_date"]:
        raise ValueError("Annotation clock differs from recording")
    duration = raw.n_times / raw.info["sfreq"]
    rows = normalize(zip(annotations.onset, annotations.duration, annotations.description), duration)
    report = summarize(rows)
    # Rows are annotation intervals, not necessarily fixed-length epochs.
    report["annotation_intervals"] = report.pop("epochs")
    report.update(dataset="Sleep-EDF Expanded 1.0.0", record="SC4001",
                  license=LICENSE, source="https://physionet.org/content/sleep-edfx/1.0.0/",
                  files=manifest, channels=raw.ch_names,
                  mne_version=mne.__version__, numpy_version=np.__version__,
                  matplotlib_version=matplotlib.__version__)
    first_sleep = next(r for r in rows if r["stage"] in ("N1", "N2", "N3", "REM"))
    start = first_sleep["start_seconds"]
    stop = min(start + 30, duration)
    channel = "EEG Fpz-Cz"
    values, times = raw.get_data(picks=[channel], start=round(start * raw.info["sfreq"]),
                                stop=round(stop * raw.info["sfreq"]), return_times=True)
    if not np.isfinite(values).all():
        raise ValueError("Non-finite EEG samples in preview")
    report["preview"] = {"channel": channel, "start_seconds": start,
                         "end_seconds": stop, "annotation_at_start": first_sleep["stage"],
                         "sample_rate_hz": raw.info["sfreq"], "filtered": False,
                         "finite_samples": True}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "summary.json").write_text(json.dumps(report, indent=2, allow_nan=False))
    with (args.output_dir / "annotations.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, axes = plt.subplots(2, 1, figsize=(12, 7))
    levels = {"W": 0, "REM": 1, "N1": 2, "N2": 3, "N3": 4, "UNKNOWN": 5}
    for row in rows:
        a = row["start_seconds"] / 3600
        b = a + row["duration_seconds"] / 3600
        axes[0].plot([a, b], [levels[row["stage"]]] * 2,
                     color="#999999" if row["stage"] == "UNKNOWN" else "#237e91", linewidth=2)
    axes[0].set(yticks=range(6), yticklabels=list(levels), ylim=(5.5, -0.5),
                xlabel="Horas desde el inicio del registro", title="Fases anotadas por expertos · registro completo")
    axes[0].axvspan(start / 3600, stop / 3600, color="#dc7e38", alpha=0.5)
    axes[1].plot(times - start, values[0] * 1e6, color="#253d62", linewidth=0.65)
    axes[1].set(xlabel="Segundos desde el inicio del fragmento", ylabel="EEG (µV)",
                title=f"{channel} · 30 s desde la primera fase de sueño · sin filtrar")
    for ax in axes:
        ax.grid(alpha=0.15)
    fig.suptitle("Primera exploración de EEG y sueño", fontsize=20, x=0.08, ha="left")
    fig.text(0.08, 0.025, "Sleep-EDF Expanded / PhysioNet · ODC-By 1.0 · SC4001\n"
             "Anotaciones R&K: 3 y 4 agrupadas en N3. Ejemplo de investigación; no diagnóstico.", fontsize=9)
    fig.tight_layout(rect=(0.02, 0.09, 1, 0.94), h_pad=2)
    fig.savefig(args.output_dir / "sleep_preview.png", dpi=160)
    plt.close(fig)
    print(json.dumps({k: report[k] for k in ("observed_minutes", "annotated_sleep_minutes", "stage_minutes")}, indent=2))


if __name__ == "__main__":
    main()
