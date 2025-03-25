"""
Simulación de un problema más sencillo. Se toman tres puntos equidistantes en una línea recta.
A continuación se añade un ruido gaussiano en la coordenada perpendicular (y) a la línea recta.
Se calcula la distancia total de 3 maneras: 
1. Sumando las distancias entre puntos consecutivos
2. Calculando la distancia entre el primer y el último punto
3. distancia real entre los puntos
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulacion_recta():
    datos = []
    for i in range(10000):
        # Crear los puntos
        x = np.array([0, 10, 20], dtype=float)
        # Añadir ruido gaussiano a las coordenadas x e y
        x += np.random.normal(0, 0.1, 3)
        y = np.array([0, 0, 0]) + np.random.normal(0, 0.1, 3)

        # debugging
        # print(x)
        # print(y)

        #calcular la distancia real(solo coordenada x)
        dist_real = np.sum(np.diff(x))
        # print(dist_real)

        #calcular distancia total entre puntos consecutivos
        dist_consecutivos = np.sum(np.sqrt(np.diff(x)**2 + np.diff(y)**2))
        # print(dist_consecutivos)

        #calcular distancia total entre el primer y el último punto
        dist_primero_ultimo = np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2)
        # print(dist_primero_ultimo)

        #crear dataframe con los datos
        datos.append({
            'L_real': dist_real,
            'L_consecutivos': dist_consecutivos,
            'L_primero_ultimo': dist_primero_ultimo
        })

    df_datos = pd.DataFrame(datos)

    # crear histogramas
    import matplotlib.pyplot as plt 

    plt.figure(figsize=(10, 6))
    plt.hist(df_datos['L_consecutivos'], bins=20, color='red', alpha=0.4, edgecolor='red')
    plt.hist(df_datos['L_primero_ultimo'], bins=20, color='blue', alpha=0.4, edgecolor='blue')

    # añadir media
    plt.axvline(df_datos['L_real'].mean(), color='black', linewidth=1)
    plt.axvline(df_datos['L_consecutivos'].mean(), color='red', linestyle='dashed', linewidth=1)
    plt.axvline(df_datos['L_primero_ultimo'].mean(), color='blue', linestyle='dashed', linewidth=1)

    plt.legend(['Media Real', 'Media Consecutivos', 'Media Primero_ultimo'])
    plt.xlabel('Distancia')
    plt.ylabel('Frecuencia')
    plt.title('Comparación de Histogramas vertical')
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

# Llamar a la función
curva()