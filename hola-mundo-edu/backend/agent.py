"""
Agente conversacional sobre Educación Formal 2024.
Prioridad:
1. Intentar usar Grok (vía grook) si está disponible.
2. Si no, responder con un motor local basado en los datos agregados.
Nunca inventa cifras.
"""

import json
import re
from pathlib import Path
from typing import Optional

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PROCESSED = BASE_DIR / "data" / "processed"

# ============================================================
# CARGA DE CONTEXTO
# ============================================================

def cargar_contexto_dict() -> dict:
    """Carga los datos agregados que generó analytics.py."""
    contexto = {}

    ruta_json = DATA_PROCESSED / "indicadores_nacionales.json"
    if ruta_json.exists():
        with open(ruta_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            contexto["indicadores"] = data.get("indicadores", {})
            contexto["insights"] = data.get("insights", [])
            contexto["promedio_retiro"] = data.get("promedio_retiro_nacional")

    ruta_depto = DATA_PROCESSED / "resumen_departamentos.parquet"
    if ruta_depto.exists():
        df = pd.read_parquet(ruta_depto)
        contexto["por_departamento"] = df[
            ["Departamento", "total", "tasa_promocion", "tasa_retiro"]
        ].to_dict(orient="records")

    for nombre in ["area", "sector", "nivel", "pueblo"]:
        ruta = DATA_PROCESSED / f"brecha_{nombre}.parquet"
        if ruta.exists():
            df = pd.read_parquet(ruta)
            contexto[f"brecha_{nombre}"] = df.to_dict(orient="records")

    return contexto


def cargar_contexto() -> str:
    return json.dumps(cargar_contexto_dict(), ensure_ascii=False, indent=2)


# ============================================================
# RESPUESTA LOCAL (fallback)
# ============================================================

def _respuesta_local(pregunta: str, ctx: dict) -> str:
    """Motor simple basado en palabras clave. Solo usa datos reales."""
    p = pregunta.lower().strip()
    ind = ctx.get("indicadores", {})
    insights = ctx.get("insights", [])
    por_depto = ctx.get("por_departamento", [])

    # Total de estudiantes
    if any(k in p for k in ["cuántos estudiantes hay en total", "cuantos estudiantes hay en total", "total de estudiantes", "matrícula total", "matricula total", "cuántos estudiantes hay", "cuantos estudiantes hay"]) and "luna" not in p and "marte" not in p:
        total = ind.get("total_estudiantes")
        if total is not None:
            return (
                f"Según los datos procesados de Educación Formal 2024, "
                f"se registraron **{total:,}** estudiantes (inscripciones)."
            )

    # Tasa de promoción / retiro nacional
    if "promoción" in p or "promocion" in p or "aprobaron" in p:
        t = ind.get("tasa_promocion")
        if t is not None:
            return f"La tasa de promoción a nivel nacional fue del **{t}%**."

    if "retiro" in p or "abandon" in p or "desert" in p:
        t = ind.get("tasa_retiro")
        if t is not None:
            return (
                f"La tasa de retiro (abandono) a nivel nacional fue del **{t}%**. "
                f"Esto equivale a aproximadamente {int(ind.get('total_estudiantes', 0) * t / 100):,} estudiantes."
            )

    # Departamento más crítico
    if any(k in p for k in ["departamento más crítico", "mayor tasa de retiro", "peor departamento", "más alto retiro"]):
        if por_depto:
            # Ya viene ordenado por tasa_retiro descendente en analytics
            peor = max(por_depto, key=lambda x: x.get("tasa_retiro", 0))
            return (
                f"El departamento con la **mayor tasa de retiro** es **{peor['Departamento']}** "
                f"con **{peor['tasa_retiro']}%**. "
                f"Allí se registraron {peor['total']:,} estudiantes."
            )

    # Pregunta por un departamento específico
    for d in por_depto:
        nombre = d["Departamento"].lower()
        if nombre in p:
            return (
                f"En **{d['Departamento']}** se registraron **{d['total']:,}** estudiantes. "
                f"Tasa de promoción: **{d['tasa_promocion']}%**. "
                f"Tasa de retiro: **{d['tasa_retiro']}%**."
            )

    # Brecha rural / urbana
    if "rural" in p or "urbana" in p or "urbano" in p:
        brecha = ctx.get("brecha_area", [])
        if brecha:
            lineas = []
            for row in brecha:
                area = row.get("Area", "")
                lineas.append(
                    f"- **{area}**: promoción {row.get('tasa_promocion')}%, "
                    f"retiro {row.get('tasa_retiro')}%"
                )
            return "Comparación por área:\n\n" + "\n".join(lineas)

    # Nivel más afectado
    if "nivel" in p and ("más" in p or "mayor" in p or "crítico" in p or "abandono" in p):
        brecha = ctx.get("brecha_nivel", [])
        if brecha:
            limpio = [r for r in brecha if r.get("Nivel") not in ("Ignorado", "Desconocido")]
            if limpio:
                peor = max(limpio, key=lambda x: x.get("tasa_retiro", 0))
                return (
                    f"El nivel con mayor tasa de retiro es **{peor['Nivel']}** "
                    f"({peor['tasa_retiro']}%)."
                )

    # Panorama general / insights
    if any(k in p for k in ["panorama", "resumen", "qué pasa", "qué significan", "general", "insight"]):
        if insights:
            return "Estos son los hallazgos principales según el análisis de los datos:\n\n" + "\n\n".join(
                f"• {i}" for i in insights
            )

    # Respuesta por defecto
    return (
        "No tengo esa información exacta en los datos agregados disponibles.\n\n"
        "Puedo responder sobre:\n"
        "- Total de estudiantes y tasas nacionales de promoción/retiro\n"
        "- Resultados por departamento\n"
        "- Brechas rural-urbana, por sector, por nivel y por pueblo\n"
        "- Los insights principales del análisis\n\n"
        "Prueba reformular la pregunta o explora las pestañas del dashboard."
    )


# ============================================================
# SYSTEM PROMPT PARA GROK
# ============================================================

SYSTEM_PROMPT = """
Eres un asistente experto en los datos de Educación Formal 2024 de Guatemala.

REGLAS OBLIGATORIAS:
1. Solo puedes usar la información que te doy en el contexto.
2. Nunca inventes cifras ni porcentajes.
3. Si no tienes el dato, di exactamente: "No tengo esa información en los datos disponibles".
4. Responde siempre en español, claro y sencillo.
5. Cuando des un número, menciona de dónde sale (indicadores nacionales, resumen por departamento, etc.).

Contexto de datos reales:
{contexto}
"""


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def preguntar_al_agente(pregunta: str, historial: list | None = None) -> str:
    """
    Función que usa el frontend.
    Intenta Grok; si falla, usa el motor local.
    """
    ctx = cargar_contexto_dict()
    contexto_str = json.dumps(ctx, ensure_ascii=False, indent=2)

    # 1. Intentar Grok si está instalado
    try:
        from grook import Grook
        mensaje = SYSTEM_PROMPT.format(contexto=contexto_str) + f"\n\nPregunta del usuario: {pregunta}"
        grok = Grook(model="grok-3-auto")
        respuesta = grok.ask(mensaje)
        return respuesta
    except ImportError:
        # No está instalado grook → usar fallback local
        return _respuesta_local(pregunta, ctx)
    except Exception as e:
        # Cualquier otro error de red/API → fallback local + aviso
        local = _respuesta_local(pregunta, ctx)
        return (
            f"{local}\n\n"
            f"_(Nota: el servicio de Grok no estuvo disponible en este momento. "
            f"La respuesta anterior se generó solo con los datos locales.)_"
        )


# ============================================================
# PRUEBA RÁPIDA
# ============================================================

if __name__ == "__main__":
    print("Probando agente (modo local + Grok si está disponible)...\n")

    preguntas = [
        "¿Cuántos estudiantes hay en total?",
        "¿Qué departamento tiene la mayor tasa de retiro?",
        "Dame el panorama general de la educación en 2024",
        "¿Cómo está el área rural comparado con la urbana?",
    ]

    for p in preguntas:
        print(f"Pregunta: {p}")
        print(f"Respuesta: {preguntar_al_agente(p)}")
        print("-" * 60)
