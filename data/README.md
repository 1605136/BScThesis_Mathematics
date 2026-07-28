# Data (`data`)

## Purpose

This directory contains the scripts used to download, preprocess and generate the datasets required by the optimization models.

The final datasets generated in this directory are used by the modules in `src/` to construct the optimization models.

## Directory contents

| File | Description |
|------|-------------|
| `download_omie.py` | Downloads electricity market data from OMIE. |
| `generator_el_prices.py` | Processes electricity price data. |
| `generator_gas_prices.py` | Processes natural gas price data. |
| `generator_wind_production.py` | Processes wind production data. |
| `generator_demand.py` | Processes electricity, heating and cooling demand data. |
| `generator_historical_data.py` | Combines the processed datasets into a single historical dataset (`historical_data.csv`). |
| `generator_scenarios.py` | Generates representative stochastic scenarios from the historical dataset. |

## Directory structure

| Directory | Description |
|----------|-------------|
| `raw/` | Original downloaded datasets. |
| `processed/` | Intermediate processed datasets used to construct the final historical dataset. |

## Outputs

The scripts in this directory generate the input files required by the optimization models, including:

- `historical_data.csv`
- `scenarios_*.csv`
- `params.xlsx`

## Notes

The scripts in this directory are intended for data preparation. Since the processed datasets are already included in the repository, users can reproduce the optimization models without executing these scripts.
