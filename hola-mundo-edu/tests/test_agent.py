"""Tests básicos del agente (modo local)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from agent import preguntar_al_agente, cargar_contexto_dict


def test_contexto_existe():
    ctx = cargar_contexto_dict()
    assert "indicadores" in ctx
    assert "total_estudiantes" in ctx.get("indicadores", {})


def test_respuesta_total():
    r = preguntar_al_agente("¿Cuántos estudiantes hay en total?")
    assert "202" in r or "estudiantes" in r.lower()


def test_no_inventa():
    r = preguntar_al_agente("¿Cuántos estudiantes hay en la Luna?")
    assert "no tengo" in r.lower() or "no disponible" in r.lower() or "reformular" in r.lower()


if __name__ == "__main__":
    test_contexto_existe()
    test_respuesta_total()
    test_no_inventa()
    print("✅ Todos los tests del agente pasaron")
