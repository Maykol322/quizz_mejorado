import streamlit as st
import time
from datetime import datetime
import pandas as pd
import json
import os

# ======================
# CONFIGURACIÓN INICIAL
# ======================
st.set_page_config(
    page_title="Quiz Interactivo Pro",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Cargar estilos CSS
def load_css():
    css = """
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.02);
        }
        .question-card {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
        .score-display {
            font-size: 1.2rem;
            font-weight: bold;
            color: #2c3e50;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# ======================
# GESTIÓN DE DATOS
# ======================
def load_questions():
    """Carga las preguntas desde un archivo JSON o usa las predeterminadas"""
    if os.path.exists("questions.json"):
        with open("questions.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return [
    {"pregunta": "¿Qué lenguaje se ejecuta principalmente en navegadores web?", "opciones": ["Java", "Python", "JavaScript", "C++"], "respuesta_correcta": "JavaScript"},
    {"pregunta": "¿Qué significa 'IDE' en programación?", "opciones": ["Internet Development Environment", "Integrated Development Environment", "Internal Debugging Engine", "Intelligent Design Editor"], "respuesta_correcta": "Integrated Development Environment"},
    {"pregunta": "¿Cuál de estos es un lenguaje orientado a objetos?", "opciones": ["HTML", "Python", "SQL", "CSS"], "respuesta_correcta": "Python"},
    {"pregunta": "¿Qué estructura permite repetir instrucciones en programación?", "opciones": ["Condicional", "Bucle", "Variable", "Función"], "respuesta_correcta": "Bucle"},
    {"pregunta": "¿Qué símbolo se usa para comentar una línea en Python?", "opciones": ["//", "/*", "#", "--"], "respuesta_correcta": "#"},

    {"pregunta": "¿Cuál es la fórmula del agua?", "opciones": ["CO2", "H2O", "O2", "CH4"], "respuesta_correcta": "H2O"},
    {"pregunta": "¿Qué planeta es conocido como el planeta rojo?", "opciones": ["Marte", "Venus", "Júpiter", "Saturno"], "respuesta_correcta": "Marte"},
    {"pregunta": "¿Qué órgano humano bombea la sangre?", "opciones": ["Pulmón", "Riñón", "Corazón", "Hígado"], "respuesta_correcta": "Corazón"},
    {"pregunta": "¿Qué científico propuso la teoría de la relatividad?", "opciones": ["Newton", "Tesla", "Einstein", "Galileo"], "respuesta_correcta": "Einstein"},
    {"pregunta": "¿Cuál es la unidad básica de la vida?", "opciones": ["Átomo", "Célula", "Molécula", "Tejido"], "respuesta_correcta": "Célula"},

    {"pregunta": "¿En qué año llegó Cristóbal Colón a América?", "opciones": ["1492", "1500", "1512", "1485"], "respuesta_correcta": "1492"},
    {"pregunta": "¿Qué imperio construyó el Coliseo?", "opciones": ["Egipcio", "Romano", "Griego", "Inca"], "respuesta_correcta": "Romano"},
    {"pregunta": "¿Quién fue el primer presidente de los Estados Unidos?", "opciones": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "John Adams"], "respuesta_correcta": "George Washington"},
    {"pregunta": "¿Dónde se firmó la Declaración de Independencia de EE. UU.?", "opciones": ["Boston", "Filadelfia", "Nueva York", "Washington D.C."], "respuesta_correcta": "Filadelfia"},
    {"pregunta": "¿En qué siglo fue la Revolución Francesa?", "opciones": ["XV", "XVI", "XVII", "XVIII"], "respuesta_correcta": "XVIII"},

    {"pregunta": "¿Quién escribió 'Cien años de soledad'?", "opciones": ["Mario Vargas Llosa", "Julio Cortázar", "Gabriel García Márquez", "Pablo Neruda"], "respuesta_correcta": "Gabriel García Márquez"},
    {"pregunta": "¿Cuál es la obra más famosa de Miguel de Cervantes?", "opciones": ["La Odisea", "El Quijote", "Fausto", "La Ilíada"], "respuesta_correcta": "El Quijote"},
    {"pregunta": "¿Qué poeta escribió '20 poemas de amor y una canción desesperada'?", "opciones": ["Neruda", "Borges", "Benedetti", "Machado"], "respuesta_correcta": "Neruda"},
    {"pregunta": "¿Qué género literario es una narración breve con moraleja?", "opciones": ["Fábula", "Poema", "Ensayo", "Novela"], "respuesta_correcta": "Fábula"},
    {"pregunta": "¿Cuál de estos escritores fue peruano?", "opciones": ["Julio Cortázar", "Gabriel García Márquez", "Mario Vargas Llosa", "Pablo Neruda"], "respuesta_correcta": "Mario Vargas Llosa"},
]

preguntas = load_questions()

# ======================
# ESTADO DE LA APLICACIÓN
# ======================
def init_session_state():
    if "puntuacion" not in st.session_state:
        st.session_state.puntuacion = 0
    if "pregunta_actual" not in st.session_state:
        st.session_state.pregunta_actual = 0
    if "tiempo_inicio" not in st.session_state:
        st.session_state.tiempo_inicio = time.time()
    if "respuestas_usuario" not in st.session_state:
        st.session_state.respuestas_usuario = []
    if "quiz_completado" not in st.session_state:
        st.session_state.quiz_completado = False

init_session_state()

# ======================
# COMPONENTES DE UI
# ======================
def show_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🧠 Quiz Interactivo Pro")
        st.markdown("Demuestra tus conocimientos en programación, ciencia, historia y literatura.")
    with col2:
        st.markdown(f"<div class='score-display'>Puntuación: {st.session_state.puntuacion}/{len(preguntas)}</div>", 
                    unsafe_allow_html=True)
        
        # Mostrar barra de progreso
        progress = st.session_state.pregunta_actual / len(preguntas)
        st.progress(progress)

def show_timer():
    tiempo_transcurrido = time.time() - st.session_state.tiempo_inicio
    tiempo_por_pregunta = 30  # segundos
    tiempo_restante = max(0, tiempo_por_pregunta - (tiempo_transcurrido % tiempo_por_pregunta))
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"⏱️ Tiempo restante: {int(tiempo_restante)}s")
    with col2:
        st.caption(f"📝 Pregunta {st.session_state.pregunta_actual + 1} de {len(preguntas)}")

# ======================
# LÓGICA DEL QUIZ
# ======================
def siguiente_pregunta(seleccion):
    """Maneja la transición entre preguntas"""
    pregunta_actual = preguntas[st.session_state.pregunta_actual]
    
    # Guardar respuesta del usuario
    st.session_state.respuestas_usuario.append({
        "pregunta": pregunta_actual["pregunta"],
        "respuesta_usuario": seleccion,
        "respuesta_correcta": pregunta_actual["respuesta_correcta"],
        "es_correcta": seleccion == pregunta_actual["respuesta_correcta"],
        "tiempo": time.time() - st.session_state.tiempo_inicio
    })
    
    # Actualizar puntuación
    if seleccion == pregunta_actual["respuesta_correcta"]:
        st.session_state.puntuacion += 1
    
    # Mover a la siguiente pregunta o finalizar
    if st.session_state.pregunta_actual < len(preguntas) - 1:
        st.session_state.pregunta_actual += 1
    else:
        st.session_state.quiz_completado = True
    
    st.rerun()

def show_question():
    """Muestra la pregunta actual"""
    pregunta = preguntas[st.session_state.pregunta_actual]
    
    with st.container():
        st.markdown(f"<div class='question-card'>", unsafe_allow_html=True)
        st.subheader(pregunta["pregunta"])
        
        # Mostrar opciones con índice (A, B, C, D)
        opciones = pregunta["opciones"]
        letras = ["A", "B", "C", "D"]
        seleccion = st.radio(
            "Selecciona una opción:",
            options=opciones,
            format_func=lambda x: f"{letras[opciones.index(x)]}) {x}",
            key=f"pregunta_{st.session_state.pregunta_actual}"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Responder", key=f"btn_{st.session_state.pregunta_actual}"):
            siguiente_pregunta(seleccion)

def show_results():
    """Muestra los resultados finales"""
    st.balloons()
    st.success(f"🎉 ¡Quiz completado! Puntuación final: {st.session_state.puntuacion}/{len(preguntas)}")
    
    # Mostrar estadísticas
    st.subheader("📊 Análisis de Resultados")
    
    # Gráfico de rendimiento
    df_results = pd.DataFrame(st.session_state.respuestas_usuario)
    st.bar_chart(df_results["es_correcta"].value_counts().rename({True: "Correctas", False: "Incorrectas"}))
    
    # Tiempo promedio por pregunta
    avg_time = df_results["tiempo"].mean()
    st.metric("⏱️ Tiempo promedio por pregunta", f"{avg_time:.1f} segundos")
    
    # Botón para reiniciar
    if st.button("🔄 Reiniciar Quiz"):
        st.session_state.puntuacion = 0
        st.session_state.pregunta_actual = 0
        st.session_state.quiz_completado = False
        st.session_state.tiempo_inicio = time.time()
        st.session_state.respuestas_usuario = []
        st.rerun()

# ======================
# EJECUCIÓN PRINCIPAL
# ======================
def main():
    show_header()
    show_timer()
    
    if not st.session_state.quiz_completado:
        show_question()
    else:
        show_results()

if __name__ == "__main__":
    main()