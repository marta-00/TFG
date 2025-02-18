
from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plot

"""
#leer_datos_csv('datos/Carrera_de_mañana.gpx.csv')
coord, fig = leer_datos_gpx('datos/Carrera_de_mañana(1).gpx')
plot.show()
dist_tramo, dist_total = distancia(coord)
print(f'Distancia total de la carrera: {dist_total} m')
print(f'Altitud de la carrera: {altitud(coord)} m')

"""
import pandas as pd
# Calcular la distancia media con los datos de magnitudes.csv


# Leer el archivo CSV con la codificación 'latin1'
datos = pd.read_csv('magnitudes.csv', delimiter=',', encoding='latin1')
# calcular la distancia total media
distancia_media = datos['Distancia_total(m)'].mean()
print(f'Distancia media de la carrera: {distancia_media} m')