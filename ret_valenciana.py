import ee
import re


ee.Initialize(project='earth-engine-tfg')

stations_fc = ee.FeatureCollection("projects/earth-engine-tfg/assets/estaciones")

stations_fc = stations_fc.map(lambda f: f.setGeometry(f.geometry()))

station_names = [
    "Bèlgida","Bétera", "Cheste",  
    "Chulilla", "Godelleta", "Llutxent",
    "Llíria", "Montesa", "Pedralba", 
    "Requena cerrito", "Villanueva de Castellón", "Campo Arcís",
    "Camp de Mirra", "Dénia", "Monforte del Cid", "Ondara", "Pinoso", "Planes"
]

stations_fc = stations_fc.filter(ee.Filter.inList('Name', station_names))

collection = (
    ee.ImageCollection("FAO/WAPOR/3/L1_RET-E")
    .filterBounds(stations_fc.geometry())
    .filterDate('2020-01-01', '2025-01-01')
)

print("Número de imágenes:", collection.size().getInfo())

def sanitize_name(name):
    return re.sub(r'[^A-Za-z0-9_-]', '_', name)

def export_station(feature):
    station_name = feature.get('Name').getInfo()
    print(f"Exportando datos para estación: {station_name}")

    def daily_for_point(image):
        value = image.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=feature.geometry(),
            scale=18924,
            maxPixels=1e13,
            tileScale=4
        )
        return ee.Feature(None, {
            'Fecha': image.date().format('YYYY-MM-dd'),
            'RET_mm_dia': value.get('L1-RET-E'),
            'Estacion': station_name
        })

    daily_fc = collection.map(daily_for_point)

    safe_name = sanitize_name(station_name)

    task = ee.batch.Export.table.toDrive(
        collection=daily_fc,
        description=f'RET_{safe_name}_2020_2024',
        folder='RET_por_estacion',
        fileFormat='CSV'
    )
    task.start()
    print(f" Tarea de exportación iniciada para {station_name}")

stations_list = stations_fc.toList(stations_fc.size())
for i in range(stations_fc.size().getInfo()):
    feature = ee.Feature(stations_list.get(i))
    export_station(feature)

print("Revisa https://code.earthengine.google.com/tasks")
