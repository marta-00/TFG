"""
Script para calcular todas las magnitudes:
    - Distancia de cada tramo y distancia total de la carrera
    - Altitud (desnivel positivo acumulado)
    - Velocidad media
    - grafico en 2D con las coordenadas x,y
    - separación datos 
    - histograma 
"""

def distancia (coordenadas):
    """
    Función que calcula la distancia total de una carrera a partir de las coordenadas x,y.
    Se calcula la distancia en cada tramo de la carrera y se suman todas las distancias.
    INPUT: coordenadas: array con las coordenadas x,y
    RETURN: distancias: array con las distancias de cada tramo de la carrera
            distancia total de la carrera en metros
    """
    import numpy as np
    # Distancia entre dos puntos = sqrt((x2-x1)^2 + (y2-y1)^2)
    # crear array con zeros para almacenar las distancias de cada tramo
    distancias_tramo = [] 
    for i in range(1, len(coordenadas[0])):
        distancias_tramo.append(np.sqrt((coordenadas[0][i] - coordenadas[0][i - 1]) ** 2 +
                                  (coordenadas[1][i] - coordenadas[1][i - 1]) ** 2))

    # Sumar todas las distancias recorridas en cada tramo de la carrera
    distancia_total = sum(distancias_tramo)
    return distancias_tramo, distancia_total

def altitud(coordenadas):
    """
    Función que calcula la altitud (desnivel positivo acumulado). Esto es se suman las
    altitudes subidas pero no se restan las bajadas.
    INPUT: coordenadas: array con las coordenadas x,y y la elevación
    RETURN: altitud: array con el desnivel positivo acumulado en metros
    """
    altitud = 0
    for i in range(1, len(coordenadas[2])):
        if coordenadas[2][i] > coordenadas[2][i-1]:
            altitud += coordenadas[2][i] - coordenadas[2][i-1]
    return altitud

def grafico(coordenadas):
    """
    Función que crea una gráfica en 2d con las coordenadas x,y y lo muestra en pantalla
    INPUT: coordenadas: array con las coordenadas x,y
    """
    # cambiar el eje de coordenadas para que en el eje y el punto mas bajo de la 
    # carrera sea el 0 y lo mismo en el eje x
    x = coordenadas[0] - min(coordenadas[0])
    y = coordenadas[1] - min(coordenadas[1])
    
    # Crear y mostrar una gráfica en 2d con las coordenadas x,y
    import matplotlib.pyplot as plt

    plt.plot(x, y)
    plt.show()

import matplotlib.pyplot as plt

def separar_datos(coordenadas, n_separacion):
    coord_pares = [subarray[::n_separacion] for subarray in coordenadas]   # Posiciones 0, 2, 4...
    coord_impares = [subarray[1::n_separacion] for subarray in coordenadas] # Posiciones 1, 3...
    return coord_pares, coord_impares


def crear_histogramas(array1, array2=None, array3=None, nombre1='Array 1', nombre2='Array 2', nombre3='Array 3'):
    import matplotlib.pyplot as plt
    import math
    # Crear una lista de arrays de datos y sus nombres
    datos = [(array1, nombre1)]
    
    if array2 is not None:
        datos.append((array2, nombre2))
    if array3 is not None:
        datos.append((array3, nombre3))
    
    # Determinar el número de histogramas a crear
    num_histogramas = len(datos)
    
    # Crear una figura con subgráficas
    fig, axs = plt.subplots(1, num_histogramas, figsize=(5 * num_histogramas, 4))
    
    # Si solo hay un conjunto de datos, axs no es un array
    if num_histogramas == 1:
        axs = [axs]
    
    # Crear histogramas para cada conjunto de datos
    for i, (array, nombre) in enumerate(datos):
        num_bins = int(math.sqrt(len(array)))  # Número de bins igual a la raíz cuadrada de la longitud del array
        axs[i].hist(array, bins=num_bins, alpha=0.7, color='blue')
        axs[i].set_title(nombre)
        axs[i].set_xlabel('Valores')
        axs[i].set_ylabel('Frecuencia')
        axs[i].set_xlim(0, max(array) + 1)  # Establecer el límite máximo en función del valor máximo del array
    
    # Ajustar el layout
    plt.tight_layout()
    plt.show()

def detectar_atipicos_zscore(datos, umbral=3):
    import numpy as np
    media = np.mean(datos)
    std_dev = np.std(datos)
    
    z_scores = [(x, (x - media) / std_dev) for x in datos]
    atipicos = [x for x, z in z_scores if abs(z) > umbral]
    
    return atipicos


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

    #print(f"Distancia total: {dist_total}")
    #print(f"Distancia total pares: {dist_total_pares}")
    #print(f"Distancia total impares: {dist_total_impares}")

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
    return fig, dist_tramo_pares, dist_tramo_impares
