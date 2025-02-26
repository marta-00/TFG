from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plt

coord = leer_datos_gpx('datos_bici/Morning_Ride (5).gpx')
grafico(coord)

