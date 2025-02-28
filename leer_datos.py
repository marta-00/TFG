"""
Script con las funciones para leer los datos de un archivo CSV y GPX (longitud, latitud y elevación)
y mostrar una gráfica en 2D con las coordenadas x,y

"""
def leer_datos_csv(nombre_archivo):
    """
    Función que lee un archivo csv con los datos de una carrera 
    INPUT: nombre_archivo: nombre del archivo csv
    RETURN: None
    """
    # abrir y leer archivo csv de la carpeta datos

    import pandas as pd
    from pyproj import Proj, transform  # biblioteca python para transformar coordenadas. Tiene en cuenta la curvatura terrestre
    import numpy as np

    # Leer datos csv
    datos = pd.read_csv(nombre_archivo, delimiter=',', encoding='latin1')
    #print(datos) debugging

    # Obtener los datos de la latitud(lat52), longitud(lon53) y elevacion(ns1:ele54) de la carrera
    latitud = datos['lat52']
    longitud = datos['lon53']
    elevacion = datos['ns1:ele54']

    #print(latitud)   debugging
    #print(longitud)  debugging
    #print(elevacion) debugging

    # Transformar los datos de latitud y longitud a coordenadas x,y
    # Definir el sistema de coordenadas de latitud y longitud
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:3395')

    # Transformar las coordenadas
    x, y = transform(inProj, outProj, longitud, latitud)

    # Crear un array con las coordenadas x,y y la elevacion
    coordenadas = np.array([x, y, elevacion])
    # print(coordenadas)   debugging

def leer_datos_gpx(nombre_archivo):
    """
    Función que lee un archivo gpx con los datos de una carrera y crea un array
    con los datos transformados a coordenadas x,y y con la elevación en metros 

    INPUT:    nombre_archivo: nombre del archivo gpx
    RETURN:   Coordenadas en formato numpy array 
    """
    # leer archivo gpx de la carpeta datos
    import gpxpy
    from pyproj import Transformer  # biblioteca python para transformar coordenadas. Tiene en cuenta la curvatura terrestre
    import numpy as np

    # Abrir el archivo GPX
    with open(nombre_archivo, "r", encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)  # Parsear el contenido del GPX

    coordenadas = []
    # Recorrer tracks, segmetos y puntos para obtener todas las coordenadas
    # longitud y latitud en grados y altitud en metros sobre el nivel del mar
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # añadir los datos a coordenadas
                coordenadas.append([point.longitude, point.latitude, point.elevation])
                # print(f"Lat: {point.latitude}, Lon: {point.longitude}, Alt: {point.elevation}") debugging

    # print(coordenadas)   debugging

    # Transformar los datos de latitud y longitud a coordenadas x,y
    # Se pasa de WGS84=EPSG:4326 (latitud y longitud) a EPSG:32630 (coordenadas x,y) en Cantabria
    # always_xy=True para que las coordenadas sean x,y y no y,x
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32630", always_xy=True)

    # Transformar las coordenadas
    x, y = transformer.transform([i[0] for i in coordenadas], [i[1] for i in coordenadas])

    # Crear un array con las coordenadas x,y y la elevacion
    coordenadas = np.array([x, y, [i[2] for i in coordenadas]])
    #print(coordenadas)   debugging

    return coordenadas

def descarga_archivos():
    import os
    import requests

    # Lista de URLs
    urls = [
        "http://www.strava.com/activities/11605563825/export_gpx",
        "http://www.strava.com/activities/11603305251/export_gpx",
        "http://www.strava.com/activities/11603060550/export_gpx",
        "http://www.strava.com/activities/11604271418/export_gpx",
        "http://www.strava.com/activities/11602568347/export_gpx",
        "http://www.strava.com/activities/11601902223/export_gpx",
        "http://www.strava.com/activities/11602359365/export_gpx",
        "http://www.strava.com/activities/11602663826/export_gpx",
        "http://www.strava.com/activities/11602504151/export_gpx",
        "http://www.strava.com/activities/11602375771/export_gpx",
        "http://www.strava.com/activities/11601984255/export_gpx",
        "http://www.strava.com/activities/11602556890/export_gpx",
        "http://www.strava.com/activities/11602604518/export_gpx",
        "http://www.strava.com/activities/11601896081/export_gpx",
        "http://www.strava.com/activities/11603179371/export_gpx",
        "http://www.strava.com/activities/11602021734/export_gpx",
        "http://www.strava.com/activities/11603238222/export_gpx",
        "http://www.strava.com/activities/11637916079/export_gpx",
        "http://www.strava.com/activities/11610025403/export_gpx"
    ]

    # Crear la carpeta 'datos_altitud' si no existe
    os.makedirs('datos_altitud', exist_ok=True)

    # Descargar cada archivo GPX
    for url in urls:
        # Extraer el ID de la URL
        activity_id = url.split('/')[-2]
        response = requests.get(url)

        if response.status_code == 200:
            # Guardar el archivo con el nombre del ID
            file_path = os.path.join('datos_altitud', f'{activity_id}.gpx')
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f'Descargado: {file_path}')
        else:
            print(f'Error al descargar {url}: {response.status_code}')

