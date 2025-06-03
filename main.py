"""
Script principal para la ejecución y análisis de datos de carreras a partir de archivos GPX.

Este script realiza las siguientes tareas:

    - Lectura y procesamiento inicial de datos de carreras (función `inicial`), que incluye
    la limpieza y marcado de datos, cálculo de distancias totales y almacenamiento
    de resultados en un archivo CSV. (Función obsoleta)

    - Comparación de resultados mediante diferentes algoritmos de análisis de distancia
    (función `main`), que aplica algoritmos específicos (S y D cuadrado) sobre los datos
    originales y limpios, y genera histogramas comparativos para visualizar las diferencias.

    - Visualización gráfica de segmentos generados por el algoritmo sobre una carrera
    específica (función `grafico_carrera_algoritmo`).

    - Análisis estadístico preliminar de las distribuciones de datos limpios según tipos
    de histograma (función `prueba_carrera`), con agrupación por características del histograma.

Importa funciones especializadas para lectura, limpieza, cálculo y clasificación de datos
de los módulos: leer_datos, limpiar_datos, magnitudes, algoritmo y carreras.

El script está orientado a facilitar un análisis detallado y comparativo
de carreras, evaluando la efectividad de métodos de filtrado y cálculo de distancias.
"""
#imports
from leer_datos import leer_datos_gpx
from limpiar_datos import *
from magnitudes import distancia
from algoritmo import *
from carreras import clasificar_histogramas

def inicial(): 
    """
    [Obsoleta] Función para procesamiento inicial de datos de carreras.

    Lee los archivos GPX en la carpeta 'datos', limpia y marca los datos, calcula
    la distancia total recorrida y guarda los resultados en un archivo CSV.

    Nota: Esta función fue usada como primer main, pero actualmente no está en uso.
    """
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
    """
    Función principal para analizar y comparar datos de carreras.

    - Lee archivos GPX desde la carpeta 'datos'.
    - Clasifica histogramas y calcula desviaciones estándar (sigma).
    - Calcula distancias usando datos originales y aplicando dos algoritmos diferentes (S y D^2).
    - Limpia los datos y aplica el algoritmo D^2 con el sigma calculado.
    - Genera un histograma comparativo mostrando las distribuciones de distancia
      para datos iniciales y filtrados.
    """
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
            S, S_array, distancia_alg,segmentos = algoritmo_S(x_alg,y_alg,0.5)
            hist_algoritmo_S.append(distancia_alg)

            # APLICAR ALGORTIMO D
            x_alg = df_coord['x'].tolist()
            y_alg = df_coord['y'].tolist()
            #aplicar algoritmo 
            S, S_array, distancia_alg, segmentos = algoritmo_D_cuadrado(x_alg,y_alg, 2)
            hist_algoritmo_D.append(distancia_alg)

            # LIMPIAR DATOS + ALGORITMO 
            df_coord_limpias = limpiar_y_marcar_datos(f'datos/{nombre_archivo}')
            df_filtrado = df_coord_limpias[df_coord_limpias['marcado'] == True]
            distancia_limpio = distancia(df_filtrado)

            ## Obtener listas solo con los valores marcados como True
            x_limpio = df_filtrado['x'].tolist()
            y_limpio = df_filtrado['y'].tolist()  

            ## aplicar algoritmo
            S_limpio, S_array_limpio, distancia_limpio, segmentos = algoritmo_D_cuadrado(x_limpio,y_limpio,sigma)
            hist_limpios.append(distancia_limpio)
    
    #calcular media y desviación estandar de los datos
    # import numpy as np
    # media = np.mean(hist_incial)
    # desviacion_estandar = np.std(hist_incial)

    # print("datos iniciales")
    # print(f"media: {media}")
    # print(f"desviacion estandar: {desviacion_estandar}")

    # media = np.mean(hist_algoritmo_D)
    # desviacion_estandar = np.std(hist_algoritmo_D)

    # print("datos algoritmo D^2")
    # print(f"media: {media}")
    # print(f"desviacion estandar: {desviacion_estandar}")

    # media = np.mean(hist_algoritmo_S)
    # desviacion_estandar = np.std(hist_algoritmo_S)

    # print("datos algoritmo S")
    # print(f"media: {media}")
    # print(f"desviacion estandar: {desviacion_estandar}")
    
    # crear histograma comparativo
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.hist(np.array(hist_incial), bins=20, alpha=0.5, label='Inicial', color='blue')
    #plt.hist(np.array(hist_algoritmo_D), bins=20, alpha=0.5, label='Algoritmo D^2', color='blue')
    #plt.hist(np.array(hist_algoritmo_S), bins=20, alpha=0.5, label='Algoritmo S', color='red')
    plt.hist(hist_limpios, bins=20, alpha=0.5, label='Filtrado', color='red')

    # # Línea vertical en 21.0975 km (media maratón)
    # #plt.axvline(x=21097, color='red', linestyle='--', linewidth=2, label='Media maratón (21097 m)')

    plt.title('Histograma comparativo de filtrado de datos')
    plt.xlabel('Distancia')
    plt.ylabel('Frecuencia')
    plt.grid()
    plt.legend()
    plt.show()

def grafico_carrera_algoritmo():
    """
    Crea un gráfico de una carrera específica mostrando los segmentos
    rectos detectados por el algoritmo D^2 aplicado sobre los datos limpios.

    Usa el archivo 'Carrera_de_mañana(5).gpx' para la visualización.
    """
    df_coord = leer_datos_gpx(f'datos/Carrera_de_mañana(5).gpx')

    # APLICAR ALGORTIMO S
    x_alg = df_coord['x'].tolist()
    y_alg = df_coord['y'].tolist()
    # #aplicar algoritmo 
    # S, S_array, distancia_alg, segmentos = algoritmo_D_cuadrado(x_alg,y_alg)

    df_coord_limpias = limpiar_y_marcar_datos(f'datos/Carrera_de_mañana(5).gpx')
    df_filtrado = df_coord_limpias[df_coord_limpias['marcado'] == True]

    # Obtener listas solo con los valores marcados como True
    x_limpio = df_filtrado['x'].tolist()
    y_limpio = df_filtrado['y'].tolist()  

    # aplicar algoritmo
    S_limpio, S_array_limpio, distancia_limpio, segmentos = algoritmo_D_cuadrado(x_limpio,y_limpio,2)

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


