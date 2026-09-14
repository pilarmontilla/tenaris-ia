import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    json_path = "dataset/Dataset hackathon/2026.09.09 Dataset hackathon/annotations.json"
    
    with open(json_path, 'r') as f:
        data = json.load(f)

    clases = []
    for img in data:
        if not img.get('defects'):
            clases.append('Sano (Sin Defecto)')
        else:
            for d in img['defects']:
                clases.append(d['class'])
                
    df = pd.DataFrame(clases, columns=['Defecto'])
    
    conteo = df['Defecto'].value_counts().reset_index()
    conteo.columns = ['Tipo de Estado', 'Cantidad']
    
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    
    colores = ['#8CC63F' if x == 'Sano (Sin Defecto)' else '#009CA6' for x in conteo['Tipo de Estado']]
    if len(colores) > 2:
        colores[2] = '#7A3E93' 
        
    ax = sns.barplot(x='Cantidad', y='Tipo de Estado', data=conteo, palette=colores)
    
    for p in ax.patches:
        ax.annotate(f"{int(p.get_width())}", 
                    (p.get_width() + 5, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', fontweight='bold', color='#333333')

    plt.title('Auditoría del Dataset: Distribución de Estados del Mandril', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Cantidad de Muestras (Fotogramas)', fontsize=12)
    plt.ylabel('')
    
    sns.despine()
    plt.tight_layout()
    
    output = 'distribucion_defectos.png'
    plt.savefig(output, dpi=300)
    print(f"Gráfico generado: {output}")

if __name__ == '__main__':
    main()

