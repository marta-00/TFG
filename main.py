
from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plot
import numpy as np

def zig_zag (coord):
    """
    Función de dado un array con tres subarrays de coordenadas (x, y, z) lo separa en
    dos arrays, uno con las coordenadas pares y otro con las impares. 
    Con estos datos calcula la distancia de cada tramo y la total con estos nuevos 
    arrays y muestra una figura con tres histogramas.

    INPUT: coordenadas: array con tres subarrays de coordenadas (x, y, z)
    RETURN: None
    """
    # Extraer pares e impares dentro de cada subarray
    coord_pares = [subarray[::2] for subarray in coord]   # Posiciones 0, 2, 4...
    coord_impares = [subarray[1::2] for subarray in coord] # Posiciones 1, 3...

    # calcular distancias con los nuevos arrays
    dist_tramo_pares, dist_total_pares = distancia(coord_pares)
    dist_tramo_impares, dist_total_impares = distancia(coord_impares)
    dist_tramo, dist_total = distancia(coord)

    print(f"Distancia total: {dist_total}")
    print(f"Distancia total pares: {dist_total_pares}")
    print(f"Distancia total impares: {dist_total_impares}")

    # Definir el número de bins de cada histograma
    num_bins = (len(coord[0]))
    num_bins_par = (len(coord_pares[0]))
    num_bins_impar = (len(coord_impares[0]))

    # Crear la figura con 3 subgráficos en una sola columna
    fig, axes = plot.subplots(3, 1, figsize=(8, 12))  # 3 filas, 1 columna

    # Primer histograma
    axes[0].hist(dist_tramo, bins=num_bins, color='blue', edgecolor='black', alpha=0.7)
    axes[0].set_title("Histograma - distancias")

    # Segundo histograma
    axes[1].hist(dist_tramo_pares, bins=num_bins_par, color='green', edgecolor='black', alpha=0.7)
    axes[1].set_title("Histograma - distancias pares")

    # Tercer histograma
    axes[2].hist(dist_tramo_impares, bins=num_bins_impar, color='red', edgecolor='black', alpha=0.7)
    axes[2].set_title("Histograma - distancias impares")

    # Ajustar espaciado entre gráficos
    plot.tight_layout()
    # Maximo de ejes x es el valor maximo 
    axes[0].set_xlim(0, max(dist_tramo))
    axes[1].set_xlim(0, max(dist_tramo_pares))
    axes[2].set_xlim(0, max(dist_tramo_impares))

    # Mostrar gráfico
    plot.show()


#leer_datos_csv('datos/Carrera_de_mañana.gpx.csv')
coord = leer_datos_gpx('datos/Carrera_de_mañana(5).gpx')
zig_zag(coord)


def main():
    # crear archivo csv para almacenar datos
    magnitudes = open('magnitudes.csv', 'w')
    magnitudes.write(f"Nombre,Distancia_total(m),Altitud(m),Velocidad(m/s)\n")

    # bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    import os
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            coord =leer_datos_gpx(f'datos/{nombre_archivo}')
            # print(len(coord[1]))
            dist_tramo,dist_total = distancia(coord)
            alt = altitud(coord)
            magnitudes.write(f"{nombre_archivo},{dist_total},{alt},{0}\n")

            # tratamiento datos distancias_tramo
            # coger datos alternos del array dist_tramo y hacer un histograma con los datos
            # 