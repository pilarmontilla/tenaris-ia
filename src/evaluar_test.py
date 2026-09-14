import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ultralytics import YOLO
import cv2

def evaluar_semaforo(boxes):
    peor_estado = "VERDE"
    if len(boxes) == 0: return peor_estado
    for box in boxes:
        conf = float(box.conf[0])
        w_norm, h_norm = float(box.xywhn[0][2]), float(box.xywhn[0][3])
        area_pct = w_norm * h_norm
        estado_actual = "AMARILLO"
        if conf >= 0.65 and area_pct >= 0.01:
            estado_actual = "ROJO"
        if estado_actual == "ROJO": peor_estado = "ROJO"
        elif estado_actual == "AMARILLO" and peor_estado != "ROJO": peor_estado = "AMARILLO"
    return peor_estado

def main():
    print("🚀 Iniciando auditoría del modelo sobre el set de Test...")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(BASE_DIR, 'runs/detect/mandrel_detector_v1/weights/best.pt')
    TEST_IMAGES = os.path.join(BASE_DIR, 'dataset_yolo/images/test')
    TEST_LABELS = os.path.join(BASE_DIR, 'dataset_yolo/labels/test')
    
    model = YOLO(MODEL_PATH)
    
    img_paths = glob.glob(os.path.join(TEST_IMAGES, '*.png'))
    
    resultados = []
    
    verdaderos_positivos = 0  
    verdaderos_negativos = 0  
    falsos_positivos = 0      
    falsos_negativos = 0      
    
    for img_p in img_paths:
        base_name = os.path.basename(img_p)
        txt_name = base_name.replace('.png', '.txt')
        txt_path = os.path.join(TEST_LABELS, txt_name)
        
        realidad_roto = False
        if os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
            realidad_roto = True
            
        img = cv2.imread(img_p)
        results = model.predict(img, conf=0.15, verbose=False)
        estado_ia = evaluar_semaforo(results[0].boxes)
        
        prediccion_roto = True if estado_ia in ["AMARILLO", "ROJO"] else False
        
        if realidad_roto and prediccion_roto:
            verdaderos_positivos += 1
            clasificacion = 'Acierto (Defecto detectado)'
        elif not realidad_roto and not prediccion_roto:
            verdaderos_negativos += 1
            clasificacion = 'Acierto (Sano confirmado)'
        elif not realidad_roto and prediccion_roto:
            falsos_positivos += 1
            clasificacion = 'Error (Falsa Alarma)'
        elif realidad_roto and not prediccion_roto:
            falsos_negativos += 1
            clasificacion = 'Error (Defecto No Detectado)'
            
        resultados.append({
            'Archivo': base_name,
            'Realidad': 'Roto' if realidad_roto else 'Sano',
            'IA_Dijo': estado_ia,
            'Evaluacion': clasificacion
        })

    df = pd.DataFrame(resultados)
    df.to_csv('reporte_inferencia_test.csv', index=False)
    
    df_errores = df[df['Evaluacion'].str.contains('Error')]
    df_errores.to_csv('imagenes_mal_detectadas.csv', index=False)
    
    total = len(img_paths)
    aciertos = verdaderos_positivos + verdaderos_negativos
    efectividad = (aciertos / total) * 100
    
    print("\n" + "="*50)
    print(f"📊 RESUMEN DE TEST (Total Evaluado: {total} mandriles)")
    print("="*50)
    print(f"✅ ACIERTOS TOTALES: {aciertos} ({efectividad:.1f}%)")
    print(f"   - Mandriles Rotos bien detectados: {verdaderos_positivos}")
    print(f"   - Mandriles Sanos bien detectados: {verdaderos_negativos}")
    print(f"❌ ERRORES TOTALES: {falsos_positivos + falsos_negativos}")
    print(f"   - Falsas Alarmas (Sano pero dijo roto): {falsos_positivos}")
    print(f"   - PELIGRO (Roto pero dijo sano): {falsos_negativos}")
    print("="*50)
    print("📁 Se guardó 'imagenes_mal_detectadas.csv' con los nombres de las fotos donde se equivocó.")
    
    matriz = [[verdaderos_positivos, falsos_negativos],
              [falsos_positivos, verdaderos_negativos]]
              
    plt.figure(figsize=(7,5))
    sns.heatmap(matriz, annot=True, fmt='d', cmap=['#F0F2F6', '#009CA6'], cbar=False,
                xticklabels=['IA Predijo Roto', 'IA Predijo Sano'],
                yticklabels=['Realmente Roto', 'Realmente Sano'],
                annot_kws={"size": 20, "weight": "bold"})
    
    plt.title(f'Matriz de Confusión (Efectividad {efectividad:.1f}%)', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('matriz_confusion_test.png', dpi=300)
    print("🖼️ Se guardó el gráfico 'matriz_confusion_test.png'")

if __name__ == '__main__':
    main()

