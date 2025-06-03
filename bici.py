"""
Script para el análisis de datos de recorridos en bicicleta a partir de archivos GPX.

Este script incluye funciones para:
- Leer y procesar múltiples archivos GPX con datos de recorridos.
- Detectar y eliminar segmentos curvos y atípicos en las trayectorias.
- Calcular magnitudes como distancia, altitud y velocidad.
- Generar y guardar gráficos de recorrido, histogramas de distancias y velocidades.
- Comparar la variación de la distancia total recorrida al separar los datos en diferentes
  cantidades de segmentos (n) para varias carreras.

Estas herramientas facilitan el análisis y visualización del comportamiento de las rutas
de bicicleta, con énfasis en la segmentación y comparación de recorridos.
"""

from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plt

coord = leer_datos_gpx('datos_bici/Morning_Ride (5).gpx')


def graficos_total_bici():
    """
    Función que crea un archivo CSV y guarda los datos de la distancia total, altitud y velocidad de cada 
    carrera. 
    También guarda todos los gráficos (recorrido, velocidad y distancia) en una carpeta con el nombre de la carrera
    """
    # crear archivo csv para almacenar datos
    import os
    import matplotlib.pyplot as plt
    # magnitudes = open('magnitudes_bici.csv', 'w')
    # magnitudes.write(f"Nombre,Distancia_total(m),Altitud(m),Velocidad(m/s)\n")

    # bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    for nombre_archivo in os.listdir('datos_bici'):
        if nombre_archivo.endswith('.gpx'):
            # leer archivo gpx
            coord =leer_datos_gpx(f'datos_bici/{nombre_archivo}')
            # print(len(coord[1])) #debugging

            #crear una carpeta para guardar los datos de cada carpeta dentro deresultados\carreras con el nombre de la carrera
            carpeta = f'resultados/bici/{nombre_archivo}'
            os.makedirs(carpeta, exist_ok=True)

            ## QUITAR COORDENADAS CURVA
            x_nuevo, y_nuevo = (detectar_curva(coord))
            coord = [x_nuevo, y_nuevo, coord[2]]

            # calcular magnitudes
            dist_tramo, dist_total = distancia(coord)
            alt = altitud(coord)

            ## QUITAR COORDENADAS ATIPICOS
            dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
            
            # RECORRIDO
            graf = grafico(coord)
            plt.savefig(f'{carpeta}/recorrido_sin_curva.png')
            plt.close(graf)

            # DISTANCIAS TRAMO
            dist_td = crear_histogramas(dist_tramo, nombre1 = "distancias_sin_curva_atipicos")
            plt.savefig(f'{carpeta}/distancias_sin_curva_atipicos.png')
            plt.close(dist_td)

            # VELOCIDADES
            # calcular velocidad instantánea
            velocidades = velocidad(dist_tramo)
            figura = crear_histogramas(velocidades, nombre1 = "velocidades_sin_curva_atipicos")
            # añadir a carpeta histogramas_velocidad
            plt.savefig(f'{carpeta}/velocidades_sin_curva_atipicos.png')
            plt.close(figura)

            # MAGNITUDES 
            # añadir magnitudes al archivo csv
            #magnitudes.write(f"{nombre_archivo},{dist_total},{alt},{0}\n")
            
    #magnitudes.close()

def comparación_distancias():
    """
    Función que separa los datos separados n veces y crea un gráfico comparando cómo varía la 
    distancia total de la carrera en función de n. 
    En un mismo gráfico se incluyen 3 carreras distintas para poder compararlas.
    """ 
    coord1 = leer_datos_gpx('datos_bici/Bicicleta_por_la_mañana (1).gpx')
    coord2 = leer_datos_gpx('datos_bici/Bicicleta_por_la_mañana (5).gpx')
    coord3 = leer_datos_gpx('datos_bici/Bicicleta_por_la_mañana (7).gpx')
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
    distancia_triatlon = 40000  # Distancia en metros
    plt.axhline(y=distancia_triatlon, color='red', linestyle='--', label='Triatlón (40 km)')

    plt.title('Comparación de Distancias Totales en Función de n')
    plt.xlabel('Número de Separaciones (n)')
    plt.ylabel('Distancia Total (m)')
    plt.xticks(ticks=range(1, len(distancias_totales) + 1))
    plt.legend(['Bicicleta_por_la_mañana (1)', 'Bicicleta_por_la_mañana (5))', 'Bicicleta_por_la_mañana (7)'])
    plt.grid()
    plt.show()

comparación_distancias()