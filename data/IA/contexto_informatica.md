# Caso Tenaris: Desafío de Detección Proactiva de Anomalías en Tubos Sin Costura

## Contexto del Problema y Desafío Tecnológico
Tenaris enfrenta un desafío crítico en su línea de producción de tubos de acero sin costura, destinados a operar en condiciones extremas (a miles de metros bajo tierra y con altísimas presiones). Actualmente, el proceso consiste en calentar tochos de acero hasta los 1200°C para volverlos maleables ("plastilina dura") y perforarlos mediante un **mandril** mientras se los moldea con rodillos.

El problema radica en que el **control de calidad se realiza de manera reactiva, al final del proceso productivo**. Cualquier desperfecto en el mandril (debido a desgaste, adherencia de polvo o ralladuras) se traslada directamente a la cara interna de los tubos generados. Como resultado, si un mandril está defectuoso, la anomalía recién se detecta al finalizar el lote (batch), provocando una tasa de descarte de entre un 5% y 10%. Actualmente, la inspección visual del mandril la realiza un operario humano cuando la línea se detiene, un proceso propenso a errores y no automatizado.

## Enfoque Informático: Industria 4.0, IoT y Computer Vision

El objetivo es transformar un proceso de manufactura pesada en un sistema ciberfísico impulsado por datos, abordándolo desde las siguientes dimensiones:

### 1. Adquisición de Datos en Ambientes Hostiles (IoT)
El desafío primordial de IoT es la captura de datos en un ambiente industrial con temperaturas que alcanzan los 1200°C, partículas en suspensión, suciedad y vibraciones extremas.
- Se requieren sensores y cámaras especializadas (como cámaras térmicas o de espectro no visible) con protección industrial (enclosures) capaces de operar en estas condiciones extremas.
- La transmisión de estos datos requiere redes industriales robustas y de baja latencia para garantizar la integridad y disponibilidad de la información generada por la cámara de calor y otros sensores durante el proceso de laminado.

### 2. Automatización de Inspecciones Visuales mediante Computer Vision
El ojo humano es subjetivo, susceptible a la fatiga y a cometer errores. Es necesario implementar modelos de Computer Vision capaces de:
- Identificar automáticamente defectos en la superficie del mandril (ralladuras, alteraciones geométricas, polvo adherido) de forma sistemática y precisa.
- Cuantificar el porcentaje de anomalías para que el sistema evalúe de manera autónoma si debe detenerse la producción o reemplazarse el mandril, eliminando la dependencia de la inspección humana periódica y manual.

### 3. Inferencia en Tiempo Real y Toma de Decisiones Proactiva
Para alcanzar el objetivo de desperdicio cero y control de calidad proactivo, el análisis de las imágenes y métricas no puede esperar al final de la línea.
- El sistema debe procesar el flujo de datos de manera continua.
- Al detectar un mandril comprometido, debe emitir alertas tempranas o integrarse directamente al PLC (Controlador Lógico Programable) de la planta para interrumpir o ajustar el proceso antes de arruinar el tocho de acero o la serie completa.

### 4. Arquitectura de Procesamiento: Edge Computing vs Cloud
El volumen masivo de datos (imágenes en alta resolución y/o video) y los estrictos requerimientos de baja latencia obligan a definir una arquitectura distribuida:

- **Edge Computing (Computación en el Borde):** Es la capa ideal para la *inferencia en tiempo real* (detección de defectos). Desplegar modelos de IA directamente en hardware robusto (Edge AI) físicamente cercano al mandril evita los problemas de ancho de banda y latencia de red, garantizando los tiempos de respuesta en milisegundos necesarios para alertar al sistema de control de piso de planta.
- **Cloud Computing (Computación en la Nube):** Constituye el entorno óptimo para el almacenamiento a largo plazo, la analítica avanzada, el re-entrenamiento continuo de los modelos de Deep Learning con los nuevos casos detectados, y el monitoreo global de métricas operativas.

En conclusión, este caso representa un desafío integral para diseñar una **arquitectura híbrida Edge-to-Cloud** dentro del paradigma de la **Industria 4.0**, aplicando Inteligencia Artificial para migrar desde un control de calidad reactivo y manual hacia un sistema automatizado, resiliente y preventivo.

