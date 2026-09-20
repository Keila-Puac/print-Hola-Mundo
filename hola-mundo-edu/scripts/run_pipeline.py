"""
Pipeline completo de Educación Formal 2024.
1. Ingesta + decodificación
2. Cálculo de indicadores e insights
"""

import sys
from pathlib import Path

# Añadir backend al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from ingestion import run_ingestion
from analytics import run_analytics


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Pipeline Educación Formal 2024")
    parser.add_argument(
        "--completo",
        action="store_true",
        help="Procesar los 22 departamentos (por defecto solo 3 de prueba)",
    )
    args = parser.parse_args()

    solo_prueba = not args.completo

    print("=" * 60)
    print(" PIPELINE COMPLETO - Educación Formal 2024")
    print("=" * 60)

    print("\n[1/2] Ejecutando ingesta...")
    run_ingestion(solo_prueba=solo_prueba)

    print("\n[2/2] Ejecutando analytics...")
    run_analytics()

    print("\n" + "=" * 60)
    print("✅ Pipeline terminado correctamente")
    print("=" * 60)
    print("\nPara levantar el dashboard:")
    print("  streamlit run frontend/app.py")
