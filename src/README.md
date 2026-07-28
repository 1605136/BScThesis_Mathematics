# Source code (`src`)

## Purpose

This directory contains the core source code of the project. It includes the implementation of the Energy Hub optimization models and functions for loading and processing input data shared across the execution scripts.

The modules contained in this directory are imported by the scripts in `run/`, `metrics/`, and `plots/`.

## Directory contents

| File            | Description                                                                                                                            |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `models.py`     | Definition of the deterministic and stochastic Energy Hub optimization models (EH1, EH2 and EH3) using Pyomo.  Each model includes "Sets, Parameters, Variables, Objective Function, and Contraints"                      |
| `input_data.py` | Functions for reading input datasets, loading model parameters, and preparing the data structures required by the optimization models. |
| `__init__.py`   | Marks the directory as a Python package, allowing its modules to be imported throughout the repository.                                |

## Inputs

The functions contained in this directory read information from the `data/` directory, including:

| Input file | Description |
|------------|-------------|
| `params.xlsx` | Technical, economic and operational parameters of the Energy Hub models. |
| `historical_data.csv` | Historical time-series data (e.g., demand, renewable generation and market information). |
| `scenarios_*.csv` | Representative stochastic scenarios generated from the historical data and used in the stochastic optimization models. |


The exact input files required by each function are documented within the corresponding source code.

## Outputs

This directory does not produce output files. It only provides reusable functions that are imported and executed by other scripts within the repository.

## Usage

The modules are intended to be imported rather than executed directly. Typical usage is:

```python
from src.input_data import load_input_data
from src.models import *_model
```

## Notes

This directory only contains reusable source code. Numerical experiments, performance analyses and figure generation are implemented in the `run/`, `metrics/`, and `plots/` directories, respectively.
