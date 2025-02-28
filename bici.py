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
    magnitudes = open('magnitudes_bici.csv', 'w')
    magnitudes.write(f"Nombre,Distancia_total(m),Altitud(m),Velocidad(m/s)\n")

    # bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    for nombre_archivo in os.listdir('datos_bici'):
        if nombre_archivo.endswith('.gpx'):
            # leer archivo gpx
            coord =leer_datos_gpx(f'datos_bici/{nombre_archivo}')
            # print(len(coord[1])) #debugging

            #crear una carpeta para guardar los datos de cada carpeta dentro deresultados\carreras con el nombre de la carrera
            carpeta = f'resultados/bici/{nombre_archivo}'
            os.makedirs(carpeta, exist_ok=True)

            # calcular magnitudes
            dist_tramo, dist_total = distancia(coord)
            alt = altitud(coord)
            
            # ## RECORRIDO
            # graf = grafico(coord)
            # plt.savefig(f'{carpeta}/recorrido.png')
            # plt.close(graf)

            ## DISTANCIAS TRAMO
            dist_td = crear_histogramas(dist_tramo, "distancias")
            plt.savefig(f'{carpeta}/distancias_total_datos.png')
            plt.close(dist_td)

            # # VELOCIDADES
            # # calcular velocidad instantánea
            # velocidades = velocidad(dist_tramo)
            # figura = crear_histogramas(velocidades, nombre1 = "velocidades")
            # #añadir a carpeta histogramas_velocidad
            # plt.savefig(f'{carpeta}/velocidades.png')
            # plt.close(figura)

            # MAGNITUDES 
            # añadir magnitudes al archivo csv
            magnitudes.write(f"{nombre_archivo},{dist_total},{alt},{0}\n")
            
    magnitudes.close()

graficos_total_bici()