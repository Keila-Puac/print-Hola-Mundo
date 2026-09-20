"""
Página: Por Departamento
Muestra indicadores e insights por departamento.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys
import json

sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "backend"))
from config import DATA_PROCESSED
from analytics import generar_insight_departamento


@st.cache_data
def cargar_resumen():
    return pd.read_parquet(DATA_PROCESSED / "resumen_departamentos.parquet")


@st.cache_data
def cargar_promedio_nacional():
    ruta = DATA_PROCESSED / "indicadores_nacionales.json"
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("promedio_retiro_nacional", 0.0)


def mostrar_departamentos():
    st.title("Indicadores por Departamento")
    st.markdown(
        "Selecciona un departamento para ver sus resultados y una explicación "
        "clara de lo que significan los números."
    )
    st.markdown("---")

    try:
        df = cargar_resumen()
        promedio_nacional = cargar_promedio_nacional()
    except Exception as e:
        st.error("No se encontraron los datos procesados. Ejecuta primero el pipeline.")
        st.code("python scripts/run_pipeline.py")
        st.stop()

    # Selector de departamento
    departamentos = sorted(df["Departamento"].unique().tolist())
    depto_sel = st.selectbox(
        "Elige un departamento",
        options=departamentos,
        index=0
    )

    fila = df[df["Departamento"] == depto_sel].iloc[0]

    # ============================================================
    # KPIs del departamento
    # ============================================================
    st.subheader(f"Resultados de {depto_sel}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de estudiantes", f"{int(fila['total']):,}")

    with col2:
        st.metric(
            "% Promoción",
            f"{fila['tasa_promocion']}%",
            delta=None
        )

    with col3:
        st.metric(
            "% No promovidos",
            f"{fila['tasa_no_promocion']}%"
        )

    with col4:
        delta_retiro = fila["tasa_retiro"] - promedio_nacional
        st.metric(
            "% Retiro",
            f"{fila['tasa_retiro']}%",
            delta=f"{delta_retiro:+.1f} vs nacional",
            delta_color="inverse"
        )

    st.markdown("")

    # ============================================================
    # Insight generado automáticamente
    # ============================================================
    st.subheader("¿Qué significa esto?")
    insight = generar_insight_departamento(fila, promedio_nacional)
    st.info(insight)

    st.markdown("---")

    # ============================================================
    # Comparación visual con el resto del país
    # ============================================================
    st.subheader("Comparación con todos los departamentos")

    df_ordenado = df.sort_values("tasa_retiro", ascending=True).copy()
    df_ordenado["color"] = df_ordenado["Departamento"].apply(
        lambda x: "#e74c3c" if x == depto_sel else "#3498db"
    )

    fig = px.bar(
        df_ordenado,
        x="tasa_retiro",
        y="Departamento",
        orientation="h",
        text="tasa_retiro",
        color="color",
        color_discrete_map="identity",
        labels={"tasa_retiro": "Tasa de retiro (%)", "Departamento": ""},
        title="Tasa de retiro por departamento (el seleccionado aparece en rojo)"
    )
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    fig.update_layout(
        height=max(400, len(df) * 28),
        showlegend=False,
        margin=dict(t=50, b=20),
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tabla completa
    with st.expander("Ver tabla completa de todos los departamentos"):
        tabla = df[["Departamento", "total", "tasa_promocion", "tasa_no_promocion", "tasa_retiro"]].copy()
        tabla.columns = ["Departamento", "Estudiantes", "% Promoción", "% No promovidos", "% Retiro"]
        st.dataframe(
            tabla.style.format({
                "Estudiantes": "{:,.0f}",
                "% Promoción": "{:.1f}",
                "% No promovidos": "{:.1f}",
                "% Retiro": "{:.1f}"
            }),
            hide_index=True,
            use_container_width=True
        )

    st.caption(
        "Fuente: Microdatos de Educación Formal 2024 · Instituto Nacional de Estadística (INE). "
        "Los porcentajes se calculan sobre el total de inscripciones del departamento."
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Por Departamento", layout="wide")
    mostrar_departamentos()
