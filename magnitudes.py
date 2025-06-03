"""
Este script está diseñado para analizar datos de una carrera o recorrido obtenidos a partir de coordenadas GPS o similares. 
Su objetivo principal es calcular varias magnitudes físicas y estadísticas relacionadas con el trayecto, tales como:

    1. Cálculo de distancias:
    - Distancia entre puntos consecutivos marcados para identificar tramos relevantes.
    - Distancia total recorrida sumando todos los tramos seleccionados.
    
    2. Análisis de altitud:
    - Cálculo del desnivel positivo acumulado (altitud) a partir de datos de elevación.
    - Filtrado estadístico para identificar valores atípicos en la altitud, usando desviaciones estándar.
    - Análisis y resumen estadístico de la altitud en cada tramo del recorrido.
    
    3. Velocidad media y velocidades instantáneas:
    - Estimación de la velocidad promedio en cada tramo basado en distancias y tiempos.
    - Detección de posibles zonas donde la velocidad cambia abruptamente.
    
    4. Análisis de curvas y ángulos:
    - Cálculo del ángulo entre vectores consecutivos para detectar zonas de curvas o cambios de dirección.
    - Uso del producto escalar para determinar la magnitud del cambio direccional en cada punto.
    
    5. Segmentación y separación de datos:
    - División del conjunto de coordenadas en subconjuntos para análisis más detallados o comparativos.
    - Marcado y filtrado de puntos para seleccionar subconjuntos específicos según criterios definidos.
    
    6. Detección de valores atípicos:
    - Uso del método z-score para detectar puntos o valores que se desvían significativamente del comportamiento esperado.
    
    7. Clasificación del comportamiento del recorrido:
    - Análisis del histograma de distancias entre puntos consecutivos para clasificar el tipo de recorrido (normal, bimodal, extensa).
    - Estimación de parámetros estadísticos relevantes como la desviación estándar para cada tipo de distribución.
    
    8. Cálculo de distancias geométricas:
    - Cálculo de la distancia mínima desde un punto a una línea o segmento, útil para medir desviaciones o errores de posición.
    - Cálculo recursivo de distancias basado en puntos consecutivos para detectar irregularidades en el recorrido.

El script está pensado para trabajar con un DataFrame de pandas que contenga al menos las columnas de coordenadas (x, y), elevación y una columna booleana para marcar puntos relevantes. Cada función es modular y puede aplicarse independientemente, facilitando la extensión o personalización según el análisis requerido.

Este conjunto de herramientas es ideal para estudios de rutas deportivas, senderismo, análisis de recorridos geográficos y cualquier situación donde se requiera un análisis exhaustivo de la distancia, elevación y comportamiento espacial de un trayecto.
"""

import pandas as pd


def distancia(df_coordenadas):
    """
    Función optimizada que calcula la distancia entre puntos marcados como True a partir de las coordenadas x,y.
    Se calcula la distancia entre cada par de puntos marcados como True y se almacena en la columna 'distancia'.
    
    INPUT: df_coordenadas: DataFrame con las coordenadas x,y, elevación y un booleano
    RETURN: distancia_total: distancia total de la carrera en metros
    """
    import numpy as np

    # Inicializar la columna de distancia en 0
    df_coordenadas['distancia'] = 0.0

    # Filtrar el DataFrame para obtener solo las coordenadas marcadas como True
    df_filtrado = df_coordenadas[df_coordenadas['marcado'] == True]

    # Si no hay puntos marcados, retornar 0
    if df_filtrado.empty:
        return 0.0

    # Extraer las coordenadas x e y del DataFrame filtrado
    x_coords = df_filtrado['x'].values
    y_coords = df_filtrado['y'].values

    # Calcular las diferencias entre puntos consecutivos (vectorizado)
    dx = np.diff(x_coords)
    dy = np.diff(y_coords)
    # Calcular las distancias entre puntos consecutivos (vectorizado)
    distancias = np.sqrt(dx**2 + dy**2)

    # Asignar las distancias calculadas al DataFrame filtrado
    df_coordenadas.loc[df_filtrado.index[1:], 'distancia'] = distancias

    # La distancia para el primer punto marcado es 0 (ya inicializado)

    # Calcular la distancia total solo para los puntos marcados
    distancia_total = distancias.sum()

    return distancia_total

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

    #print(f"La altitud total con > 0 es: {altitud_acumulada} m")

    # Análisis de altitudes
    media = df_tramos['altitud_tramo'].mean()
    desviacion_estandar = df_tramos['altitud_tramo'].std()

    # Filtrar tramos donde altitud_tramo > -1sigma
    sigma1 = media - 1 * desviacion_estandar
    alt_tramo1 = df_tramos[df_tramos['altitud_tramo'] > sigma1]
    alt_total1 = alt_tramo1['altitud_tramo'].sum()
    #print(f"La altitud total con > -sigma es: {alt_total1} m")

    # Filtrar tramos donde altitud_tramo > 1sigma
    sigma2 = media + 1 * desviacion_estandar
    alt_tramo2 = df_tramos[df_tramos['altitud_tramo'] > sigma2]
    alt_total2 = alt_tramo2['altitud_tramo'].sum()
    #print(f"La altitud total con > sigma es: {alt_total2} m")

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

def angulo(df_coordenadas):
    """
    Función que detecta zonas de curva en una carrera. Se calcula el ángulo como el producto escalar de dos 
    vectores. 
    INPUT: df_coordenadas: DataFrame con las columnas 'x', 'y', 'elevación' y 'marcado'
    RETURN: df_coordenadas: DataFrame modificado con una nueva columna 'ángulo' en la segunda posición.
    """
    import pandas as pd
    import math 

    # Filtrar solo los puntos marcados como True
    df_coordenadas_filtrado = df_coordenadas[df_coordenadas['marcado'] == True]

    # Extraer las columnas del DataFrame filtrado
    x = df_coordenadas_filtrado['x'].values
    y = df_coordenadas_filtrado['y'].values
    angulos = []

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

    # Añadir la columna de ángulos al DataFrame original
    # Rellenar con NaN para los índices que no tienen ángulo calculado
    df_coordenadas['ángulo'] = 0.0
    df_coordenadas.loc[df_coordenadas_filtrado.index[1:-1], 'ángulo'] = angulos

    return df_coordenadas


def clasificar_histogramas(df, plot=False):
    """
    Clasifica el histograma de las distancias entre puntos consecutivos.

    Parámetros:
        df (pd.DataFrame): DataFrame con columnas 'x' e 'y' representando coordenadas.
        plot (bool): Si True, muestra el histograma con la densidad.

    Retorna:
        str: Tipo de histograma ('normal', 'bimodal', 'extensa')
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.signal import find_peaks
    from scipy.stats import gaussian_kde, kurtosis

    # Calcular distancias entre puntos consecutivos
    dx = df['x'].diff().dropna()
    dy = df['y'].diff().dropna()
    distancias = np.sqrt(dx**2 + dy**2)

    if len(distancias) < 10:
        return 'extensa'  # No hay suficientes datos
    
    # 2. Recorte de outliers extremos
    umbral = np.percentile(distancias, 90)
    distancias_filtradas = distancias[distancias <= umbral]

    if len(distancias_filtradas) < 5:
        return 'extensa'

    # 3. KDE y detección de picos
    kde = gaussian_kde(distancias_filtradas)
    xs = np.linspace(distancias_filtradas.min(), distancias_filtradas.max(), 500)
    density = kde(xs)

    # Detectar picos prominentes
    peaks, properties = find_peaks(density, height=np.max(density)*0.1, distance=10)
    peak_heights = properties['peak_heights']

    # Detectar valles entre los dos picos principales (si los hay)
    if len(peaks) >= 2:
        sorted_idx = np.argsort(peak_heights)[::-1]  # orden descendente
        top_peaks = peaks[sorted_idx[:2]]
        left, right = np.sort(top_peaks)
        valley_region = density[left:right]
        valley_min = np.min(valley_region)
        valley_ratio = valley_min / np.mean(peak_heights[sorted_idx[:2]])
    else:
        valley_ratio = 0


    # --- Clasificación ---
    if len(peaks) == 1:
        clasificacion = 'normal'

        # Calcular sigma directamente para distribución unimodal
        mu = np.mean(distancias_filtradas)
        sigma = np.std(distancias_filtradas)
        #print(f"Sigma estimada (unimodal): {sigma:.4f}")


    elif len(peaks) == 2 and valley_ratio < 0.6:
        clasificacion = 'bimodal'
        # Encontrar el punto de valle entre los dos picos principales
        valley_idx = np.argmin(density[left:right]) + left
        valley_x = xs[valley_idx]

        # Separar los datos según el valle
        grupo1 = distancias_filtradas[distancias_filtradas <= valley_x]
        grupo2 = distancias_filtradas[distancias_filtradas > valley_x]

        # Calcular medias y sigmas individuales
        mu1, sigma1 = np.mean(grupo1), np.std(grupo1)
        mu2, sigma2 = np.mean(grupo2), np.std(grupo2)

        # Proporciones de cada grupo
        w1 = len(grupo1) / (len(grupo1) + len(grupo2))
        w2 = 1 - w1

        # Media total
        mu_total = w1 * mu1 + w2 * mu2

        # Varianza total con la fórmula de mezcla
        var_total = w1 * (sigma1**2 + (mu1 - mu_total)**2) + w2 * (sigma2**2 + (mu2 - mu_total)**2)
        sigma = np.sqrt(var_total)

        # Puedes imprimirla, retornarla o usarla en más análisis
        #print(f"Sigma total estimada (bimodal): {sigma:.4f}")

    else:
        clasificacion = 'extensa'
        # Calcular sigma directa para distribución extensa (sin estructura clara)
        mu = np.mean(distancias_filtradas)
        sigma = np.std(distancias_filtradas)
        #print(f"Sigma estimada (extensa): {sigma:.4f}")


    if plot:
        plt.hist(distancias_filtradas, bins=30, density=True, alpha=0.3, label='Histograma', color='gray')
        plt.plot(xs, density, label='KDE', color='blue')
        plt.plot(xs[peaks], density[peaks], 'ro', label='Picos detectados')
        if len(peaks) >= 2:
            plt.fill_between(xs[left:right], 0, density[left:right], color='orange', alpha=0.2, label='Valle')
        plt.axvline(umbral, color='red', linestyle='--', alpha=0.3, label=f'Corte 90%')
        plt.title(f"Clasificación: {clasificacion}")
        plt.xlabel("Distancia")
        plt.ylabel("Densidad")
        plt.legend()
        plt.show()

    return clasificacion, sigma



## PREPARACIÓN KALMAN

def distancia_punto_a_segmento(p1, p2, p):
    """
    Calcula la distancia mínima desde un punto 'p' hasta el segmento definido por los puntos 'p1' y 'p2'.

    Parámetros:
    - p1: tuple o lista con las coordenadas (x, y) del primer punto del segmento.
    - p2: tuple o lista con las coordenadas (x, y) del segundo punto del segmento.
    - p: tuple o lista con las coordenadas (x, y) del punto desde el cual se calcula la distancia.

    Retorna:
    - distancia mínima (float) entre el punto 'p' y el segmento 'p1-p2'.

    Método:
    - Calcula la proyección ortogonal del punto sobre el segmento.
    - Si la proyección cae fuera del segmento, calcula la distancia a los extremos.
    - Usa álgebra vectorial y normas Euclidianas.
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
    Calcula las distancias desde cada punto en un DataFrame a los segmentos formados por sus dos puntos anteriores.

    Parámetros:
    - df: pandas.DataFrame que contiene al menos las columnas 'x' e 'y' con coordenadas.

    Retorna:
    - pandas.DataFrame con las columnas:
      - 'punto': coordenadas del punto actual.
      - 'distancia': distancia mínima desde este punto al segmento formado por los dos puntos previos.

    Método:
    - Itera desde el tercer punto en adelante.
    - Para cada punto i, calcula la distancia al segmento formado por los puntos i-2 e i-1.
    - Utiliza la función 'distancia_punto_a_segmento' para el cálculo de distancia.
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
    Genera un histograma para analizar la distribución de las distancias calculadas entre puntos y segmentos.

    Parámetros:
    - distancias_df: pandas.DataFrame con al menos la columna 'distancia' que contiene valores numéricos.

    Retorna:
    - Objeto o datos relacionados con el histograma (dependiendo de la implementación, podría ser matplotlib.figure o arrays de frecuencia).

    Método:
    - Calcula la frecuencia de valores de distancia en rangos definidos.
    - Permite visualizar la dispersión o agrupación de distancias.
    - Utilizado para detectar patrones, como agrupaciones, valores atípicos o comportamiento bimodal.
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

