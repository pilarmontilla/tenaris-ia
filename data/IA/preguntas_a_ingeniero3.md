# Análisis y Puntos Clave: Entrevista al Ingeniero (Ronda 3)

Este documento resume los últimos detalles operativos relevados en la tercera ronda de preguntas, consolidando el enfoque que debe tener el modelo.

## 1. El Mecanismo de Recambio
* **Sistema "Revólver":** Se mencionó que el mecanismo físico de intercambio o rotación de los mandriles es relativamente rápido y funciona como el tambor de un "revólver". Esto reafirma la viabilidad de hacer cambios dinámicos si la Inteligencia Artificial detecta un problema, sin generar demoras masivas en la planta.

## 2. Frecuencia de Actualización de Reglas
* **Reglas estáticas:** Actualmente, la formalización de ciertas decisiones operativas o actualizaciones de procesos se da con una frecuencia muy baja (ej. una vez al año). 
* **El valor de la IA:** Introducir un modelo que tome decisiones en tiempo real foto a foto, y que pueda reentrenarse continuamente, rompe con la lentitud burocrática del proceso actual.

## 3. Filosofía de Implementación ("Keep it Simple")
* **No ahogarse en los detalles:** A lo largo de las respuestas, la recomendación técnica subyacente es clara: para que el proyecto sea un éxito en la competencia, la herramienta de Inteligencia Artificial debe enfocarse primariamente en procesar la imagen para buscar flujos, roturas o anomalías. 
* Tratar de conectar todos los factores al mismo tiempo (temperaturas, variables del horno, bases de datos externas) podría hacer que se "metan en un mar de detalles". 
* **Conclusión para el Pitch:** Presenten un sistema robusto de procesamiento de imágenes. Que el MVP detecte el error visual y tome la decisión (Cambiar / No Cambiar). Dejen la integración con las otras bases de datos como un "Roadmap futuro" o "Fase 2".

