# ==========================================================================
# TAREA 4: SCRIPT DE STREAMLIT (app_ecotransito.py)
# ==========================================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# 1. Configuración de página
st.set_page_config(
    page_title="EcoTransito CDMX",
    page_icon="🌎",
    layout="wide"
)

st.title("🌎 Dashboard EcoTransito CDMX")
st.write("Aplicación interactiva para visualizar calidad del aire y tráfico.")

# --------------------------------------------------------------------------
# 2. Carga y filtrado de datos con barra lateral
# (Aquí puedes reemplazar con lectura de CSV real)
data = {
    'ID_Registro': ['REG-001','REG-002','REG-003','REG-004','REG-005'],
    'Timestamp': pd.date_range("2026-10-01 08:00:00", periods=5, freq="H"),
    'Zona_Estacion': ['centro_historico','zona_oriente','zona_oriente','zona_sur','zona_sur'],
    'Concentracion_PM25': [35.4, 42.1, 120.5, 310.0, 18.2],
    'Nivel_NO2': [42.1, 48.5, 89.2, 195.0, 22.4],
    'Indice_Trafico_Vehicular': [85.0, 92.5, 98.0, 15.0, 45.0],
    'Estado_Sensor': ['Normal','Normal','Alerta','Falla','Normal']
}
df = pd.DataFrame(data)

zonas = st.sidebar.multiselect("Selecciona zonas:", df['Zona_Estacion'].unique(), default=df['Zona_Estacion'].unique())
df_filtered = df[df['Zona_Estacion'].isin(zonas)]

# --------------------------------------------------------------------------
# 3. Métricas principales (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Promedio PM2.5", f"{df_filtered['Concentracion_PM25'].mean():.2f}")
col2.metric("Promedio NO2", f"{df_filtered['Nivel_NO2'].mean():.2f}")
col3.metric("Promedio Tráfico", f"{df_filtered['Indice_Trafico_Vehicular'].mean():.2f}")

# --------------------------------------------------------------------------
# 4. Pestañas interactivas de visualización (Plotly + Seaborn)
tab1, tab2, tab3, tab4 = st.tabs(["📈 PM2.5", "📦 NO2", "🚗 Tráfico", "⚙️ Estado Sensor"])

with tab1:
    st.subheader("Evolución temporal de PM2.5")
    fig = px.line(df_filtered, x="Timestamp", y="Concentracion_PM25", color="Zona_Estacion", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Distribución de NO2 por zona")
    fig, ax = plt.subplots()
    sns.boxplot(data=df_filtered, x="Zona_Estacion", y="Nivel_NO2", ax=ax)
    st.pyplot(fig)

