import streamlit as st
import requests
import json
import pandas as pd

import tab1
import tab2
import tab3

# Configuración de la página
st.set_page_config(
    page_title="Embryoxite LAB - Predicción de Recuperación de Ovocitos",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #3498db;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 16px;
        line-height: 1.6;
        color: #555;
    }
    .highlight {
        color: #e74c3c;
        font-weight: 600;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        font-size: 0.8rem;
        color: #7f8c8d;
        margin-top: 2rem;
    }
    .metric-card {
        background-color: #f1f8fe;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #3498db;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
    }
    /* Color personalizado para los sliders */
    div[data-baseweb="slider"] div[role="progressbar"] {
        background-color: #3498db !important;
    }
    div[class="stRadio"] label {
        background-color: #f1f8fe;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)



# Crear una barra lateral con información y opciones
with st.sidebar:
    st.image("pagina/Logo-Embryoxite.png", width=200)
    
    st.markdown("---")
    st.markdown("### Acerca de Embryoxite")
    st.markdown("""
    Embryoxite es una empresa dedicada a la aplicación de inteligencia artificial 
    en el campo de la medicina reproductiva.
    """)
    
    st.markdown("### Enlaces")
    st.markdown("[🌐 Sitio web](https://embryoxite.life/)")
    st.markdown("[🔗 LinkedIn](https://www.linkedin.com/company/embryoxite)")
    
    st.markdown("---")
    st.markdown("### Contacto")
    st.markdown("📧 info@embryoxite.life")


# Titulo
st.markdown('<h1 class="main-header">Embryoxite LAB</h1>', unsafe_allow_html=True)
st.markdown("""
Plataforma avanzada de inteligencia artificial para la predicción de recuperación 
de ovocitos en pacientes de tratamientos de reproducción asistida.

""")


# Sección principal de predicción
st.markdown('<h2 class="sub-header">Predicción de Recuperación de Ovocitos</h2>', unsafe_allow_html=True)

# Crear pestañas para separar la entrada de datos y los resultados
tabs = st.tabs(["📊 Inicio", "🔍 Modelo", "Detalles del modelo"])

with tabs[0]:
  tab1.show()

with tabs[1]:
  tab2.show()

with tabs[2]:
  tab3.show()

