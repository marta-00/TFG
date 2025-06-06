"""
Simulación de diferentes escenarios para analizar la estimación de distancias
cuando se añade ruido gaussiano a puntos distribuidos espacialmente.
Se comparan varias formas de calcular la distancia entre puntos:

    1. Suma de distancias entre puntos consecutivos.
    2. Distancia entre el primer y último punto.
    3. Distancia real (ideal sin ruido).
    4. Distancia estimada por diferentes algoritmos personalizados (D y S).
"""
from algoritmo import *
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Simulaciones simples (recta, recta variando sigma y semicírculo)

def simulacion_recta():
    """
    Simula tres puntos equidistantes en una línea recta con ruido gaussiano.
    Compara distintas formas de medir la distancia total.
    """
    np.random.seed(42) 
    datos = []
    for i in range(10000):
        x = np.array([0, 10, 20], dtype=float)
        y = np.array([0, 0, 0], dtype=float)

        #calcular la distancia real(solo coordenada x)
        dist_real = np.sum(np.diff(x))
        # print(dist_real)

        # Añadir ruido gaussiano a las coordenadas x e y
        x += np.random.normal(0, 0.1, len(x))
        y += np.random.normal(0, 0.1, len(y))

        # debugging
        # print(x)
        # print(y)

        #calcular distancia total entre puntos consecutivos
        dist_consecutivos = np.sum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))
        # print(dist_consecutivos)

        #calcular distancia total entre el primer y el último punto
        dist_primero_ultimo = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
        # print(dist_primero_ultimo)

        # calcular distancia usando el algoritmo simple
        D, D_Array = algoritmo_simple(x, y)
        #crear dataframe con los datos
        datos.append({
            'L_real': dist_real,
            'L_consecutivos': dist_consecutivos,
            'L_primero_ultimo': dist_primero_ultimo,
            'D': D
        })

    df_datos = pd.DataFrame(datos)

    # # crear histogramas
    # import matplotlib.pyplot as plt 

    # plt.figure(figsize=(10, 6))
    # plt.hist(df_datos['L_consecutivos'], bins=20, color='red', alpha=0.4, edgecolor='red')
    # plt.hist(df_datos['L_primero_ultimo'], bins=20, color='blue', alpha=0.4, edgecolor='blue')

    # # añadir media
    # plt.axvline(df_datos['L_real'].mean(), color='black', linewidth=1)
    # plt.axvline(df_datos['L_consecutivos'].mean(), color='red', linestyle='dashed', linewidth=1)
    # plt.axvline(df_datos['L_primero_ultimo'].mean(), color='blue', linestyle='dashed', linewidth=1)

    # plt.legend(['Media Real', 'Media Consecutivos', 'Media Primero_ultimo'])
    # plt.xlabel('Distancia')
    # plt.ylabel('Frecuencia')
    # plt.title('Comparación de Histogramas vertical')
    # plt.grid()
    # plt.show()

    #distribución con D
    plt.figure(figsize=(10, 6))
    plt.hist(df_datos['D'], bins=20, color='red', alpha=0.4, edgecolor='red')
    plt.xlabel('Distancia D')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de D')
    plt.grid()
    plt.show()

def sigma():
    """
    Analiza cómo afecta el nivel de ruido (sigma) en las estimaciones de distancia.
    """

    # Definir el rango de valores de sigma
    sigmas = np.arange(0.1, 100, 0.1)

    # Inicializar listas para almacenar los resultados
    L_real_list = []
    L_consecutivos_list = []
    L_primero_ultimo_list = []

    # Número de simulaciones por cada sigma
    num_simulaciones = 1000

    # Generar datos
    for sigma in sigmas:
        L_real_temp = []
        L_consecutivos_temp = []
        L_primero_ultimo_temp = []
        
        for _ in range(num_simulaciones):
            # Crear los puntos
            x = np.array([0, 10, 20], dtype=float) + np.random.normal(0, sigma, 3)
            y = np.array([0, 0, 0]) + np.random.normal(0, sigma, 3)

            # Calcular la distancia real (solo coordenada x)
            dist_real = 20
            L_real_temp.append(dist_real)

            # Calcular distancia total entre puntos consecutivos
            dist_consecutivos = np.sum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))
            L_consecutivos_temp.append(dist_consecutivos)

            # Calcular distancia total entre el primer y el último punto
            dist_primero_ultimo = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
            L_primero_ultimo_temp.append(dist_primero_ultimo)

        # Calcular la media de las distancias para el sigma actual
        L_real_list.append(np.mean(L_real_temp))
        L_consecutivos_list.append(np.mean(L_consecutivos_temp))
        L_primero_ultimo_list.append(np.mean(L_primero_ultimo_temp))

    # Crear un DataFrame con los datos
    df_datos = pd.DataFrame({
        'sigma': sigmas,
        'L_real': L_real_list,
        'L_consecutivos': L_consecutivos_list,
        'L_primero_ultimo': L_primero_ultimo_list
    })

    # ## COMPARACIÓN CON SIGMA
    # Graficar los resultados
    plt.figure(figsize=(12, 6))

    # Graficar L_consecutivos como scatter
    plt.subplot(1, 2, 1)
    plt.scatter(df_datos['sigma'], df_datos['L_consecutivos'], label='L_consecutivos', color='orange', s=1)
    plt.title('Distancia Consecutivos vs Sigma')
    plt.xlabel('Sigma')
    plt.ylabel('L_consecutivos')
    plt.grid()

    # Graficar L_primero_ultimo como scatter
    plt.subplot(1, 2, 2)
    plt.scatter(df_datos['sigma'], df_datos['L_primero_ultimo'], label='L_primero_ultimo', color='green', s=1)
    plt.title('Distancia Primero-Ultimo vs Sigma')
    plt.xlabel('Sigma')
    plt.ylabel('L_primero_ultimo')
    plt.grid()

    plt.tight_layout()
    plt.show()

def curva(): 
    """
    Simula tres puntos sobre una media circunferencia, añade ruido,
    y compara estimaciones de longitud de arco.
    """
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt 

    # Inicializar la lista de datos
    datos = []
    # Definir el número de simulaciones
    num_simulaciones = 10000
    r = 1 # radio de la circunferencia

    # Generar los datos
    for i in range(num_simulaciones):
        # Crear los puntos en la media circunferencia
        theta = np.linspace(0, np.pi, 3)  # 3 puntos entre 0 y pi
        x = np.cos(theta)  # Coordenadas x
        y = np.sin(theta)  # Coordenadas y

        # Añadir ruido gaussiano a las coordenadas x e y
        x_noisy = x + np.random.normal(0, 0.1, 3)
        y_noisy = y + np.random.normal(0, 0.1, 3)

        # Calcular la distancia real sobre la circunferencia
        dist_real = 0
        for j in range(len(theta) - 1):
            delta_theta = theta[j + 1] - theta[j]
            dist_real += r * delta_theta  # Distancia en el arco

        # Calcular distancia total entre puntos consecutivos
        dist_consecutivos = np.sum(np.sqrt(np.diff(x_noisy)**2 + np.diff(y_noisy)**2))

        # Calcular distancia total entre el primer y el último punto
        dist_primero_ultimo = np.sqrt((x_noisy[-1] - x_noisy[0])**2 + (y_noisy[-1] - y_noisy[0])**2)

        # Crear dataframe con los datos
        datos.append({
            'L_real': dist_real,
            'L_consecutivos': dist_consecutivos,
            'L_primero_ultimo': dist_primero_ultimo
        })

    # Crear un DataFrame
    df_datos = pd.DataFrame(datos)

    # Visualizar la media circunferencia
    plt.figure(figsize=(10, 6))
    # Graficar la media circunferencia original sin ruido
    theta_original = np.linspace(0, np.pi, 100)  # Más puntos para una curva suave
    x_original = np.cos(theta_original)
    y_original = np.sin(theta_original)
    plt.plot(x_original, y_original, color='green', label='Media Circunferencia Original')

    # Graficar los puntos con ruido
    for i in range(num_simulaciones):
        theta = np.linspace(0, np.pi, 3)  # 3 puntos en la media circunferencia
        x = np.cos(theta) + np.random.normal(0, 0.1, 3)
        y = np.sin(theta) + np.random.normal(0, 0.1, 3)
        plt.scatter(x, y, color='red', alpha=0.1)  # Puntos con ruido

    # Configurar el gráfico
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Media Circunferencia con Ruido')
    plt.legend()
    plt.grid()
    plt.axis('equal')  # Para mantener la proporción de la circunferencia
    plt.show()

    # Crear histogramas
    plt.figure(figsize=(10, 6))
    plt.hist(df_datos['L_consecutivos'], bins=20, color='red', alpha=0.4, edgecolor='red', label='L_consecutivos')
    plt.hist(df_datos['L_primero_ultimo'], bins=20, color='blue', alpha=0.4, edgecolor='blue', label='L_primero_ultimo')

    # Añadir media
    plt.axvline(df_datos['L_real'].mean(), color='black', linewidth=1, label='Media Real')
    plt.axvline(df_datos['L_consecutivos'].mean(), color='red', linestyle='dashed', linewidth=1, label='Media Consecutivos')
    plt.axvline(df_datos['L_primero_ultimo'].mean(), color='blue', linestyle='dashed', linewidth=1, label='Media Primero_ultimo')

    # Configurar el gráfico
    plt.legend()
    plt.xlabel('Distancia')
    plt.ylabel('Frecuencia')
    plt.title('Comparación de Histogramas')
    plt.grid()
    plt.show()

# Simulación de graficos para la variable D^2

def dif_D():
    """
    Analiza cómo varía la diferencia entre los valores consecutivos del arreglo D² calculado 
    por el algoritmo `algoritmo_D_cuadrado`, cuando se simulan 9 puntos alineados con ruido gaussiano.
    
    Representa gráficamente las diferencias entre D²[i] y D²[i-1] para visualizar su dispersión
    en relación con la desviación estándar (sigma) del ruido.
    """

    #crear simulación recta donde va variando el numero de puntos en la simulación (1-5)
    x = np.linspace(0, 80, 9)  # 5 puntos entre 0 y 20
    y = np.zeros(9)

    sigma = 1
    # Añadir ruido gaussiano a las coordenadas x e y
    x += np.random.normal(0, sigma, len(x))
    y += np.random.normal(0, sigma, len(y))

    #calcular D²
    D, D_Array = algoritmo_D_cuadrado(x, y)

    #calcular diferencia entre D[i] y D[i-1] 
    dif = np.diff(D_Array)
    dif = np.insert(dif, 0, D_Array[0])  # Inserta el primer elemento al inicio


    #representar dif frente a numero de puntos
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(dif) + 1), dif, marker='o', linestyle='-')
    #añadir lineas horizontales en +/- sigma
    plt.axhline(y=sigma, color='r', linestyle='--', label='Sigma')
    plt.axhline(y=-sigma, color='r', linestyle='--')

    plt.xlabel('Número de Puntos')
    plt.ylabel('Diferencia D²[i] - D²[i-1]')
    plt.title('Diferencia entre D²[i] y D²[i-1]')
    plt.grid()
    #plt.ylim(-3 * sigma, 3 * sigma)
    plt.show() 
    
def dif_D_histograma():
    """
    Compara la distribución del valor total de D² normalizado por sigma² para dos configuraciones:
    - 4 puntos (3 segmentos)
    - 8 puntos (7 segmentos)

    Realiza múltiples simulaciones para obtener histogramas de las variaciones y calcular el rango
    del 68% de confianza, luego compara estos límites con el caso de más puntos.
    """
    num_simulaciones = 1000
    sigma = 1
    variaciones = []
    variaciones2 = []
    D_simulaciones = []
    D2_simulaciones = []

    for _ in range(num_simulaciones):
        # Crear simulación con 3 puntos
        x = np.linspace(0, 30, 4)  # 3 puntos entre 0 y 80
        y = np.zeros(4)

        # Añadir ruido gaussiano a las coordenadas x e y
        x += np.random.normal(0, sigma, len(x))
        y += np.random.normal(0, sigma, len(y))

        # Calcular D
        D, D_array = algoritmo_D_cuadrado(x, y, 1)
        D_simulaciones.append(D/sigma**2)
        # Calcular la variación entre D[i] y D[i-1]
        dif = np.diff(D_array)
        if len(dif) > 0:
            variacion = np.sum(dif) / (sigma ** 2)  # Dividir por sigma^2
            variaciones.append(variacion)

        # Crear simulación con 8 puntos
        x2 = np.linspace(0, 70, 8)  # 4 puntos entre 0 y 80
        y2 = np.zeros(8)

        # Añadir ruido gaussiano a las coordenadas x e y
        x2 += np.random.normal(0, sigma, len(x2))
        y2 += np.random.normal(0, sigma, len(y2))

        # Calcular D
        D2, D2_array = algoritmo_D_cuadrado(x2, y2, 1)
        D2_simulaciones.append(D2/sigma**2)
        # Calcular la variación entre D[i] y D[i-1]
        dif2 = np.diff(D2_array)
        if len(dif2) > 0:
            variacion2 = np.sum(dif2) / (sigma ** 2)  # Dividir por sigma^2
            variaciones2.append(variacion2)

    # Calcular la media y desviación estándar
    media = np.mean(variaciones)
    desviacion = np.std(variaciones)

    # Definir límites para el 68%, 95% y 99.7% de los datos
    limite_68_inf = media - desviacion
    limite_68_sup = media + desviacion
    print(limite_68_inf)
    print(limite_68_sup)
    limite_n_inf = (8-4) * limite_68_inf
    limite_n_sup = (8-4) * limite_68_sup

    # Crear histograma
    plt.figure(figsize=(10, 6))
    plt.hist(D2_simulaciones, bins=30, alpha=0.5, color='red', edgecolor='red', label='8 puntos')
    plt.hist(D_simulaciones, bins=30, alpha=0.5, color='blue', label='4 puntos')
    # plt.axvline(limite_68_inf, color='black', linestyle='dashed', linewidth=1)
    # plt.axvline(limite_68_sup, color='black', linestyle='dashed', linewidth=1)
    # plt.axvline(limite_n_inf, color='green', linestyle='dashed', linewidth=1)
    # plt.axvline(limite_n_sup, color='green', linestyle='dashed', linewidth=1)
    plt.ylabel('Frecuencia')
    plt.xlabel('ΔD² / σ²')
    plt.legend()
    plt.title('Histograma de ΔD²(68%)')
    plt.grid()
    plt.show()

def cambio_h():
    """
    Estudia cómo afecta una pequeña elevación (h) en una de las coordenadas Y a la distancia D²
    estimada por el algoritmo `algoritmo_D_cuadrado`.

    Se simulan configuraciones donde se incrementa h en el último punto en pasos crecientes, y
    se analiza el impacto en el valor total de D². Se grafica D² en función de h².
    """

    distancias = []
    for i in np.arange(0, 1, 0.1):
        x = np.array([0, 10, 20, 30], dtype=float)
        y = np.array([0, 0, 0, i], dtype=float)

        np.random.seed(23)
        # Añadir ruido gaussiano a las coordenadas x e y
        x += np.random.normal(0, 0.3, len(x))
        y += np.random.normal(0, 0.3, len(y))

        D, D_array = algoritmo_D_cuadrado(x, y)

        #calcular diferencia D
        dif = np.diff(D_array)

        distancias.append(D)
    
    #crear plot
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(0, 1, 0.1)**2, distancias, marker='o', linestyle='-')
    plt.xlabel('Cambio en h²')
    plt.ylabel('D²')
    plt.title('Cambio en h² vs D²')
    plt.grid()
    plt.show()


# Simulación de graficos para la variable S

def dif_S_histograma():
    """
    Realiza múltiples simulaciones para comparar la distribución de las variaciones del parámetro S,
    normalizadas por sigma, en dos configuraciones:
    - 4 puntos (3 segmentos)
    - 8 puntos (7 segmentos)

    Para cada configuración, genera ruido gaussiano en las coordenadas, calcula S con el algoritmo
    `algoritmo_S` y registra la suma de las diferencias entre valores consecutivos de S. 

    Luego, genera un histograma comparativo para visualizar la frecuencia de estas variaciones en ambas configuraciones.
    """

    num_simulaciones = 1000
    sigma = 1
    variaciones = []
    variaciones2 = []
    S_simulaciones = []
    S2_simulaciones = []
    for _ in range(num_simulaciones):
        # Crear simulación con 4 puntos
        x = np.linspace(0, 30, 4)  # 4 puntos entre 0 y 80
        y = np.zeros(4)

        # Añadir ruido gaussiano a las coordenadas x e y
        x += np.random.normal(0, sigma, len(x))
        y += np.random.normal(0, sigma, len(y))

        # Calcular S
        S, S_Array = algoritmo_S(x, y, 1)
        S_simulaciones.append(S/sigma)
        # print(S_Array)
        # Calcular la variación entre S[i] y S[i-1]
        dif = np.diff(S_Array)
        if len(dif) > 0:
            variacion = np.sum(dif) / (sigma)  # Dividir por sigma
            variaciones.append(variacion)


        # Crear simulación con 8 puntos
        x2 = np.linspace(0, 70, 8)  # 4 puntos entre 0 y 80
        y2 = np.zeros(8)

        # Añadir ruido gaussiano a las coordenadas x e y
        x2 += np.random.normal(0, sigma, len(x2))
        y2 += np.random.normal(0, sigma, len(y2))

        # Calcular S
        S2, S2_Array = algoritmo_S(x2, y2, 1)
        S2_simulaciones.append(S2/sigma)
        # print(S_Array)
        # Calcular la variación entre S[i] y S[i-1]
        dif2 = np.diff(S2_Array)
        if len(dif2) > 0:
            variacion2 = np.sum(dif2) / (sigma)  # Dividir por sigma
            variaciones2.append(variacion2)

    
   # Calcular la media y desviación estándar
    media = np.mean(S_simulaciones)
    desviacion = np.std(S_simulaciones)

    # Definir límites para el 68%, 95% y 99.7% de los datos
    limite_68_inf = media - desviacion
    limite_68_sup = media + desviacion
    print(limite_68_inf)
    print(limite_68_sup)

    limite_n_inf = (10-4) * limite_68_inf
    limite_n_sup = (10-4) * limite_68_sup

    #Crear histograma
    plt.figure(figsize=(10, 6))
    plt.hist(variaciones2, bins=30, alpha=0.5, color='red', edgecolor='red', label='8 puntos')
    plt.hist(variaciones, bins=30, alpha=0.5, color='blue', label='4 puntos')
    # plt.axvline(limite_68_inf, color='black', linestyle='dashed', linewidth=1)
    # plt.axvline(limite_68_sup, color='black', linestyle='dashed', linewidth=1)
    # plt.axvline(limite_n_inf, color='green', linestyle='dashed', linewidth=1)
    # plt.axvline(limite_n_sup, color='green', linestyle='dashed', linewidth=1)
    plt.xlabel('ΔS / σ')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de S')
    plt.legend()
    plt.grid()
    plt.show()


def cambio_h_S():
    """
    Evalúa cómo varía el parámetro S calculado por el algoritmo `algoritmo_S` al modificar el valor
    de h en una secuencia de puntos con ruido gaussiano.

    Se incrementa h en pasos enteros desde 0 hasta 99 y se calcula S para cada configuración, graficando
    la relación entre el cambio en h y el valor resultante de S.
    """
    distancias = []
    for i in np.arange(0, 100, 1):
        x = np.array([0, 10, 20, 30, 40, 50, 60], dtype=float)
        y = np.array([0, 0, 0, 0, 10, 20, 30], dtype=float)

        np.random.seed(23)
        # Añadir ruido gaussiano a las coordenadas x e y
        x += np.random.normal(0, 0.3, len(x))
        y += np.random.normal(0, 0.3, len(y))

        S, S_array = algoritmo_S(x, y)

        #calcular diferencia D
        dif = np.diff(S_array)

        distancias.append(S)
    
    #crear plot
    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(0, 100, 1), distancias, marker='o', linestyle='-')
    plt.xlabel('Cambio en h')
    plt.ylabel('S')
    plt.title('Cambio en h vs S')
    plt.grid()
    plt.show()


# recta + recta con cambio de dirección

def cambio_alfa_curva():
    """
    Simula una curva modificando el ángulo alfa (de 0 a 60 grados) que forman tres puntos consecutivos,
    manteniendo los primeros tres puntos con y=0 y calculando la posición de los tres siguientes en función del ángulo.

    Añade ruido gaussiano a los puntos y calcula el parámetro S con el algoritmo `algoritmo_S` para cada valor
    de alfa. Finalmente, grafica la variación de S en función del ángulo alfa en grados.
    """
    distancias = []
    alfas = []

    # Puntos fijos x para 10 puntos
    x = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90], dtype=float)

    # Primeros tres puntos con y=0
    y = np.zeros(10, dtype=float)

    # Iteramos sobre alfa en radianes 0 a 60 grados
    rango_alfas = np.linspace(0, np.deg2rad(60), 100)

    # Semilla para ruido
    np.random.seed(23)

    for alfa in rango_alfas:
        # Los primeros tres puntos tienen y=0
        y[:3] = 0

        # El punto inicial para los últimos tres es (x[2], y[2]) == (20,0)
        x_base = x[2]
        y_base = y[2]

        # Distancia horizontal entre puntos consecutivos, asumimos 10
        d = 10

        # Calculamos las posiciones y para los últimos tres puntos en función del alfa
        # se alejan formando ese ángulo alfa con la horizontal partiendo desde (x_base, y_base)
        for i in range(3, 6):
            # Incremento horizontal desde el punto base
            dx = d * (i - 2)  # para puntos 3,4,5 son 10,20,30
            # y = y_base + dx * tan(alfa)
            y[i] = y_base + dx * np.tan(alfa)

        # Añadimos ruido gaussiano a x e y (igual para todos los puntos)
        x_noisy = x + np.random.normal(0, 0.3, len(x))
        y_noisy = y + np.random.normal(0, 0.3, len(y))

        D, D_array = algoritmo_S(x, y)
        dif = np.diff(D_array)
        distancias.append(D)
        alfas.append(np.rad2deg(alfa))

    # Graficar S vs alfa
    plt.figure(figsize=(8,5))
    plt.plot(alfas, distancias, marker='o', linestyle='-')
    plt.xlabel('Ángulo Alfa (grados)')
    plt.ylabel(' S')
    plt.title('Variación de S con Alfa (10 puntos)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def cambio_alfa():
    """
    Calcula y grafica la diferencia ΔD² entre valores consecutivos del parámetro D² calculado
    con el algoritmo `algoritmo_D_cuadrado` para un conjunto de puntos donde se modifican
    las alturas h (componentes y) en algunos puntos.

    Muestra cómo varía ΔD² en función del cambio en h (altura).
    """

    distancias = []

    # Puntos fijos x para 6 puntos
    x = np.array([0, 10, 20, 30, 40, 50, 60, 70], dtype=float)

    # Primeros tres puntos con y=0
    y = np.array([0, 0, 0, 10, 20, 30, 40, 50], dtype=float)

    D, D_array = algoritmo_D_cuadrado(x, y)
    
    dif = np.diff(D_array)
    #dif = np.insert(dif, 0, D_array[0]) 
    #print(dif)
    y_values =  y[2:-1]
    #print(y_values)  #debugging

    #mostrar grafico
    plt.figure(figsize=(10, 6))
    plt.plot( y_values, dif, marker='o', linestyle='-')
    plt.xlabel('h')
    plt.ylabel(' ΔD^2')
    plt.title('ΔD^2 en función de h (giro 45º)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# simulacion deteccion curvas

def deteccion_curva():
    """
    Simula una curva con puntos que cambian de dirección y calcula el parámetro S usando `algoritmo_S`.

    Por defecto, simula una línea recta con un cambio de dirección al final (últimos dos puntos elevados),
    añade opcionalmente ruido gaussiano (comentado) y muestra la distancia calculada.

    Se incluye código comentado para generar una curva semicircular con ruido y visualizar los puntos.
    """
    #np.random.seed(42) 
    datos = []
    for i in range(1):
        # SIMULACIÓN RECTA
        x = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80], dtype=float)
        y = np.array([0, 0, 0, 0, 0, 0, 0, 10, 20], dtype=float)

        # Añadir ruido gaussiano a las coordenadas x e y
        #x += np.random.normal(0, 0.5, len(x))
        #y += np.random.normal(0, 0.5, len(y))

        # debugging
        #print(x)
        #print(y)


        # SIMULACIÓN CURVA
        # r = 1.7
        # #Crear los puntos en la media circunferencia
        # theta = np.linspace(0, np.pi, 20)  # 3 puntos entre 0 y pi
        # x = r * np.cos(theta)  # Coordenadas x
        # y = r * np.sin(theta)  # Coordenadas y

        # # Añadir ruido gaussiano a las coordenadas x e y
        # x_noisy = x + np.random.normal(0, 0.1, 20)
        # y_noisy = y + np.random.normal(0, 0.1, 20)

        S, S_array, distancia = algoritmo_S(x,y)
        print(distancia)

        # #dibujar los puntos x,y
        # plt.figure(figsize=(10, 6))
        # plt.plot(x, y, 'o', label='Puntos')
        # #plt.plot(x_noisy, y_noisy, 'x', label='Puntos con Ruido')
        # plt.xlabel('X')
        # plt.ylabel('Y')
        # plt.title('Puntos cambio de dirección')
        # #plt.legend()
        # plt.grid()
        # plt.axis('equal')
        # plt.show()
        
        


    


