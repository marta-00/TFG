"""
Script con el proceso para obtener una sigma estimativa de las carreras reales.

Este script utiliza datos reales de una carrera (en formato GPX) para calcular un parámetro 'S' que mide la desviación de una trayectoria recta.
Luego, compara este valor con resultados simulados en diferentes niveles de ruido (sigma) para estimar la sigma más cercana a la realidad.

Contiene dos funciones principales:
- tramo_recto(): compara el valor S de un tramo recto real con simulaciones para estimar sigma.
- pendiente(): calcula la pendiente de un conjunto de puntos (posiblemente de un tramo de carrera).
"""

from leer_datos import *
from algoritmo import *
import numpy as np
import matplotlib.pyplot as plt


## MÉTODO COMPARACIÓN CON SIMULACIÓN

def tramo_recto(): 
    """
    Selecciona un tramo recto de una carrera (primeros 30 puntos) y compara la desviación (S) calculada 
    con valores simulados con diferentes niveles de ruido (sigma) para estimar una sigma que se asemeje al tramo real.

    Input: None
    Returns: None (solo genera una gráfica comparativa y muestra valores en consola)
    """
    #los primeros 30 datos son rectos. 
    #leer archvio gpx
    df_coord = leer_datos_gpx('datos/Carrera_de_mañana(2).gpx')

    # coger los primeros 30 datos
    df_coord = df_coord.iloc[:30]

    x = df_coord['x'].tolist()
    y = df_coord['y'].tolist()
    # print(x)
    # print(y)

    #calcular la S de los datos reales en línea recta
    S_real, S_array_real, dist = algoritmo_S(x,y)
    #print(S_real)
    print(dist)
    # SIMULACIÓN
    # Parámetros
    n_puntos = 30
    espacio = 3.5  # metros entre puntos
    sigmas = np.arange(0.1, 1.1, 0.1)

    # Almacenar promedio de S por sigma
    S_sim_array = []

    for sigma in sigmas:
        S_vals = []
        
        for _ in range(100):  # 100 simulaciones
            x_sim = np.arange(0, n_puntos * espacio, espacio)
            y_sim = np.linspace(0, -0.1 * x_sim[-1], n_puntos)

            
            # Añadir ruido
            x_sim_noisy = x_sim + np.random.normal(0, sigma, n_puntos)
            y_sim_noisy = y_sim + np.random.normal(0, sigma, n_puntos)
            
            # Calcular S
            S_sim, S_array_sim, dist = algoritmo_S(x_sim_noisy, y_sim_noisy)
            S_vals.append(S_sim)
        
        # Promedio de las 100 simulaciones para esta sigma
        S_sim_array.append(np.mean(S_vals))
    print(dist)
    # Graficar
    plt.plot(sigmas, S_sim_array, label='S simulada (promedio de 100)')
    plt.axhline(y=S_real, color='r', linestyle='--', label='S real')
    plt.xlabel('Sigma')
    plt.ylabel('S')
    plt.title('S vs Sigma (media de 100 simulaciones)')
    plt.legend()
    plt.show()

def pendiente():
    """
    Calcula la pendiente (coeficiente lineal m) de una nube de puntos (X, Y) mediante regresión lineal.

    Input: None (usa vectores X e Y definidos en el cuerpo)
    Returns: None (imprime la pendiente en consola)
    """
    import numpy as np

    X = np.array([434712.92040367285, 434708.3837676649, 434705.95258096093, 434703.4415741465, 434698.73883864784, 434696.879305168, 434691.62859529286, 434689.2017131745, 434686.85572712595, 434683.14312078775, 434682.09147200716, 434676.5819261434, 434674.3136058823, 434672.12618147547, 434666.9337560985, 434664.50256548845, 434662.15119370713, 434656.8918695307, 434654.94820870954, 434649.68349832733, 434648.1410860652, 434646.59867354983, 434642.0652581082, 434640.0396226582, 434634.13204935397, 434631.94354358705, 434629.7550375315, 434626.1880637801, 434624.5647525725, 434618.73483976006])

    Y = np.array([4812388.0666529955, 4812387.444203402, 4812387.023489732, 4812386.714618819, 4812385.649512035, 4812385.7786029475, 4812386.60697391, 4812386.630497891, 4812386.653238572, 4812387.577774913, 4812387.587969857, 4812386.752836692, 4812386.441623726, 4812386.129627166, 4812384.62501703, 4812384.20431828, 4812383.671778027, 4812383.611712835, 4812383.408426142, 4812382.793077045, 4812382.252695501, 4812381.712314307, 4812381.423082976, 4812381.109527377, 4812380.944699949, 4812380.521658493, 4812380.098617746, 4812379.355747202, 4812378.816155933, 4812378.317383337])
    m, b = np.polyfit(X, Y, 1)
    print(f"Pendiente: {m}")

