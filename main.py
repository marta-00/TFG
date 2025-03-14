"""
Main script for running the application
"""
#imports
from leer_datos import leer_datos_gpx
from limpiar_datos import *
from graficos import grafico, crear_histogramas
from magnitudes import *

def main(): 
    # calcular datos iniciales (sin limpiar datos)
    datos_inicial = datos_total_carreras('datos_altitud')
    # print(datos_inicial)

    # limpiar y marcar datos
    resultados_limpios = []
    for nombre_archivo in os.listdir('datos_altitud'):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            df_coord_limpias = limpiar_y_marcar_datos(f'datos_altitud/{nombre_archivo}')

            # Calcular magnitudes
            dist_tramo, dist_total = distancia(df_coord_limpias)
            alt = altitud(df_coord_limpias)
            #print(dist_total)
            # Agregar los resultados a la lista
            resultados_limpios.append({
                'nombre_carrera': nombre_archivo,
                'distancia_total': dist_total,
                'altitud': alt
            })

    # Convertir la lista de resultados a un DataFrame
    datos_limpios = pd.DataFrame(resultados_limpios)
    # print(datos_limpios)
    
    #crear 1 histograma con los datos de la distancia total en datos_inicial y datos_limpios

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.hist(datos_inicial['distancia_total'], 
            bins=int((len(datos_inicial['distancia_total']) )), 
            color='blue', alpha=0.5, edgecolor='blue')

    plt.hist(datos_limpios['distancia_total'], 
            bins=int((len(datos_limpios['distancia_total']) )), 
            color='red', alpha=0.5, edgecolor='red')

    # añadir media y desviación estándar
    plt.axvline(datos_inicial['distancia_total'].mean(), color='blue', linestyle='dashed', linewidth=1)
    plt.axvline(datos_limpios['distancia_total'].mean(), color='red', linestyle='dashed', linewidth=1)
    plt.legend(['Media Inicial', 'Media Limpiados'])
    plt.xlabel('Distancia')
    plt.ylabel('Frecuencia')
    plt.title('Comparación de Histogramas vertical')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()