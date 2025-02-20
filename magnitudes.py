"""
Script para calcular todas las magnitudes:
    - Distancia de cada tramo y distancia total de la carrera
    - Altitud (desnivel positivo acumulado)
    - Velocidad media
"""
from leer_datos import leer_datos_gpx
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
