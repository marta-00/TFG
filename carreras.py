
from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plt

def una_carrera():
    #leer_datos_csv('datos/Carrera_de_mañana.gpx.csv')
    coord = leer_datos_gpx('datos/Carrera_de_mañana(8).gpx')

    #grafico(coord)
    df_tramo, dist_total = distancia(coord)
    #obtener las distancias de cada tramo 
    dist_tramo = df_tramo['Distancia (m)']
    x_atipico = []
    y_atipico = []

    for i in range(len(dist_tramo) - 1, -1, -1):  # Iterar en orden inverso
        if dist_tramo[i] > 10:
            x_atipico.append(df_tramo['Punto Final'][i][0])
            y_atipico.append(df_tramo['Punto Final'][i][1])
            
            # Filtrar las coordenadas atípicas usando NumPy
            coord = coord[:, ~(np.isin(coord[0], df_tramo['Punto Final'][i][0]) & np.isin(coord[1], df_tramo['Punto Final'][i][1]))]

            # Recalcular distancias
            df_tramo, dist_total = distancia(coord)
            dist_tramo = df_tramo['Distancia (m)']
    
    #crea un grafico x frente a y con los datos coord en azul y los datos atipicos en rojo con solo los puntos 
    plt.plot(x_atipico, y_atipico, color='red')
    plt.plot(coord[0], coord[1], color='blue')
    plt.show()
    
    # # calcular velocidad instantánea
    # velocidades = velocidad(dist_tramo)
    # velocidades = list(set(velocidades)-set(detectar_atipicos_zscore(velocidades)))
    # crear_histogramas(velocidades, nombre1 = "velocidades")

    # # separar datos
    # coord_pares, coord_impares = separar_datos(coord, 5)

    # # obtener distancias_tramo
    # dist_tramo, dist_total = distancia(coord)
    # dist_tramo_par, dist_total_par = distancia(coord_pares)
    # dist_tramo_impar, dist_total_impar = distancia(coord_impares)

    # crear histograma con las distancias de los tramos
    #crear_histogramas(dist_tramo, nombre1 = "total")


    # # dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
    # # dist_tramo_par = list(set(dist_tramo_par)-set(detectar_atipicos_zscore(dist_tramo_par)))
    # # dist_tramo_impar = list(set(dist_tramo_impar)-set(detectar_atipicos_zscore(dist_tramo_impar)))


    # dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
    # dist_tramo_par = list(set(dist_tramo_par)-set(detectar_atipicos_zscore(dist_tramo_par)))
    # dist_tramo_impar = list(set(dist_tramo_impar)-set(detectar_atipicos_zscore(dist_tramo_impar)))

    # crear_histogramas(dist_tramo, dist_tramo_par, dist_tramo_impar, "total", "pares", "impares")
    # print(f"distancia total: {dist_total}")
    # print(f"distancia total pares: {dist_total_par}")
    # print(f"distancia total impares: {dist_total_impar}")
    # plt.show()

    ## CURVAS
    # x_nuevo, y_nuevo = (detectar_curva(coord))

    # print(len(coord[0]))
    # print(len(x_nuevo))

    # coord_nuevas = [x_nuevo, y_nuevo, coord[2]]
    # grafico(coord_nuevas)
    # plt.show()

def total_carreras():
    # leer archivo magnitudes.csv
    import pandas as pd
    magnitudes = pd.read_csv('magnitudes.csv', delimiter=',', encoding='latin1')
    #print(magnitudes)

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
    distancias = magnitudes['Distancia_total(m)']
    distancias_par = magnitudes['Distancia_par(m)']
    distancias_impar = magnitudes['Distancia_impar(m)']

    #calcular error absoluto, dato exacto 21097,5 m
    error_total = abs(distancias - 21097.5)
    error_par = abs(distancias_par - 21097.5)
    error_impar = abs(distancias_impar - 21097.5)

    for i in range(len(error_total)):
        nombre_carrera = magnitudes['Nombre'][i]
        if error_total[i] > error_par[i] and error_total[i] > error_impar[i]:
            print(f"La medida mejora")
        else:
            print(f"la medida empeora para la carrera: {nombre_carrera}")

def graficos_total_carreras():
    """
    Función que crea un archivo CSV y guarda los datos de la distancia total, altitud y velocidad de cada 
    carrera. 
    También guarda todos los gráficos (recorrido, velocidad y distancia) en una carpeta con el nombre de la carrera
    """
    # crear archivo csv para almacenar datos
    import os
    import matplotlib.pyplot as plt
    #magnitudes = open('magnitudes.csv', 'w')
    #magnitudes.write(f"Nombre,Distancia_total(m),Altitud(m),Velocidad(m/s)\n")

    # bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # leer archivo gpx
            coord =leer_datos_gpx(f'datos/{nombre_archivo}')
            # print(len(coord[1])) #debugging
            
            ## QUITAR COORDENADAS CURVA
            x_nuevo, y_nuevo = (detectar_curva(coord))
            coord = [x_nuevo, y_nuevo, coord[2]]

            #crear una carpeta para guardar los datos de cada carpeta dentro deresultados\carreras con el nombre de la carrera
            carpeta = f'resultados/carreras/{nombre_archivo}'
            os.makedirs(carpeta, exist_ok=True)

            # calcular magnitudes
            dist_tramo, dist_total = distancia(coord)
            alt = altitud(coord)
            
            ## QUITAR COORDENADAS ATIPICOS
            dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
            
            ## RECORRIDO
            graf = grafico(coord)
            plt.savefig(f'{carpeta}/recorrido_sin_curva.png')
            plt.close(graf)

            ## DISTANCIAS TRAMO
            #separar datos
            # coord_pares, coord_impares = separar_datos(coord, 2)
            # obtener distancias_tramo
            # dist_tramo, dist_total = distancia(coord)
            # dist_tramo_par, dist_total_par = distancia(coord_pares)
            # dist_tramo_impar, dist_total_impar = distancia(coord_impares)
            #crear histogramas
            dist_td = crear_histogramas(dist_tramo, nombre1 = "distancias_sin_curva_atipicos")
            plt.savefig(f'{carpeta}/distancias_sin_curva_atipicos.png')
            plt.close(dist_td)
            #imagen = crear_histogramas(dist_tramo_par, dist_tramo_impar, "pares", "impares")
            # añadir a carpeta 
            #plt.savefig(f'{carpeta}/distancias_mitad_datos.png')
            #plt.close(imagen)

            # VELOCIDADES
            # calcular velocidad instantánea
            velocidades = velocidad(dist_tramo)
            figura = crear_histogramas(velocidades, nombre1 = "velocidades_sin_curva_atipicos")
            #añadir a carpeta histogramas_velocidad
            plt.savefig(f'{carpeta}/velocidades_sin_curva_atipicos.png')
            plt.close(figura)

            # MAGNITUDES 
            # añadir magnitudes al archivo csv
            # magnitudes.write(f"{nombre_archivo},{dist_total},{alt},{0}\n")
            
    #magnitudes.close()

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

una_carrera()

