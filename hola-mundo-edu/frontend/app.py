"""
Educación Clara GT — Dashboard principal
Hackaton AI Builders GT 2026
"""

import streamlit as st
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "views"))
sys.path.insert(0, str(ROOT.parent / "backend"))

from views.home import mostrar_home
from views.departamentos import mostrar_departamentos
from views.brechas import mostrar_brechas
from views.chat import mostrar_chat

st.set_page_config(
    page_title="Educación Clara GT",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ocultar el menú multipágina automático de Streamlit
st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none !important; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📚 Educación Clara GT")
st.sidebar.markdown("Datos de Educación Formal 2024 · INE Guatemala")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegación",
    options=[
        "🏠 Panorama Nacional",
        "🗺️ Por Departamento",
        "⚖️ Brechas y Desigualdades",
        "💬 Pregúntale a los datos",
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Hackaton AI Builders GT 2026")
st.sidebar.caption("Fuente: datos.ine.gob.gt")

if pagina == "🏠 Panorama Nacional":
    mostrar_home()
elif pagina == "🗺️ Por Departamento":
    mostrar_departamentos()
elif pagina == "⚖️ Brechas y Desigualdades":
    mostrar_brechas()
elif pagina == "💬 Pregúntale a los datos":
    mostrar_chat()