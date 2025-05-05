"""
Script para calcular todo lo realcionado con la altitud
"""
from leer_datos import leer_datos_gpx
from magnitudes import *

#histograma altitud todas las carreras
def histograma_altitud():
    """
    Función que crea un histograma de la altitud de todas las carreras
    """
    import os
    import matplotlib.pyplot as plt
    import pandas as pd

    # Crear una lista para almacenar los datos de altitud
    altitudes = []

    # Bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    for nombre_archivo in os.listdir('datos_altitud'):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            altitud_acumulada, alt_total1, alt_total2, df_tramos = calcular_altitud_y_analizar(f'datos_altitud/{nombre_archivo}')
            # Agregar los datos de altitud a la lista
            altitudes.append(altitud_acumulada)
            print(f"Altitud acumulada de {nombre_archivo}: {altitud_acumulada} m")
            
            df_coord = leer_datos_gpx(f'datos_altitud/{nombre_archivo}')
            print(len(df_coord['elevacion'].tolist()))

    # Crear el histograma de altitud
    # plt.hist(altitudes, bins=50, color='blue', alpha=0.7)
    # plt.title('Histograma de Altitud')
    # plt.xlabel('Altitud (m)')
    # plt.ylabel('Frecuencia')
    
    # # Guardar el histograma en un archivo PNG
    # plt.show()

def altitud_carrera(nombre_archivo):
    """
    Función que calcula la altitud de una carrera
    """
    import matplotlib.pyplot as plt
    import numpy as np
    # Leer archivo gpx
    df_coord = leer_datos_gpx(f'datos_altitud/{nombre_archivo}')
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

#altitud_carrera('11601896081.gpx') #altitud bien
#altitud_carrera('11637916079.gpx') #altitud rara

def comp_alt():
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

