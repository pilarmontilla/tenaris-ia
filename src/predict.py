import cv2
from ultralytics import YOLO
import os
import glob
import random

# Rutas
MODEL_PATH = 'runs/detect/mandrel_detector_v1/weights/best.pt'
TEST_DIR = 'dataset_yolo/images/test'
OUTPUT_DIR = 'test_results'

def evaluar_semaforo(boxes):
    """
    Lógica de negocio de Tenaris (Semáforo Paranoico)
    """
    peor_estado = "[OK] APTO PARA PRODUCCION"
    color = (0, 255, 0) # BGR para OpenCV (Verde)
    
    if len(boxes) == 0:
        return peor_estado, color
        
    for box in boxes:
        conf = float(box.conf[0])
            
        # Calcular área relativa (0.0 a 1.0)
        w_norm, h_norm = float(box.xywhn[0][2]), float(box.xywhn[0][3])
        area_pct = w_norm * h_norm
        
        estado_actual = "AMARILLO"
        # Regla del Rojo
        if conf >= 0.80 and area_pct >= 0.02:
            estado_actual = "ROJO"
        
        # Guardar el peor estado encontrado en todo el mandril
        if estado_actual == "ROJO":
            peor_estado = "[CRITICO] DESCARTAR MANDRIL"
            color = (0, 0, 255) # Rojo en BGR
        elif estado_actual == "AMARILLO" and peor_estado != "[CRITICO] DESCARTAR MANDRIL":
            peor_estado = "[ALERTA] REVISION MANUAL REQUERIDA"
            color = (0, 255, 255) # Amarillo en BGR
            
    return peor_estado, color

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Error: No se encontró el modelo entrenado en {MODEL_PATH}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Cargando la IA entrenada...")
    model = YOLO(MODEL_PATH)
    
    # Tomar algunas fotos al azar de nuestro examen final secreto (TEST)
    todas_las_fotos = glob.glob(os.path.join(TEST_DIR, '*.png'))
    random.shuffle(todas_las_fotos)
    fotos_prueba = todas_las_fotos[:10] # Probamos 10 fotos
    
    print(f"\nEvaluando {len(fotos_prueba)} imágenes del Test Set...\n")
    
    for img_path in fotos_prueba:
        # Hacer prediccion. conf=0.15 asegura que no descarte sospechas pequeñas (umbral paranoico)
        results = model.predict(img_path, conf=0.15, verbose=False)
        
        for r in results:
            estado, color = evaluar_semaforo(r.boxes)
            
            # Pedirle a YOLO que dibuje los recuadros que encontró
            im_bgr = r.plot()
            
            # Imprimir nuestro cartel gigante del Semáforo
            # Letra más chica (0.55) y más fina (grosor 1) a pedido del usuario
            cv2.putText(im_bgr, estado, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1)
            
            base_name = os.path.basename(img_path)
            out_path = os.path.join(OUTPUT_DIR, base_name)
            cv2.imwrite(out_path, im_bgr)
            
            print(f"{estado} -> Guardado en {OUTPUT_DIR}/{base_name}")

if __name__ == '__main__':
    main()

