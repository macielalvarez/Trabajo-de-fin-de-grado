import pandas as pd

archivo_entrada = r".\DATOS IVIA 2.0\ivia4\necesidad_de_riego.csv"
archivo_salida = r".\DATOS IVIA 2.0\ivia4\graficaaaaaaa.csv"

df = pd.read_csv(
    archivo_entrada,
    sep=";",  
    decimal=",",    
    encoding="utf-8"
)

df["Fecha"] = pd.to_datetime(
    df["Fecha"],
    format="mixed",      
    dayfirst=True,
    errors="coerce" 
)

df = df.dropna(subset=["Fecha"])

fechas_objetivo = [
    (3, 10),   # 10 de marzo
    (7, 10),   # 10 de julio
    (9, 10)    # 10 de septiembre
]

df_filtrado = df[
    df["Fecha"].apply(lambda x: (x.month, x.day) in fechas_objetivo)
]

df_filtrado = df_filtrado.sort_values("Fecha")

df_filtrado.to_csv(
    archivo_salida,
    sep=";",
    decimal=",",
    index=False,
    encoding="utf-8"
)

print("Archivo generado correctamente:", archivo_salida)