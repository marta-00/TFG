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
    distancia_total = []
    distancia = 0
    contador = 0
    suma_x = 0
    suma_y = 0
    S_array = []
    x_0 = x[0]
    y_0 = y[0]
    i = 2 #tomar 3 puntos
    while i < len(x):
        #print(f"Inicio de iteración: i = {i}")
        if i == 2:
            limite_68_inf = (-1.2305206390463337)
            limite_68_sup =  1.2468331005055695
        else: 
            limite_68_inf = ((i+2)-3) * (-1.2305206390463337)
            limite_68_sup = ((i+2)-3) *  1.2468331005055695

        alpha = math.atan2(y[i] - y_0, x[i] - x_0)
        # print(f"alpha: {alpha}")
        #calcular sumatorios
        suma_x += (x[i-1] - x_0)
        # print(f"sumatorio x: {suma_x}")
        suma_y += (y[i-1] - y_0)
        # print(f"sumatorio y: {suma_y}")

        #calcular S
        S = (np.cos(alpha)) * suma_y - (np.sin(alpha)) * suma_x 
        S_array.append(S)
        # print(f"Iteración {i-1}: D = {D}")

        if S>limite_68_inf and S<limite_68_sup: 
            #es una recta
            distancia = math.sqrt((x[i] - x_0)**2 + (y[i] - y_0)**2)
            #print("RECTA")
            i += 1
        else: 
            #es una curva
            #print("CURVA")
            #calcular distancia linea recta entre (x0,y0) y (xi-1,yi-1)
            distancia_total.append(distancia)

            suma_x = 0
            suma_y = 0
            S = 0
            S_array = []
            x_0 = x[i-1]
            y_0 = y[i-1]

           
           
        #print(f"Fin de iteración: i = {i}")
        
        #print(f"distancia: {distancia}")
    
    distancia_total.append(distancia)
    distancia_carrera = sum(distancia_total)
    return S, S_array, distancia_carrera



# Crear los puntos
# x = np.linspace(0, 3, 4)  # 3 puntos entre 0 y 1
# y = [4,3,6,4]  # 3 puntos entre 0 y 1
# D = algoritmo_simple(x,y)
# print(D)

def variacion_limites():
    limites_sup = []
    limites_inf = []
    i = 2 #tomar 3 puntos
    for i in range(2, 10):
        #print(f"Inicio de iteración: i = {i}")
        if i == 2:
            limite_68_inf = (-1.2305206390463337)
            limite_68_sup =  1.2468331005055695
            limites_inf.append(limite_68_inf)
            limites_sup.append(limite_68_sup)
        else: 
            limite_68_inf = ((i+2)-3) * (-1.2305206390463337)
            limite_68_sup = ((i+2)-3) *  1.2468331005055695
            limites_inf.append(limite_68_inf)
            limites_sup.append(limite_68_sup)
    
    #plot limites vs i
    import matplotlib.pyplot as plt
    plt.plot(range(3, 11), limites_sup, label='limite sup')
    plt.plot(range(3, 11), limites_inf, label='limite inf')
    plt.legend()
    plt.xlabel('número de puntos')
    plt.ylabel('limite')
    plt.title('Variación de los límites para S')
    plt.show()

