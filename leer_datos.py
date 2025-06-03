"""
Script con las funciones para leer los datos de un archivo CSV, GPX y FIT (longitud, latitud y elevación)
y mostrar una gráfica en 2D con las coordenadas x, y.
Incluye funciones para:
- Leer datos desde archivos CSV, GPX y FIT
- Transformar coordenadas geográficas a proyectadas
- Descargar múltiples archivos GPX desde URLs

Librerías utilizadas: pandas, numpy, pyproj, gpxpy, fitparse, requests, os
"""
def leer_datos_csv(nombre_archivo):
    """
        Función que lee un archivo CSV con los datos de una carrera, extrae latitud, longitud y elevación,
        y transforma las coordenadas geográficas a coordenadas proyectadas x, y.

        INPUT:
            nombre_archivo (str): Ruta al archivo CSV a leer.
        
        RETURN:
            None (los datos transformados se almacenan internamente como una matriz NumPy)
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
        Función que lee un archivo GPX con los datos de una carrera y devuelve un DataFrame con:
        - Coordenadas transformadas (x, y)
        - Elevación (en metros)
        - Columna 'marcado' con valor True para todas las filas

        INPUT:
            nombre_archivo (str): Ruta al archivo GPX a leer.

        RETURN:
            df (pandas.DataFrame): DataFrame con columnas ['x', 'y', 'elevacion', 'marcado']
    """
    # leer archivo gpx de la carpeta datos
    import gpxpy
    from pyproj import Transformer  # biblioteca python para transformar coordenadas. Tiene en cuenta la curvatura terrestre
    import pandas as pd  # Importar pandas
    import numpy as np

    # Abrir el archivo GPX
    with open(nombre_archivo, "r", encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)  # Parsear el contenido del GPX

    coordenadas = []
    # Recorrer tracks, segmentos y puntos para obtener todas las coordenadas
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                # añadir los datos a coordenadas
                coordenadas.append([point.longitude, point.latitude, point.elevation])

    # Transformar los datos de latitud y longitud a coordenadas x,y
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32630", always_xy=True)

    # Transformar las coordenadas
    x, y = transformer.transform([i[0] for i in coordenadas], [i[1] for i in coordenadas])

    # Crear un DataFrame con las coordenadas x,y y la elevación
    df = pd.DataFrame({
        'x': x,
        'y': y,
        'elevacion': [i[2] for i in coordenadas],
        'marcado': True  # Columna booleana con True para todas las filas
    })

    # Eliminar duplicados basados en las columnas 'x' y 'y'
    # df = df.drop_duplicates(subset=['x', 'y'], keep='first')

    # Restablecer los índices del DataFrame
    # df.reset_index(drop=True, inplace=True)

    return df

def descarga_archivos():
    """
        Función que descarga múltiples archivos GPX desde una lista de URLs de actividades Strava
        y los guarda en la carpeta 'datos_bcn'. Crea la carpeta si no existe.

        INPUT:
            None

        RETURN:
            None (guarda archivos localmente)
    """
    import os
    import requests

    # Lista de URLs
    urls = [
        "https://www.strava.com/activities/13897904188/export_gpx",
        "https://www.strava.com/activities/13898874147/export_gpx",
        "https://www.strava.com/activities/13897548181/export_gpx",
        "https://www.strava.com/activities/13899135741/export_gpx",
        "https://www.strava.com/activities/13899648518/export_gpx",
        "https://www.strava.com/activities/13897255907/export_gpx",
        "https://www.strava.com/activities/13897682446/export_gpx",
        "https://www.strava.com/activities/13897269898/export_gpx",
        "https://www.strava.com/activities/13897321127/export_gpx",
        "https://www.strava.com/activities/13899062590/export_gpx",
        "https://www.strava.com/activities/13897643202/export_gpx",
        "https://www.strava.com/activities/13897256931/export_gpx",
        "https://www.strava.com/activities/13897952983/export_gpx",
        "https://www.strava.com/activities/13897369924/export_gpx",
        "https://www.strava.com/activities/13898130192/export_gpx",
        "https://www.strava.com/activities/13897427088/export_gpx",
        "https://www.strava.com/activities/13897212447/export_gpx",
        "https://www.strava.com/activities/13897368942/export_gpx",
        "https://www.strava.com/activities/13898011242/export_gpx",
        "https://www.strava.com/activities/13897569781/export_gpx",
        "https://www.strava.com/activities/13897778897/export_gpx",
        "https://www.strava.com/activities/13900706064/export_gpx",
        "https://www.strava.com/activities/13897785634/export_gpx",
        "https://www.strava.com/activities/13898056080/export_gpx",
        "https://www.strava.com/activities/13897296710/export_gpx",
        "https://www.strava.com/activities/13898602613/export_gpx",
        "https://www.strava.com/activities/13897879717/export_gpx",
        "https://www.strava.com/activities/13898186282/export_gpx",
        "https://www.strava.com/activities/13898272841/export_gpx",
        "https://www.strava.com/activities/13901316349/export_gpx",
        "https://www.strava.com/activities/13897891812/export_gpx",
        "https://www.strava.com/activities/13898102300/export_gpx"
    ]


    # Crear la carpeta 'datos_altitud' si no existe
    os.makedirs('datos_bcn', exist_ok=True)

    # Descargar cada archivo GPX
    for url in urls:
        # Extraer el ID de la URL
        activity_id = url.split('/')[-2]
        response = requests.get(url)

        if response.status_code == 200:
            # Guardar el archivo con el nombre del ID
            file_path = os.path.join('datos_bcn', f'{activity_id}.gpx')
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f'Descargado: {file_path}')
        else:
            print(f'Error al descargar {url}: {response.status_code}')


#descarga_archivos()  # Descomentar para descargar los archivos GPX



def leer_datos_fit(nombre_archivo):
    """
        Función que lee un archivo FIT con los datos de una carrera, extrae latitud, longitud,
        elevación y tiempo, y transforma las coordenadas a proyectadas (x, y).

        INPUT:
            nombre_archivo (str): Ruta del archivo .FIT a procesar.

        RETURN:
            df (pandas.DataFrame): DataFrame con columnas ['x', 'y', 'elevacion', 'tiempo', 'marcado']
    """
    from fitparse import FitFile
    from pyproj import Transformer  # biblioteca python para transformar coordenadas. Tiene en cuenta la curvatura terrestre
    import pandas as pd  # Importar pandas

    # Abrir el archivo FIT
    fitfile = FitFile(nombre_archivo)

    coordenadas = []
    tiempos = []
    # Recorrer los registros del archivo FIT
    for record in fitfile.get_messages('record'):
        # Extraer los datos de latitud, longitud, elevación y tiempo
        latitude = record.get_value('position_lat')
        longitude = record.get_value('position_long')
        elevation = record.get_value('altitude')
        timestamp = record.get_value('timestamp')

        # Convertir latitud y longitud de semicírculos a grados decimales
        if latitude is not None and longitude is not None:
            latitude = (latitude / (2**31)) * 180
            longitude = (longitude / (2**31)) * 180
            coordenadas.append([longitude, latitude, elevation])
            tiempos.append(timestamp)

    # Transformar los datos de latitud y longitud a coordenadas x,y
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32630", always_xy=True)

    # Transformar las coordenadas
    x, y = transformer.transform([i[0] for i in coordenadas], [i[1] for i in coordenadas])

    # Crear un DataFrame con las coordenadas x,y, elevación y tiempo
    df = pd.DataFrame({
        'x': x,
        'y': y,
        'elevacion': [i[2] for i in coordenadas],
        'tiempo': tiempos,  # Agregar la columna de tiempo
        'marcado': True  # Columna booleana con True para todas las filas
    })

    return df
