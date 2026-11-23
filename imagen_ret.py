import ee
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import shape
import os


ee.Initialize(project='earth-engine-tfg')
comunidad_fc = ee.FeatureCollection("projects/earth-engine-tfg/assets/comunidadV")
stations_fc = ee.FeatureCollection("projects/earth-engine-tfg/assets/estaciones1")

station_names = [
    "Bèlgida","Bétera", "Cheste",  
    "Chulilla", "Godelleta", "Llutxent",
    "Llíria", "Montesa", "Pedralba", 
    "Requena cerrito", "Villanueva de Castellón", "Campo Arcís",
    "Camp de Mirra", "Dénia", "Monforte del Cid", "Ondara", "Pinoso", "Planes"
]

stations_fc = stations_fc.filter(ee.Filter.inList('Name', station_names))

def plot_station_filled(feature, output_folder):
    station_name = feature.get('Name').getInfo()
    print(f"Generando mapa para: {station_name}")
    lon, lat = feature.geometry().coordinates().getInfo()

    delta_deg = 0.16  # ~18 km
    minx, maxx = lon - delta_deg/2, lon + delta_deg/2
    miny, maxy = lat - delta_deg/2, lat + delta_deg/2

    pixel_size = 0.016  # ~1.8 km para simular subdivisión
    cells = []
    x = minx
    while x < maxx:
        y = miny
        while y < maxy:
            cells.append(shape({"type": "Polygon", "coordinates": [[
                [x, y],
                [x+pixel_size, y],
                [x+pixel_size, y+pixel_size],
                [x, y+pixel_size],
                [x, y]
            ]]}))
            y += pixel_size
        x += pixel_size
    grid = gpd.GeoDataFrame(geometry=cells, crs="EPSG:4326")

    fig, ax = plt.subplots(figsize=(8, 8))

    comunidad_geojson = comunidad_fc.geometry().getInfo()
    comunidad_shape = shape(comunidad_geojson)
    comunidad_gdf = gpd.GeoDataFrame(geometry=[comunidad_shape], crs="EPSG:4326")
    comunidad_gdf.plot(ax=ax, color="#f0f0f0", edgecolor='black', linewidth=1.5, label='Comunidad Valenciana')

    from shapely.geometry import box
    station_square = gpd.GeoDataFrame(geometry=[box(minx, miny, maxx, maxy)], crs="EPSG:4326")
    station_square.plot(ax=ax, color="#a6cee3", alpha=0.5, edgecolor='blue', linewidth=1.5, label='Zona ~18 km')

    grid.boundary.plot(ax=ax, color='red', alpha=0.3, linewidth=0.7, label='Píxeles WaPOR simulados')

    ax.plot(lon, lat, 'bo', markersize=8, label='Estación')

    plt.title(f"{station_name} - Área de estación con simulación de píxeles", fontsize=12)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")

    plt.annotate("N",
                 xy=(maxx - 0.01, maxy - 0.01),
                 xytext=(maxx - 0.01, maxy - 0.03),
                 arrowprops=dict(facecolor='black', width=2, headwidth=8),
                 ha='center', fontsize=10)

    scale_km = 10
    scale_deg = scale_km / 111
    plt.plot([minx + 0.01, minx + 0.01 + scale_deg], [miny + 0.01, miny + 0.01], color='black', linewidth=2)
    plt.text(minx + 0.01, miny + 0.012, f"{scale_km} km", fontsize=9)

    plt.legend()
    plt.tight_layout()

    import os
    output_path = os.path.join(output_folder, f"{station_name.replace(' ', '_')}_map.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ Mapa guardado: {output_path}")

output_folder = r"C:\Users\macie\OneDrive\Escritorio\Estaciones_Mapas1"
os.makedirs(output_folder, exist_ok=True)

stations_list = stations_fc.toList(stations_fc.size())
for i in range(stations_fc.size().getInfo()):
    feature = ee.Feature(stations_list.get(i))
    plot_station_filled(feature, output_folder)

print("✅ Todos los mapas generados.")
