


from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plot


#leer_datos_csv('datos/Carrera_de_mañana.gpx.csv')
#coord, fig = leer_datos_gpx('datos/Carrera_de_mañana(1).gpx')
#plot.show()
#dist_tramo, dist_total = distancia(coord)
#print(dist_total)


# bucle que recorre todos los archivos GPX de la carpeta datos y los abre con la función leer_datos_gpx
import os
for nombre_archivo in os.listdir('datos'):
    if nombre_archivo.endswith('.gpx'):
        coord,fig =leer_datos_gpx(f'datos/{nombre_archivo}')
        # print (f'Archivo {nombre_archivo} leído') debugging
        print(altitud(coord))