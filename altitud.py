"""
Script para calcular todo lo relacionado con la altitud.

Este script contiene funciones que:
- Generan histogramas de altitud para múltiples carreras.
- Calculan y visualizan el perfil de altitud de una carrera específica.
- Comparan métricas de altitud entre varias rutas.
- Representan gráficamente la altitud en función del tiempo.

Requiere módulos personalizados: leer_datos, magnitudes.
Los datos deben estar organizados en carpetas como 'datos_treviso', 'datos_reloj', y 'datos_altitud'.

"""
from leer_datos import *
from magnitudes import *

#histograma altitud todas las carreras
def histograma_altitud():
    """
    Crea un histograma de la altitud acumulada para todas las carreras 
    en la carpeta 'datos_treviso'.

    Inputs:
    - No recibe argumentos, pero lee todos los archivos .gpx de 
    la carpeta 'datos_treviso'.

    Returns:
    - No retorna valores, muestra un histograma en pantalla con 
    los valores de altitud acumulada.
    """
    import os
    import matplotlib.pyplot as plt
    import pandas as pd

    # Crear una lista para almacenar los datos de altitud
    altitudes = []

    # Bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    for nombre_archivo in os.listdir('datos_treviso'):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            altitud_acumulada, alt_total1, alt_total2, df_tramos = calcular_altitud_y_analizar(f'datos_treviso/{nombre_archivo}')
            # Agregar los datos de altitud a la lista
            altitudes.append(altitud_acumulada)
            print(f"Altitud acumulada de {nombre_archivo}: {altitud_acumulada} m")
            
            #df_coord = leer_datos_gpx(f'datos_treviso/{nombre_archivo}')
            #print(len(df_coord['elevacion'].tolist()))

    # Crear el histograma de altitud
    plt.hist(altitudes, bins=50, color='blue', alpha=0.7)
    plt.title('Histograma de Altitud')
    plt.xlabel('Altitud (m)')
    plt.ylabel('Frecuencia')
    
    # Guardar el histograma en un archivo PNG
    plt.show()

def altitud_carrera(nombre_archivo):
    """
    Calcula y grafica las diferencias de altitud registradas en una carrera.

    Inputs:
    - nombre_archivo (str): nombre del archivo .fit de la carpeta 'datos_reloj'.

    Returns:
    - No retorna valores, muestra un histograma y imprime la altitud acumulada.
    """
    import matplotlib.pyplot as plt
    import numpy as np
    # Leer archivo gpx
    df_coord = leer_datos_fit(f'datos_reloj/{nombre_archivo}')
    # Calcular altitud acumulada y total
    altitudes = df_coord['elevacion'].tolist()
    dif = np.diff(altitudes)

    num_bins = int(len(dif)/10)  # Número de bins para el histograma
    #crear histograma
    plt.hist(dif, bins=num_bins, color='blue', alpha=0.7)
    plt.title('Histograma de Altitud')
    plt.xlabel('Altitud (m)')
    plt.ylabel('Frecuencia')
    plt.show()
    altitud_acumulada= sum(altitudes)
    print(f"Altitud acumulada del viaje en avión ({nombre_archivo}): {altitud_acumulada} m")

altitud_carrera('F3RI4309.FIT') #altitud bien
#altitud_carrera('11637916079.gpx') #altitud rara

def comp_alt():
    """
        Compara distintas métricas de altitud de todos los archivos en 'datos_altitud'.
        
        Inputs:
        - No recibe argumentos, pero analiza todos los archivos .gpx en la carpeta 'datos_altitud'.

        Returns:
        - No retorna valores, muestra histogramas comparativos de las métricas de altitud.
    """
    resultados = []
    import os
    for nombre_archivo in os.listdir('datos_altitud'):
            if nombre_archivo.endswith('.gpx'):
                # Leer archivo gpx
                # df_coord = leer_datos_gpx(f'datos/{nombre_archivo}')
                altitud_cero, alt_men, alt_mas, df_tramos = calcular_altitud_y_analizar(f'datos_altitud/{nombre_archivo}')
                
                # Agregar los resultados a la lista
                resultados.append({
                    'nombre_carrera': nombre_archivo,
                    'altitud_cero': altitud_cero,
                    'altitud_sigma': alt_mas,
                    'altitud_men_sigma': alt_men
                })

    resultados_df = pd.DataFrame(resultados)

    #crear histograma
    import matplotlib.pyplot as plt
    bin = int(len(resultados_df['altitud_cero']))
    plt.figure(figsize=(10, 6))
    plt.hist(resultados_df['altitud_cero'], bins=bin, color='blue', alpha=0.4)
    plt.hist(resultados_df['altitud_sigma'], bins=bin, color='green', alpha=0.5)
    plt.hist(resultados_df['altitud_men_sigma'], bins=bin, color='red', alpha=0.5)
    #añadir media
    plt.axvline(resultados_df['altitud_cero'].mean(), color='blue', linestyle='dashed', linewidth=1)
    plt.axvline(resultados_df['altitud_sigma'].mean(), color='green', linestyle='dashed', linewidth=1)
    plt.axvline(resultados_df['altitud_men_sigma'].mean(), color='red', linestyle='dashed', linewidth=1)
    plt.legend(['Altitud > 0', 'Altitud > sigma', 'Altitud > -sigma'])
    plt.xlabel('Altitud (m)')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de Altitud(carrera vertical)')
    plt.grid()
    plt.show()

import matplotlib.pyplot as plt
def movimiento_tiempo(nombre_archivo):
    """
        Representa gráficamente la altitud en función del tiempo transcurrido.

        Inputs:
        - nombre_archivo (str): nombre del archivo .fit de la carpeta 'datos_reloj'.

        Returns:
        - No retorna valores, muestra una gráfica de altitud vs. tiempo.
    """
    # Leer archivo fit
    df_coord = leer_datos_fit(f'datos_reloj/{nombre_archivo}')

    #obtener variables: altitud y tiempo
    altitudes = df_coord['elevacion'].tolist()
    tiempo = df_coord["tiempo"].tolist()

    # Calcular tiempo transcurrido en segundos desde el primer timestamp
    tiempo_inicial = tiempo[0]
    tiempo_transcurrido = [(t - tiempo_inicial).total_seconds() for t in tiempo]

    # Crear la gráfica
    plt.figure(figsize=(12, 6))
    plt.plot(tiempo_transcurrido, altitudes, marker='o', linestyle='-', color='b')
    plt.title('Movimiento de Altitud en Función del Tiempo Transcurrido')
    plt.xlabel('Tiempo transcurrido (s)')
    plt.ylabel('Altitud (m)')
    plt.grid()
    plt.tight_layout()  # Ajustar el layout para que no se solapen elementos
    plt.show()

    
