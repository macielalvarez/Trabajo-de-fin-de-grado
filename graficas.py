import pandas as pd
import matplotlib.pyplot as plt
import os
from math import pi
import matplotlib.dates as mdates

archivo = r".\DATOS IVIA\ivia_descargas16\datos_vina_vino_2020_2024.csv"
os.makedirs("graficos", exist_ok=True)

carpeta_base = os.path.dirname(archivo)

# Crear carpeta "graficos" dentro de esa misma ruta
carpeta_graficos = os.path.join(carpeta_base, "graficos")
os.makedirs(carpeta_graficos, exist_ok=True)

with open(archivo, "r", encoding="utf-8") as f:
    primera_linea = f.readline()
if "\t" in primera_linea:
    sep = "\t"
elif ";" in primera_linea:
    sep = ";"
else:
    sep = ","

df = pd.read_csv(archivo, sep=sep, encoding="utf-8")
df.columns = df.columns.str.strip()

df["FechaHora"] = pd.to_datetime(df["Fecha"] + " " + df["Hora"], errors="coerce", dayfirst=True)

cols_numericas = ["Temperatura", "Humedad relativa", "Radiación (w/m²)", 
                  "Velocidad del viento (Km/h)", "Precipitación (mm)"]
for col in cols_numericas:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(",", ".").astype(float)

print("\n Datos cargados para graficar.")
print(f"Registros: {len(df)}")
print(df.head())


# TEMPERATURA ↔ HUMEDAD 
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()
ax1.plot(df["FechaHora"], df["Temperatura"],
         color="red",
         alpha=0.6,
         linewidth=1.5,
         label="Temperatura (°C)")
ax2.plot(df["FechaHora"], df["Humedad relativa"],
         color=(0.53, 0.81, 0.98, 0.25),
         linewidth=1)
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Temperatura (°C)", color=(1, 0, 0, 0.7))
ax1.tick_params(axis='y', colors=(1, 0, 0, 0.7))
ax2.set_ylabel("Humedad relativa (%)",
               color=(0.53, 0.81, 0.98, 0.5))
plt.title("Temperatura vs Humedad relativa")
fig.tight_layout()
plt.savefig(os.path.join(carpeta_graficos, "temperatura_humedad.png"), dpi=150)
plt.close()

# Radiación vs Precipitación 
fig, ax1 = plt.subplots(figsize=(10, 5))
ax2 = ax1.twinx()

ax1.plot(df["FechaHora"], df["Radiación (w/m²)"], color="orange", label="Radiación")
ax2.bar(df["FechaHora"], df["Precipitación (mm)"], color="blue", alpha=0.3, label="Precipitación")

ax1.set_xlabel("Fecha")
ax1.set_ylabel("Radiación (W/m²)", color="orange")
ax2.set_ylabel("Precipitación (mm)", color="blue")

plt.title("Radiación vs Precipitación")
fig.tight_layout()
plt.savefig(os.path.join(carpeta_graficos, "radiacion_precipitacion.png"), dpi=150)
plt.close()

# Velocidad vs Dirección del viento
direccion_a_grados = {
    "N": 0, "NNE": 22.5, "NE": 45, "ENE": 67.5,
    "E": 90, "ESE": 112.5, "SE": 135, "SSE": 157.5,
    "S": 180, "SSO": 202.5, "SO": 225, "OSO": 247.5,
    "O": 270, "ONO": 292.5, "NO": 315, "NNO": 337.5
}

df["Dirección del viento grados"] = df["Dirección del viento"].map(direccion_a_grados)

fig, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(df["FechaHora"], df["Velocidad del viento (Km/h)"],
         color="blue", linewidth=1, alpha=0.7, label="Velocidad (Km/h)")
ax1.set_ylabel("Velocidad (Km/h)", color="blue")
ax1.set_ylim(-5, df["Velocidad del viento (Km/h)"].max() + 10)

ax2 = ax1.twinx()
ax2.plot(df["FechaHora"], df["Dirección del viento grados"],
         color="red", linewidth=0.5, alpha=0.6, label="Dirección (°)")
ax2.set_ylabel("Dirección del viento (°)", color="red")
ax2.set_ylim(-20, 380)

plt.title("Viento - Dirección (estilo IVIA)")
fig.tight_layout()
plt.savefig(os.path.join(carpeta_graficos, "viento_direccion_estilo_IVIA.png"), dpi=150)
plt.close()

print("\n Gráficos generados correctamente en la carpeta 'graficos/'")