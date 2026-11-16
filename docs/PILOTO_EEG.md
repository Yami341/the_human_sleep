# Primer piloto EEG — 6 de noviembre de 2026

Se importó una pareja PSG/hipnograma pública de Sleep-EDF Expanded 1.0.0 (SC4001). El descargador verifica SHA-256 contra el listado de PhysioNet y reutiliza archivos locales sólo si coinciden. Descarga aproximadamente 48,4 MB, no toda la base.

## Reproducir

Probado con Python 3.15. Las dependencias del piloto son independientes del resumen CSV que sólo requiere biblioteca estándar.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements-pilot.txt
MPLCONFIGDIR=.cache/matplotlib .venv/bin/python sleep_edf_pilot.py --data-dir data/private/sleep-edf --output-dir reports/local-pilot
.venv/bin/python -m unittest discover -s tests -v
```

El comando descarga dos EDF, el listado de hashes y una copia HTML de la licencia. Produce summary.json, annotations.csv y sleep_preview.png. Conservar estos resultados localmente; esta PR no publica las señales ni anotaciones individuales.

## Resultado descriptivo observado

Registro de 1.325 minutos (22 h 5 min), con 326,5 minutos etiquetados como sueño. Contiene también largos períodos de vigilia; dividir sueño entre toda la grabación **no es eficiencia del sueño**. No disponemos aquí de una ventana validada de tiempo en cama.

Se leyeron dos canales EEG y otros canales de la grabación. No hay ECG en este registro: no se calcula frecuencia cardiaca ni HRV. La figura muestra el hipnograma completo y 30 segundos de EEG Fpz-Cz sin filtrar, desde la primera anotación de sueño.

Son etiquetas expertas existentes, no predicciones del prototipo. No se puede inferir enfermedad, calidad clínica del sueño ni rendimiento poblacional a partir de este ejemplo.

## Decisiones de procesamiento y verificación

- Lectura con MNE, manteniendo las señales en disco; conversión de voltios a µV para la figura.
- Verificación de fecha y hora de inicio de ambos encabezados EDF. MNE devuelve orig_time=None para estas anotaciones; no se inventa una fecha ni se desplazan las señales.
- Recorte de anotaciones al intervalo real de señal. R&K 3/4 se agrupan en N3 y se conserva original_label; movimiento, no puntuado y huecos son UNKNOWN.
- Rechazo de etiquetas desconocidas, solapamientos y valores no finitos. Comprobación de muestras finitas en el fragmento mostrado; esto no es detección completa de artefactos.
- Diez pruebas unitarias correctas y ejecución de integración con los dos archivos reales. Figura inspeccionada visualmente.

## Procedencia y licencia

Contiene información de [Sleep-EDF Expanded, PhysioNet](https://physionet.org/content/sleep-edfx/1.0.0/), disponible bajo [ODC Attribution License v1.0](https://physionet.org/content/sleep-edfx/view-license/1.0.0/).

Kemp B, Zwinderman AH, Tuk B, Kamphuisen HAC, Oberyé JJL. Analysis of a sleep-dependent neuronal feedback loop: the slow-wave microcontinuity of the EEG. IEEE-BME 47(9):1185–1194 (2000). DOI: 10.1109/10.867928.
PhysioNet: Pollard et al. (2026), PhysioNet as a global platform for biomedical research. DOI: 10.1038/s44360-026-00096-z.

La licencia permite uso de la base con atribución, incluido comercial, dentro de los derechos que cubre. No concede por sí sola derechos de marca, patentes ni otros derechos sobre contenidos. Esta comprobación habilita el piloto documentado; no constituye aprobación de un producto clínico.

Siguiente paso: inspección de calidad por canal y ampliación a varias personas antes de desarrollar un baseline de clasificación.
