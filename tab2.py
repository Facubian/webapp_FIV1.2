import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functions import distribution

# Función para cargar los datos
@st.cache_data
def load_data():
    import pandas as pd
    data = pd.read_csv("pagina/data_etiquetada.csv")
    return data

data = load_data()

# Función para transformar datos
def transform(data):
    return np.log(data)


def show():
  tab1, tab2 = st.tabs(["📊 Ingresar datos", "🔍 Resultados"])
  with tab1:
      st.markdown('<p class="info-text">Ingrese los valores para cada variable y observe la distribución en relación a nuestra base de datos:</p>', unsafe_allow_html=True)
    
      col1, col2, col3 = st.columns(3)
    
      with col1:
          st.markdown('<h4>Edad del paciente</h4>', unsafe_allow_html=True)
          age = st.slider("", 18, 50, 34, key="age_slider")
          fig = plt.figure(figsize=(6, 3))
          distribution(data, "edad paciente", age)
          st.markdown(f"<p>Valor ingresado: <span class='highlight'>{age} años</span></p>", unsafe_allow_html=True)
    
      with col2:
          st.markdown('<h4>Hormona Antimulleriana (AMH)</h4>', unsafe_allow_html=True)
          amh_log = st.slider("", 0.01, 13.0, 2.5, key="amh_slider")
          fig = plt.figure(figsize=(6, 3))
          distribution(data, "amh", amh_log)
          st.markdown(f"<p>Valor ingresado: <span class='highlight'>{amh_log} ng/ml</span></p>", unsafe_allow_html=True)
    
      with col3:
          st.markdown('<h4>Recuento de Folículos Antrales</h4>', unsafe_allow_html=True)
          total_rfa = st.slider("", 1, 25, 10, key="rfa_slider")
          fig = plt.figure(figsize=(6, 3))
          distribution(data, "total rfa", total_rfa)
          st.markdown(f"<p>Valor ingresado: <span class='highlight'>{total_rfa}</span></p>", unsafe_allow_html=True)
    
      # Botón para calcular predicción
      if st.button("Calcular Predicción", type="primary"):
          st.session_state.calculate = True
      else:
          if 'calculate' not in st.session_state:
              st.session_state.calculate = False

  with tab2:
    if st.session_state.get('calculate', False):
        # Preparar datos para la predicción
        df_pred = pd.DataFrame([[age, amh_log, total_rfa]])
        
        # Normalización de datos
        u_edad = 34.60
        u_amh = 2.52929
        u_rfa = 9.9528
        s_edad = 5.4431
        s_amh = 2.38858
        s_rfa = 5.32975
        
        amhn = (amh_log-u_amh)/s_amh
        edadn = (age-u_edad)/s_edad
        rfan = (total_rfa-u_rfa)/s_rfa
        
        df_pred2 = pd.DataFrame([[edadn, amhn, rfan]])
        
        # Asignar nombres de columnas
        columns = ['edad paciente', 'amh_log', 'total rfa']
        df_pred.columns = columns
        
        columns = ['edad paciente', 'amh', 'total rfa']
        df_pred2.columns = columns
        
        # Transformación logarítmica para AMH
        df_pred['amh_log'] = df_pred['amh_log'].apply(transform)
        
        # Cargar modelos
        @st.cache_resource
        def load_models():
            model1 = joblib.load('pagina/RL1_model.pkl')
            model2 = joblib.load('pagina/RL2_model.pkl')
            model3 = joblib.load('pagina/RF_model.pkl')
            return model1, model2, model3
        
        model1, model2, model3 = load_models()
        
        # Función para obtener predicciones
        def obtener_predicciones(df_pred, df_pred2):
            # Modelo 1 y 2 (Ensamble de regresores logísticos)
            prediction1 = model1.predict(df_pred)
            prediction2 = model2.predict(df_pred)
            
            # Lógica para combinar predicciones
            if prediction1 == 0:
                result = 0  # ≤4
            elif prediction1 == 1:
                if prediction2 == 1:
                    result = 2  # >9
                elif prediction2 == 0:
                    result = 1  # 5-9
            else:
                result = None
            
            # Modelo 3 (Random Forest)
            prediction3 = model3.predict(df_pred2)
            
            # Probabilidades para visualización
            proba1 = model1.predict_proba(df_pred)[0]
            proba2 = model2.predict_proba(df_pred)[0]
            proba3 = model3.predict_proba(df_pred2)[0]
            
            return prediction1, prediction2, result, prediction3, proba1, proba2, proba3
        
        # Obtener predicciones
        prediction1, prediction2, result, prediction3, proba1, proba2, proba3 = obtener_predicciones(df_pred, df_pred2)
        
        # Convertir resultados a texto
        if result == 0:
            result_str = "Menor o igual a 4"
            result_color = "#e74c3c"  # Rojo
        elif result == 1:
            result_str = "5-9"
            result_color = "#f39c12"  # Naranja
        elif result == 2:
            result_str = "Mayor a 9"
            result_color = "#2ecc71"  # Verde
        else:
            result_str = "No disponible"
            result_color = "#7f8c8d"  # Gris
        
        if prediction3 == 1:
            result_str2 = "Menor o igual a 4"
            result_color2 = "#e74c3c"  # Rojo
        elif prediction3 == 2:
            result_str2 = "5-9"
            result_color2 = "#f39c12"  # Naranja
        elif prediction3 == 3:
            result_str2 = "Mayor a 9"
            result_color2 = "#2ecc71"  # Verde
        else:
            result_str2 = "No disponible"
            result_color2 = "#7f8c8d"  # Gris
        
        # Mostrar resultados
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3>Resumen de datos del paciente</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Edad", f"{age} años")
        with col2:
            st.metric("AMH", f"{amh_log} ng/ml")
        with col3:
            st.metric("Folículos Antrales", f"{total_rfa}")
        
        st.markdown('<h3>Resultados de la predicción</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="card">
                <h4>Ensamble de Regresores Logísticos (LR)</h4>
                <p>Número esperado de ovocitos: <span style="font-size: 1.5rem; color: {result_color}; font-weight: bold;">{result_str}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Visualización de probabilidades para LR
            categories = ['≤4', '5-9', '>9']
            probs = [proba1[0] if result == 0 else (1-proba1[0]) * proba2[0] if result == 1 else (1-proba1[0]) * (1-proba2[0])]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[categories[result]],
                y=[100],
                marker_color=result_color,
                text=[f"{100:.1f}%"],
                textposition='auto',
                name="Probabilidad"
            ))
            fig.update_layout(
                title="Confianza de la predicción",
                yaxis_title="Probabilidad (%)",
                height=250,
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown(f"""
            <div class="card">
                <h4>Random Forest (RF)</h4>
                <p>Número esperado de ovocitos: <span style="font-size: 1.5rem; color: {result_color2}; font-weight: bold;">{result_str2}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Visualización de probabilidades para RF
            categories2 = ['≤4', '5-9', '>9']
            rf_probs = [proba3[0], proba3[1], proba3[2]]
            
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=categories2,
                y=[p*100 for p in rf_probs],
                marker_color=['#e74c3c', '#f39c12', '#2ecc71'],
                text=[f"{p*100:.1f}%" for p in rf_probs],
                textposition='auto',
                name="Probabilidad"
            ))
            fig2.update_layout(
                title="Distribución de probabilidades",
                yaxis_title="Probabilidad (%)",
                height=250,
                margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Recomendación basada en los resultados
        st.markdown('<h3>Interpretación clínica</h3>', unsafe_allow_html=True)
        
        if result == prediction3-1:  # Ambos modelos coinciden
            st.markdown(f"""
            <div class="card" style="background-color: #d5f5e3;">
                <h4>Alta confianza en la predicción</h4>
                <p class="info-text">
                Ambos modelos coinciden en que la paciente tiene alta probabilidad de obtener 
                <span style="font-weight: bold;">{result_str}</span> ovocitos.
                </p>
                <p class="info-text">
                Este nivel de coincidencia entre modelos indica una predicción de alta confianza.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card" style="background-color: #fdebd0;">
                <h4>Predicción con consideraciones</h4>
                <p class="info-text">
                Los modelos indican diferentes resultados:<br>
                - Ensamble de Regresores Logísticos: <span style="font-weight: bold;">{result_str}</span> ovocitos<br>
                - Random Forest: <span style="font-weight: bold;">{result_str2}</span> ovocitos
                </p>
                <p class="info-text">
                Esta diferencia sugiere que podría ser útil considerar factores adicionales antes de tomar decisiones clínicas.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sugerencias basadas en los valores de entrada
        st.markdown('<h3>Observaciones adicionales</h3>', unsafe_allow_html=True)
        
        # Lógica para comentarios personalizados
        comments = []
        
        if age > 40:
            comments.append("La edad avanzada (>40 años) puede influir significativamente en la calidad ovocitaria, independientemente del recuento.")
        
        if amh_log < 1.0:
            comments.append("El valor de AMH es bajo, lo que podría sugerir una reserva ovárica reducida.")
        elif amh_log > 5.0:
            comments.append("El valor de AMH es elevado, lo que puede indicar buena reserva ovárica pero también puede estar asociado con síndrome de ovario poliquístico.")
        
        if total_rfa < 5:
            comments.append("El recuento de folículos antrales es bajo, lo que correlaciona con los resultados de la predicción.")
        elif total_rfa > 15:
            comments.append("El recuento de folículos antrales es alto, lo que generalmente se asocia con buena respuesta a la estimulación.")
        
        if not comments:
            comments.append("Los valores ingresados se encuentran dentro de los rangos típicos de nuestra base de datos.")
        
        for comment in comments:
            st.markdown(f"""
            <div class="card">
                <p class="info-text">• {comment}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card">
            <p class="info-text">Ingrese los datos del paciente en la pestaña "Ingreso de datos" y presione "Calcular Predicción" para ver los resultados aquí.</p>
        </div>
        """, unsafe_allow_html=True)
