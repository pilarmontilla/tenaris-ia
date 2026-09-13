import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    json_path = "dataset/Dataset hackathon/2026.09.09 Dataset hackathon/annotations.json"
    
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 1. Extraer los datos
    clases = []
    for img in data:
        if not img.get('defects'):
            clases.append('Sano (Sin Defecto)')
        else:
            for d in img['defects']:
                clases.append(d['class'])
                
    # 2. Crear DataFrame de Pandas
    df = pd.DataFrame(clases, columns=['Defecto'])
    
    # 3. Contar ocurrencias
    conteo = df['Defecto'].value_counts().reset_index()
    conteo.columns = ['Tipo de Estado', 'Cantidad']
    
    # 4. Configurar estilo del gráfico (Colores Tenaris del Dashboard)
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    # Asignar colores: Verde para Sano, Cyan/Violeta para los defectos
    colores = ['#8CC63F' if x == 'Sano (Sin Defecto)' else '#009CA6' for x in conteo['Tipo de Estado']]
    if len(colores) > 2:
        colores[2] = '#7A3E93' # Violeta para el tercer defecto si existe
        
    ax = sns.barplot(x='Cantidad', y='Tipo de Estado', data=conteo, palette=colores)
    
    # Agregar los números al lado de cada barra
    for p in ax.patches:
        ax.annotate(f"{int(p.get_width())}", 
                    (p.get_width() + 5, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', fontweight='bold', color='#333333')

    # Estética
    plt.title('Auditoría del Dataset: Distribución de Estados del Mandril', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Cantidad de Muestras (Fotogramas)', fontsize=12)
    plt.ylabel('')
    
    # Limpiar bordes
    sns.despine()
    plt.tight_layout()
    
    # Guardar
    output = 'distribucion_defectos.png'
    plt.savefig(output, dpi=300)
    print(f"Gráfico generado: {output}")

if __name__ == '__main__':
    main()

