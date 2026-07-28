# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:11:48 2026

@author: Miriam_Ucendo
@filename: generator_el_prices

"creates a file with all the prices for the DA and IDA2 in
the Spanish Electrical Market, for a year"
"""
from pathlib import Path
from datetime import datetime
import pandas as pd

# =====================================================
# CONFIGURACIÓN
# =====================================================

ROOT = Path(r"C:\Users\Miriam Ucendo\Documents\UNI\5\TFG_mates\code\EH2_mod\nuevo\data")

DA_FOLDER = ROOT / "raw" / "DA"
IDA_FOLDER = ROOT / "raw" / "IDA2"

print("=== Generador de precios OMIE ===\n")

fecha_inicio = datetime.strptime(
    input("Fecha inicial (dd/mm/yyyy): "),
    "%d/%m/%Y"
).date()

fecha_fin = datetime.strptime(
    input("Fecha final (dd/mm/yyyy): "),
    "%d/%m/%Y"
).date()

if fecha_inicio > fecha_fin:
    raise ValueError("La fecha inicial debe ser anterior a la final.")

OUTPUT = (
    ROOT / "processed" /
    f"precios_el_{fecha_inicio.strftime('%Y%m%d')}_{fecha_fin.strftime('%Y%m%d')}.csv"
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def obtener_fecha(archivo):
    """
    Extrae la fecha del nombre del archivo.

    DA:
        marginalpdbc_20250101.1

    IDA:
        marginalpibc_2025010101.1
    """

    nombre = archivo.stem

    if nombre.startswith("marginalpdbc"):
        fecha = nombre.split("_")[1]

    elif nombre.startswith("marginalpibc"):
        fecha = nombre.split("_")[1][:8]

    else:
        raise ValueError(f"No se reconoce el archivo: {archivo.name}")

    return datetime.strptime(fecha, "%Y%m%d").date()


def leer_precios(archivo):
    """
    Lee un fichero .1/.2/.3 de OMIE.

    Devuelve una lista con:
        - 24 precios (resolución horaria)
        - 96 precios (resolución 15 minutos)
        - 23 / 25 / 92 / 100 los días de cambio de hora
    """
    precios = []

    with open(archivo, encoding="latin1") as f:
        next(f)  # Cabecera ("MARGINALPIBC;")
        for linea in f:
            linea = linea.strip()
            if linea == "*":
                break
            campos = linea.split(";")
            precios.append(float(campos[4]))

    if len(precios) == 0:
        print(f"Archivo vacío: {archivo.name}")
        return precios

    if len(precios) not in (24, 23, 25, 92, 96, 100):
        raise ValueError(
            f"{archivo.name}: número inesperado de periodos ({len(precios)})"
        )

    return precios
    """
    Lee un fichero .1/.2/.3 de OMIE.

    Devuelve una lista con:
        - 24 precios (resolución horaria)
        - 96 precios (resolución 15 minutos)
        
        - 23 / 25 los días de cambio de hora
        
    los ficheros de omie tienen la siguiente cabecera:
        Año;Mes;Día;Periodo;Precio_ES;Precio_PT
    """

    precios = []

    with open(archivo, encoding="latin1") as f:

        next(f)      # Cabecera

        for linea in f:

            linea = linea.strip()

            if linea == "*":
                break

            campos = linea.split(";")

            precios.append(float(campos[4]))
            print(precios)
            
            if len(precios) == 0:
                print(f"Archivo vacío: {archivo.name}")
                continue
        
            if len(precios) not in (24, 23, 25, 92, 96, 100):
                raise ValueError(
                    f"{archivo.name}: número inesperado de periodos ({len(precios)})"
                )

    return precios


# =====================================================
# MERCADO DIARIO
# =====================================================

def leer_DA(carpeta, fecha_inicio, fecha_fin):

    registros = []
    dias_saltados = []

    archivos = sorted(carpeta.glob("marginalpdbc_*.*"))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos en {carpeta}"
        )

    print(f"Mercado diario: {len(archivos)} archivos encontrados")

    for archivo in archivos:

        fecha = obtener_fecha(archivo)

        if not (fecha_inicio <= fecha <= fecha_fin):
            continue

        precios = leer_precios(archivo)
        
        if not precios:
            dias_saltados.append((fecha, "archivo vacío"))
            continue

        # Saltar días con cambio horario
        if len(precios) in (23, 25, 92, 100):
            print(f"Saltando día con cambio horario: {archivo.name}")
            dias_saltados.append((fecha, "cambio horario"))
            continue

        # Si vienen a 15 minutos -> media horaria
        if len(precios) == 96:

            precios = (
                pd.Series(precios)
                .groupby(lambda i: i // 4)
                .mean()
                .tolist()
            )

        if len(precios) != 24:
            raise ValueError(
                f"{archivo.name}: número inesperado de periodos ({len(precios)})"
            )

        for hora, precio in enumerate(precios, start=1):

            registros.append({
                "Fecha": fecha,
                "Hora": hora,
                "Precio_DA": round(precio, 3)
            })

    return pd.DataFrame(registros), dias_saltados


# =====================================================
# IDA - SESIÓN 2
# =====================================================

def leer_IDA(carpeta, fecha_inicio, fecha_fin):

    registros = []
    dias_saltados = []

    archivos = sorted(carpeta.glob("marginalpibc_*.*"))

    if not archivos:
        raise FileNotFoundError(
            f"No se encontraron archivos en {carpeta}"
        )

    print(f"IDA sesión 2: {len(archivos)} archivos encontrados")

    for archivo in archivos:

        fecha = obtener_fecha(archivo)

        if not (fecha_inicio <= fecha <= fecha_fin):
            continue

        precios = leer_precios(archivo)

        if not precios:
            dias_saltados.append((fecha, "archivo vacío"))
            continue
        
        if len(precios) == 0:
            print(f"Archivo vacío: {archivo.name}")
            continue

        # Saltar días con cambio horario
        if len(precios) in (23, 25, 92, 100):
            print(f"Saltando día con cambio horario: {archivo.name}")
            dias_saltados.append((fecha, "cambio horario"))
            continue

        if len(precios) != 96:
            raise ValueError (
                f"{archivo.name}: número inesperado de periodos ({len(precios)})")
            dias_saltados.append((fecha, f"{len(precios)} periodos"))
            continue
        
        # Partición horaria, no cada 15min
        precios_hora = (
            pd.Series(precios)
            .groupby(lambda i: i // 4)
            .mean()
            .tolist()
        )

        for hora, precio in enumerate(precios_hora, start=1):

            registros.append({
                "Fecha": fecha,
                "Hora": hora,
                "Precio_IDA": round(precio, 3)
            })

    return pd.DataFrame(registros), dias_saltados


# =====================================================
# EJECUCIÓN
# =====================================================

print("\nLeyendo mercado diario...")
da, da_descartados = leer_DA(DA_FOLDER, fecha_inicio, fecha_fin)

print("\nLeyendo IDA sesión 2...")
ida, ida_descartados = leer_IDA(IDA_FOLDER, fecha_inicio, fecha_fin)

print("\nCombinando datos...")

precios = (
    da.merge(
        ida,
        on=["Fecha", "Hora"],
        how="inner"
    )
    .sort_values(["Fecha", "Hora"])
    .reset_index(drop=True)
)

# Dias descartados
print("\n=== DÍAS DESCARTADOS ===")

print("\nMercado Diario:")
if len(da_descartados) == 0:
    print("  Ninguno")
else:
    for fecha, motivo in da_descartados:
        print(f"  {fecha} -> {motivo}")

print("\nMercado Intradiario:")
if len(ida_descartados) == 0:
    print("  Ninguno")
else:
    for fecha, motivo in ida_descartados:
        print(f"  {fecha} -> {motivo}")
        
# =====================================================
# COMPROBACIONES
# =====================================================

dias = precios["Fecha"].nunique()

print(f"\nDías leídos: {dias}")
print(f"Registros: {len(precios)}")

esperados = dias * 24

if len(precios) != esperados:
    raise ValueError(
        f"Se esperaban {esperados} registros y hay {len(precios)}."
    )

# =====================================================
# EXPORTAR
# =====================================================

precios.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8"
)

print("\nCSV generado correctamente:")
print(OUTPUT)

print("\nPrimeras filas:")
print(precios.head())