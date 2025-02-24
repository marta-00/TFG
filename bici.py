from leer_datos import leer_datos_gpx
from magnitudes import *
import matplotlib.pyplot as plt

coord = leer_datos_gpx('datos_bici/Morning_Ride (5).gpx')
#grafico(coord)

dist_tramo, dist_total = distancia(coord)
# calcular velocidad instantánea
velocidades = velocidad(dist_tramo)
velocidades = list(set(velocidades)-set(detectar_atipicos_zscore(velocidades)))
crear_histogramas(velocidades, nombre1 = "velocidades")

# separar datos
coord_pares, coord_impares = separar_datos(coord, 2)

# obtener distancias_tramo
dist_tramo, dist_total = distancia(coord)
dist_tramo_par, dist_total_par = distancia(coord_pares)
dist_tramo_impar, dist_total_impar = distancia(coord_impares)

# crear histograma con las distancias de los tramos
# crear_histogramas(dist_tramo, dist_tramo_par, dist_tramo_impar, "total", "pares", "impares")


dist_tramo = list(set(dist_tramo)-set(detectar_atipicos_zscore(dist_tramo)))
dist_tramo_par = list(set(dist_tramo_par)-set(detectar_atipicos_zscore(dist_tramo_par)))
dist_tramo_impar = list(set(dist_tramo_impar)-set(detectar_atipicos_zscore(dist_tramo_impar)))

crear_histogramas(dist_tramo, dist_tramo_par, dist_tramo_impar, "total", "pares", "impares")
plt.show()