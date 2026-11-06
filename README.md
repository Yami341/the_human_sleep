# The Human Sleep — plataforma de investigación
Investigación y desarrollo de herramientas reproducibles para estudiar sueño y señales fisiológicas. Proyecto independiente de Yami341, sin afiliación con The Human Sleep Project / BDSP.

**Estado:** fase inicial. No es un dispositivo médico ni un sistema validado de diagnóstico. Se ha importado y visualizado una grabación pública de Sleep-EDF; no se han entrenado modelos.

## Objetivo inicial
Construir una plataforma para investigadores que integre señales, anotaciones y calidad de datos. Primer objetivo experimental: caracterizar sueño y vigilia y comparar medidas con anotaciones de polisomnografía en adultos. EEG y señales cardiacas necesitan fuentes apropiadas; un reloj o anillo no mide EEG.

## Documentación
- [Investigación y fuentes](docs/INVESTIGACION.md)
- [Datos, permisos y estrategia de acceso](docs/DATOS.md)
- [Producto, validación y hoja de ruta](docs/PRODUCTO.md)
- [Primer piloto con EEG real y pasos para reproducirlo](docs/PILOTO_EEG.md)

## Primer componente ejecutable
Resumen descriptivo de anotaciones de sueño normalizadas en CSV, usando solamente la biblioteca estándar de Python 3.10 o superior:

```sh
python3 sleep_summary.py examples/synthetic_epochs.csv
python3 -m unittest discover -s tests -v
```

El ejemplo es sintético y de dos minutos: prueba el formato, no representa una noche ni evidencia clínica. La herramienta no clasifica señales ni diagnostica; resume etiquetas ya disponibles. Rechaza huecos, solapamientos y valores inválidos. No infiere eficiencia del sueño sin una ventana de tiempo en cama válida.

## Datos
No publicar EDF, ECG, exportaciones de Health, identificadores de participantes, tokens, datos clínicos ni modelos sujetos a restricciones en este repositorio público. Mantener datos en almacenamiento privado autorizado. Guardar aquí código, documentación, esquemas y ejemplos sintéticos.

No se otorga una licencia de software en esta fase; la decisión de licencia del proyecto queda pendiente. Las licencias de datos y herramientas externas son independientes.
