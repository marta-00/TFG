
from leer_datos import *
from magnitudes import *
from graficos import *
from algoritmo import *
"""
GUARDAR GRAFICOS EN CARPETA
#crear una carpeta para guardar los datos de cada carpeta dentro deresultados\carreras con el nombre de la carrera
            carpeta = f'resultados/carreras/{nombre_archivo}'
            os.makedirs(carpeta, exist_ok=True)
        
            ## RECORRIDO
            graf = grafico(coord)
            plt.savefig(f'{carpeta}/recorrido_sin_curva.png')
            plt.close(graf)

            ## DISTANCIAS TRAMO
            #crear histogramas
            dist_td = crear_histogramas(dist_tramo, nombre1 = "distancias_sin_curva_atipicos")
            plt.savefig(f'{carpeta}/distancias_sin_curva_atipicos.png')
            plt.close(dist_td)
            #imagen = crear_histogramas(dist_tramo_par, dist_tramo_impar, "pares", "impares")
            #añadir a carpeta 
            #plt.savefig(f'{carpeta}/distancias_mitad_datos.png')
            #plt.close(imagen)

            # VELOCIDADES
            # calcular velocidad instantánea
            figura = crear_histogramas(velocidades, nombre1 = "velocidades_sin_curva_atipicos")
            #añadir a carpeta histogramas_velocidad
            plt.savefig(f'{carpeta}/velocidades_sin_curva_atipicos.png')
            plt.close(figura)
"""


def una_carrera():
    import matplotlib.pyplot as plt
    # Leer datos del archivo GPX
    df_coord = leer_datos_gpx('datos/Carrera_de_mañana(8).gpx')
    x = df_coord['x'].tolist()
    y = df_coord['y'].tolist()

    S, S_array, distancia = algoritmo_S(x,y)
    print(distancia)

    # # Calcular distancia tramo y total
    # L_total = distancia(df_coord)
    # print(f"La distancia total: {L_total}")
    # print(df_coord)

    # # Obtener las distancias de los tramos
    # L_tramo = df_dist['Distancia (m)']

    # # Encontrar todos los índices donde la distancia es mayor a 90 metros
    # indices_mayor_90 = [i for i in range(len(L_tramo)) if L_tramo[i] > 90]

    # if indices_mayor_90:
    #     puntos_a_marcar = set()
    #     for i in indices_mayor_90:
    #         # Obtener las coordenadas del punto final para esta distancia
    #         p_final_x = df_dist['Punto Final'][i][0]
    #         p_final_y = df_dist['Punto Final'][i][1]

    #         # Agregar las coordenadas finales al conjunto
    #         puntos_a_marcar.add((p_final_x, p_final_y))
            
    #     # Marcar como False los puntos obtenidos en la variable df_coord
    #     df_coord.loc[df_coord[['x', 'y']].apply(tuple, axis=1).isin(puntos_a_marcar), 'marcado'] = False
    
    # grafico(df_coord)
    # plt.show()
            
        
    # while True: 
    #     # Calcular distancia tramo y total
    #     df_dist, L_total = distancia(df_coord)
    #     print(f"La distancia total: {L_total}")

    #     # Obtener las distancias de los tramos
    #     L_tramo = df_dist['Distancia (m)']

    #     # Encontrar todos los índices donde la distancia es mayor a 90 metros
    #     indices_mayor_90 = [i for i in range(len(L_tramo)) if L_tramo[i] > 90]

    #     if indices_mayor_90:
    #         puntos_a_marcar = set()
    #         for i in indices_mayor_90:
    #             # Obtener las coordenadas del punto final para esta distancia
    #             p_final_x = df_dist['Punto Final'][i][0]
    #             p_final_y = df_dist['Punto Final'][i][1]

    #             # Agregar las coordenadas finales al conjunto
    #             puntos_a_marcar.add((p_final_x, p_final_y))
            
    #         # Marcar como False los puntos obtenidos en la variable df_coord
    #         df_coord.loc[df_coord[['x', 'y']].apply(tuple, axis=1).isin(puntos_a_marcar), 'marcado'] = False

    #         print(f"Se han marcado como False los puntos finales de los tramos mayores a 90 metros: {indices_mayor_90}")
    #     else:
    #         print("No hay tramos con distancia mayor a 90 metros.")
    #         break  # Salir del bucle si no hay tramos que cumplan la condición

def total_carreras():
    # leer archivo magnitudes.csv
    import pandas as pd
    magnitudes = pd.read_csv('magnitudes.csv', delimiter=',', encoding='latin1')
    #print(magnitudes)

    ##separar

    # # crear histograma con las distancias medias
    # import matplotlib.pyplot as plt
    # distancias = magnitudes['Distancia_total(m)']
    # plt.hist(distancias, bins=len(distancias), color='blue', edgecolor='blue', alpha=0.7)

    # # añadir en rojo una recta en el valor 21.097
    # plt.axvline(x=21097, color='red', linestyle='--')

    # plt.title("Histograma - distancias medias")
    # plt.xlabel("Distancia total (m)")
    # plt.ylabel("Número de carreras")
    # plt.show()

    # # crear histograma con las altitudes
    # altitudes = magnitudes['Altitud(m)']
    # plt.hist(altitudes, bins=len(altitudes), color='green', edgecolor='green', alpha=0.7)
    # plt.title("Histograma - altitudes")
    # plt.xlabel("Altitud (m)")
    # plt.ylabel("Número de carreras")
    # plt.show()

    ## comparar distancias
    # obtener distancias
    # distancias = magnitudes['Distancia_total(m)']
    # distancias_par = magnitudes['Distancia_par(m)']
    # distancias_impar = magnitudes['Distancia_impar(m)']

    # #calcular error absoluto, dato exacto 21097,5 m
    # error_total = abs(distancias - 21097.5)
    # error_par = abs(distancias_par - 21097.5)
    # error_impar = abs(distancias_impar - 21097.5)

    # for i in range(len(error_total)):
    #     nombre_carrera = magnitudes['Nombre'][i]
    #     if error_total[i] > error_par[i] and error_total[i] > error_impar[i]:
    #         print(f"La medida mejora")
    #     else:
    #         print(f"la medida empeora para la carrera: {nombre_carrera}")

def comparación_distancias():
    """
    Función que separa los datos separados n veces y crea un gráfico comparando cómo varía la 
    distancia total de la carrera en función de n. 
    En un mismo gráfico se incluyen 3 carreras distintas para poder compararlas.
    """ 
    coord1 = leer_datos_gpx('datos/Carrera_de_mañana(1).gpx')
    coord2 = leer_datos_gpx('datos/Carrera_de_mañana(5).gpx')
    coord3 = leer_datos_gpx('datos/Carrera_de_mañana(8).gpx')
    datos = [coord1, coord2, coord3]

    #crear figura 
    plt.figure(figsize=(10, 6))

    for i,coord in enumerate(datos):
        distancias_totales = []
        dist_tramo, dist_total = distancia(coord)
        distancias_totales.append(dist_total)
        for n in range(2, 20, 1):
            dat1, dat2 = separar_datos(coord, n)
            # calcular distancias
            dist_1, dist_total2 = distancia(dat1)
            distancias_totales.append(dist_total2)

        #añadir datos a la figura
        plt.plot(range(1, len(distancias_totales) + 1), distancias_totales, marker='o')
    # Configurar el gráfico
    distancia_media_maraton = 21097.5  # Distancia en metros
    plt.axhline(y=distancia_media_maraton, color='red', linestyle='--', label='Media Maratón (21.0975 km)')

    plt.title('Comparación de Distancias Totales en Función de n')
    plt.xlabel('Número de Separaciones (n)')
    plt.ylabel('Distancia Total (m)')
    plt.xticks(ticks=range(1, len(distancias_totales) + 1))
    plt.legend(['Carrera_de_mañana(1)', 'Carrera_de_mañana(5)', 'Carrera_de_mañana(8)'])
    plt.grid()
    plt.show()

def histograma_n_dist():
    """
    Función que lee todos los archivos gpx. Crea una figura con 6 graficos. 
    Los gráficos son histogramas de la distancia total. Se comparan 6 graficos para distintas
    separaciones de n (función separar_datos)
    """
    import os
    import matplotlib.pyplot as plt
    import numpy as np
    L_total_1 = []
    L_total_2 = []
    L_total_5 = []
    L_total_9 = []
    L_total_13 = []
    L_total_20 = []
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # leer archivo gpx
            df_coord =leer_datos_gpx(f'datos/{nombre_archivo}')

            #separar datos 
            coord_lista, distancias_totales = separar_datos(df_coord, 1)
            L_total_1.append(distancias_totales[0])

            coord_lista, distancias_totales = separar_datos(df_coord, 2)
            L_total_2.extend([distancias_totales[0], distancias_totales[1]])

            coord_lista, distancias_totales = separar_datos(df_coord, 5)
            L_total_5.extend([distancias_totales[0], distancias_totales[1], distancias_totales[2], distancias_totales[3], distancias_totales[4]])
    
            coord_lista, distancias_totales = separar_datos(df_coord, 9)
            L_total_9.extend([distancias_totales[0], distancias_totales[1], distancias_totales[2], distancias_totales[3], distancias_totales[4]])
    

            coord_lista, distancias_totales = separar_datos(df_coord, 13)
            L_total_13.extend([distancias_totales[0], distancias_totales[1], distancias_totales[2], distancias_totales[3], distancias_totales[4]])
    
            coord_lista, distancias_totales = separar_datos(df_coord, 20)
            L_total_20.extend([distancias_totales[0], distancias_totales[1], distancias_totales[2], distancias_totales[3], distancias_totales[4]])
    
    #crear 6 graficos para cada L_total_i
    plt.figure(figsize=(12, 8))

    # Lista de distancias totales y títulos
    distancias = [L_total_1, L_total_2, L_total_5, L_total_9, L_total_13, L_total_20]
    titulos = [
        "Histograma - Distancias totales con n=1",
        "Histograma - Distancias totales con n=2",
        "Histograma - Distancias totales con n=5",
        "Histograma - Distancias totales con n=9",
        "Histograma - Distancias totales con n=13",
        "Histograma - Distancias totales con n=20"
    ]

    for i, (L_total, titulo) in enumerate(zip(distancias, titulos)):
        plt.subplot(3, 2, i + 1)
        
        # Calcular el histograma
        bins = int(len(L_total)**0.5)  # Ajusta el número de bins según sea necesario
        hist, bin_edges = np.histogram(L_total, bins=bins)
        
        # Calcular los centros de los bins
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
        
        # Dibujar el histograma como barras
        plt.bar(bin_centers, hist, width=np.diff(bin_edges), color='blue', edgecolor='blue', alpha=0.7, align='center')
        
        # añadir linea roja en 21095m
        plt.axvline(x=21095, color='red', linestyle='--')
        # Dibujar la línea que conecta los máximos de cada bin
        #plt.plot(bin_centers, hist, color='red', marker='o', linestyle='-', linewidth=2)
        
        # Configurar el título y etiquetas
        plt.title(titulo)
        plt.xlabel("Distancia total (m)")
        plt.ylabel("Número de carreras")

    plt.tight_layout()  # Ajustar el espaciado entre subgráficas
    plt.show()


# df_coord = leer_datos_gpx('datos/Media_Maratón_Santander_2024.gpx')
# df_dist_kalman = calcular_distancias_recursivas(df_coord)
# crear_histograma(df_dist_kalman)


def clasificar_histogramas(df, plot=False):
    """
    Clasifica el histograma de las distancias entre puntos consecutivos.

    Parámetros:
        df (pd.DataFrame): DataFrame con columnas 'x' e 'y' representando coordenadas.
        plot (bool): Si True, muestra el histograma con la densidad.

    Retorna:
        str: Tipo de histograma ('normal', 'bimodal', 'extensa')
    """
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from scipy.signal import find_peaks
    from scipy.stats import gaussian_kde, kurtosis

    # Calcular distancias entre puntos consecutivos
    dx = df['x'].diff().dropna()
    dy = df['y'].diff().dropna()
    distancias = np.sqrt(dx**2 + dy**2)

    if len(distancias) < 10:
        return 'extensa'  # No hay suficientes datos
    
    # 2. Recorte de outliers extremos
    umbral = np.percentile(distancias, 90)
    distancias_filtradas = distancias[distancias <= umbral]

    if len(distancias_filtradas) < 5:
        return 'extensa'

    # 3. KDE y detección de picos
    kde = gaussian_kde(distancias_filtradas)
    xs = np.linspace(distancias_filtradas.min(), distancias_filtradas.max(), 500)
    density = kde(xs)

    # Detectar picos prominentes
    peaks, properties = find_peaks(density, height=np.max(density)*0.1, distance=10)
    peak_heights = properties['peak_heights']

    # Detectar valles entre los dos picos principales (si los hay)
    if len(peaks) >= 2:
        sorted_idx = np.argsort(peak_heights)[::-1]  # orden descendente
        top_peaks = peaks[sorted_idx[:2]]
        left, right = np.sort(top_peaks)
        valley_region = density[left:right]
        valley_min = np.min(valley_region)
        valley_ratio = valley_min / np.mean(peak_heights[sorted_idx[:2]])
    else:
        valley_ratio = 0


    # --- Clasificación ---
    if len(peaks) == 1:
        clasificacion = 'normal'

        # Calcular sigma directamente para distribución unimodal
        mu = np.mean(distancias_filtradas)
        sigma = np.std(distancias_filtradas)
        #print(f"Sigma estimada (unimodal): {sigma:.4f}")


    elif len(peaks) == 2 and valley_ratio < 0.6:
        clasificacion = 'bimodal'
        # Encontrar el punto de valle entre los dos picos principales
        valley_idx = np.argmin(density[left:right]) + left
        valley_x = xs[valley_idx]

        # Separar los datos según el valle
        grupo1 = distancias_filtradas[distancias_filtradas <= valley_x]
        grupo2 = distancias_filtradas[distancias_filtradas > valley_x]

        # Calcular medias y sigmas individuales
        mu1, sigma1 = np.mean(grupo1), np.std(grupo1)
        mu2, sigma2 = np.mean(grupo2), np.std(grupo2)

        # Proporciones de cada grupo
        w1 = len(grupo1) / (len(grupo1) + len(grupo2))
        w2 = 1 - w1

        # Media total
        mu_total = w1 * mu1 + w2 * mu2

        # Varianza total con la fórmula de mezcla
        var_total = w1 * (sigma1**2 + (mu1 - mu_total)**2) + w2 * (sigma2**2 + (mu2 - mu_total)**2)
        sigma = np.sqrt(var_total)

        # Puedes imprimirla, retornarla o usarla en más análisis
        #print(f"Sigma total estimada (bimodal): {sigma:.4f}")

    else:
        clasificacion = 'extensa'
        # Calcular sigma directa para distribución extensa (sin estructura clara)
        mu = np.mean(distancias_filtradas)
        sigma = np.std(distancias_filtradas)
        #print(f"Sigma estimada (extensa): {sigma:.4f}")


    if plot:
        plt.hist(distancias_filtradas, bins=30, density=True, alpha=0.3, label='Histograma', color='gray')
        plt.plot(xs, density, label='KDE', color='blue')
        plt.plot(xs[peaks], density[peaks], 'ro', label='Picos detectados')
        if len(peaks) >= 2:
            plt.fill_between(xs[left:right], 0, density[left:right], color='orange', alpha=0.2, label='Valle')
        plt.axvline(umbral, color='red', linestyle='--', alpha=0.3, label=f'Corte 90%')
        plt.title(f"Clasificación: {clasificacion}")
        plt.xlabel("Distancia")
        plt.ylabel("Densidad")
        plt.legend()
        plt.show()

    return clasificacion, sigma

def eliminar_carreras_atipicas():
    import os
    for nombre_archivo in os.listdir('datos_bici'):
        if nombre_archivo.endswith('.gpx'):
            # Leer archivo gpx
            df_coord = leer_datos_gpx(f'datos_bici/{nombre_archivo}')
            tipo, sigma = clasificar_histogramas(df_coord, False)

            #DISTANCIAS INICIALES
            distancia_inicial = distancia(df_coord)
            print(f'{nombre_archivo}: {distancia_inicial}')

#eliminar_carreras_atipicas()