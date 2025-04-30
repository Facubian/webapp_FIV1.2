import streamlit as st

def show():
  st.markdown('<h2 class="sub-header">Detalles de los modelos</h2>', unsafe_allow_html=True)
    
  st.markdown("""
    <div class="card">
        <h3>Ensamble de Regresores Logísticos (LR)</h3>
        <p class="info-text">
        Este modelo utiliza dos clasificadores logísticos en cascada:
        <ul>
            <li>Primer clasificador: Predice si el número de ovocitos será ≤4 o >4</li>
            <li>Segundo clasificador: Para casos >4, predice si será 5-9 o >9</li>
        </ul>
        Parámetros de entrenamiento:
        <ul>
            <li>Regularización L2</li>
            <li>Validación cruzada de 5 folds</li>
            <li>Balanceo de clases</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
  st.markdown("""
    <div class="card">
        <h3>Random Forest (RF)</h3>
        <p class="info-text">
        Este modelo utiliza un Random Forest para clasificar directamente en tres categorías:
        <ul>
            <li>Clase 1: ≤4 ovocitos</li>
            <li>Clase 2: 5-9 ovocitos</li>
            <li>Clase 3: >9 ovocitos</li>
        </ul>
        Parámetros de entrenamiento:
        <ul>
            <li>Número de árboles: 100</li>
            <li>Profundidad máxima: 10</li>
            <li>Features por split: sqrt</li>
        </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)
