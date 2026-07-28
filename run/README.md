# Execution scripts (`run`)

## Purpose

This directory contains the execution scripts used to solve the Energy Hub optimization models.

The scripts import the model formulations and data-processing functions from the `src/` directory, execute the optimization problems using Pyomo, and save the obtained results in the `outputs/` directory.

## Directory contents

| File | Description |
|------|-------------|
| `EH1_run.py` | Execution script for the deterministic EH1 optimization model. |
| `EH2_run.py` | Execution script for the deterministic EH2 optimization model. |
| `EH3_run.py` | Execution script for the deterministic EH3 optimization model. |
| `EH1_stc_run.py` | Execution script for the stochastic EH1 optimization model. |
| `EH2_stc_run.py` | Execution script for the stochastic EH2 optimization model. |
| `EH3_stc_run.py` | Execution script for the stochastic EH3 optimization model. |
| `EH1_study_day_run.py` | Execution script for running the EH1 model for a specific study day. |

## Inputs

The execution scripts use the functions implemented in `src/` and require the input data stored in the `data/` directory:

| Input | Description |
|-------|-------------|
| `params.xlsx` | Technical, economic and operational parameters of the Energy Hub models. |
| `historical_data.csv` | Historical time-series data used for scenario generation and model inputs. |
| `scenarios_*.csv` | Stochastic scenarios used by the stochastic optimization models. |

## Outputs

The execution scripts generate optimization results stored in the `outputs/` directory.

Generated files include:

- Optimization results for each Energy Hub configuration.
- First-stage and second-stage decision variables.
- Scenario-dependent results for stochastic models.

The generated Excel files follow the naming convention:

```text
*_results_{study_day}.xlsx
```

where:

- `*` identifies the corresponding Energy Hub model (e.g., `EH1`, `EH2`, `EH3`, `EH1_stc`, `EH2_stc`, etc.).
- `{study_day}` is the selected study day in the format `YYYY-MM-DD`.

## Notes

The scripts in this directory are the main entry points for reproducing the optimization experiments presented in the thesis. The mathematical formulation of the models is implemented separately in `src/models.py`.

## User-configurable parameters

Before executing a script, the user may select the study day:

```python
study_day = "2026-05-20"
```

The required date format is:

```text
YYYY-MM-DD
```

For example:

```python
study_day = "2026-05-20"
```

## Execution

Once the configuration variables have been checked, the scripts can be executed from the repository root:

```bash
python run/EH1_run.py
```

The generated results are automatically stored in the `outputs/` directory.
