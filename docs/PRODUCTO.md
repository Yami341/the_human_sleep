# Producto y protocolo inicial
Propuesta de trabajo, pendiente de entrevistas y colaboración clínica.

## Primer producto
Plataforma de investigación para equipos universitarios y laboratorios: importar registros autorizados, inspeccionar calidad, visualizar señales/anotaciones, extraer medidas reproducibles y comparar cohortes. Posteriormente, evaluar servicios para farmacéuticas orientados a medidas exploratorias en estudios. No prometer un marcador válido para decisiones de ensayo sin validación y acuerdos específicos.

La comercialización inicial podría ser licencia de software, despliegue privado y soporte analítico. No vender registros de participantes. La demanda, precios y disposición a pagar todavía no están validados.

## Primer experimento
Pregunta: ¿podemos reproducir medidas descriptivas y un baseline sueño/vigilia en adultos con etiquetas PSG y trazabilidad completa?
- Rama EEG: Sleep-EDF con reglas de etiquetas explícitas.
- Rama wearable: Sleep-Accel, validada por separado.
- Rama cardiaca posterior: Apnea-ECG; no combinar estas personas con las de EEG.
- No extrapolar a infancia ni a Alzheimer/TDAH.

## Hoja de ruta por entregables
1. **Fundación (esta entrega):** investigación, catálogo, límites, protocolo y resumen de anotaciones CSV con ejemplo sintético.
2. **Ingesta:** seleccionar fuente y versión con permisos; lectores EDF/WFDB o tablas; hashes, canales, unidades y calidad. Criterio: reproducción de un lote pequeño sin pérdida silenciosa.
3. **Exploración:** hipnograma, espectro EEG, frecuencia cardiaca y artefactos cuando existan señales adecuadas. Mostrar ausencias, no inventarlas. Criterio: revisión manual de ejemplos y cotejo con anotaciones.
4. **Baseline:** clasificador sencillo y comparación reproducible; mantener al sujeto completo en un único conjunto. Criterio: informe con intervalos de confianza y resultados por persona, no sólo por ventana.
5. **Validación externa:** segundo centro/cohorte, diferencias de edad, sexo, comorbilidad y dispositivo. Criterio: análisis de errores y límites antes de afirmar utilidad.
6. **Piloto institucional:** entrevistas con 3–5 equipos, protocolo compartido, derechos de uso y revisión clínica. Criterio: problema concreto y colaboración verificable.
7. **Ampliaciones:** datos longitudinales, laboratorio y biomarcadores neurológicos sólo si existen etiquetas y vínculos adecuados. Pediatría como protocolo separado.

## Diseño del sistema propuesto
Almacenamiento privado de señales → lectores por fuente → control de calidad y sincronización → características versionadas → análisis/modelos → informe reproducible.
GitHub conserva código y documentación. Entornos y controles de acceso separan participantes, proyectos y acuerdos. Un futuro panel puede mostrar señales, cobertura, procedencia y limitaciones.

Primera versión local en Python. Selección de librerías de señales, backend, panel y nube pendiente de pruebas de ingesta; no necesita infraestructura AWS para comenzar.

## Validación
- División por sujeto, con todas sus noches juntas; detectar duplicados y fugas.
- Ajustar normalización y parámetros únicamente con entrenamiento.
- Separar validación para ajustar modelos y prueba final intacta; luego cohorte externa.
- Fases: macro-F1, matriz de confusión, kappa y error en duración; no sólo exactitud.
- Eventos futuros: sensibilidad, precisión, falsas alarmas por noche y calibración cuando se emitan probabilidades.
- Intervalos de confianza con remuestreo por sujeto; documentar selección y exclusiones.
- Comparar con un baseline simple. Predefinir umbrales de aceptación con el equipo clínico.
- Controlar edad, medicamentos, apnea, centro y hardware antes de interpretar asociaciones neurológicas.
- Para progresión de enfermedad: etiquetas diagnósticas independientes, seguimiento temporal y prueba prospectiva.
- Para probar beneficio de una intervención: asociación observacional no basta para establecer causalidad.

## Datos clínicos y población
Integración futura de resultados realmente medidos con unidades, laboratorio, fecha y contexto. No deducir déficits nutricionales de sueño/FC ni producir recomendaciones de suplementos con el prototipo.
En pediatría se requieren datos y criterios específicos, revisión ética y permisos aplicables; entrenar en adultos no valida niños.

## Marco para comercialización
Definir primero finalidad prevista, usuario y decisiones que apoyará. En la UE, una finalidad médica puede hacer aplicable MDR/IVDR; llamarlo “investigación” no resuelve por sí solo su clasificación. Se necesitará evaluación regulatoria para la función concreta antes de comercializarla como diagnóstico.
Fuente: [MDCG 2019-11 rev.1, junio 2025](https://health.ec.europa.eu/document/download/b45335c5-1679-4c71-a91c-fc7a4d37f12b_en?filename=md_mdcg_2019_11_guidance_qualification_classification_software_en.pdf).

Antes de incorporar participantes, concretar consentimiento o base jurídica aplicable, custodia, acceso, retención y acuerdos de tratamiento. Este documento no determina una clasificación regulatoria ni sustituye esa evaluación.

## Pendiente de decidir
País del primer mercado, colaboración con unidad de sueño, población inicial concreta, presupuesto y licencia de nuestro software. No se han iniciado contactos con instituciones ni contratado servicios.
