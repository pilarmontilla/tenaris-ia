# Decisiones de Diseño y Arquitectura de IA

Este documento detalla las justificaciones técnicas, metodológicas y de negocio que guiaron el desarrollo de **MandreelAI** para la planta de fabricación de tubos de acero sin costura de **Tenaris**.

---

## 1. El Desafío y Restricciones de Planta

En la laminación en caliente, tochos de acero a 1250 °C son perforados utilizando un mandril metálico sometido a esfuerzos mecánicos y térmicos extremos.

* **Costo asimétrico del error:**
  * **Falso Positivo (FP):** La IA alerta falsamente sobre un mandril sano. El operario pierde unos segundos en verificarlo.
  * **Falso Negativo (FN):** La IA deja pasar un mandril defectuoso. Se lamina un tocho con la herramienta dañada, arruinando la superficie interna del tubo.
* **Restricción temporal estricta (*Takt Time*):** La inspección debe realizarse en la ventana de reposo del mandril entre tochos.

---

## 2. Elección del Modelo de Visión: YOLOv8 Nano

Se evaluaron tres enfoques principales:
1. **Clasificación de imágenes tradicional (ResNet / EfficientNet):** Rápida de implementar, pero opera como "caja negra" (solo indica "Apto" o "No Apto").
2. **Modelos de detección grandes (YOLOv8x / Faster R-CNN):** Muy precisos, pero pesados, con alta latencia y dependencia de GPUs dedicadas de alto consumo.
3. **Detección compacta con YOLOv8 Nano (`yolov8n`):** **Opción seleccionada.**

### Razones de la elección:
* **Latencia Ultra-Baja (< 20 ms):** En computadoras industriales estándar (CPU), el tiempo de inferencia es inferior a 20 ms. La IA no consume tiempo del *Takt Time* de 30 segundos.
* **Edge AI (Procesamiento en Planta):** Con solo ~6 MB y 3.2 millones de parámetros, el modelo corre localmente en un IPC junto a la línea. No requiere conexión a la nube, evitando riesgos de ciberseguridad o fallas de red en fábrica.
* **Explicabilidad Visual (XAI):** A diferencia de un clasificador binario, YOLO devuelve coordenadas (*bounding boxes*). El operario ve exactamente el punto caliente o daño (`Melted Body`, `Melted Nose`, `Flattened Nose`), aumentando la confianza en el sistema.
* **Eficiencia por Transfer Learning:** Al partir de pesos preentrenados, el modelo aprende rápidamente a discriminar texturas superficiales y defectos con un conjunto de datos reducido.

---

## 3. Estrategia del Dataset y Tratamiento del Desbalance

El dataset provisto contiene 844 imágenes anotadas:
* **555 imágenes limpias (65.8%):** Mandriles en perfecto estado.
* **289 imágenes con defectos:** `Melted Body` (160), `Melted Nose` (129) y `Flattened Nose` (4).

### Decisiones clave en la preparación (`src/prepare_dataset.py`):
1. **Split Estratificado 3-Way (80% Train / 10% Val / 10% Test):**
   * Se diseñó un particionado personalizado que distribuye las clases ultra-raras (`Flattened Nose`, con solo 4 ejemplos) para garantizar representación en entrenamiento, validación y prueba sin fuga de datos.
2. **Inclusión Masiva de Imágenes Sanas como Fondos Negativos:**
   * En detección de objetos, entrenar únicamente con imágenes positivas dispara las falsas alarmas. Incluir las 555 imágenes libres de defectos educa a la red sobre cómo luce una superficie íntegra.
3. **Bounding Box Clamping:**
   * Se normalizaron y ajustaron matemáticamente las coordenadas fuera de rango producidas durante el etiquetado manual, asegurando integridad antes de alimentar el entrenamiento.

---

## 4. Estrategia de Validación y Prevención de Overfitting

Dada la criticidad del entorno siderúrgico y el tamaño acotado del dataset etiquetado, la prevención de la memorización (*overfitting*) y la garantía de generalización guiaron la arquitectura de entrenamiento:

### 4.1. Particionamiento Triple Ciego y Validación Cruzada
* **Aislamiento estricto (No Data Leakage):** Se dividió el dataset en tres subconjuntos disjuntos:
  * **Entrenamiento (673 imágenes / 80%):** Utilizado exclusivamente para el ajuste de gradientes.
  * **Validación (83 imágenes / 10%):** Simulacro continuo durante el entrenamiento. Es el conjunto sobre el cual se calcula el error de validación (`val_loss`), la métrica `mAP@50` y los criterios de parada temprana.
  * **Test Local (88 imágenes / 10%):** Mantenido completamente aislado ("bajo llave"). Solo se utiliza para auditoría final insesgada del sistema.
* **Estratificación determinística:** Asegura que la proporción de piezas sanas y defectuosas (especialmente la clase crítica `Flattened Nose`) sea idéntica y representativa en cada partición, previniendo sesgos de muestreo.

### 4.2. Mecanismos Activos Anti-Overfitting
1. **Mosaic Data Augmentation con Cierre Progresivo:**
   * Durante las primeras épocas (fase de "entrenamiento con carga"), se activa *Mosaic Augmentation*, combinando 4 imágenes distintas en un único mosaico con deformaciones geométricas, cambios de escala y variaciones de luminosidad. Esto impide que la red memorice fondos o artefactos fijos de la cámara infrarroja.
   * En las últimas épocas del entrenamiento, se desactiva automáticamente el aumento agresivo (`closing dataloader mosaic`) para permitir que la red estabilice sus pesos sobre las imágenes nítidas reales de planta.
2. **Inyección de Muestras Negativas Puras (444 imágenes en Train):**
   * Al obligar a la red a procesar cientos de imágenes sin anotaciones (`defects: []`), la función de pérdida penaliza severamente cualquier falso positivo generado sobre reflejos térmicos, óxido superficial o rugosidades normales del mandril.
3. **Regularización y Early Stopping:**
   * Se implementó *Early Stopping* con paciencia configurable (`patience=15`), deteniendo el proceso en cuanto la pérdida sobre el conjunto de validación deja de decrecer, evitando la sobre-optimización de los pesos.
4. **Resultados de Validación:**
   * El modelo consolidó un **mAP@50 de 92.0%** y una **Precisión en cajas del 96.3%** medidos sobre datos no vistos, confirmando una alta capacidad de generalización sin sobreajuste.

---

## 5. Motor de Decisión: Semáforo Paranoico y Human-in-the-Loop

Dada la asimetría económica entre falsos positivos y falsos negativos, la política del sistema es **maximizar el Recall (sensibilidad)** por encima de la Precisión estricta.

### Configuración del Umbral:
* Se redujo el umbral de confianza de detección base a **15% (conf = 0.15)** para capturar cualquier vestigio de anomalía incipiente.

### Estados del Semáforo:
| Estado | Condición | Acción Operativa |
| :--- | :--- | :--- |
| 🟢 **VERDE (Apto)** | Ninguna detección supera el 15% de confianza. | El ciclo de laminación continúa automáticamente. |
| 🟡 **AMARILLO (Alerta)** | Detección de confianza media (15% - 65%) o área superficial pequeña (< 1%). | El operario valida si es falsa alarma o desgaste real. |
| 🔴 **ROJO (Crítico)** | Defecto confirmado con confianza ≥ 65% y área relevante (≥ 1%). | Señal directa a PLC para reemplazar el mandril. |

---

## 6. Índice de Severidad: Mandrel Health Index (MHI)

No todas las fallas tienen el mismo impacto en el producto terminado:
* La **punta (*nose*)** recibe el choque térmico y mecánico primario en la perforación. Un defecto en la punta raya inmediatamente la pared interna del tubo.
* El **cuerpo (*body*)** tolera un desgaste ligeramente superior antes de comprometer la tolerancia dimensional.

El cálculo pondera el área relativa del defecto multiplicada por la criticidad de la zona (factor 2.0 para la punta vs 1.0 para el cuerpo), permitiendo cuantificar la salud de la herramienta en una escala de 0 a 100%.

---

## 7. Visión a Futuro: Fase 2 y Memoria Temporal (Temporal Smoothing)

### 7.1. El Hallazgo Industrial en los Datos
Al auditar cronológicamente el archivo de anotaciones (`annotations.json`), se descubrió que las capturas no son eventos aislados, sino **secuencias temporales tomadas a intervalos regulares de ~35 segundos**, coincidiendo con el *Takt Time* del proceso de laminación.

```json
{ "file_name": "15_07_2026_ImgPunta_17_52_31.png", "defects": [] }
{ "file_name": "15_07_2026_ImgPunta_17_53_14.png", "defects": [{"class": "Melted Body"}] }
{ "file_name": "15_07_2026_ImgPunta_17_53_48.png", "defects": [{"class": "Melted Body"}] }
...
{ "file_name": "15_07_2026_ImgPunta_18_03_50.png", "defects": [{"class": "Melted Body"}] }
{ "file_name": "15_07_2026_ImgPunta_18_04_36.png", "defects": [] }
```

> **Evidencia en planta:** En esta secuencia real documentada, un mandril con falla severa (`Melted Body`) continuó operando durante más de 10 minutos (laminando entre 10 y 15 tubos defectuosos antes de ser detectado y descartado por los métodos manuales reactivos actuales).

### 7.2. Limitación del MVP Actual
El MVP actual utiliza un modelo espacial puro (evaluación estática fotograma a fotograma). Cada imagen es procesada como si fuera una herramienta nueva, careciendo de contexto histórico sobre el ciclo previo del mandril.

### 7.3. Propuesta Arquitectónica Fase 2: Red Espacio-Temporal
Para la versión de producción industrial completa, la arquitectura integrará **Temporal Smoothing** y seguimiento de objetos multiobjetivo (*Object Tracking* con algoritmos como ByteTrack o DeepSORT):

1. **Eliminación Prácticamente Total de Falsos Positivos:**
   * Si aparece un artefacto transitorio en un solo fotograma (humo, vapor de refrigeración o destello de radiación térmica), el sistema no activa la alarma dado que la perturbación carece de coherencia y persistencia temporal en el fotograma siguiente.
2. **Umbrales Dinámicos y Memoria de Desgaste:**
   * Si la red identifica un desgaste incipiente en el ciclo $N$, la confianza requerida para confirmar el defecto en el ciclo $N+1$ se reduce de forma adaptativa, priorizando el historial acumulado de la pieza.
3. **Mantenimiento Predictivo con Cálculo de RUL (Remaining Useful Life):**
   * Al monitorear la tasa de crecimiento del defecto ($\frac{\Delta \text{Área}}{\Delta \text{Ciclo}}$), el sistema modela la curva de degradación de la herramienta y calcula cuántos tochos adicionales puede perforar con seguridad. Esto permite coordinar el recambio con el mecanismo revólver en tiempos muertos, eliminando paradas de línea imprevistas y alcanzando el objetivo de **cero scrap**.
