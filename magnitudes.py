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
    #plt.show()

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
    # plt.show()

def detectar_atipicos_zscore(datos, umbral=3):
    """
    Función que detecta los valores atípicos de un conjunto de datos utilizando el z-score.
    el z-score se calcula como z = (x - media) / desviación estándar
    INPUT: datos: array con los datos a analizar
           umbral: valor umbral para considerar un valor atípico
    RETURN: atipicos: array con los valores atípicos
    """
    import numpy as np
    media = np.mean(datos)
    std_dev = np.std(datos)
    
    z_scores = [(x, (x - media) / std_dev) for x in datos]
    atipicos = [x for x, z in z_scores if abs(z) > umbral]
    
    return atipicos

def velocidad(distancia_tramo):
    """
    Función que calcula la velocidad instantánea en cada posición. Al no conocer el intervalo de tiempo en el que se han
    tomado los datos o el tiempo total se asume en función del número de datos del archivo: 
        - 7000 - 6000 : toma de medidas cada 1s 
        - 3000 : toma de medidas cada 2s
        - 2000 : toma de medidas cada 3s
        - 1500 : toma de medidas cada 4s
        - 1000 : toma de medidas cada 5s
    INPUT: distancia_tramo: array con las distancias de cada tramo
    RETURN: velocidad: array con las velocidades instantáneas
    """
    # calcular la longitud del array
    longitud = len(distancia_tramo)

    if longitud > 5000:
        intervalo = 1   
        velocidad = [distancia_tramo[i] / intervalo for i in range(longitud)]
    elif longitud >= 3000:
        intervalo = 2
        velocidad = [distancia_tramo[i] / intervalo for i in range(longitud)]
    elif longitud >= 2000:
        intervalo = 3
        velocidad = [distancia_tramo[i] / intervalo for i in range(longitud)]
    elif longitud >= 1500:
        intervalo = 4
        velocidad = [distancia_tramo[i] / intervalo for i in range(longitud)]
    elif longitud >= 900:
        intervalo = 5
        velocidad = [distancia_tramo[i] / intervalo for i in range(longitud)]
    else:
        intervalo = 6
        velocidad = [distancia_tramo[i] / intervalo for i in range(longitud)]
    
    return velocidad

def detectar_curva(coordenadas):
    """
    Función que detecta zonas de curva en una carrera. Se calcula el angulo como el producto escalar de dos 
    vectores. 
    INPUT: coordenadas: array con las coordenadas x,y
    RETURN: angulos: array con los ángulos de las curvas en radianes
    """
    import math
    import numpy as np
    x = coordenadas[0]
    y = coordenadas[1]
    angulos = []
    x_nuevo =[]
    y_nuevo = []
    for i in range(1, len(x) - 1):
        # Vectores entre los puntos (i-1, i) y (i, i+1)
        vector1 = (x[i] - x[i-1], y[i] - y[i-1])
        vector2 = (x[i+1] - x[i], y[i+1] - y[i])

        # Producto escalar de los vectores
        producto_escalar = vector1[0] * vector2[0] + vector1[1] * vector2[1]

        # Magnitudes de los vectores
        magnitud1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
        magnitud2 = math.sqrt(vector2[0]**2 + vector2[1]**2)

        # Calcular el ángulo usando el producto escalar y las magnitudes
        if magnitud1 * magnitud2 != 0:  # Evitar división por cero
            cos_angulo = producto_escalar / (magnitud1 * magnitud2)
            angulo = math.acos(cos_angulo)
            angulos.append(angulo)
        else:
            angulos.append(0)  # Si la magnitud es cero, el ángulo es cero
        
        if angulos[i-1] > 0.5:
            print(f"Curva detectada en el punto {i}")
        else: 
            x_nuevo.append(x[i])
            y_nuevo.append(y[i])
            
    return (x_nuevo,y_nuevo)

    

    
