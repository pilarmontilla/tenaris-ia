# Estrategia de Entrenamiento (YOLOv8)

Para garantizar que la IA detecte roturas reales en la fábrica y no solo "memorice" las fotos, aplicamos estándares estrictos de Machine Learning.

## 1. División de Datos (Data Split)
De las 844 imágenes originales anotadas, forzamos un embudo del **80/10/10**:

* **Entrenamiento (673 fotos / 80%):** Los libros de estudio de la IA. 
  * *Estrategia antialarmas:* Inyectamos 444 imágenes de mandriles 100% sanos para enseñarle a la red a no dar "falsas alarmas" por reflejos o polvillo.
* **Validación (83 fotos / 10%):** El simulacro de examen. Son fotos que la IA *nunca* vio durante el estudio. La métrica final de éxito se calcula exclusivamente aquí.
* **Test Local (88 fotos / 10%):** Fotos guardadas bajo llave para pruebas de robustez absolutas.

## 2. El Entrenamiento (75 Épocas) y la Curva de Aprendizaje
El modelo se entrenó usando aceleración GPU con una técnica de distorsión controlada.

1. **Fase de "Entrenamiento con Pesas" (Épocas 1 a 65):**
   Se activa *Mosaic Data Augmentation*. El motor funde 4 imágenes distintas en una sola, deforma las piezas y las desenfoca. Al obligar a la IA a buscar fallas en modo difícil, la precisión se estanca artificialmente cerca del 70%.
   
2. **El "Sprint Final" (Épocas 65 a 75):**
   El motor apaga automáticamente todas las distorsiones visuales (`closing dataloader mosaic`). Al enfrentarse a fotos limpias de fábrica por primera vez tras 65 ciclos duros, **la curva de aprendizaje pega un salto genuino y se consolida en un 92% de precisión**.

## 3. Resultado Final
* **Precisión General (mAP50):** 92.0%
* **Precisión de cajas (P):** 96.3% (Prácticamente nulos falsos positivos).
* **Ausencia de Overfitting:** Comprobado empíricamente, ya que el puntaje máximo se obtuvo íntegramente sobre el set aislado de validación.
