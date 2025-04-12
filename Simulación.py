"""
Simulación de un problema más sencillo. Se toman tres puntos equidistantes en una línea recta.
A continuación se añade un ruido gaussiano en la coordenada perpendicular (y) a la línea recta.
Se calcula la distancia total de 3 maneras: 
1. Sumando las distancias entre puntos consecutivos
2. Calculando la distancia entre el primer y el último punto
3. distancia real entre los puntos
"""
from algoritmo import algoritmo_simple
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulacion_recta():
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

def dif_D():
    #crear simulación recta donde va variando el numero de puntos en la simulación (1-5)
    x = np.linspace(0, 80, 9)  # 5 puntos entre 0 y 20
    y = np.zeros(9)

    sigma = 1
    # Añadir ruido gaussiano a las coordenadas x e y
    x += np.random.normal(0, sigma, len(x))
    y += np.random.normal(0, sigma, len(y))

    #calcular D
    D, D_Array = algoritmo_simple(x, y)

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
    plt.ylabel('Diferencia D[i] - D[i-1]')
    plt.title('Diferencia entre D[i] y D[i-1]')
    plt.grid()
    #plt.ylim(-3 * sigma, 3 * sigma)
    plt.show() 
        
dif_D()

def cambio_h():
    for i in range(1000):
        x = np.array([0, 10, 20, 30], dtype=float)
        y = np.array([0, 0, 0, 0], dtype=float)

        # Añadir ruido gaussiano a las coordenadas x e y
        x += np.random.normal(0, 0.1, len(x))
        y += np.random.normal(0, 0.1, len(y))

        D, D_array = algoritmo_simple(x, y)
        