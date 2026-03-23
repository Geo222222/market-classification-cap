# Market Classification and Scenario Analysis System

## Overview

This repository contains the implementation of the **Market Classification and Scenario Analysis System**, a graduate capstone project that combines financial time-series analysis, market microstructure features, and machine learning to study short-horizon market regimes.

Instead of building a trading or execution platform, this project focuses on **research questions** about how well machine learning models can classify intraday market regimes and how robust those classifications are under controlled changes in key market features.

This project is developed as part of the **Master of Science in Computer Science (MSCS)** program.

---

## Running the live data collector (`data_pipeline`)

The collector lives under `src/data_pipeline/`. Python does not see it as `data_pipeline` until **`src` is on the module path**. Use either:

**Option A - editable install (recommended, works from any directory)**

```bash
cd market-classification-cap
pip install -e .
python -m data_pipeline
```

**Option B - no install (from repository root)**

```bash
python run_collector.py
```

**Option C - set `PYTHONPATH` (from repository root)**

```powershell
# PowerShell
$env:PYTHONPATH = "src"
python -m data_pipeline
```

```bash
# bash
PYTHONPATH=src python -m data_pipeline
```

**Option D - run from `src/`**

```bash
cd src
python -m data_pipeline
```

See `src/data_pipeline/README.md` for config, credentials, CSV output paths, and the Tk collector UI.

---

## Core Research Questions

The system serves as an experimental platform for two primary research questions:

- **RQ1 - Regime Classification Quality**  
  To what extent can machine learning models, trained on short-horizon price-change and microstructure/indicator features, reliably classify intraday market regimes (e.g., trending, ranging, volatile) compared to rule-based indicator baselines?

- **RQ2 - Scenario Sensitivity and Robustness**  
  How sensitive and robust are these regime classifications to controlled changes in key market features (such as volatility, volume, order-book imbalance, and money flow indicators), as explored through a systematic what-if scenario analysis?

---

## Project Objectives

The primary objectives of this project are:

- Ingest raw trade and order-book data and aggregate it into multi-horizon OHLCV windows (e.g., 5s-60m).
- Implement a feature engineering pipeline centered on **percentage price change** and **market-defining indicators** that capture both directional and liquidity conditions (e.g., volatility, volume, MFI, spread, depth imbalance).
- Define transparent, rule-based regime labels using rolling returns and volatility over intraday windows.
- Develop and evaluate machine learning models for regime classification, comparing them to rule-based baselines (RQ1).
- Build a scenario analysis engine that perturbs key features and measures how regime predictions respond (RQ2).
- Provide an interactive interface or notebooks for visualizing regimes, model outputs, and scenario responses.

---

## System Architecture (High Level)

The system is organized into several core components:

- **Data Ingestion**  
  Retrieves intraday market data (trades and, where available, order-book snapshots) from APIs or local datasets and aggregates them into multi-horizon bar data during regular trading hours.

- **Feature Engineering and Labeling**  
  Constructs features based on percentage price change, volatility, volume, money flow, and order-book structure, and generates rule-based regime labels from rolling return and volatility thresholds.

- **Machine Learning Models**  
  Trains and evaluates classification models (e.g., Logistic Regression, Random Forest, Gradient Boosting) to predict market regimes defined by the labeling rules.

- **Evaluation and Reporting**  
  Compares models to rule-based baselines using metrics (accuracy, macro F1, per-class F1), confusion matrices, and regime timelines, and summarizes results in a reproducible way.

- **Scenario Analysis Engine**  
  Applies controlled perturbations to selected features (e.g., simulate higher volatility or volume) and measures how regime predictions change to study model sensitivity and robustness.

- **Visualization and Interface**  
  Provides plots and, optionally, a lightweight UI (e.g., Streamlit or Dash) or notebooks to explore data, regimes, model outputs, and scenario effects.

---

## Project Structure (Intended)

```text
market-classification-cap/
├── docs/
│   ├── requirements/
│   └── design/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── data_pipeline/
│   ├── features/
│   ├── models/
│   ├── evaluation/
│   ├── scenario_analysis/
│   └── app/
├── requirements.txt
└── README.md
```

---

## Technologies

The project will utilize the following technologies:

- **Python**
- **Pandas / NumPy** for data processing and feature engineering
- **Scikit-learn** (and optionally other ML libraries) for classification models and evaluation
- **Matplotlib / Plotly / Seaborn** for visualization
- **Streamlit or Dash** for an optional interactive user interface
- **Git / GitHub** for version control and project tracking

---

## Current Development Status

The project is currently in the **requirements and high-level design phase**. Initial tasks include:

- Finalizing research questions and requirements (see `docs/requirements/Martin_ProjectRequirementsDocument.md`).
- Designing the data ingestion and feature engineering pipeline.
- Selecting datasets and defining regime labeling rules.
- Planning model evaluation and scenario analysis experiments.

Subsequent phases will focus on implementation of the data pipeline, feature engineering, labeling, modeling, evaluation, and visualization / interface layers.

---

## Author

**Djuvane Martin**  
Master of Science in Computer Science

---

## License

This project is developed for academic purposes as part of a graduate capstone project.
