
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
