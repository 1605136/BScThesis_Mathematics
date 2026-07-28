# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:59:04 2026

@author: Miriam_Ucendo
@filename: download_omie

automate download elctricity prices from the Spanish Market
"""

from pathlib import Path
from datetime import date, timedelta
import requests

# =====================================================
# CONFIGURACIÓN
# =====================================================

YEAR = 2026

ROOT = Path("data/raw")

DA_FOLDER = ROOT / "DA"
IDA_FOLDER = ROOT / "IDA2"

DA_FOLDER.mkdir(parents=True, exist_ok=True)
IDA_FOLDER.mkdir(parents=True, exist_ok=True)

# =====================================================
# DESCARGA
# =====================================================

def descargar(url, destino):

    if destino.exists():
        print(f"✓ {destino.name}")
        return

    r = requests.get(url, timeout=30)

    if r.status_code == 200:

        destino.write_bytes(r.content)
        print(f"↓ {destino.name}")

    else:

        print(f"✗ Error {r.status_code}: {destino.name}")

# =====================================================
# RECORRER EL AÑO
# =====================================================

dia = date(YEAR, 1, 1)

while dia <= date(YEAR, 12, 31):

    fecha = dia.strftime("%Y%m%d")

    # -------------------------
    # Mercado diario
    # -------------------------

    nombre = f"marginalpdbc_{fecha}.1"

    url = (
        "https://www.omie.es/en/file-download"
        f"?parents=marginalpdbc&filename={nombre}"
    )

    descargar(url, DA_FOLDER / nombre)

    # -------------------------
    # IDA - Sesión 2
    # -------------------------

    nombre = f"marginalpibc_{fecha}02.1"

    url = (
        "https://www.omie.es/en/file-download"
        f"?parents=marginalpibc&filename={nombre}"
    )

    descargar(url, IDA_FOLDER / nombre)

    dia += timedelta(days=1)

print("\nDescarga finalizada.")