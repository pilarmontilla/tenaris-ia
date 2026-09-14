from ultralytics import YOLO

def main():
    model = YOLO('yolov8n.pt')

    print("Iniciando el entrenamiento express...")
    results = model.train(
        data='dataset_yolo/dataset.yaml', 
        epochs=15,                        
        imgsz=640,                        
        batch=16,                         
        name='mandrel_detector_v1',       
        patience=15,                      
        cache=False                       
    )
    
    print("¡Entrenamiento finalizado!")

if __name__ == '__main__':
    main()