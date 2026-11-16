"""Five distinct Sleep-EDF participants, first night only; descriptive pilot."""
import argparse
import json
from pathlib import Path
import mne
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sleep_edf_pilot import download, normalize, LICENSE
from sleep_summary import summarize
from eeg_quality import scan, WINDOW_SECONDS, FLAT_RANGE_UV, HIGH_ABSOLUTE_UV

PAIRS = [("SC4001E0-PSG.edf", "SC4001EC-Hypnogram.edf"),
         ("SC4011E0-PSG.edf", "SC4011EH-Hypnogram.edf"),
         ("SC4021E0-PSG.edf", "SC4021EH-Hypnogram.edf"),
         ("SC4031E0-PSG.edf", "SC4031EC-Hypnogram.edf"),
         ("SC4041E0-PSG.edf", "SC4041EC-Hypnogram.edf")]
CHANNELS = ("EEG Fpz-Cz", "EEG Pz-Oz")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    reports = []
    for pair in PAIRS:
        record = pair[0][:6]
        print("Processing " + record, flush=True)
        manifest = download(args.data_dir, pair)
        with (args.data_dir / pair[0]).open("rb") as a, (args.data_dir / pair[1]).open("rb") as b:
            a.seek(168)
            b.seek(168)
            if a.read(16) != b.read(16):
                raise ValueError("Source clocks differ: " + record)
        raw = mne.io.read_raw_edf(args.data_dir / pair[0], preload=False, verbose="ERROR")
        ann = mne.read_annotations(args.data_dir / pair[1])
        if ann.orig_time is not None and ann.orig_time != raw.info["meas_date"]:
            raise ValueError("Annotation clock differs")
        rows = normalize(zip(ann.onset, ann.duration, ann.description), raw.n_times / raw.info["sfreq"])
        summary = summarize(rows)
        summary["annotation_intervals"] = summary.pop("epochs")
        quality = {}
        for channel in CHANNELS:
            if channel not in raw.ch_names:
                quality[channel] = {"status": "missing_channel"}
                continue
            result = scan(raw.get_data(picks=[channel])[0] * 1e6, raw.info["sfreq"])
            # Attribute exact overlap of flagged windows to annotated sleep.
            sleep_rows = [r for r in rows if r["stage"] in ("N1", "N2", "N3", "REM")]
            overlap = sum(max(0, min(w["start_seconds"] + w["duration_seconds"],
                                    r["start_seconds"] + r["duration_seconds"]) -
                               max(w["start_seconds"], r["start_seconds"]))
                          for w in result["windows"] if w["flagged"] for r in sleep_rows)
            sleep_seconds = summary["annotated_sleep_minutes"] * 60
            result["flagged_sleep_percent"] = 100 * overlap / sleep_seconds if sleep_seconds else None
            result["status"] = "scanned"
            quality[channel] = result
        report = {"record": record, "participant": pair[0][:5], "files": manifest,
                  "summary": summary, "quality": quality}
        reports.append(report)
        (args.output_dir / (record + ".json")).write_text(json.dumps(report, indent=2, allow_nan=False))
    metadata = {"dataset": "Sleep-EDF Expanded 1.0.0", "license": LICENSE,
                "selection": "First night, participants SC400-SC404; convenience sample",
                "thresholds": {"window_seconds": WINDOW_SECONDS, "flat_range_uv_below": FLAT_RANGE_UV,
                               "absolute_amplitude_uv_above": HIGH_ABSOLUTE_UV},
                "versions": {"mne": mne.__version__, "numpy": np.__version__, "matplotlib": matplotlib.__version__},
                "reports": reports}
    (args.output_dir / "cohort.json").write_text(json.dumps(metadata, indent=2, allow_nan=False))
    lines = ["# Piloto comparativo: cinco personas", "", "Una primera noche por persona; muestra de conveniencia, no representativa.", "",
             "| Registro | Registro (h) | Sueño anotado (min) | EEG frontal marcado (%) | EEG posterior marcado (%) |",
             "|---|---:|---:|---:|---:|"]
    for r in reports:
        def pct(c):
            q = r["quality"][c]
            return f'{q["flagged_percent"]:.2f}' if q["status"] == "scanned" else "ausente"
        s = r["summary"]
        lines.append(f'| {r["record"]} | {s["observed_minutes"]/60:.2f} | {s["annotated_sleep_minutes"]:.1f} | {pct(CHANNELS[0])} | {pct(CHANNELS[1])} |')
    lines += ["", "Los porcentajes de señal marcada corresponden a toda la grabación, incluida vigilia. Los JSON incluyen también el porcentaje dentro del sueño anotado.",
              "", "## Interpretación y límites", "",
              "Se marcan ventanas de 30 s si contienen valores no finitos, rango inferior a 1 µV o amplitud absoluta superior a 200 µV. Son umbrales exploratorios elegidos para revisión manual, no criterios clínicos validados. Una marca no demuestra artefacto; no se eliminan ventanas ni se corrigen las anotaciones expertas.",
              "No se detectan todos los artefactos, desconexiones ni saturaciones. Una señal finita o sin marcas no garantiza calidad. Los valores ausentes codificados como constantes pueden generar una marca plana, pero no permiten determinar la causa.",
              "La duración registrada incluye vigilia extensa: no interpretar sueño/registro como eficiencia del sueño. Las fases son anotaciones existentes, con R&K 3/4 agrupadas en N3. No hay diagnóstico ni modelo entrenado.",
              "", "## Procedencia", "",
              "Contiene información de [Sleep-EDF Expanded / PhysioNet](https://physionet.org/content/sleep-edfx/1.0.0/), bajo [ODC-By 1.0](" + LICENSE + "). Archivos verificados con SHA-256; hashes y versiones en cohort.json.",
              "Kemp et al. (2000), DOI 10.1109/10.867928; Pollard et al. (2026), DOI 10.1038/s44360-026-00096-z."]
    (args.output_dir / "INFORME.md").write_text("\n".join(lines) + "\n")
    fig, ax = plt.subplots(figsize=(10, 5))
    bottom = np.zeros(len(reports))
    for stage, color in zip(("N1", "N2", "N3", "REM"), ("#a6c9e2", "#4596b8", "#244663", "#df9e61")):
        values = np.array([r["summary"]["stage_minutes"][stage] for r in reports])
        ax.bar([r["record"] for r in reports], values, bottom=bottom, label=stage, color=color)
        bottom += values
    ax.set(ylabel="Minutos anotados", title="Sueño anotado · cinco personas, una noche por persona")
    ax.legend(ncol=4, frameon=False)
    fig.text(0.1, 0.02, "Sleep-EDF / PhysioNet · ODC-By 1.0 · Fases expertas, no predicciones ni diagnóstico", fontsize=9)
    fig.tight_layout(rect=(0, .06, 1, 1))
    fig.savefig(args.output_dir / "comparacion.png", dpi=150)
    plt.close(fig)
    print("Completed five records", flush=True)


if __name__ == "__main__":
    main()
