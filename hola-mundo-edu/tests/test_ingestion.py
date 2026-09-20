"""Tests básicos de la ingesta."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from config import SECTOR, AREA, RESULTADO, DEPARTAMENTOS
from ingestion import normalizar_codigo_establecimiento, extraer_municipio, decodificar_dataframe
import pandas as pd


def test_normalizar_codigo():
    assert normalizar_codigo_establecimiento("00-01-0001-42") == "01-01-0001-42"
    assert normalizar_codigo_establecimiento("01-05-0012-43") == "01-05-0012-43"
    assert normalizar_codigo_establecimiento(None) is None


def test_extraer_municipio():
    assert extraer_municipio("19-01-0001-42") == "19-01"
    assert extraer_municipio("01-05-0012-43") == "01-05"


def test_decodificar_basico():
    df = pd.DataFrame({
        "Sector": [1, 2],
        "Área": [1, 2],
        "Resultado_F": [1, 5],
        "Departamento_F": [1, 19],
        "CodEstablecimiento": ["00-01-0001-42", "19-01-0001-42"],
    })
    out = decodificar_dataframe(df)
    assert out["Sector"].tolist() == ["Público", "Privado"]
    assert out["Area"].tolist() == ["Urbana", "Rural"]
    assert out["Resultado"].tolist() == ["Promovido", "No promovido"]
    assert out["Departamento"].tolist() == ["Guatemala", "Zacapa"]
    assert out["CodEstablecimiento"].iloc[0].startswith("01-")


if __name__ == "__main__":
    test_normalizar_codigo()
    test_extraer_municipio()
    test_decodificar_basico()
    print("✅ Todos los tests de ingestion pasaron")
