
# Development of algorithms for optimizing GPS measurements in sports competitions 

This project is the Bachelor's Thesis (TFG) for the Physics degree. It consists of analyzing GPS data from various 
types of races (half marathon, cycling race, and high-altitude races) and improving the data using different algorithms 
to achieve greater accuracy in race metrics (total distance, altitude, etc.). (The code, comments and final report are
written in spanish)

## PROGRESS
1. Data Reading: Working with GPX data.
2. Calculation of Metrics and Graphs: Analyzing the data to understand it.
3. Data Cleaning: Removing outlier data.
4. Simulation: A small simulation using only 3 or 4 points to determine which algorithms may work.
5. Algorithm Development.

## Tech stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) 
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) 
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

# Organización

leer_datos: script con todas las funciones para descargar y leer los archivos GPX, TCX y FIT
magnitudes_ script con todas las funciones para calcular las distintas magnitudes empleadas
graficos: script con las funciones para crear graficos básicos (recorrido de la carrera)

simulaciones: script donde se realizan las simulaciones con parametros distintos y donde se analizan los resultados de
los algoritmos en una simulacion controlada

algoritmo: script donde se encuentran los algoritmos finales empleados

sigma: script donde se calcula y analizan las sigmas de las carreras

main: script donde se aplica el algoritmo final y se ven los resultados 

altitud: script donde se analiza la altitud de las carreras
