"""
Módulo para la visualización gráfica de datos de carreras.

Este módulo incluye funciones para:

- Graficar coordenadas X, Y diferenciando entre puntos marcados y no marcados.
- Mostrar visualizaciones parciales o completas de las trayectorias.
- Graficar la relación entre el ángulo de curva y la distancia de cada tramo
  para análisis de comportamiento en las carreras.

Funciones principales:

- grafico1(df): grafica toda la trayectoria desplazando las coordenadas para que empiecen en (0,0).
- grafico(df): grafica solo los primeros 1000 puntos sin desplazamiento.
- graf_angulo_dist(df_coord): grafica la relación entre ángulo (en grados) y distancia del tramo.

Todas las funciones esperan un DataFrame con columnas mínimas ['x', 'y', 'marcado'], y para
graf_angulo_dist se espera que el DataFrame contenga datos válidos para calcular distancias y ángulos.
"""

from magnitudes import *
from leer_datos import leer_datos_gpx

def grafico1(df):
    """
    Crea una gráfica 2D de coordenadas X e Y ajustadas para empezar en el origen.
    Diferencia puntos marcados (azul) y no marcados (rojo).
    
    INPUT:
        df: DataFrame con columnas 'x', 'y', y 'marcado' (booleano).
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

def grafico(df):
    """
    Crea una grafica con la relación entre ángulo (grados) y distancia (metros) de los tramos de una carrera.
    
    INPUT:
        df_coord: DataFrame con datos de la carrera, debe incluir columna 'marcado' para filtrar datos válidos.
    """
    import matplotlib.pyplot as plt
    
    # Seleccionar solo los primeros 1000 datos
    df = df.head(1000)

    # Separar los datos en marcados y no marcados
    marcados = df[df['marcado'] == True]
    no_marcados = df[df['marcado'] == False]

    # Graficar los puntos marcados en azul
    plt.scatter(marcados['x'], marcados['y'], 
             color='blue', label='Marcados', alpha=0.5)
    
    # Graficar los puntos no marcados en rojo (scatter)
    plt.scatter(no_marcados['x'], no_marcados['y'], 
                color='red', label='No Marcados', alpha=0.5)
    
    # Etiquetas y título
    plt.xlabel('Coordenadas X')
    plt.ylabel('Coordenadas Y')
    plt.title('Gráfica de Coordenadas')
    plt.legend()
    plt.grid()
    
    # Mostrar la gráfica
    plt.show()

def graf_angulo_dist(df_coord):
    """
    Función que para una carrera calcula la distancia de cada tramo y el ángulo. 
    Después hace un gráfico comparando ambos(x=angulo, y=distancia)
    INPUT: nombre_dato: string:  nombre completo de la carrera(datos/Carrera_de_mañana(8).gpx)
    """
    import matplotlib.pyplot as plt
    import numpy as np

    # Filtrar solo los puntos marcados como True
    df_coord_filtrado = df_coord[df_coord['marcado'] == True]

    # Calcular la distancia de cada tramo
    df_dist, L_total = distancia(df_coord_filtrado)
    dist_tramo = df_dist['Distancia (m)']
    #print(len(df_dist['Distancia (m)']))  #debugging

    # Calcular los ángulos 
    df_angulos = detectar_curva(df_coord_filtrado)
    angulos = df_angulos['ángulo']
    #print(len(df_angulos['ángulo'])) #debugging

    # Pasar los ángulos de radianes a grados
    angulos = np.degrees(angulos)

    # Para calcular las distancias se utilizan 2 puntos y para el ángulo se utilizan 3.
    # Hay 1 dato menos de ángulos que de distancias. 
    # SOLUCIÓN : eliminar la última distancia
    # Se va a asignar cada ángulo i a la distancia del tramo de i-1 a i. Por la forma de 
    # calcular los datos, el 1º ángulo corresponde a la 1º distancia.

    # Eliminar último dato de df_dist['Distancia (m)']
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