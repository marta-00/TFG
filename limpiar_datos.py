
from leer_datos import leer_datos_gpx
from magnitudes import *
from graficos import *
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import numpy as np

def datos_total_carreras(nombre_carpeta):
    """
    Función que crea un DataFrame con los datos de la distancia total y altitud de cada 
    carrera. 
    También guarda todos los gráficos (recorrido, velocidad y distancia) en una carpeta con el nombre de la carrera.
    RETURN: DataFrame con los valores de nombre carrera, distancia total y altitud.
    """
    # Crear una lista para almacenar los resultados
    resultados = []

    # Bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    for nombre_archivo in os.listdir(nombre_carpeta):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            df_coord = leer_datos_gpx(f'{nombre_carpeta}/{nombre_archivo}')

            # Calcular magnitudes
            dist_tramo, dist_total = distancia(df_coord)
            alt = altitud(df_coord)

            # Agregar los resultados a la lista
            resultados.append({
                'nombre_carrera': nombre_archivo,
                'distancia_total': dist_total,
                'altitud': alt
            })

            # Aquí puedes agregar el código para guardar gráficos si es necesario
            # plt.savefig(f'graficos/{nombre_archivo}.png')  # Ejemplo de cómo guardar gráficos

    # Convertir la lista de resultados a un DataFrame
    resultados_df = pd.DataFrame(resultados)

    return resultados_df

def limpiar_y_marcar_datos1(nombre_dato):
    """
    Función que limpia los datos de un DataFrame eliminando las filas con valores atípicos.
    Se considera que un valor es atípico si:
        - la distancia de un tramo está a más de 3 desviaciones estándar de la media. Se elimina
          el punto final de ese tramo.
        - La distancia de un tramo está a más de 1 desviación estándar de la media y el ángulo es
          mayor a 20 grados.
    INPUT: nombre_dato: string: nombre completo de la carrera (datos/Carrera_de_mañana(8).gpx)
    RETURN: df_coord: DataFrame: DataFrame con los datos de la carrera limpios.
    """
    # Leer los datos
    df_coord = leer_datos_gpx(nombre_dato)

    # Calcular distancia tramo y total
    df_dist, L_total = distancia(df_coord)
    # print("Distancia total:", L_total)

    # Obtener las distancias de los tramos
    L_tramo = df_dist['Distancia (m)']

    # Marcar puntos atípicos basados en distancia
    for _ in range(3):  # Ejecutar el proceso 3 veces
        media = L_tramo.mean()
        desviacion_estandar = L_tramo.std()

        # Definir los umbrales para puntos atípicos
        umbral_superior = media + 2 * desviacion_estandar
        umbral_inferior = media - 2 * desviacion_estandar

        # Encontrar todos los índices donde la distancia es mayor al umbral superior o menor al umbral inferior
        indices_atipicos = [i for i in range(len(L_tramo)) if L_tramo[i] > umbral_superior or L_tramo[i] < umbral_inferior]

        if not indices_atipicos:
            break  # Salir del bucle si no hay más puntos atípicos

        puntos_a_marcar = set()
        for i in indices_atipicos:
            # Obtener las coordenadas del punto final para esta distancia
            p_final_x = df_dist['Punto Final'][i][0]
            p_final_y = df_dist['Punto Final'][i][1]

            # Agregar las coordenadas finales al conjunto
            puntos_a_marcar.add((p_final_x, p_final_y))

        # Marcar como False los puntos obtenidos en la variable df_coord
        df_coord.loc[df_coord[['x', 'y']].apply(tuple, axis=1).isin(puntos_a_marcar), 'marcado'] = False

        # Actualizar L_tramo después de marcar los puntos
        df_dist, L_total = distancia(df_coord)
        L_tramo = df_dist['Distancia (m)']
    # print("Distancia total después de limpiar distancias:", L_total)
    # Calcular los ángulos 
    df_angulos = detectar_curva(df_coord)
    angulos = df_angulos['ángulo']

    # Pasar los ángulos de radianes a grados
    angulos = np.degrees(angulos)

    # Eliminar el último dato de dist_tramo
    dist_tramo = df_dist['Distancia (m)'][:-1]

    # Calcular la media y la desviación estándar de las distancias
    media_distancia = dist_tramo.mean()
    desviacion_estandar_distancia = dist_tramo.std()

    # Definir el umbral para la distancia
    umbral_superior = media_distancia + 1 * desviacion_estandar_distancia

    # Verificar las condiciones y marcar las coordenadas finales
    for i in range(len(dist_tramo)):
        if dist_tramo[i] > umbral_superior and angulos[i] > 20:
            # Marcar la coordenada final del tramo como False
            if i + 1 < len(df_coord):  # Asegurarse de que no se salga del índice
                df_coord.at[i + 1, 'marcado'] = False

    # print("Distancia total después de limpiar ángulos:", distancia(df_coord)[1])

    return df_coord

import pandas as pd
import numpy as np

def limpiar_y_marcar_datos(nombre_dato):
    """
    Función que limpia los datos de un DataFrame eliminando las filas con valores atípicos.
    Se considera que un valor es atípico si:
        - la distancia de un tramo está a más de 3 desviaciones estándar de la media. Se elimina
          el punto final de ese tramo.
    INPUT: nombre_dato: string: nombre completo de la carrera (datos/Carrera_de_mañana(8).gpx)
    RETURN: df_coord: DataFrame: DataFrame con los datos de la carrera limpios.
    """
    # Leer los datos
    df_coord = leer_datos_gpx(nombre_dato)
    
    # Calcular distancia tramo y total
    df_dist, L_total = distancia(df_coord)
    L_tramo = df_dist['Distancia (m)']
    # print(f"La distancia total: {L_total}")

    # Calcular la media y desviación estándar
    media = L_tramo.mean()
    desviacion_estandar = L_tramo.std()

    # Definir los umbrales para puntos atípicos
    umbral_superior = media + 4 * desviacion_estandar

    # mirar puntos uno a uno
    i = 0
    while i < len(L_tramo):
        if L_tramo[i] > umbral_superior:
            # Coordenadas a marcar
            p_final_x = df_dist['Punto Final'][i][0]
            p_final_y = df_dist['Punto Final'][i][1]
            
            # Marcar como False los puntos obtenidos en la variable df_coord
            df_coord.loc[(df_coord['x'] == p_final_x) & (df_coord['y'] == p_final_y), 'marcado'] = False

            # Actualizar L_tramo después de marcar los puntos
            df_dist, L_total = distancia(df_coord)
            L_tramo = df_dist['Distancia (m)']

            # Calcular la media y desviación estándar
            media = L_tramo.mean()
            desviacion_estandar = L_tramo.std()

            # Actualizar umbral para puntos atípicos
            umbral_superior = media + 4 * desviacion_estandar

            #reiniciar el bucle
            i=0

        else:
            i += 1
            
    return df_coord


def limpiar_y_marcar_datos5(nombre_dato):
    """
    Función que limpia los datos de un DataFrame eliminando las filas con valores atípicos.
    Se considera que un valor es atípico si:
        - la distancia de un tramo está fuera de los límites definidos por el rango intercuartílico (IQR).
    INPUT: nombre_dato: string: nombre completo de la carrera (datos/Carrera_de_mañana(8).gpx)
    RETURN: df_coord: DataFrame: DataFrame con los datos de la carrera limpios.
    """
    # Leer los datos
    df_coord = leer_datos_gpx(nombre_dato)
    
    # Calcular distancia tramo y total
    df_dist, L_total = distancia(df_coord)
    L_tramo = df_dist['Distancia (m)']

    # Calcular Q1, Q3 y IQR
    Q1 = L_tramo.quantile(0.25)
    Q3 = L_tramo.quantile(0.75)
    IQR = Q3 - Q1

    # Definir los umbrales para puntos atípicos
    umbral_inferior = Q1 - 1.5 * IQR
    umbral_superior = Q3 + 1.5 * IQR

    # Mirar puntos uno a uno
    i = 0
    while i < len(L_tramo):
        if L_tramo[i] < umbral_inferior or L_tramo[i] > umbral_superior:
            # Coordenadas a marcar
            p_final_x = df_dist['Punto Final'][i][0]
            p_final_y = df_dist['Punto Final'][i][1]
            
            # Marcar como False los puntos obtenidos en la variable df_coord
            df_coord.loc[(df_coord['x'] == p_final_x) & (df_coord['y'] == p_final_y), 'marcado'] = False

            # Actualizar L_tramo después de marcar los puntos
            df_dist, L_total = distancia(df_coord)
            L_tramo = df_dist['Distancia (m)']

            # Recalcular Q1, Q3 y IQR
            Q1 = L_tramo.quantile(0.25)
            Q3 = L_tramo.quantile(0.75)
            IQR = Q3 - Q1

            # Actualizar umbrales para puntos atípicos
            umbral_inferior = Q1 - 1.5 * IQR
            umbral_superior = Q3 + 1.5 * IQR

            # Reiniciar el bucle
            i = 0
        else:
            i += 1
            
    return df_coord

# Llamar a la función para limpiar y marcar datos
df_limpio = limpiar_y_marcar_datos5('datos/Carrera_de_mañana(7).gpx')
df_distancias, dist_total = distancia(df_limpio)
print(dist_total)
grafico(df_limpio)
graf_angulo_dist(df_limpio)