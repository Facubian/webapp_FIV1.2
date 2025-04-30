import streamlit as st

def show():
    # Sección de introducción
  with st.container():
    col1, col2 = st.columns(2)
    with col1:
      st.markdown("""
    <h2 class="sub-header">¿Qué es Embryoxite LAB?</h2>
    <p class="info-text">
    Embryoxite LAB combina modelos avanzados de inteligencia artificial entrenados con datos reales 
    para predecir el número potencial de ovocitos a recuperar en pacientes sometidos a tratamientos 
    de reproducción asistida. Esta herramienta ayuda a los médicos a optimizar protocolos y 
    proporcionar expectativas más precisas a sus pacientes.
    </p>""", unsafe_allow_html=True)
    
    with col2:
      st.markdown('<h3 class="sub-header">Modelos disponibles:</h3>', unsafe_allow_html=True)
      scol1, scol2 = st.columns(2)
      with scol1:
    
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">LR</div>
            <div class="metric-label">Ensamble de regresores logísticos v1</div>
        </div>
        """, unsafe_allow_html=True)
      with scol2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">RF</div>
            <div class="metric-label">Random Forest v1</div>
        </div>
        """, unsafe_allow_html=True)
    
      st.markdown('</div>', unsafe_allow_html=True)