
# Desarrollo de algoritmos para la optimización de medidas GPS en competiciones deportivas

Este proyecto constituye el Trabajo de Fin de Grado (TFG) para el Grado en Física. Su objetivo principal es el análisis de datos GPS obtenidos en distintas competiciones deportivas —como medias maratones, carreras ciclistas y eventos en alta montaña— con el fin de mejorar su precisión mediante el desarrollo y aplicación de diversos algoritmos.

El trabajo combina simulaciones controladas y datos reales para analizar magnitudes clave como la distancia total, la altitud, la velocidad y otros parámetros derivados. Para ello, se han diseñado y comparado distintos algoritmos de corrección y suavizado de datos GPS, prestando especial atención al análisis estadístico de los errores y a la representación gráfica de los resultados.

> **Idioma:** Todo el código, comentarios y documentación están escritos en español.

---

## 📁 Estructura del proyecto

| Archivo / Módulo | Descripción |
|------------------|-------------|
| `main.py`        | Script principal del proyecto. Ejecuta el algoritmo final sobre los datos reales, muestra los resultados y permite visualizar el efecto de las correcciones. |
| `leer_datos.py`  | Contiene funciones para descargar, leer y parsear archivos de datos GPS en formatos GPX, TCX y FIT. |
| `magnitudes_.py` | Funciones para el cálculo de magnitudes físicas y deportivas relevantes: distancia recorrida, velocidad, aceleración, etc. |
| `graficos.py`    | Funciones para la visualización básica de los recorridos y parámetros medidos (mapas, perfiles de altitud, gráficas de velocidad, etc.). |
| `simulaciones.py`| Simulaciones en escenarios controlados para probar y comparar el rendimiento de los algoritmos bajo distintos parámetros. |
| `algoritmo.py`   | Implementación de los algoritmos principales de corrección y mejora del GPS (filtros, suavizados, modelos estadísticos). |
| `sigma.py`       | Cálculo y análisis de las desviaciones estándar (sigmas) asociadas a los datos GPS de cada carrera. Se utiliza para validar la fiabilidad de las correcciones. |
| `altitud.py`     | Análisis detallado del perfil de altitud en las distintas carreras, así como correcciones por interpolación o suavizado. |

---

## 🛠️ Tecnologías utilizadas

El proyecto ha sido desarrollado íntegramente en Python, utilizando librerías científicas y de visualización ampliamente empleadas en el análisis de datos:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) 
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white) 
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

### 🔧 Otras herramientas utilizadas

![SciPy](https://img.shields.io/badge/scipy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)  
> Para análisis numérico avanzado y filtrado de señales.

![Geopy](https://img.shields.io/badge/geopy-%234285F4.svg?style=for-the-badge&logo=earth&logoColor=white)
![gpxpy](https://img.shields.io/badge/gpxpy-%23FFD700.svg?style=for-the-badge&logo=mapbox&logoColor=black)  
> Para manejo y cálculo con coordenadas geográficas (distancias, trayectorias, elevación, etc.).

![fitparse](https://img.shields.io/badge/fitparse-333333?style=for-the-badge&logo=garmin&logoColor=white)  
> Para parsear archivos de dispositivos deportivos en formato `.fit`.

![OS](https://img.shields.io/badge/os-666666?style=for-the-badge&logo=linux&logoColor=white)
![glob](https://img.shields.io/badge/glob-888888?style=for-the-badge&logo=code&logoColor=white)
![XML](https://img.shields.io/badge/xml-e34c26?style=for-the-badge&logo=xml&logoColor=white)  
> Para manejo de ficheros, estructura de carpetas y lectura de archivos estructurados como `.gpx` o `.tcx`.


