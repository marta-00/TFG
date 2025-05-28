"""
Main script for running the application
"""
#imports
from leer_datos import leer_datos_gpx
from limpiar_datos import *
from magnitudes import distancia
from algoritmo import *
from carreras import clasificar_histogramas

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
    hist_algoritmo_D = []
    hist_algoritmo_S = []
    hist_limpios = []
    hist_incial = []
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            df_coord = leer_datos_gpx(f'datos/{nombre_archivo}')
            tipo, sigma = clasificar_histogramas(df_coord, False)

            #DISTANCIAS INICIALES
            distancia_inicial = distancia(df_coord)
            hist_incial.append(distancia_inicial)

            # APLICAR ALGORTIMO S
            x_alg = df_coord['x'].tolist()
            y_alg = df_coord['y'].tolist()
            #aplicar algoritmo 
            S, S_array, distancia_alg,segmentos = algoritmo_S(x_alg,y_alg,sigma)
            hist_algoritmo_S.append(distancia_alg)

            # APLICAR ALGORTIMO D
            x_alg = df_coord['x'].tolist()
            y_alg = df_coord['y'].tolist()
            #aplicar algoritmo 
            S, S_array, distancia_alg, segmentos = algoritmo_D_cuadrado(x_alg,y_alg,sigma)
            hist_algoritmo_D.append(distancia_alg)

            # LIMPIAR DATOS + ALGORITMO 
            df_coord_limpias = limpiar_y_marcar_datos(f'datos/{nombre_archivo}')
            df_filtrado = df_coord_limpias[df_coord_limpias['marcado'] == True]

            #Obtener listas solo con los valores marcados como True
            x_limpio = df_filtrado['x'].tolist()
            y_limpio = df_filtrado['y'].tolist()  

            #aplicar algoritmo
            S_limpio, S_array_limpio, distancia_limpio, segmentos = algoritmo_D_cuadrado(x_limpio,y_limpio,sigma)
            hist_limpios.append(distancia_limpio)
    
    # crear histograma comparativo
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.hist(np.array(hist_incial)/21097, bins=20, alpha=0.5, label='Inicial', color='green')
    plt.hist(np.array(hist_algoritmo_D)/21097, bins=20, alpha=0.5, label='Algoritmo D^2', color='blue')
    plt.hist(np.array(hist_algoritmo_S)/21097, bins=20, alpha=0.5, label='Algoritmo S', color='red')
    #plt.hist(hist_limpios, bins=20, alpha=0.5, label='Algoritmo D^2 + Filtrado', color='red')

    # Línea vertical en 21.0975 km (media maratón)
    #plt.axvline(x=21097, color='red', linestyle='--', linewidth=2, label='Media maratón (21097 m)')

    plt.title('Histograma comparativo de distancias')
    plt.xlabel('Distancia (m)')
    plt.ylabel('Frecuencia')
    plt.grid()
    plt.legend()
    plt.show()


def grafico_carrera_algoritmo():
    """
    Funcion que crea un grafico de la carrera con las rectas que crea el algoritmo.
    """
    df_coord = leer_datos_gpx(f'datos/Carrera_de_mañana(8).gpx')

    # APLICAR ALGORTIMO S
    x_alg = df_coord['x'].tolist()
    y_alg = df_coord['y'].tolist()
    # #aplicar algoritmo 
    # S, S_array, distancia_alg, segmentos = algoritmo_D_cuadrado(x_alg,y_alg)
    
    df_coord_limpias = limpiar_y_marcar_datos(f'datos/media_maratón_santander_2024.gpx')
    df_filtrado = df_coord_limpias[df_coord_limpias['marcado'] == True]

    # Obtener listas solo con los valores marcados como True
    x_limpio = df_filtrado['x'].tolist()
    y_limpio = df_filtrado['y'].tolist()  

    # aplicar algoritmo
    S_limpio, S_array_limpio, distancia_limpio, segmentos = algoritmo_S(x_limpio,y_limpio,1)

    # Graficar los segmentos rectos
    graficar_segmentos(x_alg, y_alg, segmentos)

def prueba_carrera():
    S_modal = []
    S_bimodal = []
    S_extendida = []
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            df_coord_limpias = limpiar_y_marcar_datos(f'datos/{nombre_archivo}')
            df_filtrado = df_coord_limpias[df_coord_limpias['marcado'] == True]
            tipo, sigma = clasificar_histogramas(df_filtrado, False)

            # if tipo == 'normal':
            #     #print('modal')
            #     # Calcular la sigma del histograma
            #     sigma = df_filtrado['distancia'].std()
            #     S_modal.append(sigma)
            # elif tipo == 'bimodal':
            #     #print('bimodal')
            #     # Calcular la sigma del histograma
            #     sigma = df_filtrado['distancia'].std()
            #     S_bimodal.append(sigma)
            # else:
            #     #print('extendida')
            #     # Calcular la sigma del histograma
            #     sigma = df_filtrado['distancia'].std()
            #     S_extendida.append(sigma)
    
    #media de las sigmsa
    # media_modal = np.mean(S_modal)
    # media_bimodal = np.mean(S_bimodal)
    # media_extendida = np.mean(S_extendida)
    # print(f"Media de las sigmas modal: {media_modal}")
    # print(S_modal)
    # #print(f"Media de las sigmas bimodal: {media_bimodal}")
    # #print(S_bimodal)
    # print(f"Media de las sigmas extendida: {media_extendida}")
    # print(S_extendida)



if __name__ == "__main__":
    grafico_carrera_algoritmo()
    #main()
    #prueba_carrera()