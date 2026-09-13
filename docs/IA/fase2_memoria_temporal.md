# Fase 2: Escalamiento y Memoria Temporal (Temporal Smoothing)

Este documento detalla el análisis de datos secuenciales y la propuesta técnica a futuro (Fase 2) para presentar ante el jurado. Es el argumento técnico que demuestra entendimiento profundo del ciclo industrial de Tenaris.

## 1. El Descubrimiento en los Datos (Takt Time)
Analizando el archivo de anotaciones crudo (`annotations.json`), descubrimos que las imágenes térmicas no son muestras aisladas, sino secuencias temporales del mismo mandril trabajando en la línea.

**Evidencia (Secuencia de 10 minutos):**
```json
{ "file_name": "15_07_2026_ImgPunta_17_52_31.png", "defects": [] }
{ "file_name": "15_07_2026_ImgPunta_17_53_14.png", "defects": [{"class": "Melted Body"}] }
{ "file_name": "15_07_2026_ImgPunta_17_53_48.png", "defects": [{"class": "Melted Body"}] }
{ "file_name": "15_07_2026_ImgPunta_17_54_24.png", "defects": [{"class": "Melted Body"}] }
...
{ "file_name": "15_07_2026_ImgPunta_18_03_50.png", "defects": [{"class": "Melted Body"}] }
{ "file_name": "15_07_2026_ImgPunta_18_04_36.png", "defects": [] }
```

**Conclusión Industrial:** 
El ciclo de laminación de un tubo ocurre aproximadamente cada **35 segundos**. En este caso documentado, el mandril operó roto ("Melted Body") durante más de 10 minutos (laminando unos 10-15 tubos defectuosos) antes de ser finalmente removido de la línea.

---

## 2. Limitación del MVP Actual
Actualmente, el MVP utiliza **YOLOv8** de forma aislada. Es un modelo espacial (analiza frame por frame) sin "memoria". Si un mandril tiene un defecto en el ciclo 1, el modelo evalúa el ciclo 2 como si fuera una pieza completamente nueva, sin contexto histórico.

---

## 3. Propuesta Técnica para Fase 2 (Roadmap)
Para el producto final, la arquitectura de IA no será solo espacial, sino **Espacio-Temporal**, incorporando técnicas de **Temporal Smoothing** y **Object Tracking** (ej. DeepSORT o ByteTrack).

### Beneficios Clave:
1. **Reducción drástica de Falsos Positivos:** Si aparece un artefacto en un solo frame (por humo o ruido del sensor infrarrojo), el sistema no dispara la alarma porque la anomalía no tiene persistencia temporal (no aparece en el frame siguiente).
2. **Contexto de Degradación:** Si la red detecta un desgaste leve en el ciclo 1, baja automáticamente su umbral de confianza para ese mismo mandril en el ciclo 2, priorizando el historial de la herramienta.
3. **Mantenimiento Predictivo Real:** Permite medir la *velocidad de crecimiento* del Bounding Box. Si el área defectuosa crece a un ritmo de X% por ciclo, el PLC puede predecir matemáticamente cuántos tubos más soporta antes del descarte, programando el cambio sin interrumpir la línea (cero tiempos muertos no planificados).

---

## 4. Guion Sugerido para el Pitch (QA con el Jurado)

> *"Analizando los datos crudos, descubrimos que las imágenes están correlacionadas cada ~35 segundos, lo que coincide con el Takt Time de la línea. Vimos casos donde un mandril roto laminó 10 tubos seguidos antes de ser descartado."*
>
> *"Nuestro MVP actual detecta cada foto de manera individual con alta precisión. Sin embargo, nuestro diseño para la Fase de Producción incorpora 'Temporal Smoothing'. Esto significa que la IA tendrá memoria: si una falla aparece en un solo ciclo, se ignora como humo o ruido. Si persiste y crece durante 3 ciclos, se dispara la alarma. Esto lleva los falsos positivos casi a cero y nos permite trazar una curva de degradación exacta para predecir la rotura mucho antes de que ocurra."*

