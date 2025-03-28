import numpy as np
import pandas as pd
import math

# calcular Distancia
# D = (cos(alpha))**2 * sum(y_j-y_0) + (sin(alpha))**2 * sum(x_j-x_0) - 2*sum((x_j-x_0)*(y_j-y_0)*cos(alpha)*sin(alpha))
def algoritmo_simple():
    # Crear los puntos
    x = np.linspace(0, 1, 4)  # 3 puntos entre 0 y 1
    y = [0,1,2,0]  # 3 puntos entre 0 y 1

    # definir variables almacenables
    suma_x = 0
    suma_y = 0
    suma_xy = 0

    i = 2 #tomar 3 puntos
    while i < len(x):
        alpha = math.atan2(y[i] - y[0], x[i] - x[0])
        #calcular sumatorios
        suma_x += x[i-1] - x[0]
        suma_y += y[i-1] - y[0]
        suma_xy += (x[i-1] - x[0]) * (y[i-1] - y[0])
        #calcular D
        D = (np.cos(alpha)**2) * suma_y + (np.sin(alpha)**2) * suma_x - 2 * suma_xy * np.cos(alpha) * np.sin(alpha)
        print(f"Iteración {i-1}: D = {D}")
        i += 1

algoritmo_simple()