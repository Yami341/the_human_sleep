# Catálogo y acceso
Revisión inicial: 2026-11-04. “Público”, “gratuito” y “autorizado para un producto comercial” son propiedades diferentes.

| Recurso | Utilidad | Acceso/licencia observada | Decisión inicial |
|---|---|---|---|
| [HSP / BDSP](https://registry.opendata.aws/bdsp-hsp/) | PSG clínicas, investigación de sueño y salud cerebral | Catálogo AWS enlaza licencia restringida; política BDSP vigente limita su vía de investigación a uso no comercial | No descargar ni entrenar para producto sin acuerdo apropiado |
| [Sleep-EDF Expanded 1.0.0](https://physionet.org/content/sleep-edfx/1.0.0/) | EEG/EOG y anotaciones de fases | Acceso abierto; texto de licencia debe registrarse antes de importar | Piloto EEG pequeño |
| [Apnea-ECG 1.0.0](https://physionet.org/content/apnea-ecg/1.0.0/) | ECG y etiquetas de apnea | Open Data Commons Attribution v1.0 en la ficha | Piloto cardiaco separado, con atribución y revisión de términos |
| [Sleep-Accel 1.0.0](https://physionet.org/content/sleep-accel/1.0.0/) | Wearable con etiquetas PSG | Open Data Commons Attribution v1.0 en la ficha | Primera comparación wearable/PSG |
| [NSRR](https://sleepdata.org/about) | Cohortes PSG y variables clínicas | Acceso individual sujeto al acuerdo de cada conjunto | Elegir cohorte externa tras revisar diccionario y acuerdo |
| [NCH Sleep DataBank](https://arxiv.org/abs/2102.13284) | Extensión pediátrica con datos clínicos | Solicitud y condiciones por verificar antes de usar | Fase pediátrica independiente |

Sleep-EDF contiene 197 registros y anotaciones históricas R&K; documentar conversión de fases 3/4 a N3, conservar etiquetas originales y excluir movimiento/no puntuado del denominador puntuable. No asumir que incluye ECG porque sea un conjunto de sueño.

Apnea-ECG documenta errores en anotaciones QRS automáticas y registros c05/c06 procedentes de la misma grabación: agrupar o eliminar duplicación antes de dividir entrenamiento/prueba. No tratar diferentes nombres de archivo como personas independientes.

## Restricción determinante para HSP
La [política BDSP de acceso no comercial](https://www.bdsp.io/about/noncommercial-access-policy/), actualizada el 13-10-2026, prohíbe desarrollo/validación de productos y otros usos comerciales bajo esa vía. Solicita contactar por separado para otros acuerdos. El catálogo AWS distingue resúmenes sin restricción de señales sujetas a licencia: no extender permisos de los resúmenes a registros individuales.

Una colaboración universitaria no convierte automáticamente un proyecto comercial en investigación no comercial. No solicitar acceso con una finalidad distinta de la real.

## Acceso escalonado y costes
1. Registrar versión, URL, licencia, alcance autorizado, fecha de aprobación y responsable.
2. Revisar diccionario, población, señales, frecuencias de muestreo y etiquetas.
3. Seleccionar 5–10 registros elegibles para validar lectura y calidad; esto no alcanza para validar rendimiento clínico.
4. Descargar únicamente archivos seleccionados en almacenamiento privado; comprobar tamaños y hashes.
5. Medir tiempo, RAM y almacenamiento por noche. Estimar coste total antes de escalar.
6. Considerar procesamiento cercano a S3 sólo cuando los términos permitan ese entorno; no iniciar infraestructura de pago ni una sincronización completa por defecto.

No se ha descargado ningún registro de pacientes en esta entrega. No se ha comprobado acceso efectivo al bucket HSP ni el tamaño actual total.

## Manifiesto previsto
Por registro: dataset, versión, sujeto seudónimo local, sesión, ruta privada, checksum, señales, unidades, frecuencia de muestreo, duración, fuente de anotación, licencia/acuerdo y estado de calidad. El manifiesto individual también puede estar sujeto a restricciones: no publicarlo automáticamente.

Nunca emparejar personas de bases independientes como si fueran el mismo sujeto. Para asociar EEG, ECG, laboratorio y diagnóstico, exigir vínculo permitido y verificable dentro de la misma cohorte.
