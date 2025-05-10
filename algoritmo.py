import numpy as np
import pandas as pd
import math

# calcular Distancia
# D = (cos(alpha))**2 * sum(y_j-y_0) + (sin(alpha))**2 * sum(x_j-x_0) - 2*sum((x_j-x_0)*(y_j-y_0)*cos(alpha)*sin(alpha))
def algoritmo_D_cuadrado(x,y):
    # definir variables almacenables
    suma_x = 0
    suma_y = 0
    suma_xy = 0
    D_array = []
    i = 2 #tomar 3 puntos
    while i < len(x):
        alpha = math.atan2(y[i] - y[0], x[i] - x[0])
        # print(f"alpha: {alpha}")
        #calcular sumatorios
        suma_x += (x[i-1] - x[0])**2
        # print(f"sumatorio x: {suma_x}")
        suma_y += (y[i-1] - y[0])**2
        # print(f"sumatorio y: {suma_y}")
        suma_xy += (x[i-1] - x[0]) * (y[i-1] - y[0])
        # print(f"sumatorio xy: {suma_xy}")
        #calcular D
        D = (np.cos(alpha))**2 * suma_y + (np.sin(alpha))**2 * suma_x - 2 * suma_xy * np.cos(alpha) * np.sin(alpha)
        D_array.append(D)
        # print(f"Iteración {i-1}: D = {D}")
        i += 1
    return D, D_array

def algoritmo_S(x,y):
    # definir variables almacenables
    suma_x = 0
    suma_y = 0
    S_array = []
    i = 2 #tomar 3 puntos
    while i < len(x):
        #print(f"Inicio de iteración: i = {i}")
        if i == 2:
            limite_68_inf = (-1.2305206390463337)
            limite_68_sup =  1.2468331005055695
        else: 
            limite_68_inf = ((i+2)-3) * (-1.2305206390463337)
            limite_68_sup = ((i+2)-3) *  1.2468331005055695

        alpha = math.atan2(y[i] - y[0], x[i] - x[0])
        # print(f"alpha: {alpha}")
        #calcular sumatorios
        suma_x += (x[i-1] - x[0])
        # print(f"sumatorio x: {suma_x}")
        suma_y += (y[i-1] - y[0])
        # print(f"sumatorio y: {suma_y}")

        #calcular S
        S = (np.cos(alpha)) * suma_y - (np.sin(alpha)) * suma_x 
        S_array.append(S)
        # print(f"Iteración {i-1}: D = {D}")

        if S>limite_68_inf and S<limite_68_sup: 
            #es una recta
            #print(limite_68_inf, limite_68_sup)
            print("RECTA")
   
        else: 
            #es una curva
            #volver a empezar el calculo de S
            #print(limite_68_inf, limite_68_sup)
            print("CURVA")
            suma_x = 0
            suma_y = 0
            S = 0
            S_array = []

        i += 1
        #print(f"Fin de iteración: i = {i}")

    return S, S_array



# Crear los puntos
# x = np.linspace(0, 3, 4)  # 3 puntos entre 0 y 1
# y = [4,3,6,4]  # 3 puntos entre 0 y 1
# D = algoritmo_simple(x,y)
# print(D)

