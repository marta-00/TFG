"""

"""
from magnitudes import *
from leer_datos import leer_datos_gpx

def grafico(df):
    """
    Función que crea una gráfica en 2D con las coordenadas x, y, elevación y marcado.
    INPUT: df: DataFrame con las columnas x, y, elevación y marcado (booleano).
    """
    import matplotlib.pyplot as plt

    # Calcular el mínimo de las coordenadas x e y
    min_x = df['x'].min()
    min_y = df['y'].min()
    
    # Separar los datos en marcados y no marcados
    marcados = df[df['marcado'] == True]
    no_marcados = df[df['marcado'] == False]

    # Graficar los puntos marcados en azul
    plt.plot(marcados['x'] - min_x, marcados['y'] - min_y, 
             color='blue', label='Marcados', linewidth=2)
    
    # Graficar los puntos no marcados en rojo (scatter)
    plt.scatter(no_marcados['x'] - min_x, no_marcados['y'] - min_y, 
                color='red', label='No Marcados', alpha=0.5)
    
    # Etiquetas y título
    plt.xlabel('Coordenadas X')
    plt.ylabel('Coordenadas Y')
    plt.title('Gráfica de Coordenadas')
    plt.legend()
    plt.grid()
    
    # Mostrar la gráfica
    plt.show()

def crear_histogramas(array1, array2=None, array3=None, nombre1='Array 1', nombre2='Array 2', nombre3='Array 3'):
    """
    Función que crea un histograma con los datos de uno o varios arrays.
    El nombre del array se muestra en el título del histograma.
    INPUTS:     - array1: array con los datos a representar
                - array2: array con los datos a representar
                - array3: array con los datos a representar
                - nombre1: nombre del array 1
                - nombre2: nombre del array 2
                - nombre3: nombre del array 3
    """
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

    def angulo(nombre_dato):
        """
        Función que para una carrera calcula la distancia de cada tramo y el ángulo. 
        Después hace un gráfico comparando ambos(x=angulo, y=distancia)
        INPUT: nombre_dato: string:  nombre completo de la carrera(datos/Carrera_de_mañana(8).gpx)
        """
        import numpy as np
        df_coord = leer_datos_gpx(nombre_dato)
        
        #calcular la distancia de cada tramo
        df_dist, L_total = distancia(df_coord)
        dist_tramo = df_dist['Distancia (m)']
        #print(len(df_dist['Distancia (m)']))  #debugging

        #calcular los ángulos 
        df_angulos = detectar_curva(df_coord)
        angulos = df_angulos['ángulo']
        #print(len(df_angulos['ángulo'])) #debugging

        #pasar los angulos de radianes a grados
        angulos = np.degrees(angulos)

        # Para caluclar las distancias se utilizan 2 puntos y para el ángulo se utilizan 3.
        # Hay 1 dato menos de ángulos que de distancias. 
        # SOLUCIÓN 1: eliminar la última distancia
        # Se va a asignar cada ángulo i a la distancia del tramo de i-1 a i. Por la forma de 
        # calcular los datos, el 1º ángulo corresponde a la 1º distancia.

        # eliminar último dato de df_dist['Distancia (m)]
        dist_tramo = dist_tramo[:-1]
        #print(len(dist_tramo)) #debugging

        # Crear el gráfico comparando ángulos y distancias
        plt.figure(figsize=(10, 6))
        plt.scatter(angulos, dist_tramo, c='blue', alpha=0.5)
        plt.title('Comparación de Ángulos y Distancias')
        plt.xlabel('Ángulo (grados)')
        plt.ylabel('Distancia (m)')
        plt.grid(True)
        plt.show()