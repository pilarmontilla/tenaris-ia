# Análisis y Puntos Clave: Entrevista al Ingeniero (Ronda 1)

Este documento resume los temas logísticos, de costos y de manejo de datos conversados en la primera ronda de preguntas. 

## 1. Logística, Costos y "Lead Time"
* **Movimiento Interno:** Los tubos se mueven con grúas de techo hacia una zona de "estiva intermedia".
* **El Verdadero Costo:** El costo más grande de los defectos no es mover la grúa, sino el **Lead Time de la orden** (demoras y penalidades por no entregar a tiempo).
* **El valor agregado perdido:** Si un tubo sale mal, el material se recicla (vuelve al horno), pero se pierde todo el valor económico agregado (tiempo de horno, laminación, horas hombre).
* **Desborde:** Si la nave se llena de tubos retenidos, hay que pagar camiones para llevarlos a una playa externa (capacidad de 50 toneladas por viaje), encareciendo todo.

## 2. Proceso de Recortado y Revisión de Lotes
* **Recorte Automático:** Si un tubo de 14 metros tiene un defecto a los 12 metros, una máquina corta los 2 metros dañados (que se funden nuevamente) y se salva el resto.
* **Política de Batches:** Se revisan el 100% de los tubos. Si en un lote de 100 tubos hay 1 solo defecto, pasa. Pero si la cantidad de defectuosos supera el **10% del lote** (ej. 30 tubos), se retiene el batch completo para una revisión exhaustiva.

## 3. Defectos del Mandril (Clasificación Visual)
El ingeniero agrupó los defectos visibles en 3 grandes familias clave para la cámara:
1. **Falta de material:** Roturas o desgaste por fricción.
2. **Exceso de material (Adhesión):** Material del tocho/tubo anterior que quedó fundido y pegado al mandril.
3. **Estrés Térmico:** Deformaciones generadas por la alta temperatura. (Se reafirma que la cámara no puede estar expuesta directamente al calor extremo).

## 4. El Problema de los "Silos de Datos" (Clave para la IA)
* **¿Por qué usar fotos y no solo bases de datos?** El ingeniero reveló que los datos operativos (temperatura, grado del acero, cantidad de usos del mandril) **existen, pero están en silos independientes** (bases de datos separadas). 
* **El desafío:** Cruzar esa información en tiempo real es un desafío informático grande. 
* **La validación de su enfoque:** Por este motivo, la solución propuesta por ustedes (usar **Visión Computacional / Imágenes**) es la más pragmática. Entrenar el modelo con la foto es el mejor "MVP" (Producto Mínimo Viable). En el futuro, a ese modelo de imágenes se le puede sumar la temperatura y el grado de acero para hacerlo aún más robusto.

