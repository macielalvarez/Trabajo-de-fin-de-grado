import pandas as pd

archivo_entrada = r".\DATOS GOOGLE_EARTH\google earth10\RET_Villanueva_de_Castell_n_2020_2024.xlsx"
archivo_salida = r".\DATOS GOOGLE_EARTH\google earth10\necesidad_riego_wapor.csv"

KC_DEFECTO = 0.25
KC_ABRIL = 0.25
KC_MAYO = 0.55
KC_JUNIO_JULIO = 0.85
KC_AGOSTO = 0.95
KC_SEPTIEMBRE = 0.90
KC_OCTUBRE = 0.80

df = pd.read_excel(archivo_entrada)

df.columns = df.columns.str.strip()

print("Columnas detectadas:")
print(df.columns)

df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
df["Mes"] = df["Fecha"].dt.month

df["ETo (mm)"] = (df["ETo (mm)"].astype(str).str.replace(",", ".", regex=False))
df["ETo (mm)"] = pd.to_numeric(df["ETo (mm)"], errors="coerce")

df["Precipitación (mm)"] = (df["Precipitación (mm)"].astype(str).str.replace(",", ".", regex=False))
df["Precipitación (mm)"] = pd.to_numeric(df["Precipitación (mm)"], errors="coerce")

print("Número de filas antes de limpiar:", len(df))

df = df.dropna(subset=["Fecha", "ETo (mm)", "Precipitación (mm)"])

print("Número de filas después de limpiar:", len(df))

df["Kc"] = KC_DEFECTO

df.loc[df["Mes"] == 4, "Kc"] = KC_ABRIL
df.loc[df["Mes"] == 5, "Kc"] = KC_MAYO
df.loc[df["Mes"].isin([6, 7]), "Kc"] = KC_JUNIO_JULIO
df.loc[df["Mes"] == 8, "Kc"] = KC_AGOSTO
df.loc[df["Mes"] == 9, "Kc"] = KC_SEPTIEMBRE
df.loc[df["Mes"] == 10, "Kc"] = KC_OCTUBRE
df["ETc (mm)"] = df["ETo (mm)"] * df["Kc"]

df["RN (mm)"] = df["ETc (mm)"] - df["Precipitación (mm)"]

df.loc[df["RN (mm)"] < 0, "RN (mm)"] = 0

df.to_csv(
    archivo_salida,
    sep=";",
    decimal=",",
    index=False,
    encoding="utf-8-sig"
)

print("✔ Cálculo finalizado correctamente")
print("✔ Archivo generado:", archivo_salida)
