"""
Educación Clara GT — Dashboard principal
Hackaton AI Builders GT 2026
"""

import streamlit as st
from pathlib import Path
import sys

# Asegurar imports de páginas y backend
sys.path.append(str(Path(__file__).resolve().parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend"))

from pages.home import mostrar_home
from pages.departamentos import mostrar_departamentos
from pages.brechas import mostrar_brechas
from pages.chat import mostrar_chat

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Educación Clara GT",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILO GLOBAL
# ============================================================
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1 { color: #1a365d; }
    h2, h3 { color: #2c5282; }
    [data-testid="stSidebar"] { background-color: #f7fafc; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# MENÚ LATERAL
# ============================================================
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

# ============================================================
# ROUTING
# ============================================================
if pagina == "🏠 Panorama Nacional":
    mostrar_home()

elif pagina == "🗺️ Por Departamento":
    mostrar_departamentos()

elif pagina == "⚖️ Brechas y Desigualdades":
    mostrar_brechas()

elif pagina == "💬 Pregúntale a los datos":
    mostrar_chat()
