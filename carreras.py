
from leer_datos import leer_datos_gpx
from magnitudes import *
from graficos import *

"""
GUARDAR GRAFICOS EN CARPETA
#crear una carpeta para guardar los datos de cada carpeta dentro deresultados\carreras con el nombre de la carrera
            carpeta = f'resultados/carreras/{nombre_archivo}'
            os.makedirs(carpeta, exist_ok=True)
        
            ## RECORRIDO
            graf = grafico(coord)
            plt.savefig(f'{carpeta}/recorrido_sin_curva.png')
            plt.close(graf)

            ## DISTANCIAS TRAMO
            #crear histogramas
            dist_td = crear_histogramas(dist_tramo, nombre1 = "distancias_sin_curva_atipicos")
            plt.savefig(f'{carpeta}/distancias_sin_curva_atipicos.png')
            plt.close(dist_td)
            #imagen = crear_histogramas(dist_tramo_par, dist_tramo_impar, "pares", "impares")
            #añadir a carpeta 
            #plt.savefig(f'{carpeta}/distancias_mitad_datos.png')
            #plt.close(imagen)

            # VELOCIDADES
            # calcular velocidad instantánea
            figura = crear_histogramas(velocidades, nombre1 = "velocidades_sin_curva_atipicos")
            #añadir a carpeta histogramas_velocidad
            plt.savefig(f'{carpeta}/velocidades_sin_curva_atipicos.png')
            plt.close(figura)
"""


def una_carrera():
    import matplotlib.pyplot as plt
    # Leer datos del archivo GPX
    df_coord = leer_datos_gpx('datos/Carrera_de_mañana(8).gpx')
    
    # # Calcular distancia tramo y total
    # df_dist, L_total = distancia(df_coord)
    # print(f"La distancia total: {L_total}")

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
    Función que separa los datos separados n veces y crea un gráfico comparando cómo varía la 
    distancia total de la carrera en función de n. 
    En un mismo gráfico se incluyen 3 carreras distintas para poder compararlas.
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
    Función que lee todos los archivos gpx. Crea una figura con 6 graficos. 
    Los gráficos son histogramas de la distancia total. Se comparan 6 graficos para distintas
    separaciones de n (función separar_datos)
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
            coord_1, coord_2 = separar_datos(df_coord, 1)
            df_tramo, L_total = distancia1(coord_1)
            L_total_1.append(L_total)

            coord_1, coord_2 = separar_datos(df_coord, 2)
            df_tramo, L_total = distancia1(coord_1)
            L_total_2.append(L_total)

            coord_1, coord_2 = separar_datos(df_coord, 5)
            df_tramo, L_total = distancia1(coord_1)
            L_total_5.append(L_total)

            coord_1, coord_2 = separar_datos(df_coord, 9)
            df_tramo, L_total = distancia1(coord_1)
            L_total_9.append(L_total)

            coord_1, coord_2 = separar_datos(df_coord, 13)
            df_tramo, L_total = distancia1(coord_1)
            L_total_13.append(L_total)

            coord_1, coord_2 = separar_datos(df_coord, 20)
            df_tramo, L_total = distancia1(coord_1)
            L_total_20.append(L_total)
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
        bins = 30  # Ajusta el número de bins según sea necesario
        hist, bin_edges = np.histogram(L_total, bins=bins)
        
        # Calcular los centros de los bins
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
        
        # Dibujar el histograma como barras
        plt.bar(bin_centers, hist, width=np.diff(bin_edges), color='blue', edgecolor='blue', alpha=0.7, align='center')
        
        # Dibujar la línea que conecta los máximos de cada bin
        #plt.plot(bin_centers, hist, color='red', marker='o', linestyle='-', linewidth=2)
        
        # Configurar el título y etiquetas
        plt.title(titulo)
        plt.xlabel("Distancia total (m)")
        plt.ylabel("Número de carreras")

    plt.tight_layout()  # Ajustar el espaciado entre subgráficas
    plt.show()


df_coord = leer_datos_gpx('datos/Media_Maratón_Santander_2024.gpx')
df_dist_kalman = calcular_distancias_recursivas(df_coord)
crear_histograma(df_dist_kalman)
