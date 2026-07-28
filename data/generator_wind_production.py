# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:11:48 2026

@author: Miriam_Ucendo
@filename: generator_wind_production

Genera un CSV con la producción eólica en el formato:

Fecha,Hora,Produccion_Eolica
"""

from pathlib import Path
from datetime import datetime
import pandas as pd

# =====================================================
# CONFIGURACIÓN
# =====================================================

ROOT = Path(r"C:\Users\Miriam Ucendo\Documents\UNI\5\TFG_mates\code\EH2_mod\nuevo\data")

INPUT = ROOT / "raw" / "wind" / "ninja_wind_45.0685_7.6845_corrected.csv"

print("=== Generador de producción eólica ===\n")

fecha_inicio = datetime.strptime(
    input("Fecha inicial (dd/mm/yyyy): "),
    "%d/%m/%Y"
).date()

fecha_fin = datetime.strptime(
    input("Fecha final (dd/mm/yyyy): "),
    "%d/%m/%Y"
).date()

POTENCIA_INSTALADA = float(
    input("Potencia instalada [MW]: ")
)

OUTPUT = (
    ROOT / "processed" /
    f"wind_{fecha_inicio.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.csv"
)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# =====================================================
# LECTURA
# =====================================================

wind = pd.read_csv(
    INPUT,
    skiprows=3
)

wind["time"] = pd.to_datetime(wind["time"])

wind["Fecha"] = wind["time"].dt.date
wind["Hora"] = wind["time"].dt.hour + 1

wind = wind.rename(
    columns={
        "electricity": "Produccion_Eolica"
    }
)

# =====================================================
# FILTRAR FECHAS
# =====================================================

wind = wind[
    (wind["Fecha"] >= fecha_inicio) &
    (wind["Fecha"] <= fecha_fin)
]

# =====================================================
# SELECCIONAR COLUMNAS
# =====================================================

wind = wind[
    [
        "Fecha",
        "Hora",
        "Produccion_Eolica"
    ]
].reset_index(drop=True)

# Escalar a la potencia instalada
wind["Produccion_Eolica"] *= POTENCIA_INSTALADA

# =====================================================
# EXPORTAR
# =====================================================

wind.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8"
)

print("\nCSV generado correctamente:")
print(OUTPUT)

print("\nPrimeras filas:")
print(wind.head())