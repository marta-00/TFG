"""
Script para el análisis y visualización de datos de carreras basados en archivos GPX.

Funciones principales:

    - una_carrera(): Lee coordenadas de una carrera desde un archivo GPX, calcula parámetros con
    un algoritmo específico y muestra la distancia total calculada. Incluye código para análisis
    y marcado de tramos largos (mayores a 90 metros) y gráficos (comentado).

    - total_carreras(): Lee un archivo CSV con magnitudes de varias carreras y contiene código
    para crear histogramas y comparar errores de medición respecto a la distancia estándar
    de una media maratón (21.097,5 m) (actualmente comentado).

    - comparación_distancias(): Compara cómo varía la distancia total calculada al separar los datos
    en diferentes números de segmentos para tres carreras diferentes, graficando las comparaciones.

    - histograma_n_dist(): Procesa todos los archivos GPX de un directorio, calcula distancias totales
    para distintos niveles de separación y genera una figura con histogramas para comparar
    la distribución de estas distancias según el parámetro de separación.

Requiere los módulos externos: leer_datos, magnitudes, graficos y algoritmo, que contienen funciones
de lectura, cálculo y visualización específicas.

El script está diseñado para facilitar el análisis detallado y comparativo de datos de carreras,
permitiendo observar la precisión y variabilidad de las mediciones en diferentes condiciones.
"""

from leer_datos import *
from magnitudes import *
from graficos import *
from algoritmo import *


def una_carrera():
    """
    Lee las coordenadas de una carrera desde un archivo GPX, calcula el parámetro S
    con el algoritmo_S y muestra la distancia total calculada.

    Incluye código comentado para calcular distancias por tramo, marcar puntos y graficar,
    así como un bucle para procesar iterativamente los tramos mayores a 90 metros.
    """

    import matplotlib.pyplot as plt
    # Leer datos del archivo GPX
    df_coord = leer_datos_gpx('datos/Carrera_de_mañana(8).gpx')
    x = df_coord['x'].tolist()
    y = df_coord['y'].tolist()

    S, S_array, distancia = algoritmo_S(x,y)
    print(distancia)

    # # Calcular distancia tramo y total
    # L_total = distancia(df_coord)
    # print(f"La distancia total: {L_total}")
    # print(df_coord)

    # # Obtener las distancias de los tramos
    # L_tramo = df_dist['Distancia (m)']

    # # Encontrar todos los índices donde la distancia es mayor a 90 metros
    # indices_mayor_90 = [i for i in range(len(L_tramo)) if L_tramo[i] > 90]

    # if indices_mayor_90:
    #     puntos_a_marcar = set()
    #     for i in indices_mayor_90:
    #         # Obtener las coordenadas del punto final para esta distancia
    #         p_final_x = df_dist['Punto Final'][i][0]
    #         p_final_y = df_dist['Punto Final'][i][1]

    #         # Agregar las coordenadas finales al conjunto
    #         puntos_a_marcar.add((p_final_x, p_final_y))
            
    #     # Marcar como False los puntos obtenidos en la variable df_coord
    #     df_coord.loc[df_coord[['x', 'y']].apply(tuple, axis=1).isin(puntos_a_marcar), 'marcado'] = False
    
    # grafico(df_coord)
    # plt.show()
            
        
    # while True: 
    #     # Calcular distancia tramo y total
    #     df_dist, L_total = distancia(df_coord)
    #     print(f"La distancia total: {L_total}")

    #     # Obtener las distancias de los tramos
    #     L_tramo = df_dist['Distancia (m)']

    #     # Encontrar todos los índices donde la distancia es mayor a 90 metros
    #     indices_mayor_90 = [i for i in range(len(L_tramo)) if L_tramo[i] > 90]

    #     if indices_mayor_90:
    #         puntos_a_marcar = set()
    #         for i in indices_mayor_90:
    #             # Obtener las coordenadas del punto final para esta distancia
    #             p_final_x = df_dist['Punto Final'][i][0]
    #             p_final_y = df_dist['Punto Final'][i][1]

    #             # Agregar las coordenadas finales al conjunto
    #             puntos_a_marcar.add((p_final_x, p_final_y))
            
    #         # Marcar como False los puntos obtenidos en la variable df_coord
    #         df_coord.loc[df_coord[['x', 'y']].apply(tuple, axis=1).isin(puntos_a_marcar), 'marcado'] = False

    #         print(f"Se han marcado como False los puntos finales de los tramos mayores a 90 metros: {indices_mayor_90}")
    #     else:
    #         print("No hay tramos con distancia mayor a 90 metros.")
    #         break  # Salir del bucle si no hay tramos que cumplan la condición

def total_carreras():
    """
    Lee un archivo CSV con magnitudes de varias carreras y contiene código comentado
    para crear histogramas de distancias totales y altitudes, y comparar errores
    absolutos respecto a una distancia exacta (media maratón).
    """
    # leer archivo magnitudes.csv
    import pandas as pd
    magnitudes = pd.read_csv('magnitudes.csv', delimiter=',', encoding='latin1')
    #print(magnitudes)

    ##separar

    # # crear histograma con las distancias medias
    # import matplotlib.pyplot as plt
    # distancias = magnitudes['Distancia_total(m)']
    # plt.hist(distancias, bins=len(distancias), color='blue', edgecolor='blue', alpha=0.7)

    # # añadir en rojo una recta en el valor 21.097
    # plt.axvline(x=21097, color='red', linestyle='--')

    # plt.title("Histograma - distancias medias")
    # plt.xlabel("Distancia total (m)")
    # plt.ylabel("Número de carreras")
    # plt.show()

    # # crear histograma con las altitudes
    # altitudes = magnitudes['Altitud(m)']
    # plt.hist(altitudes, bins=len(altitudes), color='green', edgecolor='green', alpha=0.7)
    # plt.title("Histograma - altitudes")
    # plt.xlabel("Altitud (m)")
    # plt.ylabel("Número de carreras")
    # plt.show()

    ## comparar distancias
    # obtener distancias
    # distancias = magnitudes['Distancia_total(m)']
    # distancias_par = magnitudes['Distancia_par(m)']
    # distancias_impar = magnitudes['Distancia_impar(m)']

    # #calcular error absoluto, dato exacto 21097,5 m
    # error_total = abs(distancias - 21097.5)
    # error_par = abs(distancias_par - 21097.5)
    # error_impar = abs(distancias_impar - 21097.5)

    # for i in range(len(error_total)):
    #     nombre_carrera = magnitudes['Nombre'][i]
    #     if error_total[i] > error_par[i] and error_total[i] > error_impar[i]:
    #         print(f"La medida mejora")
    #     else:
    #         print(f"la medida empeora para la carrera: {nombre_carrera}")

def comparación_distancias():
    """
    Lee tres archivos GPX de distintas carreras y compara la distancia total calculada
    al separar los datos en diferentes cantidades de segmentos n. Grafica estas
    distancias totales en función de n para cada carrera en un mismo gráfico.
    """
    coord1 = leer_datos_gpx('datos/Carrera_de_mañana(1).gpx')
    coord2 = leer_datos_gpx('datos/Carrera_de_mañana(5).gpx')
    coord3 = leer_datos_gpx('datos/Carrera_de_mañana(8).gpx')
    datos = [coord1, coord2, coord3]

    #crear figura 
    plt.figure(figsize=(10, 6))

    for i,coord in enumerate(datos):
        distancias_totales = []
        dist_tramo, dist_total = distancia(coord)
        distancias_totales.append(dist_total)
        for n in range(2, 20, 1):
            dat1, dat2 = separar_datos(coord, n)
            # calcular distancias
            dist_1, dist_total2 = distancia(dat1)
            distancias_totales.append(dist_total2)

        #añadir datos a la figura
        plt.plot(range(1, len(distancias_totales) + 1), distancias_totales, marker='o')
    # Configurar el gráfico
    distancia_media_maraton = 21097.5  # Distancia en metros
    plt.axhline(y=distancia_media_maraton, color='red', linestyle='--', label='Media Maratón (21.0975 km)')

    plt.title('Comparación de Distancias Totales en Función de n')
    plt.xlabel('Número de Separaciones (n)')
    plt.ylabel('Distancia Total (m)')
    plt.xticks(ticks=range(1, len(distancias_totales) + 1))
    plt.legend(['Carrera_de_mañana(1)', 'Carrera_de_mañana(5)', 'Carrera_de_mañana(8)'])
    plt.grid()
    plt.show()

def histograma_n_dist():
    """
    Lee todos los archivos GPX en el directorio 'datos' y calcula la distancia total
    para diferentes niveles de separación (n = 1, 2, 5, 9, 13, 20).

    Crea una figura con 6 subgráficos tipo histograma para comparar la distribución
    de distancias totales según la separación n, marcando la línea de referencia
    de la media maratón (21.095 metros) en rojo.
    """
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    L_total_1 = []
    L_total_2 = []
    L_total_5 = []
    L_total_9 = []
    L_total_13 = []
    L_total_20 = []
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # leer archivo gpx
            df_coord =leer_datos_gpx(f'datos/{nombre_archivo}')

            #separar datos 
            coord_lista, distancias_totales = separar_datos(df_coord, 1)
            L_total_1.append(distancias_totales[0])

            coord_lista, distancias_totales = separar_datos(df_coord, 2)
            L_total_2.extend([distancias_totales[0], distancias_totales[1]])

            coord_lista, distancias_totales = separar_datos(df_coord, 5)
            L_total_5.extend([distancias_totales[0], distancias_totales[1], distancias_totales[2], distancias_totales[3], distancias_totales[4]])
    
            coord_lista, distancias_totales = separar_datos(df_coord, 9)
            L_total_9.extend([distancias_totales[0], distancias_totales[1], distancias_totales[2], distancias_totales[3], distancias_totales[4]])
    

            coord_lista, distancias_totales = separar_datos(df_coord, 13)
            L_total_13.extend([distancias_totales[0], distancias_totales[1], distancias_totales[2], distancias_totales[3], distancias_totales[4]])
    
            coord_lista, distancias_totales = separar_datos(df_coord, 20)
            L_total_20.extend([distancias_totales[0], distancias_totales[1], distancias_totales[2], distancias_totales[3], distancias_totales[4]])
    
    #crear 6 graficos para cada L_total_i
    plt.figure(figsize=(12, 8))

    # Lista de distancias totales y títulos
    distancias = [L_total_1, L_total_2, L_total_5, L_total_9, L_total_13, L_total_20]
    titulos = [
        "Histograma - Distancias totales con n=1",
        "Histograma - Distancias totales con n=2",
        "Histograma - Distancias totales con n=5",
        "Histograma - Distancias totales con n=9",
        "Histograma - Distancias totales con n=13",
        "Histograma - Distancias totales con n=20"
    ]

    for i, (L_total, titulo) in enumerate(zip(distancias, titulos)):
        plt.subplot(3, 2, i + 1)
        
        # Calcular el histograma
        bins = int(len(L_total)**0.5)  # Ajusta el número de bins según sea necesario
        hist, bin_edges = np.histogram(L_total, bins=bins)
        
        # Calcular los centros de los bins
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
        
        # Dibujar el histograma como barras
        plt.bar(bin_centers, hist, width=np.diff(bin_edges), color='blue', edgecolor='blue', alpha=0.7, align='center')
        
        # añadir linea roja en 21095m
        plt.axvline(x=21095, color='red', linestyle='--')
        # Dibujar la línea que conecta los máximos de cada bin
        #plt.plot(bin_centers, hist, color='red', marker='o', linestyle='-', linewidth=2)
        
        # Configurar el título y etiquetas
        plt.title(titulo)
        plt.xlabel("Distancia total (m)")
        plt.ylabel("Número de carreras")

    plt.tight_layout()  # Ajustar el espaciado entre subgráficas
    plt.show()


# df_coord = leer_datos_gpx('datos/Media_Maratón_Santander_2024.gpx')
# df_dist_kalman = calcular_distancias_recursivas(df_coord)
# crear_histograma(df_dist_kalman)

