# MandrelGuard AI: Primer Enfoque y Arquitectura del MVP

## 1. Resumen Ejecutivo y Objetivo
El objetivo de este MVP es transformar la inspección del **mandril** —herramienta crítica en la laminación en caliente de tubos sin costura en Tenaris— de un control visual reactivo y manual a un **sistema proactivo de visión computacional en tiempo real**.

La solución busca:
- Eliminar el scrap generado por mandriles defectuosos (actualmente entre el **5% y 10%** de la producción).
- Evitar costos directos asociados (\$1500 USD/tonelada, pérdida de energía térmica en hornos y demoras de entrega / *lead time*).
- Automatizar la toma de decisiones dentro de la **ventana operativa de 30 segundos** (*Takt Time* entre tochos), integrándose con el mecanismo de recambio rápido tipo "revólver" de la planta.

---

## 2. Filosofía del MVP: "Lean & Scalable" (Simple, Seguro y Escalable)
Dado que hay tiempo y recursos limitados para múltiples iteraciones de entrenamiento, el diseño técnico se rige por estas reglas:
1. **Cero Complejidad en el Entrenamiento:** No tocaremos arquitecturas internas ni funciones de pérdida raras. Usaremos **YOLOv8 estándar** "out-of-the-box", que es robusto y perdona errores. Todo el valor agregado industrial se calculará *después* de la predicción.
2. **Preparación de Datos a Prueba de Balas:** El 90% del éxito estará en cómo armamos el dataset (el script de partición garantizará que la clase rara `Flattened Nose` no se pierda, y que las 555 imágenes limpias enseñen al modelo a no dar falsas alarmas).
3. **Escalabilidad Modular:** El código se separará limpiamente: un script para preparar datos, un script de 3 líneas para entrenar, y un script de inferencia. Si a futuro Tenaris pide sumar cámaras térmicas, solo se cambia el dataset, no toda la lógica del negocio.

### 2.1. Arquitectura Desacoplada (El MVP)
```
[ Dataset Crudo ] ──(Script Seguro de Split)──► [ YOLO Format ]
                                                       │
                                                       ▼
[ Inferencia YOLOv8 ] (< 20 ms) ◄──(Entrenamiento Rápido Standard)
         │
         ▼
[ Motor de Severidad: MHI ] ──────► Cálculo matemático simple post-YOLO
         │
         ▼
[ Semáforo Operativo / Human-in-the-Loop ]
   ├── VERDE: Apto
   ├── AMARILLO: Alerta a Operario
   └── ROJO: Descarte PLC
```

### 2.1. El Motor de IA: YOLOv8 Nano (Argumentos para el Pitch)
Para el núcleo de detección, seleccionamos la arquitectura **YOLOv8 versión Nano** (You Only Look Once). Ante un jurado de ingenieros, la elección de este modelo específico se defiende con estos 4 pilares técnicos y de negocio:

1. **Velocidad y Takt Time (Latencia Cero):** El proceso siderúrgico impone una ventana de tiempo muerto de apenas 30 segundos. YOLOv8 procesa la imagen e infiere el resultado en **menos de 20 milisegundos**. La IA jamás será un cuello de botella en la línea.
2. **Factibilidad de Hardware (Edge Computing):** La versión "Nano" pesa apenas ~6 MB y tiene 3.2 millones de parámetros. Esto significa que **no requiere enviar datos a la nube** (evitando riesgos de latencia y cortes de red) ni requiere comprar GPUs de $10,000 USD. Corre perfectamente en Computadoras Industriales (IPC) estándar directamente en el piso de planta (*Edge AI*).
3. **Explicabilidad Visual (Explainable AI - XAI):** A diferencia de los clasificadores tradicionales que operan como una "caja negra" (solo dicen "Roto" o "Sano"), YOLO devuelve coordenadas `(x, y)`. Esto nos permite dibujar un recuadro (*bounding box*) exacto sobre la falla en la pantalla del SCADA. El operario no tiene que confiar a ciegas: la IA le **demuestra** dónde está el error.
4. **Transfer Learning (Eficiencia de Datos):** El modelo no aprende desde cero. Viene preentrenado con millones de formas geométricas estándar. Mediante *Transfer Learning*, solo tuvimos que hacerle un ajuste fino (*fine-tuning*) para que mapee esos conocimientos a la textura del acero, logrando altísima precisión con apenas unas cientos de imágenes de entrenamiento.

### 2.2. Mandrel Health Index (MHI - Índice de Salud del Mandril)
La salida de la red no se queda en una etiqueta; se transforma en un indicador cuantitativo de ingeniería (0 a 100% de salud):
- **Ponderación por criticidad física:** La **punta (*nose*)** del mandril sufre el impacto inicial y guía el perforado del tocho a 1200 °C; por ende, un defecto en la punta tiene una penalización el doble de severa que un defecto en el cuerpo (*body*).
  $$\text{Severidad} = \sum (\text{Área Relativa del Bounding Box} \times \text{Factor de Zona})$$
  *(donde $\text{Factor}_{\text{Nose}} = 2.0$ y $\text{Factor}_{\text{Body}} = 1.0$)*
- **Salud del Mandril:** $\text{MHI} = \max(0, 100 - \text{Severidad})$.
- **Valor agregado:** Permite evolucionar de la detección de roturas al **mantenimiento predictivo** ("este mandril puede utilizarse para 2 tochos más antes de rectificación").

### 2.3. Motor de Decisión "Human-in-the-Loop" (El Semáforo Paranoico)
El diseño de este motor se basa en la realidad económica de la planta de Tenaris, donde no todos los errores cuestan lo mismo:
* **Falso Positivo:** La IA marca un mandril sano como roto. El operario pierde 5 segundos validándolo visualmente. Costo: Bajo.
* **Falso Negativo:** La IA deja pasar un mandril roto como sano. Se perfora un tocho a 1200°C con la herramienta dañada, arruinando la cara interna del tubo. El error se detecta al final de la línea. Costo: Alto (\$1500 USD en *scrap* + pérdida de tiempo de horno + *lead time*).

**La Regla de Oro:** Debemos maximizar el *Recall* (sensibilidad). Es preferible molestar al operario humano con alertas dudosas antes que dejar pasar un defecto. Para esto, bajamos drásticamente el umbral de confianza base de la red (típicamente 25%) a un **15%**.

La lógica del Semáforo de Planta queda estructurada así:
1. **Verde (Apto Absoluto):** La red no encuentra *ningún* recuadro que supere el bajísimo umbral del 15% de confianza. Hay certeza absoluta de que el mandril está sano y avanza al siguiente tocho.
2. **Amarillo (Revisión Humana Requerida):** 
   - Se detecta una falla con confianza dudosa (entre **15% y 80%**). Significa: *"Veo una textura anormal, no sé si es luz, polvo o una rotura real"*.
   - O bien, se detecta una falla con altísima confianza pero el área afectada es minúscula (ej. < 2% de la superficie total).
   - **Acción:** Emite alerta visual en el SCADA. El operario mira la pantalla y con 1 clic decide: Falsa Alarma o Descarte.
3. **Rojo (Descarte Automático PLC):** 
   - Se detecta un defecto evidente con certeza alta (**> 80%** de confianza) y un área mayor al 2%.
   - **Acción:** Dispara una señal digital directa al PLC para que el mecanismo revólver cambie el mandril proactivamente sin detener el *Takt Time* de 30 segundos.

---

## 3. Estado del Dataset y Estrategia de Datos

### 3.1. Diagnóstico del Dataset Provisto
* **Conjunto de Entrenamiento:** 844 imágenes en escala de grises ($576 \times 256$ px).
  - **Mandriles Sanos (Clean):** 555 imágenes (65.8% del dataset).
  - **Defectos anotados:**
    - `Melted Body`: 160 instancias.
    - `Melted Nose`: 129 instancias.
    - `Flattened Nose`: 4 instancias (**desbalance extremo**).
* **Conjunto de Evaluación (Test):** 387 imágenes sin anotaciones para submission.

### 3.2. Estrategia de Preparación de Datos (El "Detrás de Escena")
Para que el modelo sea infalible en la fábrica y no memorice las imágenes, armamos un script que organiza los datos de forma inteligente:

1. **La regla del 80 / 10 / 10 (Separación de Datos):** 
   Dividimos nuestras 844 fotos etiquetadas en tres grandes grupos:
   - **Train (80%):** Es "el libro de texto". La IA mira estas fotos una y otra vez para aprender cómo se ve cada rotura.
   - **Validation (10%):** Es "el simulacro de examen". Tras cada lectura, la IA se toma una prueba acá. Si vemos que su puntaje deja de mejorar, frenamos el entrenamiento para que no se aprenda las respuestas de memoria (*Early Stopping*).
   - **Test Local (10%):** Es "el examen final". Son fotos que guardamos bajo llave. Solo las usamos al terminar todo el proyecto para demostrarle a Tenaris cómo va a rendir el sistema en la vida real.

2. **Protección de los Defectos Raros (Balanceo Inteligente):** 
   Tenemos defectos como la "Punta Aplastada" que solo aparecen en 4 fotos. Si elegimos al azar, podríamos perderlas. El código se asegura matemáticamente de poner 2 para que aprenda, 1 en el simulacro y 1 en el examen final, garantizando que aprenda a ver las fallas más inusuales.

3. **Inmunidad a Falsas Alarmas (Imágenes Sanas):** 
   Le inyectamos 555 fotos de mandriles impecables diciéndole explícitamente: *"Acá no hay absolutamente nada"*. Esto es clave para el negocio: le enseña a no ser exagerado ni inventar problemas donde no los hay.

4. **Corrección de Errores Humanos:** 
   A veces, el humano que etiquetó las fotos originales dibujó los recuadros un poco por fuera del borde de la imagen. El script corrige estos bordes matemáticamente (*Clamping*) para que todo el entrenamiento fluya sin tirar errores en la terminal.

---

## 4. Roadmap de Ejecución del MVP

### Fase 1: Preparación y Conversión de Datos
- [ ] Script de parseo de `annotations.json` $\rightarrow$ estructura YOLO (`images/` y `labels/`).
- [ ] Generación de split estratificado Train (80%) / Val (20%).
- [ ] Creación del archivo de configuración `dataset.yaml` (clases: `Melted Body`, `Melted Nose`, `Flattened Nose`).

### Fase 2: Entrenamiento del Modelo Base (YOLOv8)
- [ ] Configuración del entorno de entrenamiento (`ultralytics`).
- [ ] Fine-tuning de `yolov8n` (nano) o `yolov8s` (small) con transfer learning.
- [ ] Evaluación priorizando métricas críticas industriales: **Recall** (minimizar falsos negativos que arruinen tubos de acero) y **mAP@50**.

### Fase 3: Capa de Lógica de Negocio
- [ ] Módulo Python para cálculo del **Mandrel Health Index (MHI)** a partir de las coordenadas inferidas.
- [ ] Módulo del **Motor de Decisión** (reglas de umbrales para estados Verde, Amarillo y Rojo).

### Fase 4: Inferencia sobre Test y Submission
- [ ] Script de procesamiento batch sobre las 387 fotos de `images/test/`.
- [ ] Formateo del archivo de salida según los requisitos de entrega de la competencia.

### Fase 5: Interfaz Demostrativa (Simulador de Planta para el Pitch)
- [ ] Dashboard interactivo simple (Streamlit/Gradio):
  - Carga una foto de test simulando la llegada del mandril a la posición de reposo.
  - Ejecuta la inferencia en tiempo real.
  - Muestra el cronómetro de la ventana de 30 segundos, el mandril con sus defectos detectados, el MHI resultante y la tarjeta del Semáforo (Verde / Amarillo / Rojo).

---

## 5. Visión Futura (Roadmap para el Pitch ante Tenaris)
En la presentación se mostrará cómo este MVP sienta las bases de un sistema industrial completo:
1. **Fase 2 (Detección de Anomalías No Supervisada / Zero-Shot):** Incorporar un modelo basado en las fotos limpias (Autoencoder o Feature Embeddings) para detectar tipos de fallas inéditas que no existían en el dataset de entrenamiento.
2. **Fase 3 (Fusión Multivariada con Silos de Datos):** Integrar la visión artificial con variables operativas hoy aisladas (temperatura de tocho, ciclos acumulados del mandril, grado del acero) para un modelo predictivo multimodal.

