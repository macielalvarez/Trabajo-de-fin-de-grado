import pandas as pd
import csv

archivo = r".\DATOS IVIA\ivia_descargas3\datos_vina_vino_2020_2024.csv"

with open(archivo, "r", encoding="utf-8-sig") as f:
    dialect = csv.Sniffer().sniff(f.read(5000))
    sep = dialect.delimiter

df = pd.read_csv(
    archivo,
    sep=sep,
    engine="python",
    on_bad_lines="skip",
    encoding="utf-8-sig"
)

print("\n Archivo leído correctamente.")
print(f"Filas totales: {len(df)}, Columnas: {len(df.columns)}")
print("Columnas detectadas:", list(df.columns))

columnas_numericas = [
    "Temperatura",
    "Humedad relativa",
    "Radiación (w/m²)",
    "Velocidad del viento (Km/h)",
    "Precipitación (mm)"
]

for col in columnas_numericas:
    if col in df.columns:
        df[col] = (
            df[col].astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace(" ", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

print("\n Conversión de valores numéricos realizada correctamente.")

print("\n Verificación de valores nulos por columna:")
print(df.isnull().sum())


duplicados_mask = df.duplicated(keep=False)
duplicados = df[duplicados_mask].copy()


print(f"\n Registros duplicados encontrados (fila completa): {len(duplicados)}")

if len(duplicados) > 0:
    duplicados.to_csv(
        r".\DATOS IVIA\ivia_descargas3datos_duplicados.csv",
        index=False,
        sep=sep,
        encoding="utf-8-sig"
    )
    print(" Duplicados guardados en 'datos_duplicados.csv'.")
else:
    print(" No se encontraron filas duplicadas completas.")

df = df.drop_duplicates()


def verificar_rangos(df):
    errores = {}

    if "Temperatura" in df.columns:
        errores["Temperatura"] = df[(df["Temperatura"] < -30) 
            | (df["Temperatura"] > 50)]

    if "Humedad relativa" in df.columns:
        errores["Humedad relativa"] = df[(df["Humedad relativa"] < 0) 
            | (df["Humedad relativa"] > 100)]

    if "Radiación (w/m²)" in df.columns:
        errores["Radiación (w/m²)"] = df[(df["Radiación (w/m²)"] < 0) 
            | (df["Radiación (w/m²)"] > 1400)]

    if "Velocidad del viento (Km/h)" in df.columns:
        errores["Velocidad del viento (Km/h)"] = df[(df["Velocidad del viento (Km/h)"] < 0) 
            |(df["Velocidad del viento (Km/h)"] > 200)]

    if "Precipitación (mm)" in df.columns:
        errores["Precipitación (mm)"] = df[df["Precipitación (mm)"] < 0]

    return errores

errores = verificar_rangos(df)

print("\n Comprobación de valores fuera de rango:")
for variable, registros in errores.items():
    print(f"{variable}: {len(registros)} registros fuera de rango")

df_limpio = df.copy()

df_limpio = df_limpio.dropna(
    subset=["Temperatura", "Humedad relativa", "Radiación (w/m²)"],
    how="all"
)

df_limpio.to_csv(
    r".\DATOS IVIA\ivia_descargas3\datos_meteorologicos_limpios.csv",
    index=False,
    sep=sep,
    encoding="utf-8-sig"
)

print("\n Archivo limpio guardado como 'datos_meteorologicos_limpios.csv'")

print("\n RESUMEN FINAL POR ESTACIÓN:")

if "Estación" in df.columns:
    estaciones = df["Estación"].unique()

    for est in estaciones:
        sub = df[df["Estación"] == est]

        print("\n--------------------------------------------")
        print(f" Estación: {est}")
        print(f"   Registros totales: {len(sub)}")
        print(f"   Valores nulos:")
        print(sub.isnull().sum())
        print("--------------------------------------------")

else:
    print(" No existe la columna 'Estación' en el archivo.")


print("\n Control de calidad completado correctamente.")
