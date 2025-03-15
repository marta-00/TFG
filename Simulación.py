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

datos = []
for i in range(10000):
    # Crear los puntos
    x = np.array([0, 1, 2], dtype=float)
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
