# ==========================================================================
# TAREA 4: SCRIPT DE STREAMLIT (app_ecotransito.py)
# ==========================================================================
# ==========================================================================
# TAREA 4: SCRIPT DE STREAMLIT (app_ecotransito.py)
# ==========================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(page_title="EcoTransito CDMX", page_icon="🌎", layout="wide")
st.title("🌎 Dashboard EcoTransito CDMX")

# Datos de ejemplo (puedes reemplazar con tu CSV)
data = {
    'Timestamp': pd.date_range("2026-10-01 08:00:00", periods=10, freq="h"),
    'Zona_Estacion': ['centro_historico','zona_oriente','zona_sur','zona_oriente','zona_sur',
                      'centro_historico','zona_oriente','zona_sur','zona_oriente','zona_sur'],
    'Concentracion_PM25': [35.4, 42.1, 120.5, 310.0, 18.2, 25.0, 40.0, 55.0, 60.0, 22.0],
    'Nivel_NO2': [42.1, 48.5, 89.2, 195.0, 22.4, 30.0, 45.0, 60.0, 70.0, 25.0],
    'Indice_Trafico_Vehicular': [85.0, 92.5, 98.0, 15.0, 45.0, 60.0, 75.0, 80.0, 90.0, 50.0],
}
df = pd.DataFrame(data)

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Promedio PM2.5", f"{df['Concentracion_PM25'].mean():.2f}")
col2.metric("Promedio NO2", f"{df['Nivel_NO2'].mean():.2f}")
col3.metric("Promedio Tráfico", f"{df['Indice_Trafico_Vehicular'].mean():.2f}")

# Pestañas
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 PM2.5", "📦 NO2", "🚗 Tráfico", "⚙️ Estado Sensor",
    "🔗 Correlaciones", "📉 Dispersión", "🌐 Gráfico 3D"
])

with tab1:
    st.subheader("Evolución temporal de PM2.5")
    fig = px.line(df, x="Timestamp", y="Concentracion_PM25", color="Zona_Estacion", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Distribución de NO2 por zona")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="Zona_Estacion", y="Nivel_NO2", ax=ax)
    st.pyplot(fig)

with tab3:
    st.subheader("Histograma del tráfico vehicular")
    fig, ax = plt.subplots()
    sns.histplot(df['Indice_Trafico_Vehicular'], bins=10, kde=True, ax=ax)
    st.pyplot(fig)


with tab4:
    st.subheader("Matrices de correlación")

    # Seleccionar solo columnas numéricas
    numeric_cols = df.select_dtypes(include=['float64','int64']).columns

    st.write("Pearson:")
    st.dataframe(df[numeric_cols].corr(method="pearson"))

    st.write("Spearman:")
    st.dataframe(df[numeric_cols].corr(method="spearman"))


with tab5:
    st.subheader("Gráfico de dispersión PM2.5 vs NO2")
    fig = px.scatter(df, x="Concentracion_PM25", y="Nivel_NO2", color="Zona_Estacion", size="Indice_Trafico_Vehicular")
    st.plotly_chart(fig, use_container_width=True)

with tab6:
    st.subheader("Gráfico 3D multivariado (PM2.5, NO2, Tráfico)")
    fig = px.scatter_3d(df, x="Concentracion_PM25", y="Nivel_NO2", z="Indice_Trafico_Vehicular",
                        color="Zona_Estacion", size="Indice_Trafico_Vehicular")
    st.plotly_chart(fig, use_container_width=True)
