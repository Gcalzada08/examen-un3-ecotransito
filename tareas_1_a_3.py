# ==========================================================================
# EXAMEN UNIDAD 3 - ECOTRANSITO CDMX
# Tareas 1, 2 y 3: ingesta, limpieza, imputación y EDA
# ==========================================================================
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

# Mostrar todas las columnas al imprimir (útil para las capturas)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

# Carpeta donde viven los CSV (la misma del script)
CARPETA = Path(__file__).parent

# Columnas numéricas que usaremos en varias tareas
COLS_NUM = ["Concentracion_PM25", "Nivel_NO2", "Indice_Trafico_Vehicular"]


# ==========================================================================
# TAREA 1: INGESTA, DIAGNÓSTICO Y SUSTITUCIÓN DE CENTINELAS
# ==========================================================================

# Ingesta: cargar el dataset sucio desde el CSV (los "NaN" del archivo se leen como nulos)
df_raw = pd.read_csv(CARPETA / "cdmx_air_traffic_dirty.csv")
print("Datos cargados:", df_raw.shape[0], "filas x", df_raw.shape[1], "columnas")
print(df_raw.dtypes)

# a) Diagnóstico inicial: NaN, centinelas y duplicados
print("Conteo de NaN por columna:")
print(df_raw.isna().sum())

print("\nConteo de valores centinela (-999.0) en columnas numéricas:")
print((df_raw[COLS_NUM] == -999.0).sum())

print("\nNúmero de filas duplicadas:")
print(df_raw.duplicated().sum())

# b) Reemplazar el centinela -999.0 por NaN y eliminar filas totalmente duplicadas
df_raw = df_raw.replace(-999.0, np.nan)
df_raw = df_raw.drop_duplicates()

print("\nDataFrame sin centinelas ni duplicados:")
print(df_raw)


# ==========================================================================
# TAREA 2: LIMPIEZA, FEATURE ENGINEERING E IMPUTACIÓN
# ==========================================================================
df_clean = df_raw.copy()

# 1. Homogeneizar 'Zona_Estacion' (quitar espacios, pasar a minúsculas y mapear)
df_clean["Zona_Estacion"] = (
    df_clean["Zona_Estacion"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({
        "centro_historico": "Centro_Historico",
        "zona_oriente": "Zona_Oriente",
        "zona_sur": "Zona_Sur",
    })
)

# 2. Convertir 'Timestamp' a datetime y extraer la hora del día
df_clean["Timestamp"] = pd.to_datetime(df_clean["Timestamp"])
df_clean["Hora_Dia"] = df_clean["Timestamp"].dt.hour

# 3. Outliers por IQR en 'Concentracion_PM25' -> se reemplazan por NaN
Q1 = df_clean["Concentracion_PM25"].quantile(0.25)
Q3 = df_clean["Concentracion_PM25"].quantile(0.75)
IQR = Q3 - Q1
lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR

mask_outlier = (df_clean["Concentracion_PM25"] < lim_inf) | (df_clean["Concentracion_PM25"] > lim_sup)
df_clean.loc[mask_outlier, "Concentracion_PM25"] = np.nan

# 4. Imputación k-NN de los nulos restantes (solo columnas numéricas)
imputer = KNNImputer(n_neighbors=2)
df_clean[COLS_NUM] = imputer.fit_transform(df_clean[COLS_NUM])

print("\nDataFrame final (df_clean):")
print(df_clean)
print("\nNulos restantes por columna:")
print(df_clean.isna().sum())

# Guardar el dataset limpio; lo usa app_ecotransito.py
df_clean.to_csv(CARPETA / "cdmx_air_traffic_clean.csv", index=False)
print("\nArchivo guardado: cdmx_air_traffic_clean.csv")


# ==========================================================================
# TAREA 3: EDA Y ANÁLISIS DE CORRELACIÓN
# ==========================================================================

# 1. Estadísticas de forma para Concentracion_PM25
pm25 = df_clean["Concentracion_PM25"]
print("\nMedia:", pm25.mean())
print("Mediana:", pm25.median())
print("Desv. estándar:", pm25.std())
print("Skewness:", pm25.skew())
print("Kurtosis:", pm25.kurt())

# 2. Matrices de correlación (solo variables numéricas)
corr_pearson = df_clean[COLS_NUM].corr(method="pearson")
corr_spearman = df_clean[COLS_NUM].corr(method="spearman")

print("\nMatriz de correlación (Pearson):")
print(corr_pearson)

print("\nMatriz de correlación (Spearman):")
print(corr_spearman)

# 3. Diagnóstico de multicolinealidad: pares con |r| >= 0.85
for nombre, matriz in [("Pearson", corr_pearson), ("Spearman", corr_spearman)]:
    pares = [
        (a, b, round(matriz.loc[a, b], 3))
        for i, a in enumerate(COLS_NUM)
        for b in COLS_NUM[i + 1:]
        if abs(matriz.loc[a, b]) >= 0.85
    ]
    print(f"\nPares con |r| >= 0.85 ({nombre}):", pares if pares else "ninguno")
