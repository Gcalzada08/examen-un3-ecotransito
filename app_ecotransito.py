# ==========================================================================
# TAREA 4: SCRIPT DE STREAMLIT (app_ecotransito.py)
# Ejecutar con:  streamlit run app_ecotransito.py
# Requiere cdmx_air_traffic_clean.csv (lo genera tareas_1_a_3.py)
# ==========================================================================
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

COLS_NUM = ["Concentracion_PM25", "Nivel_NO2", "Indice_Trafico_Vehicular"]
RUTA_CSV = Path(__file__).parent / "cdmx_air_traffic_clean.csv"

# 1. Configuración de página
st.set_page_config(page_title="Sistema EcoTránsito CDMX", layout="wide")
st.title("Sistema EcoTránsito CDMX")


# 2. Carga de datos limpios (en caché para no leer el archivo en cada interacción)
@st.cache_data
def cargar_datos(ruta: Path) -> pd.DataFrame:
    return pd.read_csv(ruta, parse_dates=["Timestamp"])


if not RUTA_CSV.exists():
    st.error("No se encontró cdmx_air_traffic_clean.csv. Ejecuta primero: python tareas_1_a_3.py")
    st.stop()

df = cargar_datos(RUTA_CSV)

# 3. Barra lateral: selector dinámico de zonas
st.sidebar.header("Filtros")
zonas = sorted(df["Zona_Estacion"].unique())
zonas_sel = st.sidebar.multiselect("Zona de estación", options=zonas, default=zonas)

df_filtrado = df[df["Zona_Estacion"].isin(zonas_sel)]

# 4. KPIs (si el filtro deja la tabla vacía, se avisa y se detiene la app)
if df_filtrado.empty:
    st.warning("⚠ No hay datos para los filtros seleccionados. Ajusta la selección en la barra lateral.")
    st.stop()

col1, col2, col3 = st.columns(3)
col1.metric("Total de lecturas activas", len(df_filtrado))
col2.metric("Promedio PM₂.₅ (µg/m³)", f"{df_filtrado['Concentracion_PM25'].mean():.1f}")
col3.metric("Índice máximo de tráfico", f"{df_filtrado['Indice_Trafico_Vehicular'].max():.1f}")

# 5. Pestañas de visualización
tab1, tab2 = st.tabs(["Dispersión (Plotly)", "Correlaciones (Seaborn)"])

with tab1:
    st.subheader("Tráfico vehicular vs. PM2.5")
    fig = px.scatter(
        df_filtrado,
        x="Indice_Trafico_Vehicular",
        y="Concentracion_PM25",
        color="Zona_Estacion",
        hover_data=["ID_Registro", "Hora_Dia"],
    )
    st.plotly_chart(fig, width="stretch")

with tab2:
    st.subheader("Mapa de calor de correlación")
    corr = df_filtrado[COLS_NUM].corr()
    fig_hm, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="RdBu_r", vmin=-1, vmax=1, fmt=".2f", ax=ax)
    st.pyplot(fig_hm)
