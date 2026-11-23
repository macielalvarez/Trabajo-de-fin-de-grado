# Cálculo de la necesidad de riego en cultivos mediterráneos en la Comunidad Valenciana

**Trabajo Fin de Grado – Ingeniería Informática**

## Descripción del proyecto

Este proyecto consiste en el análisis y cálculo de las necesidades hídricas del cultivo de la vid en la Comunidad Valenciana, teniendo en cuenta las condiciones climáticas y la disponibilidad de recursos hídricos.

El objetivo principal es estudiar las necesidades de riego del cultivo mediante el procesamiento de datos meteorológicos, la aplicación de técnicas de control de calidad y el cálculo de la evapotranspiración y los requerimientos hídricos.

Para ello, se han utilizado datos del Instituto Valenciano de Investigaciones Agrarias (IVIA) y datos geoespaciales obtenidos mediante Google Earth Engine y el producto WaPOR de la FAO.

## Objetivos

- Recopilar datos meteorológicos de diferentes estaciones agroclimáticas de la Comunidad Valenciana.
- Analizar datos de evapotranspiración de referencia (ETo) y precipitación.
- Implementar procesos automatizados de limpieza y control de calidad de datos.
- Calcular la evapotranspiración del cultivo (ETc) mediante coeficientes de cultivo (Kc).
- Estimar las necesidades de riego de la vid.
- Comparar los resultados obtenidos entre diferentes estaciones y periodos.
- Analizar información geoespacial para estudiar las diferencias espaciales y temporales.

## Fuentes de datos

El proyecto utiliza principalmente dos fuentes de información:

**1. Instituto Valenciano de Investigaciones Agrarias (IVIA)**

Se recopilaron datos meteorológicos correspondientes al periodo 2020-2024 de 18 estaciones agroclimáticas de la Comunidad Valenciana.

Entre las variables utilizadas se encuentran:
- Temperatura.
- Humedad relativa.
- Radiación solar.
- Velocidad del viento.
- Precipitación.
- Evapotranspiración de referencia (ETo).

Fuente: [IVIA – Datos meteorológicos](https://riegos.ivia.es/datos-meteorologicos)

**2. Google Earth Engine y FAO WaPOR**

Se utilizaron datos geoespaciales del producto WaPOR para obtener información relacionada con la evapotranspiración real y realizar análisis complementarios entre estaciones.

Fuente: [FAO WaPOR](https://data.apps.fao.org/wapor/)

## Metodología

El desarrollo del proyecto se divide en las siguientes fases:

### 1. Adquisición de datos

Recopilación de información meteorológica de las estaciones agroclimáticas del IVIA para el periodo comprendido entre 2020 y 2024.

También se obtuvieron datos geoespaciales mediante Google Earth Engine.

### 2. Control de calidad y procesamiento

Desarrollo de scripts en Python para automatizar la limpieza y validación de los datos.

Se realizaron tareas como:
- Detección y eliminación de registros duplicados.
- Identificación de valores nulos.
- Conversión y normalización de variables numéricas.
- Comprobación de rangos de valores.
- Detección de valores atípicos.

### 3. Cálculo de las necesidades de riego

Se implementaron algoritmos para estimar las necesidades hídricas del cultivo de la vid siguiendo las directrices de la FAO.

Se utilizaron coeficientes de cultivo (Kc) variables según el mes y la fase de desarrollo fenológico.

El cálculo contempla:

- Evapotranspiración del cultivo (ETc).
- Precipitación.
- Necesidad de riego (RN).

### 4. Análisis y visualización

Se generaron gráficas y resultados para estudiar la evolución de las variables meteorológicas y comparar las necesidades hídricas entre las distintas estaciones.

## Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| Python | Desarrollo y automatización de procesos |
| Pandas | Manipulación y procesamiento de datos |
| Matplotlib | Visualización de resultados |
| Google Earth Engine | Procesamiento de información geoespacial |
| Selenium | Automatización de la obtención de datos |
| GeoPandas | Análisis y representación geográfica |
| WaPOR (FAO) | Datos de evapotranspiración |
| Jupyter / Google Colab | Análisis y experimentación |

## Estructura del repositorio

```text
├── memoria/       # Memoria del Trabajo Fin de Grado
├── scripts/       # Scripts de procesamiento y análisis
├── datos/         # Información y ejemplos de datos
├── resultados/    # Gráficas y resultados obtenidos
├── README.md
├── requirements.txt
└── .gitignore
```

## Resultados

El proyecto permite procesar información meteorológica de diferentes estaciones, aplicar controles de calidad y estimar las necesidades hídricas del cultivo de la vid.

Además, facilita el análisis de las diferencias espaciales y temporales de los requerimientos de riego en la Comunidad Valenciana.

## Autora

**Vanina Maciel Alvarez Segovia**

Graduada en Ingeniería Informática.
