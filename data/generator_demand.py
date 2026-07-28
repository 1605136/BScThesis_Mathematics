# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 19:24:39 2026

@author: Miriam_Ucendo
@filename: generator_demand

Lee un Excel con las hojas:
    - DE
    - DH
    - DC

Normaliza las tres demandas utilizando el máximo GLOBAL de todas ellas y
las reescala a una potencia instalada especificada por el usuario.

Genera un único CSV con:

Fecha,Hora,DE,DH,DC
"""

from pathlib import Path
import pandas as pd


# =====================================================
# CONFIGURACIÓN
# =====================================================

ROOT = Path(r"C:\Users\Miriam Ucendo\Documents\UNI\5\TFG_mates\code\EH2_mod\nuevo\data")

INPUT = ROOT / "raw" / "demand" / "demand_2026_corrected.xlsx"

OUTPUT = ROOT / "processed"

POTENCIA_INSTALADA = float(
    input("Potencia instalada [kW]: ")
)

OUTPUT_FILE = OUTPUT / f"demand_2026_{int(POTENCIA_INSTALADA)}kW.csv"

OUTPUT.mkdir(parents=True, exist_ok=True)

print("\n=== Generador de demanda ===\n")


# =====================================================
# FUNCIONES
# =====================================================

def leer_hoja(nombre):

    df = pd.read_excel(INPUT, sheet_name=nombre)

    df = df.rename(columns={
        "Date": "Fecha",
        "Time": "Hora",
        "power [kW]": nombre
    })

    df = df[["Fecha", "Hora", nombre]]

    # Fecha en formato español
    df["Fecha"] = pd.to_datetime(
        df["Fecha"],
        dayfirst=True
    ).dt.date

    # Hora como entero (1-24)
    df["Hora"] = (
    pd.to_datetime(
        df["Hora"].astype(str),
        format="%H:%M:%S"
    ).dt.hour
    + 1
)

    # Potencia como float
    df[nombre] = df[nombre].astype(float)

    return df


# =====================================================
# LECTURA
# =====================================================

print("Leyendo hojas...")

de = leer_hoja("DE")
dh = leer_hoja("DH")
dc = leer_hoja("DC")


# =====================================================
# MÁXIMO GLOBAL
# =====================================================

max_global = max(
    de["DE"].max(),
    dh["DH"].max(),
    dc["DC"].max()
)

print(f"Máximo global: {max_global:.3f} kW")

factor = POTENCIA_INSTALADA / max_global

print(f"Factor de escala: {factor:.6f}")


# =====================================================
# ESCALADO
# =====================================================

de["DE"] *= factor
dh["DH"] *= factor
dc["DC"] *= factor


# =====================================================
# COMBINAR
# =====================================================

demanda = (
    de.merge(
        dh,
        on=["Fecha", "Hora"],
        how="inner"
    )
    .merge(
        dc,
        on=["Fecha", "Hora"],
        how="inner"
    )
    .sort_values(["Fecha", "Hora"])
    .reset_index(drop=True)
)


# =====================================================
# COMPROBACIONES
# =====================================================

if demanda.isna().any().any():
    raise ValueError("Hay valores perdidos tras combinar las hojas.")

dias = demanda["Fecha"].nunique()

print(f"Días leídos: {dias}")
print(f"Registros: {len(demanda)}")

esperados = dias * 24

if len(demanda) != esperados:
    print(
        f"AVISO: Se esperaban {esperados} registros "
        f"y se han obtenido {len(demanda)}."
    )


# =====================================================
# REDONDEO
# =====================================================

demanda["DE"] = demanda["DE"].round(3)
demanda["DH"] = demanda["DH"].round(3)
demanda["DC"] = demanda["DC"].round(3)


# =====================================================
# EXPORTAR
# =====================================================

demanda.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("\nCSV generado correctamente:")
print(OUTPUT_FILE)

print("\nPrimeras filas:")
print(demanda.head())