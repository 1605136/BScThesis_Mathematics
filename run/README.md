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

## Usage

The scripts are intended to be executed from the repository root.

Example:

```bash
python run/EH1_run.py
```

The required input data and model configuration parameters are loaded automatically from the repository structure.

## Execution workflow

The typical workflow is:

1. Prepare the required input data in `data/`.
2. Execute the desired optimization model from this directory.
3. Results are automatically stored in `outputs/`.
4. Use the scripts in `metrics/` and `plots/` for further analysis and visualization.

## Notes

The scripts in this directory are the main entry points for reproducing the optimization experiments presented in the thesis. The mathematical formulation of the models is implemented separately in `src/models.py`.

## User configuration

Before running any script, the user should verify the repository path and the selected study day.

### Repository path

The scripts automatically locate the repository root using `Path(__file__)`:

```python
ROOT = Path(__file__).resolve().parents[1]
```

This line should be kept unchanged in the standard repository structure.

If the user stores the scripts in a different directory structure, the value of `ROOT` must be modified to point to the repository root directory.

For example:

```python
ROOT = Path(r"path/to/your/repository").resolve()
```

The repository root is the main folder containing the directories:

```text
data/
src/
run/
metrics/
plots/
outputs/
```

### Study day

The selected study day is defined through the variable:

```python
study_day = "2026-05-20"
```

This variable determines the input data and the name of the generated output files.

The required format is:

```text
YYYY-MM-DD
```

where:

- `YYYY` corresponds to the year.
- `MM` corresponds to the month.
- `DD` corresponds to the day.

Example:

```python
study_day = "2026-05-20"
```

## Execution

Once the configuration variables have been checked, the scripts can be executed from the repository root:

```bash
python run/EH1_run.py
```

The generated results are automatically stored in the `outputs/` directory.
