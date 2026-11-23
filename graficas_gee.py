import pandas as pd
archivo_entrada = r".\DATOS GOOGLE_EARTH\google earth2\necesidad_riego_wapor.csv"
archivo_salida = r".\DATOS GOOGLE_EARTH\google earth2\wapor_fechas_clave.csv"

df = pd.read_csv(
    archivo_entrada,
    sep=";",         
    decimal=",",
    encoding="utf-8"
)

df["Fecha"] = pd.to_datetime(df["Fecha"], format="mixed", dayfirst=True, errors="coerce")

fechas_objetivo = [
    (3, 10),   # 10marzo
    (7, 10),   # 10julio
    (9, 10)    # 10septiembre
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