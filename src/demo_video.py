import cv2
import os
import glob
from ultralytics import YOLO

MODEL_PATH = 'runs/detect/mandrel_detector_v1/weights/best.pt'
TEST_DIR = 'dataset_yolo/images/test'
OUTPUT_VIDEO = 'demo_planta_tenaris.mp4'

def evaluar_semaforo(boxes):
    peor_estado = "[OK] APTO PARA PRODUCCION"
    color = (0, 255, 0)
    
    if len(boxes) == 0:
        return peor_estado, color
        
    for box in boxes:
        conf = float(box.conf[0])
        w_norm, h_norm = float(box.xywhn[0][2]), float(box.xywhn[0][3])
        area_pct = w_norm * h_norm
        
        estado_actual = "AMARILLO"
        if conf >= 0.65 and area_pct >= 0.01:
            estado_actual = "ROJO"
        
        if estado_actual == "ROJO":
            peor_estado = "[CRITICO] DESCARTAR MANDRIL"
            color = (0, 0, 255)
        elif estado_actual == "AMARILLO" and peor_estado != "[CRITICO] DESCARTAR MANDRIL":
            peor_estado = "[ALERTA] REVISION MANUAL"
            color = (0, 255, 255)
            
    return peor_estado, color

def main():
    print("Iniciando simulación de cámara de planta...")
    model = YOLO(MODEL_PATH)
    
    fotos = glob.glob(os.path.join(TEST_DIR, '*.png'))
    if not fotos:
        print("No se encontraron fotos en la carpeta test.")
        return

    VIDEO_WIDTH = 800
    VIDEO_HEIGHT = 400
    FPS = 30
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (VIDEO_WIDTH, VIDEO_HEIGHT))
    
    print(f"Generando video de {len(fotos)} mandriles...")

    for img_path in fotos:
        results = model.predict(img_path, conf=0.15, verbose=False)
        
        for r in results:
            estado, color = evaluar_semaforo(r.boxes)
            im_bgr = r.plot()
            im_resized = cv2.resize(im_bgr, (VIDEO_WIDTH, VIDEO_HEIGHT))
            cv2.putText(im_resized, estado, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            frames_to_write = int(FPS * 1.5) 
            
            for _ in range(frames_to_write):
                out.write(im_resized)
            black_frame = im_resized * 0

            for _ in range(int(FPS * 0.2)):
                out.write(black_frame)

    out.release()
    print(f"¡Video generado con éxito! Archivo: {OUTPUT_VIDEO}")

if __name__ == '__main__':
    main()

