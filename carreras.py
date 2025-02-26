
from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plt

def una_carrera():
    #leer_datos_csv('datos/Carrera_de_mañana.gpx.csv')
    coord = leer_datos_gpx('datos/Carrera_de_mañana(8).gpx')
    grafico(coord)
    # dist_tramo, dist_total = distancia(coord)

    # # calcular velocidad instantánea
    # velocidades = velocidad(dist_tramo)
    # velocidades = list(set(velocidades)-set(detectar_atipicos_zscore(velocidades)))
    # crear_histogramas(velocidades, nombre1 = "velocidades")

    # # separar datos
    # coord_pares, coord_impares = separar_datos(coord, 5)

    # # obtener distancias_tramo
    # dist_tramo, dist_total = distancia(coord)
    # dist_tramo_par, dist_total_par = distancia(coord_pares)
    # dist_tramo_impar, dist_total_impar = distancia(coord_impares)

    # # crear histograma con las distancias de los tramos
    # # crear_histogramas(dist_tramo, dist_tramo_par, dist_tramo_impar, "total", "pares", "impares")


    # # dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
    # # dist_tramo_par = list(set(dist_tramo_par)-set(detectar_atipicos_zscore(dist_tramo_par)))
    # # dist_tramo_impar = list(set(dist_tramo_impar)-set(detectar_atipicos_zscore(dist_tramo_impar)))


    # dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
    # dist_tramo_par = list(set(dist_tramo_par)-set(detectar_atipicos_zscore(dist_tramo_par)))
    # dist_tramo_impar = list(set(dist_tramo_impar)-set(detectar_atipicos_zscore(dist_tramo_impar)))

    # crear_histogramas(dist_tramo, dist_tramo_par, dist_tramo_impar, "total", "pares", "impares")
    # print(f"distancia total: {dist_total}")
    # print(f"distancia total pares: {dist_total_par}")
    # print(f"distancia total impares: {dist_total_impar}")
    # plt.show()

def total_carreras():
    # leer archivo magnitudes.csv
    import pandas as pd
    magnitudes = pd.read_csv('magnitudes.csv', delimiter=',', encoding='latin1')
    #print(magnitudes)

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
    distancias = magnitudes['Distancia_total(m)']
    distancias_par = magnitudes['Distancia_par(m)']
    distancias_impar = magnitudes['Distancia_impar(m)']

    #calcular error absoluto, dato exacto 21097,5 m
    error_total = abs(distancias - 21097.5)
    error_par = abs(distancias_par - 21097.5)
    error_impar = abs(distancias_impar - 21097.5)

    for i in range(len(error_total)):
        nombre_carrera = magnitudes['Nombre'][i]
        if error_total[i] > error_par[i] and error_total[i] > error_impar[i]:
            print(f"La medida mejora")
        else:
            print(f"la medida empeora para la carrera: {nombre_carrera}")

def main():
    # crear archivo csv para almacenar datos
    import os
    import matplotlib.pyplot as plt
    magnitudes = open('magnitudes.csv', 'w')
    magnitudes.write(f"Nombre,Distancia_total(m),Distancia_par(m),Distancia_impar(m),Altitud(m),Velocidad(m/s)\n")

    #crear carpeta para guardar histogramas de cada carrera
    carpeta_histogramas = 'histogramas_distancia'
    os.makedirs(carpeta_histogramas, exist_ok=True)

    #crear carpeta para guardar histograma velocidad de cada carrera
    carpeta_histogramas_velocidad = 'histogramas_velocidad'
    os.makedirs(carpeta_histogramas_velocidad, exist_ok=True)

    # bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # leer archivo gpx
            coord =leer_datos_gpx(f'datos/{nombre_archivo}')
            # print(len(coord[1])) #debugging

            # calcular magnitudes
            dist_tramo,dist_total = distancia(coord)
            alt = altitud(coord)

            ## DISTANCIAS TRAMO
            #separar datos
            coord_pares, coord_impares = separar_datos(coord, 2)

            #obtener distancias_tramo
            dist_tramo, dist_total = distancia(coord)
            dist_tramo_par, dist_total_par = distancia(coord_pares)
            dist_tramo_impar, dist_total_impar = distancia(coord_impares)

            #eliminar datos atipicos
            dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
            dist_tramo_par = list(set(dist_tramo_par)-set(detectar_atipicos_zscore(dist_tramo_par)))
            dist_tramo_impar = list(set(dist_tramo_impar)-set(detectar_atipicos_zscore(dist_tramo_impar)))

            #crear histogramas
            imagen = crear_histogramas(dist_tramo, dist_tramo_par, dist_tramo_impar, "total", "pares", "impares")

            # añadir a carpeta histogramas
            plt.savefig(f'{carpeta_histogramas}/{nombre_archivo}.png')
            plt.close(imagen)

            ## VELOCIDADES
            #calcular velocidad instantánea
            velocidades = velocidad(dist_tramo)
            velocidades = list(set(velocidades)-set(detectar_atipicos_zscore(velocidades)))
            figura = crear_histogramas(velocidades, nombre1 = "velocidades")

            #añadir a carpeta histogramas_velocidad
            plt.savefig(f'{carpeta_histogramas_velocidad}/{nombre_archivo}.png')
            plt.close(figura)

            ## MAGNITUDES 
            # añadir magnitudes al archivo csv
            magnitudes.write(f"{nombre_archivo},{dist_total},{dist_total_par},{dist_total_impar},{alt},{0}\n")
            
    magnitudes.close()

if __name__ == "__main__":
   
    una_carrera()
