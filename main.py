"""
Main script for running the application
"""
#imports
from leer_datos import leer_datos_gpx
from limpiar_datos import *
from magnitudes import distancia
from algoritmo import algoritmo_S

def inicial(): 
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
            #alt = altitud(df_coord_limpias)
            #print(dist_total)
            # Agregar los resultados a la lista
            resultados_limpios.append({
                'nombre_carrera': nombre_archivo,
                'distancia_total': dist_total,
                #'altitud': alt
            })
            print(nombre_archivo)

    # Convertir la lista de resultados a un DataFrame
    datos_limpios = pd.DataFrame(resultados_limpios)
    # Guardar el DataFrame en un archivo CSV
    datos_limpios.to_csv('datos_limpios.csv', index=False)
    # print(datos_limpios)


def main():
    hist_algoritmo = []
    hist_limpios = []
    hist_incial = []
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            df_coord = leer_datos_gpx(f'datos/{nombre_archivo}')

            #calcular distancia inical
            distancia_inicial = distancia(df_coord)
            hist_incial.append(distancia_inicial)

            # APLICAR ALGORTIMO S
            x_alg = df_coord['x'].tolist()
            y_alg = df_coord['y'].tolist()
            #aplicar algoritmo 
            S, S_array, distancia_alg = algoritmo_S(x_alg,y_alg)
            hist_algoritmo.append(distancia_alg)

            df_coord_limpias = limpiar_y_marcar_datos(f'datos/{nombre_archivo}')
            df_filtrado = df_coord_limpias[df_coord_limpias['marcado'] == True]

            # Obtener listas solo con los valores marcados como True
            x_limpio = df_filtrado['x'].tolist()
            y_limpio = df_filtrado['y'].tolist()  

            # aplicar algoritmo
            S_limpio, S_array_limpio, distancia_limpio = algoritmo_S(x_limpio,y_limpio)
            hist_limpios.append(distancia_limpio)
    
    # crear histograma comparativo
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.hist(hist_incial, bins=20, alpha=0.5, label='Inicial', color='green')
    plt.hist(hist_algoritmo, bins=20, alpha=0.5, label='Algoritmo', color='blue')
    #plt.hist(hist_limpios, bins=20, alpha=0.5, label='Algoritmo + Limpios', color='red')

    # Línea vertical en 21.0975 km (media maratón)
    plt.axvline(x=21097, color='red', linestyle='--', linewidth=2, label='Media maratón (21097 m)')

    plt.title('Histograma comparativo de distancias')
    plt.xlabel('Distancia (m)')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()