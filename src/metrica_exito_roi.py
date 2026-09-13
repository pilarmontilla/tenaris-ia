import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # Datos basados en el tiempo de reacción (10 mins de retraso = ~15 tubos arruinados)
    # Asumimos costo de $1500 USD por tubo de acero de alta calidad descartado (Scrap)
    datos = {
        'Escenario': ['Proceso Actual\n(Detección Humana Tardía)', 'Implementación AI Vision\n(Detección Inmediata)'],
        'Tubos Descartados': [15, 1],
        'Pérdida Económica (USD)': [22500, 1500]
    }
    
    df = pd.DataFrame(datos)
    
    # Configuración del gráfico
    plt.figure(figsize=(9, 6))
    sns.set_style("whitegrid")
    
    # Colores: Gris oscuro para el problema, Cyan de Tenaris para la solución
    colores = ['#555555', '#009CA6']
    
    ax = sns.barplot(x='Escenario', y='Pérdida Económica (USD)', data=df, palette=colores)
    
    # Agregar los valores de dinero arriba de las barras
    for p in ax.patches:
        ax.annotate(f"${int(p.get_height()):,}", 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontweight='bold', color='#222222', fontsize=14, xytext=(0, 5), textcoords='offset points')

    # Estética
    plt.title('Métrica de Éxito: Reducción de Pérdidas por Incidente', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Costo de Scrap (USD)', fontsize=12)
    plt.xlabel('')
    
    # Línea de ahorro
    ahorro = df['Pérdida Económica (USD)'][0] - df['Pérdida Económica (USD)'][1]
    porcentaje = (ahorro / df['Pérdida Económica (USD)'][0]) * 100
    
    plt.annotate(f"Ahorro de ${ahorro:,}\n(-{porcentaje:.0f}% en Scrap)", 
                 xy=(1, 1500), 
                 xytext=(0.5, 12000),
                 arrowprops=dict(facecolor='#7A3E93', shrink=0.05, width=2, headwidth=8),
                 fontsize=14, fontweight='bold', color='#7A3E93',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#F9F0FA", ec="#7A3E93", lw=2))

    # Limpiar bordes
    sns.despine()
    plt.tight_layout()
    
    # Guardar
    output = 'metrica_exito_roi.png'
    plt.savefig(output, dpi=300)
    print(f"Gráfico generado: {output}")

if __name__ == '__main__':
    main()

