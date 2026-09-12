# Análisis y Puntos Clave: Entrevista al Ingeniero (Ronda 2)

Este documento centraliza todos los descubrimientos técnicos y operativos obtenidos tras la segunda ronda de preguntas con el ingeniero de Tenaris. Estos puntos validan la viabilidad técnica de la solución basada en Computer Vision e Inteligencia Artificial.

## 1. El Estado Actual de la Inspección
* **Infraestructura Existente:** El proceso de captura de imágenes *ya existe*. Actualmente, todas las fallas críticas en el mandril se detectan visualmente a través de fotos.
* **El Cuello de Botella:** El problema radica en el procesamiento manual. Un operario humano debe mirar las fotos, tardando entre **3 segundos y 5 minutos** en tomar una decisión (dependiendo de la complejidad o duda sobre el defecto). Esto genera fatiga y demoras.

## 2. Restricciones Operativas y Tiempos (Takt Time)
* **La Ventana de Oportunidad (30 Segundos):** Entre la laminación de un tocho y el siguiente, el mandril retrocede a una posición de espera. En ese instante se toma la foto y se tienen **exactamente 30 segundos** de tiempo muerto operativo para tomar una decisión.
* **Cambio Automático:** Si se detecta un defecto en esos 30 segundos, es posible ejecutar una orden de cambio automático del mandril defectuoso por uno nuevo *sin frenar el proceso continuo de la planta*.

## 3. Viabilidad Óptica (El gran alivio técnico)
* **No se requiere visión 360°:** Dado que el mandril es una "pieza de revolución" (gira constantemente durante la perforación del acero), el desgaste es simétrico. El ingeniero confirmó que lo que se observa en una sola cara (180°) es altamente representativo del estado general de la herramienta. 
* **Impacto:** Esto reduce drásticamente los costos de hardware y procesamiento computacional. Una sola cámara bien posicionada es suficiente para alimentar al modelo.
* **Trazabilidad de Errores:** Se asume la premisa de que "todos los errores críticos que generan defectos en el tubo son detectables en la foto del mandril".

## 4. Tipología de Defectos (Clases para la Red Neuronal)
El modelo de Machine Learning deberá ser entrenado específicamente para detectar y clasificar las siguientes 5 anomalías:
1. **Deformación Plástica / Aplastamiento**
2. **Fatiga Térmica** (estrés por exposición cíclica a 1200°C)
3. **Oxidación**
4. **Adhesión** (material del tocho anterior que queda fundido/pegado al mandril)
5. **Desgaste en la Punta** (la zona de mayor impacto inicial)

## 5. Estrategia de Implementación IA (Human-in-the-Loop)
El ingeniero validó positivamente el enfoque de "Umbral de Confianza" para la IA, evitando el rechazo natural de los operarios hacia la automatización total a ciegas:
* **Alta Confianza (Ej. >90%):** Si la IA detecta una falla evidente (ej. punta rota), dispara la orden al PLC y el mandril se cambia automáticamente.
* **Baja Confianza (Duda):** Si la IA detecta algo anómalo pero no está segura, no detiene la planta. Emite una alerta visual en el SCADA/Dashboard para que el humano valide la foto rápidamente y decida ("Descartar" o "Falsa Alarma").

## 6. Impacto Económico y ROI
* Se mencionó el valor de **$1500 USD por tonelada**. Si se considera que el uso de un mandril defectuoso arruina el tubo terminado en la etapa final (desperdiciando el tocho entero, el tiempo de horno y la laminación), evitar que un mandril malo ingrese al ciclo paga inmediatamente la inversión del sistema de software.

---
**Conclusión para el Pitch:** El proyecto no requiere inventar hardware invasivo. Se trata de desarrollar un **módulo de IA (Computer Vision)** que se conecte al flujo de fotos actual, procese la imagen en milisegundos durante la ventana de 30 segundos, y automatice o asista la decisión de descarte basándose en las 5 clases de defectos físicos comprobados.

