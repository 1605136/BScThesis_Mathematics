# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 18:52:10 2026

@author: Miriam_Ucendo
@filename: generator_gas_prices

Create a dataset with the DA gas price for the year {YEAR}

"""

from pathlib import Path
import pandas as pd

# ==========================================
# CONFIGURACIÓN
# ==========================================

YEAR = 2026

ROOT = Path(r"C:\Users\Miriam Ucendo\Documents\UNI\5\TFG_mates\code\EH2_mod\nuevo\data")

INPUT = ROOT / "raw" / "gas" / f"MIBGAS_Data_{YEAR}.csv"
OUTPUT = ROOT / "processed" / f"gas_{YEAR}.csv"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# ==========================================
# LEER CSV
# ==========================================

gas = pd.read_csv(
    INPUT,
    sep=";",
    skiprows=1
)

# eliminar columna vacía
gas = gas.drop(columns=["Unnamed: 7"], errors="ignore")

# ==========================================
# FILTRAR PRODUCTO
# ==========================================

gas = gas[
    (gas["Product"] == "GDAES_D+1") &
    (gas["Place of delivery"] == "PVB") &
    (gas["Area"] == "ES")
].copy()

# ==========================================
# FORMATO
# ==========================================

gas["Fecha"] = pd.to_datetime(
    gas["First Day Delivery"],
    dayfirst=True
)

gas = gas.rename(
    columns={
        "MIBGAS Daily Price [EUR/MWh]": "Precio_Gas"
    }
)

gas = gas[["Fecha", "Precio_Gas"]]

gas = gas.sort_values("Fecha").reset_index(drop=True)

# ==========================================
# EXPORTAR
# ==========================================

gas.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8"
)

print(gas.head())
print(f"\n{len(gas)} días exportados.")
print(f"Archivo guardado en:\n{OUTPUT}")