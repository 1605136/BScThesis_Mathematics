# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 12:03:07 2026

@author: Miriam_Ucendo
@filename: input_data.py

Loads and processes all parameters, incorporating the custom demand calculator.
"""

import pandas as pd

def load_input_data(
    params_file="params.xlsx",
    historical_file="historical_data.csv",
    scenarios_file="scenarios.csv"
):
    
    # 1. Leer parámetros globales y escenarios
    df_params = pd.read_excel(params_file)
    params = dict(zip(df_params["Name"], df_params["Value"]))
    
    # 2. Leer datos históricos indexados
    hist = pd.read_csv(historical_file)
    hist["Fecha"] = pd.to_datetime(hist["Fecha"]).dt.date
    
    # 3. Leer escenarios
    df_scen = pd.read_csv(scenarios_file)
    df_scen["Dia_representativo"] = pd.to_datetime(df_scen["Dia_representativo"]).dt.date
    scenarios = df_scen["Escenario"].tolist()
    probabilities = dict(zip(df_scen["Escenario"], df_scen["Probabilidad"]))
    
    # 4. Periodos
    time_periods = sorted(hist["Hora"].unique())
    
    # 5. Días representativos
    DATA = {
    "Precio_DA": {},
    "Precio_IDA": {},
    "Precio_Gas": {},

    "Wind": {},
    "DE": {},
    "DH": {},
    "DC": {},
    }
    
    scenarios_dates = dict(zip(df_scen["Escenario"],df_scen["Dia_representativo"]))

    # Guardamos TODAS las series indexadas por (fecha,hora)
    
    for _, row in hist.iterrows():

        key = (row["Fecha"], int(row["Hora"]))

        DATA["Precio_DA"][key] = float(row["Precio_DA"])
        DATA["Precio_IDA"][key] = float(row["Precio_IDA"])
        DATA["Precio_Gas"][key] = float(row["Precio_Gas"])

        DATA["Wind"][key] = float(row["Produccion_Eolica"])

        DATA["DE"][key] = float(row["DE"])
        DATA["DH"][key] = float(row["DH"])
        DATA["DC"][key] = float(row["DC"])
        
    cols = [
    "Precio_DA",
    "Precio_IDA",
    "Precio_Gas",
    "Produccion_Eolica",
    "DE",
    "DH",
    "DC"]

    if hist[cols].isnull().any().any():
        raise ValueError("Existen valores NaN en historical_data.csv")

    return (
        scenarios,
        scenarios_dates,
        time_periods,
        params,
        probabilities,
        DATA,
    )

