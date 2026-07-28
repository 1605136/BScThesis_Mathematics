# Performance metrics (`metrics`)

## Purpose

This directory contains the scripts used to evaluate the performance of the stochastic optimization models.

The implemented metrics quantify the benefit of stochastic optimization by comparing it with deterministic approaches.

## Directory contents

| File | Description |
|------|-------------|
| `metrics_EH1_run.py` | Computes the performance metrics for the EH1 stochastic model. |
| `metrics_EH2_run.py` | Computes the performance metrics for the EH2 stochastic model. |
| `metrics_EH3_run.py` | Computes the performance metrics for the EH3 stochastic model. |

## Inputs

The scripts require the optimization models and the input datasets stored in the `data/` directory.

| Input | Description |
|-------|-------------|
| `params.xlsx` | Technical, economic and operational parameters of the Energy Hub models. |
| `historical_data.csv` | Historical dataset used to construct the optimization instances. |
| `scenarios_*.csv` | Representative stochastic scenarios and their associated probabilities. |

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

The scripts compute and print the following performance metrics:

- **WS (Wait-and-See)**
- **EV (Expected Value)**
- **EEV (Expected result of the Expected Value solution)**
- **VSS (Value of the Stochastic Solution)**
- **EVPI (Expected Value of Perfect Information)**

The metrics are displayed in the console and are not stored in external files.

## Notes

These scripts should be executed after the optimization models have been validated, since they repeatedly solve deterministic and stochastic optimization problems to evaluate the performance metrics.
