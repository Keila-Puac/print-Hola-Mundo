"""
Página: Chat con los datos
Agente en lenguaje natural que responde solo con datos reales.
"""

import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "backend"))

try:
    from agent import preguntar_al_agente
except Exception as e:
    preguntar_al_agente = None
    _agent_error = str(e)


def mostrar_chat():
    st.title("💬 Pregúntale a los datos")
    st.markdown(
        "Puedes hacer preguntas en lenguaje natural sobre los datos de Educación Formal 2024. "
        "El agente **solo usa los números reales** generados por el análisis y no inventa cifras."
    )
    st.markdown("---")

    # Ejemplos de preguntas
    with st.expander("💡 Ejemplos de preguntas que puedes hacer"):
        st.markdown("""
        - ¿Cuántos estudiantes hay en total?
        - ¿Qué departamento tiene la mayor tasa de retiro?
        - ¿Cómo se comparan el área rural y la urbana?
        - ¿Cuál es el nivel educativo con más abandono?
        - ¿Por qué se señala un departamento como crítico?
        - Dame el panorama general de la educación en 2024
        """)

    # Historial de chat
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

    # Mostrar historial
    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input del usuario
    pregunta = st.chat_input("Escribe tu pregunta aquí...")

    if pregunta:
        # Mostrar pregunta del usuario
        st.session_state.mensajes.append({"role": "user", "content": pregunta})
        with st.chat_message("user"):
            st.markdown(pregunta)

        # Generar respuesta
        with st.chat_message("assistant"):
            with st.spinner("Consultando los datos..."):
                if preguntar_al_agente is None:
                    respuesta = (
                        "El agente no está disponible en este momento.\n\n"
                        f"Error técnico: {_agent_error}\n\n"
                        "Puedes revisar los indicadores en las otras pestañas del dashboard."
                    )
                else:
                    try:
                        respuesta = preguntar_al_agente(pregunta)
                    except Exception as e:
                        respuesta = (
                            f"Ocurrió un error al consultar el agente: {e}\n\n"
                            "Mientras tanto puedes explorar las pestañas de Panorama Nacional, "
                            "Por Departamento y Brechas."
                        )

                st.markdown(respuesta)

        st.session_state.mensajes.append({"role": "assistant", "content": respuesta})

    # Botón para limpiar historial
    if st.session_state.mensajes:
        if st.button("🗑️ Limpiar conversación"):
            st.session_state.mensajes = []
            st.rerun()

    st.markdown("---")
    st.caption(
        "El agente está diseñado para **no inventar cifras**. "
        "Si no tiene el dato exacto, te lo dirá claramente."
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Chat con los datos", layout="wide")
    mostrar_chat()
