# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:09:50 2026

@author: Miriam_Ucendo
@filename: plot_stc_folder.py
"""


import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ─── CONFIGURACIÓN DE LA CARPETA ────────────────────────────────────
# Pon aquí el nombre que quieras para tu carpeta:
#date = "29-05"
date = "22-06"

# Creamos la carpeta automáticamente si no existe
if not os.path.exists(date):
    os.makedirs(date)
    print(f"📁 Carpeta '{date}' creada con éxito.")

# ─── LOAD RESULTS ───────────────────────────────────────────────────
df = pd.read_excel(f"EH_stc_results_{date}.xlsx")

# Available scenarios
SCENARIOS = df["s"].unique()

# ─── COLORES ────────────────────────────────────────────────────────
Azul     = "#1F4E79"   # Azul marino
Naranja  = "#D55E00"   # Naranja oscuro
Verde    = "#2A9D8F"   # Verde petróleo
Morado   = "#7B2CBF"   # Morado elegante  
Rojo      = "#C44E52"   # Brick red

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

LINESTYLES = ["--", "-", ":"]

# =============================================================================
# MATPLOTLIB STYLE
# =============================================================================

plt.rcParams.update({

    "figure.facecolor": "white",
    "axes.facecolor": "white",

    "font.family": "Arial",

    "axes.titlesize": 20,
    "axes.titleweight": "bold",

    "axes.labelsize": 18,

    "xtick.labelsize": 15,
    "ytick.labelsize": 15,

    "legend.fontsize": 18,

    "axes.edgecolor": "#555555",
    "axes.linewidth": 0.8

})

# =============================================================================
# FUNCIÓN GENÉRICA
# =============================================================================

def plot_group(columns, labels, colors, ylabel, filename):

    plt.figure(figsize=(13,6))

    # Dibujamos todos los escenarios
    for linestyle, s in zip(LINESTYLES, SCENARIOS):

        d = df[df["s"] == s]

        for col, label, color in zip(columns, labels, colors):

            plt.plot(
                d["t"],
                d[col],
                color=color,
                lw=2.2,
                ls=linestyle,
                label=f"{label} ($\omega$({s}))"
            )

#    plt.title(title, pad=15)

    plt.xlabel("Hour")
    plt.ylabel(ylabel)

    plt.xticks(range(1,25))
    plt.xlim(1,24)

    plt.grid(axis="y", alpha=0.35)

    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # ------------------------------------------------------------------
    # Variables (marcadores)
    # ------------------------------------------------------------------
    
    variable_handles = [
        Line2D([0], [0],
               marker='o',
               color='none',
               markerfacecolor=color,
               markeredgecolor=color,
               markersize=9,
               linestyle='None')
        for color in colors
    ]
    
    # ------------------------------------------------------------------
    # Escenarios (tipos de línea)
    # ------------------------------------------------------------------
    
    scenario_handles = [
        Line2D([0], [0],
               color='black',
               lw=2.5,
               linestyle=ls)
        for ls in LINESTYLES
    ]
    
    scenario_labels = [
        r"$\omega_{\mathrm{good}}$",
        r"$\omega_{\mathrm{normal}}$",
        r"$\omega_{\mathrm{bad}}$"
    ]
    
    handles = variable_handles + scenario_handles
    
    labels_all = labels + scenario_labels
    
    plt.legend(
        handles,
        labels_all,
        ncol=7,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        columnspacing=1.4,
        handlelength=2.2,
        fontsize=16
    )
        
    # ------------------------------------------------------------------

    plt.tight_layout()

    plt.savefig(
        os.path.join(date, f"{filename}.png"),
        dpi=300,
        bbox_inches="tight"
    )
    
    plt.savefig(
        os.path.join(date, f"{filename}.pdf"),
        bbox_inches="tight"
    )
    
    plt.show()


# =============================================================================
# PLOT 1 → GAS
# =============================================================================

plot_group(
    columns=["G", "G1", "G2"],
    labels=["G", "G1", "G2"],
    colors=[Azul, Naranja, Verde],
#    title="Gas Production",
    ylabel="Power Gas (MW)",
    filename=f"01_stc_Gas_{date}"
)


# =============================================================================
# PLOT 2 → ELECTRICITY
# =============================================================================

plot_group(
    columns=["E", "E_RES_used", "E_DA", "E_TODAY"],
    labels=["E", "E_RES_used", "E_DA", "E_TODAY"],
#    columns=["E_RES", "E_DA", "E_TODAY"],
#    labels=["e_RES", "E_DA", "E_TODAY"],
    colors=[Azul, Rojo, Naranja, Verde],
#    title="Electricity Dispatch",
    ylabel="Power Electricity (MW)",
    filename=f"02_stc_Electricity_{date}"
)


# =============================================================================
# PLOT 3 → HEAT
# =============================================================================

plot_group(
    columns=["H1", "H2"],
    labels=["H1", "H2"],
    colors=[Azul, Naranja],
#    title="Heat Production",
    ylabel="Power Heat (MW)",
    filename=f"03_stc_Heat_{date}"
)