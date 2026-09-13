import os
import glob
import json
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
    print("🚀 Iniciando evaluación MASIVA sobre TODO el dataset original...")
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(BASE_DIR, 'runs/detect/mandrel_detector_v1/weights/best.pt')
    DATASET_DIR = os.path.join(BASE_DIR, 'dataset/Dataset hackathon/2026.09.09 Dataset hackathon')
    JSON_PATH = os.path.join(DATASET_DIR, 'annotations.json')
    
    # Cargar JSON original
    with open(JSON_PATH, 'r') as f:
        data_json = json.load(f)
        
    model = YOLO(MODEL_PATH)
    
    resultados = []
    
    verdaderos_positivos = 0
    verdaderos_negativos = 0
    falsos_positivos = 0
    falsos_negativos = 0
    
    # Evaluar foto por foto basándonos en el JSON
    for item in data_json:
        img_name = item['file_name']
        # 1. Realidad (Ground Truth del JSON)
        # Buscar en la subcarpeta images/train del dataset original
        img_path = os.path.join(DATASET_DIR, 'images', 'train', img_name)
        if not os.path.exists(img_path):
            # A veces pueden estar en test, buscamos por si acaso
            img_path = os.path.join(DATASET_DIR, 'images', 'test', img_name)
            if not os.path.exists(img_path):
                continue
        realidad_roto = len(item.get('defects', [])) > 0
            
        # 2. Predicción de IA
        img = cv2.imread(img_path)
        results = model.predict(img, conf=0.15, verbose=False)
        estado_ia = evaluar_semaforo(results[0].boxes)
        
        prediccion_roto = True if estado_ia in ["AMARILLO", "ROJO"] else False
        
        # 3. Contabilizar
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
            'Archivo': img_name,
            'Realidad': 'Roto' if realidad_roto else 'Sano',
            'IA_Dijo': estado_ia,
            'Evaluacion': clasificacion
        })

    # Guardar CSV de errores
    df = pd.DataFrame(resultados)
    df_errores = df[df['Evaluacion'].str.contains('Error')]
    df_errores.to_csv('errores_totales_dataset.csv', index=False)
    
    total = len(resultados)
    aciertos = verdaderos_positivos + verdaderos_negativos
    efectividad = (aciertos / total) * 100 if total > 0 else 0
    
    print("\n" + "="*50)
    print(f"📊 RESUMEN MASIVO (Total Evaluado: {total} imágenes de fábrica)")
    print("="*50)
    print(f"✅ ACIERTOS TOTALES: {aciertos} ({efectividad:.1f}%)")
    print(f"   - Mandriles Rotos bien detectados: {verdaderos_positivos}")
    print(f"   - Mandriles Sanos bien detectados: {verdaderos_negativos}")
    print(f"❌ ERRORES TOTALES: {falsos_positivos + falsos_negativos}")
    print(f"   - Falsas Alarmas (Sano pero dijo roto): {falsos_positivos}")
    print(f"   - PELIGRO (Roto pero dijo sano): {falsos_negativos}")
    print("="*50)
    print("📁 Se guardó 'errores_totales_dataset.csv' con los casos donde la IA falló sobre la base total.")
    
    # Gráfico de Torta (Aciertos vs Errores) con Leyenda lateral para evitar solapamiento
    plt.figure(figsize=(10, 6)) # Un poco más ancho para que entre la leyenda
    sns.set_style("white")
    
    datos_torta = [verdaderos_negativos, verdaderos_positivos, falsos_positivos, falsos_negativos]
    etiquetas = ['Sanos Bien Detectados', 'Rotos Bien Detectados', 'Falsa Alarma (Costo Operativo)', 'No Detectado (Peligro Crítico)']
    colores = ['#8CC63F', '#009CA6', '#FFD100', '#CC0000']
    
    # Calcular el total para los porcentajes
    total_filtrado = sum(datos_torta)
    
    # Filtrar ceros para que no rompa el gráfico
    datos_filtrados = []
    etiquetas_filtradas = []
    colores_filtrados = []
    for d, e, c in zip(datos_torta, etiquetas, colores):
        if d > 0:
            datos_filtrados.append(d)
            porcentaje = (d / total_filtrado) * 100
            # Agregar Porcentaje y Número Absoluto a la leyenda directamente
            etiquetas_filtradas.append(f"{e} - {porcentaje:.1f}% ({d})")
            colores_filtrados.append(c)

    # Dibujar torta SIN textos adentro, solo colores lisos
    separacion = [0.03] * len(datos_filtrados)
    wedges, texts = plt.pie(
        datos_filtrados, 
        colors=colores_filtrados, 
        startangle=90, 
        explode=separacion
    )
    
    # Poner las etiquetas en una leyenda limpia a la derecha
    plt.legend(wedges, etiquetas_filtradas,
               title="Clasificación de IA",
               title_fontproperties={'weight':'bold', 'size':12},
               loc="center left",
               bbox_to_anchor=(1, 0.5),
               fontsize=11)
    
    plt.title(f'Rendimiento Global del Modelo ({total} fotogramas evaluados)', fontsize=15, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('rendimiento_masivo_global.png', dpi=300, bbox_inches='tight')
    print("🖼️ Se guardó el gráfico 'rendimiento_masivo_global.png' corregido")

if __name__ == '__main__':
    main()

