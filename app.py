import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components
import os

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Sensores IoT Politecnico Gran Colombiano",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Ocultar elementos de Streamlit que no necesitamos
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 95%;
    }
</style>
""", unsafe_allow_html=True)

# Estilos CSS específicos para que las gráficas se vean como en la captura
st.markdown("""
<style>
    body {
        background-color: #1e2a3a;
        color: white;
    }
    
    /* Estilos para pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.4);
    }
    
    /* Estilos para gráficos de sensores */
    .thingspeak-container {
        background-color: #263b53;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
    }
    
    .chart-header {
        text-align: center;
        font-size: 18px;
        color: white;
        margin-bottom: 10px;
    }
    
    .chart-box {
        background-color: white;
        border-radius: 5px;
        overflow: hidden;
        margin-bottom: 20px;
    }
    
    .chart-title {
        background-color: #f1f1f1;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        color: #333;
    }
    
    .chart-iframe {
        width: 100%;
        height: 300px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Función para cargar el archivo CSV
@st.cache_data
def load_data():
    try:
        if os.path.exists('decoded_data.csv'):
            df = pd.read_csv('decoded_data.csv')
        else:
            return None
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        return df
    except Exception as e:
        return None

# Función para procesar los datos por hora
def process_hourly_data(df):
    if df is None:
        return None
    
    hourly_data = df.groupby('hour').agg({
        'temperature': 'mean',
        'humidity': 'mean',
        'co2': 'mean',
        'pressure': 'mean'
    }).reset_index()
    
    return hourly_data
# Logo e imagen de encabezado
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("poli.svg", width=300)
    except:
        st.write("Logo no encontrado. Por favor asegúrate de tener el archivo poli.svg en el directorio.")

# Título y subtítulo
st.markdown('<div class="main-header">Dashboard de Sensores IoT</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Politécnico Grancolombiano</div>', unsafe_allow_html=True)

# Crear pestañas
tab1, tab2 = st.tabs(["📡 Sensores Online", "📊 Sensor EM500-PT100"])

# Pestaña 1 - Sensores Online (ThingSpeak) - SOLUCIÓN ACTUALIZADA
with tab1:
    # Usar HTML en bruto para el diseño exacto de la captura
    components.html(
        """
        <div class="thingspeak-container">
            <div class="chart-header">Sensores IoT en Tiempo Real</div>
            
            <div class="chart-box">
                <div class="chart-title">Temperatura - Sensor IoT</div>
                <iframe 
                    class="chart-iframe" 
                    src="https://thingspeak.mathworks.com/channels/2842487/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&width=auto&height=auto"
                ></iframe>
            </div>
            
            <div class="chart-box">
                <div class="chart-title">Humedad Relativa - Sensor IoT</div>
                <iframe 
                    class="chart-iframe" 
                    src="https://thingspeak.mathworks.com/channels/2842487/charts/2?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15&width=auto&height=auto"
                ></iframe>
            </div>
            
            <div class="chart-box">
                <div class="chart-title">Humedad Suelo Planta ONE - Sensor IoT</div>
                <iframe 
                    class="chart-iframe" 
                    src="https://thingspeak.mathworks.com/channels/2899033/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15&width=auto&height=auto"
                ></iframe>
            </div>
        </div>
        <style>
            .thingspeak-container {
                background-color: #263b53;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                font-family: Arial, sans-serif;
            }
            
            .chart-header {
                text-align: center;
                font-size: 18px;
                color: white;
                margin-bottom: 15px;
                font-weight: bold;
            }
            
            .chart-box {
                background-color: white;
                border-radius: 5px;
                overflow: hidden;
                margin-bottom: 20px;
            }
            
            .chart-title {
                background-color: #f1f1f1;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                color: #333;
                border-bottom: 1px solid #ddd;
            }
            
            .chart-iframe {
                width: 100%;
                height: 300px;
                border: none;
            }
        </style>
        """,
        height=1050,  # Altura total suficiente para los tres gráficos con sus títulos
        scrolling=False
    )

# Pestaña 2 - Sensor EM500-PT100 (Archivo CSV)
with tab2:
    st.markdown('<h2 style="color: white; text-align: center;">Sensor EM500-PT100</h2>', unsafe_allow_html=True)
    
    # Cargar y procesar datos
    df = load_data()
    hourly_data = process_hourly_data(df)
    
    if hourly_data is not None:
        # Crear gráficos con plotly para mejor interactividad
        col1, col2 = st.columns(2)
        
        # Gráfico de temperatura
        with col1:
            fig_temp = px.line(
                hourly_data, 
                x='hour', 
                y='temperature',
                labels={'hour': 'Hora del día', 'temperature': 'Temperatura (°C)'},
                title='Temperatura (°C) por Hora del Día',
                line_shape='spline',
                markers=True
            )
            fig_temp.update_traces(line_color='#FF5A5F', line_width=3)
            fig_temp.update_layout(
                height=400,
                plot_bgcolor='rgba(30, 33, 48, 0.8)',
                paper_bgcolor='rgba(30, 33, 48, 0.8)',
                font=dict(color='white'),
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(0, 24)),
                    ticktext=[f'{i:02d}:00' for i in range(0, 24)],
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
            )
            st.plotly_chart(fig_temp, use_container_width=True)
            
        # Gráfico de humedad
        with col2:
            fig_hum = px.line(
                hourly_data, 
                x='hour', 
                y='humidity',
                labels={'hour': 'Hora del día', 'humidity': 'Humedad (%)'},
                title='Humedad Relativa (%) por Hora del Día',
                line_shape='spline',
                markers=True
            )
            fig_hum.update_traces(line_color='#36A2EB', line_width=3)
            fig_hum.update_layout(
                height=400,
                plot_bgcolor='rgba(30, 33, 48, 0.8)',
                paper_bgcolor='rgba(30, 33, 48, 0.8)',
                font=dict(color='white'),
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(0, 24)),
                    ticktext=[f'{i:02d}:00' for i in range(0, 24)],
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
            )
            st.plotly_chart(fig_hum, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        # Gráfico de CO2
        with col3:
            fig_co2 = px.line(
                hourly_data, 
                x='hour', 
                y='co2',
                labels={'hour': 'Hora del día', 'co2': 'CO2 (ppm)'},
                title='CO2 (ppm) por Hora del Día',
                line_shape='spline',
                markers=True
            )
            fig_co2.update_traces(line_color='#4BC0C0', line_width=3)
            fig_co2.update_layout(
                height=400,
                plot_bgcolor='rgba(30, 33, 48, 0.8)',
                paper_bgcolor='rgba(30, 33, 48, 0.8)',
                font=dict(color='white'),
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(0, 24)),
                    ticktext=[f'{i:02d}:00' for i in range(0, 24)],
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
            )
            st.plotly_chart(fig_co2, use_container_width=True)
            
        # Gráfico de presión
        with col4:
            fig_press = px.line(
                hourly_data, 
                x='hour', 
                y='pressure',
                labels={'hour': 'Hora del día', 'pressure': 'Presión (hPa)'},
                title='Presión Atmosférica (hPa) por Hora del Día',
                line_shape='spline',
                markers=True
            )
            fig_press.update_traces(line_color='#9966FF', line_width=3)
            fig_press.update_layout(
                height=400,
                plot_bgcolor='rgba(30, 33, 48, 0.8)',
                paper_bgcolor='rgba(30, 33, 48, 0.8)',
                font=dict(color='white'),
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(0, 24)),
                    ticktext=[f'{i:02d}:00' for i in range(0, 24)],
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
            )
            st.plotly_chart(fig_press, use_container_width=True)
        
        # Estadísticas generales
        st.markdown('<h3 style="color: white; margin-top: 30px;">Estadísticas de los sensores</h3>', unsafe_allow_html=True)
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            st.metric(
                label="Temperatura Promedio", 
                value=f"{df['temperature'].mean():.1f} °C",
                delta=f"{df['temperature'].mean() - 20:.1f} °C vs. referencia"
            )
        
        with stats_col2:
            st.metric(
                label="Humedad Promedio", 
                value=f"{df['humidity'].mean():.1f}%",
                delta=f"{df['humidity'].mean() - 60:.1f}% vs. ideal"
            )
            
        with stats_col3:
            st.metric(
                label="CO2 Promedio", 
                value=f"{df['co2'].mean():.0f} ppm",
                delta=f"{df['co2'].mean() - 400:.0f} ppm vs. normal"
            )
            
        with stats_col4:
            st.metric(
                label="Presión Promedio", 
                value=f"{df['pressure'].mean():.1f} hPa"
            )
        
        # Información adicional
        with st.expander("Ver detalles del dataset"):
            st.write("Información del archivo CSV cargado:")
            st.write(f"- Total de registros: {len(df)}")
            st.write(f"- Rango de fechas: {df['timestamp'].min()} a {df['timestamp'].max()}")
            st.write(f"- Temperatura mínima: {df['temperature'].min():.1f}°C, máxima: {df['temperature'].max():.1f}°C")
            st.write(f"- Humedad mínima: {df['humidity'].min():.1f}%, máxima: {df['humidity'].max():.1f}%")
            st.dataframe(df.describe())
    else:
        st.warning("No se pudieron cargar los datos del sensor EM500-PT100. Verifica que el archivo decoded_data.csv esté disponible.")
        
        # Datos de muestra en caso de error
        st.info("Mostrando datos de ejemplo para visualización:")
        
        # Crear datos de ejemplo
        hours = list(range(24))
        sample_temp = [22 + 5 * np.sin(i * np.pi/12) for i in hours]
        sample_humidity = [60 + 20 * np.sin((i + 6) * np.pi/12) for i in hours]
        sample_co2 = [400 + 100 * np.sin(i * np.pi/8) for i in hours]
        sample_pressure = [750 + 2 * np.sin(i * np.pi/6) for i in hours]
        
        sample_df = pd.DataFrame({
            'hour': hours,
            'temperature': sample_temp,
            'humidity': sample_humidity,
            'co2': sample_co2,
            'pressure': sample_pressure
        })
        
        # Mostrar gráficos con datos de ejemplo
        col1, col2 = st.columns(2)
        
        with col1:
            fig_temp = px.line(
                sample_df, 
                x='hour', 
                y='temperature',
                labels={'hour': 'Hora del día', 'temperature': 'Temperatura (°C)'},
                title='Temperatura (°C) por Hora del Día (EJEMPLO)',
                line_shape='spline',
                markers=True
            )
            fig_temp.update_traces(line_color='#FF5A5F', line_width=3)
            fig_temp.update_layout(
                height=400,
                plot_bgcolor='rgba(30, 33, 48, 0.8)',
                paper_bgcolor='rgba(30, 33, 48, 0.8)',
                font=dict(color='white'),
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(0, 24)),
                    ticktext=[f'{i:02d}:00' for i in range(0, 24)],
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
            )
            st.plotly_chart(fig_temp, use_container_width=True)
            
        # Resto de gráficos para los datos de ejemplo (similar a los anteriores)
        with col2:
            fig_hum = px.line(
                sample_df, 
                x='hour', 
                y='humidity',
                labels={'hour': 'Hora del día', 'humidity': 'Humedad (%)'},
                title='Humedad Relativa (%) por Hora del Día (EJEMPLO)',
                line_shape='spline',
                markers=True
            )
            fig_hum.update_traces(line_color='#36A2EB', line_width=3)
            fig_hum.update_layout(
                height=400,
                plot_bgcolor='rgba(30, 33, 48, 0.8)',
                paper_bgcolor='rgba(30, 33, 48, 0.8)',
                font=dict(color='white'),
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(0, 24)),
                    ticktext=[f'{i:02d}:00' for i in range(0, 24)],
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
            )
            st.plotly_chart(fig_hum, use_container_width=True)

# Pie de página
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 12px;">
        Dashboard de Sensores IoT © 2025 | Politécnico Grancolombiano
    </div>
    """, 
    unsafe_allow_html=True
)
