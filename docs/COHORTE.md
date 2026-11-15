# Piloto EEG de cinco personas

Se selecciona de forma determinista la primera noche de SC400–SC404. Es una muestra de conveniencia para verificar el procesamiento, no para estimar rendimiento clínico ni representar una población.

```sh
MPLCONFIGDIR=.cache/matplotlib .venv/bin/python cohort_pilot.py --data-dir data/private/sleep-edf --output-dir reports/local-pilot/cohort
.venv/bin/python -m unittest discover -s tests -v
```

Requiere las dependencias de requirements-pilot.txt. Descarga una pareja PSG/hipnograma por participante, verifica hashes y reutiliza las descargas válidas. Genera INFORME.md, comparacion.png y un JSON detallado por registro más cohort.json. Los resultados individuales permanecen locales.

## Control de calidad exploratorio

Se inspeccionan ambos canales EEG en ventanas no solapadas de 30 s; la última ventana parcial cuenta según su duración real. Se marca cualquier ventana con valores no finitos, rango pico a pico menor de 1 µV o amplitud absoluta superior a 200 µV. Estos umbrales son decisiones iniciales de ingeniería, no límites fisiológicos ni criterios clínicos validados.

El porcentaje marcado es la duración de la unión de ventanas marcadas dividida por duración registrada. También se calcula la intersección exacta con intervalos de sueño anotado, usando el tiempo de sueño como denominador. Los canales ausentes se registran explícitamente.

Las marcas son candidatas a inspección manual: no se descartan datos automáticamente ni se recalculan las fases expertas. No detectamos todos los tipos de artefacto, saturación o desconexión; señal sin marcas no significa señal libre de artefactos. La vigilia extensa puede influir en los porcentajes globales.

## Validación y límites

Pruebas con seno limpio, señal plana, NaN, pico de amplitud, ventanas parciales e inputs inválidos, además de las pruebas previas de anotaciones. Sin clasificador entrenado, sin estimación diagnóstica y sin análisis cardiaco. La detección de artefactos debe contrastarse con revisión humana antes de utilizarla como criterio de exclusión.

Datos: [Sleep-EDF Expanded](https://physionet.org/content/sleep-edfx/1.0.0/), [ODC-By 1.0](https://physionet.org/content/sleep-edfx/view-license/1.0.0/). Kemp et al. (2000), DOI 10.1109/10.867928; Pollard et al. (2026), DOI 10.1038/s44360-026-00096-z.
