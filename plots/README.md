# Plotting (`plots`)

## Purpose

This directory contains the scripts used to visualize the results of the optimization models and the generated stochastic scenarios.

The figures are intended to facilitate the interpretation and comparison of the different Energy Hub configurations.

## Directory contents

| File | Description |
|------|-------------|
| `plot_clustering.py` | Visualizes the representative days obtained from the time-series clustering process. |
| `plot_compare_EH.py` | Compares the optimization results obtained for the different Energy Hub configurations. |
| `plot_ESS_EH2.py` | Visualizes the operation of the Energy Storage System (ESS) in the EH2 model. |

## Inputs

The plotting scripts read the optimization results stored in the `outputs/` directory and, when required, the input datasets stored in `data/processed/`.

## User-configurable parameters

Before executing a script, the user may select the study day:

```python
study_day = "2026-05-20"
```

The required date format is:

```text
YYYY-MM-DD
```

## Outputs

The generated figures are stored in a subdirectory of `outputs/` named after the selected study day:

```text
outputs/
└── {study_day}/
    ├── figure_1.png
    ├── figure_1.pdf
    ├── figure_2.png
    ├── figure_2.pdf
    └── ...
```

Each figure is saved in both PNG and PDF formats.

## Notes

These scripts do not perform optimization. They are intended solely for visualization and analysis of the generated results.
