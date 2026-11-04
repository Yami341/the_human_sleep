# Investigación inicial
Fecha de consulta: 2026-11-04. Revisión exploratoria de fuentes primarias; no revisión sistemática ni validación clínica.

## Qué queremos medir
La **polisomnografía (PSG)** registra varias señales durante el sueño. EEG informa sobre actividad cerebral; ECG sobre actividad eléctrica cardiaca; EOG y EMG contribuyen a caracterizar fases. Respiración y oximetría aportan información que EEG y frecuencia cardiaca por sí solos no sustituyen.

| Pregunta | Alcance responsable del proyecto |
|---|---|
| Duración, fases y fragmentación | Caracterización y comparación con anotaciones expertas; identificar errores y datos ausentes. |
| Patrones compatibles con trastornos respiratorios | Línea posterior con eventos de referencia y señales respiratorias/SpO2 apropiadas. |
| Riesgo neurodegenerativo | Hipótesis exploratoria; exigir diagnóstico de referencia, seguimiento y validación externa. |
| TDAH (si esto era lo referido como TDH) | No asumir un marcador específico. Los trastornos del sueño pueden producir síntomas parecidos. |
| Necesidades nutricionales, déficits o “organismo óptimo” | No inferirlos de EEG/FC. Integrar análisis clínicos realmente medidos, contexto y evaluación profesional en una fase específica. |
| Todas las edades | Visión futura; modelos, referencias y validación diferenciados para infancia, adultos y mayores. |

El CDC explica que no existe una única prueba diagnóstica para TDAH y que otros problemas, incluidos los del sueño, pueden parecerse: [CDC](https://www.cdc.gov/adhd/signs-symptoms/index.html).
El diagnóstico de Alzheimer requiere una evaluación que puede incluir cognición, historia clínica, biomarcadores y neuroimagen; no queda demostrado por alteraciones inespecíficas de sueño o pulso: [NIH](https://health.nih.gov/health-topics-a-z/alzheimers-disease).

## Fuentes y precedentes
**The Human Sleep Project / BDSP** es el recurso identificado por la usuaria. El catálogo AWS describe PSG clínicas y el desarrollo de CAISR, que aborda fases, despertares y eventos respiratorios y motores. También plantea estudiar indicadores de salud cerebral. Eso expresa objetivos de investigación, no prueba que nuestro futuro producto pueda diagnosticar esas enfermedades. El catálogo menciona crecimiento futuro; no confundir esa previsión con volumen disponible actualmente.
Fuente: [AWS HSP](https://registry.opendata.aws/bdsp-hsp/).

**NSRR** reúne estudios de sueño, actigrafía, cuestionarios y variables clínicas. Permite plantear validación en cohortes independientes; la disponibilidad y permisos dependen del estudio.
Fuentes: [NSRR](https://sleepdata.org/about), [artículo del recurso](https://academic.oup.com/sleep/article/47/7/zsae088/7660531).

**Sleep-Accel** vincula frecuencia cardiaca y acelerometría de Apple Watch con etiquetas PSG. Es un precedente reproducible de investigación con wearable; no permite equiparar reloj con EEG ni validar detección de enfermedad en población general. Su muestra final es de 31 participantes y excluyó personas con apnea y trastorno de conducta REM.
Fuente: [PhysioNet](https://physionet.org/content/sleep-accel/1.0.0/).

## Oura y Apple Watch
Oura ofrece métricas nocturnas, frecuencia cardiaca y HRV mediante su API, sujetas a consentimiento y condiciones de acceso. Las series resumidas no equivalen a señal cruda ni a intervalos entre todos los latidos. Para múltiples usuarios se necesita una aplicación OAuth y aprobación para ampliar el límite inicial.
Fuentes: [métricas Oura](https://partnersupport.ouraring.com/hc/en-us/articles/28571089902227-Metrics-Available-via-the-Oura-API), [entrada oficial a API V2](https://cloud.ouraring.com/docs/).

Apple HealthKit es una posible integración con permiso individual; la página de autorización requiere JavaScript y no se pudo extraer íntegramente en esta revisión, por lo que la implementación y condiciones actuales quedan por verificar:
[Apple HealthKit](https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data).
Hay además datos públicos de Apple Watch en Sleep-Accel. Ninguna API supone acceso a la población completa de clientes de una marca.

No mezclar HRV RMSSD y SDNN, ni comparar métricas sin registrar algoritmo, ventana, unidades y dispositivo. No calcular HRV de intervalos RR a partir de promedios de frecuencia cardiaca.

## Posicionamiento propuesto
CAISR, las herramientas NSRR y la investigación Sleep-Accel demuestran que existe actividad comparable. Nuestra hipótesis de diferenciación es combinar trazabilidad, control de calidad, comparación entre dispositivos y análisis de cohortes reproducible. No se ha realizado todavía un estudio exhaustivo de competidores, patentes ni demanda.
