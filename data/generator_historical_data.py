# -*- coding: utf-8 -*-
"""
@author: Miriam_Ucendo
@filename: merge_historical_data

Genera un único fichero histórico con todas las variables
que utilizará el modelo y el generador de escenarios.
"""

from pathlib import Path
import pandas as pd

# =====================================================
# RUTAS
# =====================================================

ROOT = Path(r"C:\Users\Miriam Ucendo\Documents\UNI\5\TFG_mates\code\EH2_mod\nuevo\data")

PROCESSED = ROOT / "processed"

PRECIOS = PROCESSED / "precios_el_20260101_20260630.csv"
GAS = PROCESSED / "gas_2026.csv"
WIND = PROCESSED / "wind_20260101_20260630.csv"
DEMAND = PROCESSED / "demand_2026_500kW.csv"

OUTPUT = PROCESSED / "historical_data.csv"

# =====================================================
# PRECIOS ELECTRICIDAD
# =====================================================

print("Leyendo precios...")

precios = pd.read_csv(PRECIOS)

precios["Fecha"] = pd.to_datetime(precios["Fecha"])

# =====================================================
# GAS
# =====================================================

print("Leyendo gas...")

gas = pd.read_csv(GAS)

gas["Fecha"] = pd.to_datetime(gas["Fecha"])

# Expandir a 24 horas
gas = gas.loc[gas.index.repeat(24)].reset_index(drop=True)
gas["Hora"] = list(range(1,25)) * (len(gas)//24)

# =====================================================
# WIND
# =====================================================

print("Leyendo producción eólica...")

wind = pd.read_csv(WIND)

wind["Fecha"] = pd.to_datetime(wind["Fecha"])

# =====================================================
# DEMANDAS
# =====================================================

print("Leyendo demandas...")

demand = pd.read_csv(DEMAND)

demand["Fecha"] = pd.to_datetime(demand["Fecha"])

# =====================================================
# MERGE
# =====================================================

print("Combinando...")

hist = (
    precios
    .merge(gas, on=["Fecha", "Hora"])
    .merge(wind, on=["Fecha", "Hora"])
    .merge(demand, on=["Fecha", "Hora"])
    .sort_values(["Fecha", "Hora"])
    .reset_index(drop=True)
)

print(precios.iloc[:3][["Fecha","Hora"]])
print(gas.iloc[:3][["Fecha","Hora"]])
print(wind.iloc[:3][["Fecha","Hora"]])
print(demand.iloc[:3][["Fecha","Hora"]])

# =====================================================
# EXPORTAR
# =====================================================

hist.to_csv(
    OUTPUT,
    index=False
)

print()
print("Archivo generado:")
print(OUTPUT)

print()
print(hist.head())