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
    datos_inicial = datos_total_carreras('datos')
    # print(datos_inicial)

    # limpiar y marcar datos
    resultados_limpios = []
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            df_coord_limpias = limpiar_y_marcar_datos(f'datos/{nombre_archivo}')

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
            print(nombre_archivo)

    # Convertir la lista de resultados a un DataFrame
    datos_limpios = pd.DataFrame(resultados_limpios)
    # Guardar el DataFrame en un archivo CSV
    datos_limpios.to_csv('datos_limpios.csv', index=False)
    # print(datos_limpios)
    

if __name__ == "__main__":
    main()