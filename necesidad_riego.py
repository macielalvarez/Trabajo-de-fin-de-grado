import pandas as pd

archivo_entrada = r".\DATOS IVIA 2.0\ivia1\resultados-diarios.csv"
archivo_salida = r".\DATOS IVIA 2.0\ivia1\necesidad_de_riego.csv"

KC_DEFECTO = 0.25          # Enero, Febrero, Marzo, Noviembre, Diciembre
KC_ABRIL = 0.25
KC_MAYO = 0.55
KC_JUNIO_JULIO = 0.85
KC_AGOSTO = 0.95
KC_SEPTIEMBRE = 0.90
KC_OCTUBRE = 0.80

df = pd.read_csv(
    archivo_entrada,
    sep=";",
    dtype=str,
    encoding="utf-8"
)

df.columns = df.columns.str.strip()

df["Fecha"] = pd.to_datetime(
    df["Fecha"],
    format="%d/%m/%Y",
    errors="coerce"
)

df["Mes"] = df["Fecha"].dt.month

df["ETo (mm)"] = df["ETo (mm)"].str.replace(",", ".", regex=False)
df["Precipitación (mm)"] = df["Precipitación (mm)"].str.replace(",", ".", regex=False)

df["ETo (mm)"] = pd.to_numeric(df["ETo (mm)"], errors="coerce")
df["Precipitación (mm)"] = pd.to_numeric(df["Precipitación (mm)"], errors="coerce")

df = df.dropna(subset=["Fecha", "ETo (mm)", "Precipitación (mm)"])

df["Kc"] = KC_DEFECTO

df.loc[df["Mes"] == 4, "Kc"] = KC_ABRIL
df.loc[df["Mes"] == 5, "Kc"] = KC_MAYO
df.loc[df["Mes"].isin([6, 7]), "Kc"] = KC_JUNIO_JULIO
df.loc[df["Mes"] == 8, "Kc"] = KC_AGOSTO
df.loc[df["Mes"] == 9, "Kc"] = KC_SEPTIEMBRE
df.loc[df["Mes"] == 10, "Kc"] = KC_OCTUBRE

df["ETc (mm)"] = df["ETo (mm)"] * df["Kc"]

df["RN (mm)"] = df["ETc (mm)"] - df["Precipitación (mm)"]

df["RN (mm)"] = df["RN (mm)"].clip(lower=0)

df.to_csv(
    archivo_salida,
    sep=";",
    decimal=",",
    index=False,
    encoding="utf-8-sig"
)

print("✔ Cálculo finalizado correctamente")
print("✔ Archivo generado:", archivo_salida)
