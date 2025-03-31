"""
Script para calcular todas las magnitudes:
    - Distancia de cada tramo y distancia total de la carrera
    - Altitud (desnivel positivo acumulado)
    - Velocidad media
    - separación datos 
Todas las funciones reciben un df_coordenadas(leer_datos) y devuelven un dataframe.
"""

def distancia(df_coordenadas):
    """
    Función que calcula la distancia total de una carrera a partir de las coordenadas x,y.
    Se calcula la distancia en cada tramo de la carrera y se suman todas las distancias.
    
    INPUT: df_coordenadas: DataFrame con las coordenadas x,y, elevación y un booleano
    RETURN: df_tramos: DataFrame con la información de cada tramo de la carrera
            distancia_total: distancia total de la carrera en metros
    """
    import pandas as pd
    import numpy as np
    # Filtrar el DataFrame para obtener solo las coordenadas marcadas como True
    df_filtrado = df_coordenadas[df_coordenadas['marcado'] == True]

    # Crear lista para almacenar la información de cada tramo
    tramos_info = [] 
    
    # Extraer las coordenadas x e y del DataFrame filtrado
    x_coords = df_filtrado['x'].values
    y_coords = df_filtrado['y'].values

    # Calcular la distancia entre cada par de puntos
    for i in range(1, len(x_coords)):
        x1, y1 = x_coords[i - 1], y_coords[i - 1]
        x2, y2 = x_coords[i], y_coords[i]
        
        distancia_tramo = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        
        # Almacenar la información del tramo
        tramos_info.append({
            'Punto Inicial': (x1, y1),
            'Punto Final': (x2, y2),
            'Distancia (m)': distancia_tramo
        })

    # Sumar todas las distancias recorridas en cada tramo de la carrera
    distancia_total = sum(tramo['Distancia (m)'] for tramo in tramos_info)

    # Crear un DataFrame a partir de la lista de tramos
    df_tramos = pd.DataFrame(tramos_info)

    return df_tramos, distancia_total


def altitud1(df_coordenadas):
    """
    Función que calcula la altitud (desnivel positivo acumulado). Esto es se suman las
    altitudes subidas pero no se restan las bajadas.
    INPUT: df_coordenadas: DataFrame con las columnas 'x', 'y', 'elevación' y 'marcado'
    RETURN: altitud: float, el desnivel positivo acumulado en metros
            df_tramos: DataFrame con los puntos i-1, i y la altitud del tramo
    """
    import pandas as pd

    altitud_acumulada = 0
    elevaciones = df_coordenadas['elevacion'].values  # Extraer la columna de elevación
    altitud_tramo = []
    tramos = []

    for i in range(1, len(elevaciones)):
        if elevaciones[i] > elevaciones[i-1]:
            altitud_tramo.append(elevaciones[i] - elevaciones[i-1])
            altitud_acumulada += elevaciones[i] - elevaciones[i-1]
            # Guardar los puntos i-1 y i junto con la altitud del tramo
            tramos.append({
                'punto_i-1_x': df_coordenadas['x'].iloc[i-1],
                'punto_i-1_y': df_coordenadas['y'].iloc[i-1],
                'punto_i_x': df_coordenadas['x'].iloc[i],
                'punto_i_y': df_coordenadas['y'].iloc[i],
                'altitud_tramo': elevaciones[i] - elevaciones[i-1]
            })
        else: # Si la altitud no sube, no se añade a la altitud acumulada
            altitud_tramo.append(elevaciones[i] - elevaciones[i-1])
            # Guardar los puntos i-1 y i junto con la altitud del tramo
            tramos.append({
                'punto_i-1_x': df_coordenadas['x'].iloc[i-1],
                'punto_i-1_y': df_coordenadas['y'].iloc[i-1],
                'punto_i_x': df_coordenadas['x'].iloc[i],
                'punto_i_y': df_coordenadas['y'].iloc[i],
                'altitud_tramo': elevaciones[i] - elevaciones[i-1]
            })

    # Crear un DataFrame a partir de la lista de tramos
    df_tramos = pd.DataFrame(tramos)

    return altitud_acumulada, df_tramos

import pandas as pd

def calcular_altitud_y_analizar(gpx_file):
    """
    Función que calcula la altitud (desnivel positivo acumulado) y realiza un análisis
    de las altitudes de los tramos. Esto incluye calcular la media, desviación estándar,
    y filtrar tramos según condiciones específicas.
    
    INPUT: gpx_file: str, ruta al archivo GPX que contiene las coordenadas.
    RETURN: altitud_acumulada: float, el desnivel positivo acumulado en metros
            alt_total1: float, la altitud total con > -sigma
            alt_total2: float, la altitud total con > sigma
            df_tramos: DataFrame con los puntos i-1, i y la altitud del tramo
    """
    from leer_datos import leer_datos_gpx
    # Leer los datos del archivo GPX
    df_coordenadas = leer_datos_gpx(gpx_file)

    # Calcular la altitud acumulada y los tramos
    altitud_acumulada = 0
    elevaciones = df_coordenadas['elevacion'].values
    altitud_tramo = []
    tramos = []

    for i in range(1, len(elevaciones)):
        diferencia = elevaciones[i] - elevaciones[i-1]
        if diferencia > 0:
            altitud_acumulada += diferencia
        altitud_tramo.append(diferencia)
        tramos.append({
            'punto_i-1_x': df_coordenadas['x'].iloc[i-1],
            'punto_i-1_y': df_coordenadas['y'].iloc[i-1],
            'punto_i_x': df_coordenadas['x'].iloc[i],
            'punto_i_y': df_coordenadas['y'].iloc[i],
            'altitud_tramo': diferencia
        })

    # Crear un DataFrame a partir de la lista de tramos
    df_tramos = pd.DataFrame(tramos)

    print(f"La altitud total con > 0 es: {altitud_acumulada} m")

    # Análisis de altitudes
    media = df_tramos['altitud_tramo'].mean()
    desviacion_estandar = df_tramos['altitud_tramo'].std()

    # Filtrar tramos donde altitud_tramo > -1sigma
    sigma1 = media - 1 * desviacion_estandar
    alt_tramo1 = df_tramos[df_tramos['altitud_tramo'] > sigma1]
    alt_total1 = alt_tramo1['altitud_tramo'].sum()
    print(f"La altitud total con > -sigma es: {alt_total1} m")

    # Filtrar tramos donde altitud_tramo > 1sigma
    sigma2 = media + 1 * desviacion_estandar
    alt_tramo2 = df_tramos[df_tramos['altitud_tramo'] > sigma2]
    alt_total2 = alt_tramo2['altitud_tramo'].sum()
    print(f"La altitud total con > sigma es: {alt_total2} m")

    return altitud_acumulada, alt_total1, alt_total2, df_tramos

def separar_datos(df_coordenadas, n_separacion):
    """
    Función que separa las coordenadas x e y de un DataFrame en listas según el número de separación especificado,
    marca como False las coordenadas no incluidas en el array actual y calcula la distancia.

    INPUT: df_coordenadas: DataFrame con las columnas x, y, elevacion y marcado
           n_separacion: número de separación para seleccionar las coordenadas
    RETURN: coord_list: lista de listas de coordenadas x e y separadas
            distancias: lista de distancias calculadas para cada conjunto de coordenadas
    """
    # Extraer las columnas x e y
    x_coords = df_coordenadas['x'].values
    y_coords = df_coordenadas['y'].values

    coord_list = []
    dist_total = []

    # Crear listas para cada índice de separación
    for start in range(n_separacion):
        coord = []
        # Marcar todas las coordenadas como False
        df_coordenadas['marcado'] = False
        
        for i in range(start, len(x_coords), n_separacion):
            coord.append((x_coords[i], y_coords[i]))  # Agregar tupla (x, y)
            df_coordenadas.at[i, 'marcado'] = True  # Marcar como True las coordenadas seleccionadas
        
        coord_list.append(coord)
        
        # Calcular distancias solo para las coordenadas marcadas
        df_tramos, L_total = distancia(df_coordenadas)
        dist_total.append(L_total)

    return coord_list, dist_total

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

def detectar_curva(df_coordenadas):
    """
    Función que detecta zonas de curva en una carrera. Se calcula el ángulo como el producto escalar de dos 
    vectores. 
    INPUT: df_coordenadas: DataFrame con las columnas 'x', 'y', 'elevación' y 'marcado'
    RETURN: (x_nuevo, y_nuevo, df_angulos): tupla con las coordenadas x e y de los puntos que cumplen la condición
            y un DataFrame con las coordenadas (x, y) y los ángulos calculados.
    """
    import pandas as pd
    import math 
    # Filtrar solo los puntos marcados como True
    df_coordenadas_filtrado = df_coordenadas[df_coordenadas['marcado'] == True]

   # Extraer las columnas del DataFrame filtrado
    x = df_coordenadas_filtrado['x'].values
    y = df_coordenadas_filtrado['y'].values
    angulos = []
    coordenadas = []  # Para almacenar las coordenadas (x, y)
    angulos_calculados = []  # Para almacenar los ángulos calculados

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
            # Asegurarse de que cos_angulo esté en el rango [-1, 1]
            cos_angulo = max(-1, min(1, cos_angulo))
            angulo = math.acos(cos_angulo)
            angulos.append(angulo)
        else:
            angulos.append(0)  # Si la magnitud es cero, el ángulo es cero
        
        # Guardar las coordenadas (x, y) y el ángulo calculado
        coordenadas.append((x[i], y[i]))
        angulos_calculados.append(angulos[i-1])
    
    # Crear un DataFrame con las coordenadas (x, y) y los ángulos
    df_angulos = pd.DataFrame({
        'x': [coord[0] for coord in coordenadas],
        'y': [coord[1] for coord in coordenadas],
        'ángulo': angulos_calculados
    })
    
    return (df_angulos)

## PREPARACIÓN KALMAN

def distancia_punto_a_segmento(p1, p2, p):
    """
    Calcula la distancia mínima desde el punto p a la línea definida por los puntos p1 y p2.
    """
    import numpy as np
    # Vector del segmento
    segment_vector = np.array(p2) - np.array(p1)
    # Vector desde p1 a p
    point_vector = np.array(p) - np.array(p1)
    
    # Proyección del punto sobre el segmento
    segment_length_squared = np.dot(segment_vector, segment_vector)
    if segment_length_squared == 0:
        # p1 y p2 son el mismo punto
        return np.linalg.norm(point_vector)
    
    t = np.dot(point_vector, segment_vector) / segment_length_squared
    t = max(0, min(1, t))  # Limitar t a [0, 1]
    
    # Punto más cercano en el segmento
    closest_point = p1 + t * segment_vector
    return np.linalg.norm(closest_point - np.array(p))

def calcular_distancias_recursivas(df):
    """
    Calcula las distancias desde cada punto a los segmentos formados por los dos puntos anteriores.
    INPUT: df: DataFrame con las columnas x, y.
    OUTPUT: DataFrame con las distancias.
    """
    import pandas as pd
    distancias = []
    
    # Iterar sobre los puntos en el DataFrame
    for i in range(2, len(df)):
        p1 = (df.iloc[i-2]['x'], df.iloc[i-2]['y'])  # Primer punto
        p2 = (df.iloc[i-1]['x'], df.iloc[i-1]['y'])  # Segundo punto
        p = (df.iloc[i]['x'], df.iloc[i]['y'])        # Tercer punto
        
        # Calcular la distancia del punto p al segmento p1-p2
        distancia = distancia_punto_a_segmento(p1, p2, p)
        distancias.append({'punto': p, 'distancia': distancia})
    
    return pd.DataFrame(distancias)

def crear_histograma(distancias_df):
    """
    Crea un histograma de las distancias calculadas.
    INPUT: distancias_df: DataFrame con las distancias.
    """
    import matplotlib.pyplot as plt
    import math
    bin_num = int((len(distancias_df['distancia'])))
    plt.figure(figsize=(10, 6))
    plt.hist(distancias_df['distancia'], bins=bin_num, color='blue', alpha=0.7)
    plt.title('Histograma de Distancias a Segmentos')
    plt.xlabel('Distancia')
    plt.ylabel('Frecuencia')
    plt.grid()
    plt.show()