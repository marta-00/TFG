
from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plot
import numpy as np

#leer_datos_csv('datos/Carrera_de_mañana.gpx.csv')
coord = leer_datos_gpx('datos/Carrera_de_mañana(3).gpx')

# separar datos
coord_pares, coord_impares = separar_datos(coord, 2)

# obtener distancias_tramo
dist_tramo, dist_total = distancia(coord)
dist_tramo_par, dist_total_par = distancia(coord_pares)
dist_tramo_impar, dist_total_impar = distancia(coord_impares)

# crear histograma con las distancias de los tramos
# crear_histogramas(dist_tramo, dist_tramo_par, dist_tramo_impar, "total", "pares", "impares")


# dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
# dist_tramo_par = list(set(dist_tramo_par)-set(detectar_atipicos_zscore(dist_tramo_par)))
# dist_tramo_impar = list(set(dist_tramo_impar)-set(detectar_atipicos_zscore(dist_tramo_impar)))


dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
dist_tramo_par = list(set(dist_tramo_par)-set(detectar_atipicos_zscore(dist_tramo_par)))
dist_tramo_impar = list(set(dist_tramo_impar)-set(detectar_atipicos_zscore(dist_tramo_impar)))

crear_histogramas(dist_tramo, dist_tramo_par, dist_tramo_impar, "total", "pares", "impares")



def main():
    # crear archivo csv para almacenar datos
    import os
    magnitudes = open('magnitudes.csv', 'w')
    magnitudes.write(f"Nombre,Distancia_total(m),Altitud(m),Velocidad(m/s)\n")

    #crear carpeta para guardar histogramas de cada carrera
    carpeta_histogramas = 'histogramas'
    os.makedirs(carpeta_histogramas, exist_ok=True)

    # bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
    
    for nombre_archivo in os.listdir('datos'):
        if nombre_archivo.endswith('.gpx'):
            # leer archivo gpx
            coord =leer_datos_gpx(f'datos/{nombre_archivo}')
            # print(len(coord[1])) #debugging

            # calcular magnitudes
            dist_tramo,dist_total = distancia(coord)
            alt = altitud(coord)

            # añadir magnitudes al archivo csv
            magnitudes.write(f"{nombre_archivo},{dist_total},{alt},{0}\n")

            # función zig_zag
            fig = zig_zag(coord)
            fig.savefig(f"{carpeta_histogramas}/{nombre_archivo}.png")
            plot.close(fig)

    magnitudes.close()

#if __name__ == "__main__":
#    main()

