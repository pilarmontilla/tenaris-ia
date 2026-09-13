from ultralytics import YOLO

def main():
    # 1. Cargar el modelo base YOLOv8 Nano (el más rápido y liviano)
    model = YOLO('yolov8n.pt')

    # 2. Iniciar el entrenamiento express (15 épocas)
    print("Iniciando el entrenamiento express...")
    results = model.train(
        data='dataset_yolo/dataset.yaml', 
        epochs=15,                        # Bajamos a 15 para un entrenamiento de ~5 min
        imgsz=640,                        
        batch=16,                         
        name='mandrel_detector_v1',       
        patience=15,                      
        cache=False                       # Evitar usar memoria ram en exceso
    )
    
    print("¡Entrenamiento finalizado!")

if __name__ == '__main__':
    main()