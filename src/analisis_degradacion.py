import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import re

def main():
    print("Cargando JSON de anotaciones...")
    json_path = "dataset/Dataset hackathon/2026.09.09 Dataset hackathon/annotations.json"
    
    with open(json_path, 'r') as f:
        data = json.load(f)

    records = []
    for img in data:
        fname = img['file_name']
        
        # Extraer fecha y hora del formato: 15_07_2026_ImgPunta_17_52_31.png
        match = re.search(r'(\d{2})_(\d{2})_(\d{4})_.*_(\d{2})_(\d{2})_(\d{2})\.png', fname)
        if not match:
            continue
            
        day, month, year, hour, minute, second = match.groups()
        dt_str = f"{year}-{month}-{day} {hour}:{minute}:{second}"
        
        # Calcular el tamaño del defecto (Área máxima en píxeles si hay varios)
        max_area = 0
        for d in img.get('defects', []):
            area = d['width'] * d['height']
            if area > max_area:
                max_area = area
                
        records.append({
            'file_name': fname,
            'timestamp': pd.to_datetime(dt_str),
            'area_defecto_px': max_area
        })

    # 1. Crear el DataFrame de Pandas
    df = pd.DataFrame(records)
    df = df.sort_values('timestamp')

    # 2. Aislar la secuencia específica que descubriste (15 de Julio de 2026, 17:50 a 18:10)
    start_time = pd.to_datetime('2026-07-15 17:50:00')
    end_time = pd.to_datetime('2026-07-15 18:10:00')
    
    df_secuencia = df[(df['timestamp'] >= start_time) & (df['timestamp'] <= end_time)]
    
    if df_secuencia.empty:
        print("No se encontraron datos en esa ventana de tiempo. Revisá la ruta del JSON.")
        return
        
    print(f"Se encontraron {len(df_secuencia)} ciclos de máquina en esa ventana de tiempo.")

    # 3. Dibujar el Gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(df_secuencia['timestamp'], df_secuencia['area_defecto_px'], 
             marker='o', linestyle='-', color='#009CA6', linewidth=2.5, markersize=8, label='Desgaste Medido (IA)')
    
    # 4. Dibujar la línea de "ROJO" (1% del área total de la imagen de 576x256)
    area_total_img = 576 * 256
    umbral_rojo = area_total_img * 0.01
    
    plt.axhline(y=umbral_rojo, color='#CC0000', linestyle='--', linewidth=2, label='Umbral Crítico (Descarte Automático)')

    # Estética del gráfico
    plt.title('Mantenimiento Predictivo: Evolución de Degradación en Tiempo Real', fontsize=14, fontweight='bold', color='#333333')
    plt.xlabel('Hora Exacta (Cada punto es un tubo laminado)', fontsize=12)
    plt.ylabel('Gravedad de la Rotura (Píxeles cuadrados)', fontsize=12)
    
    # Formatear el eje X para que muestre Horas:Minutos:Segundos
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    # Guardar
    output_img = 'curva_degradacion.png'
    plt.savefig(output_img, dpi=300)
    print(f"¡Éxito! Gráfico generado y guardado como: {output_img}")

if __name__ == '__main__':
    main()

