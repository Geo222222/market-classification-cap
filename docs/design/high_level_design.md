## High-Level System Architecture

### Overview

The Market Classification and Scenario Analysis System is organized as a modular pipeline that transforms raw intraday market data into regime classifications, evaluation metrics, and interactive scenario analyses. The core flow is:

**Data sources → Data ingestion → Storage → Preprocessing & feature engineering → ML classification → Evaluation & scenario analysis → Visualization/dashboard and user interaction.**

The major components are:

- `Data Ingestion Module`
- `Data Storage`
- `Data Preprocessing & Feature Engineering`
- `Machine Learning Classification Pipeline`
- `Scenario Analysis Engine`
- `Evaluation & Metrics`
- `Visualization / Dashboard Interface`

---

### Component Responsibilities

#### 1. Data Ingestion Module

- **Inputs**:  
  - External APIs (exchange or market data providers)  
  - Local files (CSV or similar) containing trades and order book snapshots
- **Responsibilities**:  
  - Connect to configured data sources and fetch raw intraday data during regular trading hours.  
  - Aggregate raw trades and order book snapshots into multi-horizon OHLCV bars (e.g., 5s, 15s, 30s, 60s, 5m, 10m, 15m, 30m, 60m).  
  - Persist raw and aggregated data into the storage layer in a structured format.

#### 2. Data Storage

- **Artifacts**:  
  - Raw trades and order book snapshots  
  - Aggregated OHLCV data at multiple time horizons  
  - Processed feature matrices and regime labels  
  - Trained model artifacts and evaluation results
- **Responsibilities**:  
  - Provide a consistent location for reading/writing raw, intermediate, and processed data.  
  - Support reproducible experiments by keeping track of versions, timestamps, or configuration metadata where appropriate.

#### 3. Data Preprocessing & Feature Engineering

- **Inputs**:  
  - Aggregated OHLCV data and order book snapshots from `Data Storage`
- **Responsibilities**:  
  - Clean and align intraday data (handle missing timestamps, trading halts, and irregularities).  
  - Compute engineered features centered on **percentage price change** and **market-defining indicators** (directional and liquidity conditions), including:
    - Multi-horizon returns (5s–60m)  
    - Volatility and range measures over rolling windows  
    - Volume-based features and indicators such as Money Flow Index (MFI)  
    - Order-book features (bid–ask spread, depth, imbalance)  
    - Time-of-day indicators for intraday seasonal patterns  
  - Define regime labels from rolling returns and volatility (e.g., uptrend, downtrend, ranging, volatile).  
  - Output feature matrices and labels to `Data Storage` for training and evaluation.

#### 4. Machine Learning Classification Pipeline

- **Inputs**:  
  - Feature matrices and regime labels from `Data Storage`
- **Responsibilities**:  
  - Split data into time-respecting train/validation/test sets.  
  - Train and tune multiple classification models (e.g., Logistic Regression, Random Forest, Gradient Boosting).  
  - Compare machine learning models against rule-based baselines for **RQ1 – Regime Classification Quality**.  
  - Persist trained models and inference configurations back into `Data Storage`.  
  - Provide prediction services for the Scenario Analysis Engine and Visualization layer.

#### 5. Scenario Analysis Engine

- **Inputs**:  
  - Trained ML models and baselines from the `Machine Learning Classification Pipeline`  
  - Feature matrices (or selected time slices) from `Data Storage`  
  - User-defined scenario parameters from the `Visualization / Dashboard Interface`
- **Responsibilities**:  
  - Construct counterfactual scenarios by perturbing selected features (e.g., volatility, volume, order-book imbalance, MFI).  
  - Re-run model inference under perturbed conditions to measure changes in regime predictions.  
  - Summarize sensitivity (e.g., regime flips, probability shifts) to answer **RQ2 – Scenario Sensitivity and Robustness**.  
  - Return scenario results to the Visualization layer for inspection.

#### 6. Evaluation & Metrics

- **Inputs**:  
  - Predictions from the `Machine Learning Classification Pipeline` and rule-based baselines  
  - Ground-truth regime labels  
  - Scenario outputs from the `Scenario Analysis Engine`
- **Responsibilities**:  
  - Compute standard classification metrics (accuracy, macro F1, per-class F1).  
  - Generate confusion matrices and regime timelines.  
  - Aggregate scenario sensitivity statistics (e.g., distribution of regime flips under feature perturbations).  
  - Persist evaluation artifacts to `Data Storage` and expose them to the Visualization layer.

#### 7. Visualization / Dashboard Interface

- **Inputs**:  
  - Time-series data and regime labels from `Data Storage`  
  - Model predictions and evaluation metrics from `Evaluation & Metrics`  
  - Scenario analysis outputs from the `Scenario Analysis Engine`
- **Responsibilities**:  
  - Provide data loading and control panels for starting ingestion and feature generation.  
  - Display time-series charts with regime overlays and volatility/volume indicators.  
  - Present evaluation results (metrics, confusion matrices, timelines) for **RQ1**.  
  - Allow users to define what-if scenarios (e.g., adjust volatility or volume) and visualize how regime classifications change for **RQ2**.  
  - Serve as the main interaction surface for analysts, researchers, and students.

---

### Data Flow Description

At a high level, data flows through the system as follows:

1. **Raw Data Acquisition**  
   - External APIs and local CSVs feed raw trades and order book snapshots into the `Data Ingestion Module`.  
   - The ingestion process aggregates this data into multi-horizon OHLCV bars and writes both raw and aggregated data into `Data Storage`.

2. **Preprocessing and Feature Construction**  
   - The `Data Preprocessing & Feature Engineering` component reads aggregated OHLCV and order book data from `Data Storage`.  
   - It cleans and aligns the data, then constructs engineered features (percentage price change, volatility, volume/MFI, order-book imbalance, time-of-day).  
   - It also computes regime labels using rule-based combinations of rolling returns and volatility.  
   - Features and labels are written back to `Data Storage`.

3. **Model Training and Baseline Comparison (RQ1)**  
   - The `Machine Learning Classification Pipeline` reads features and labels, splits them into train/validation/test sets, and trains multiple ML models.  
   - Rule-based baselines are defined directly from the labeling rules or simple indicators.  
   - Predictions from ML models and baselines are passed to `Evaluation & Metrics`, which calculates metrics and generates diagnostic plots.  
   - Evaluation artifacts are saved to `Data Storage` and surfaced in the `Visualization / Dashboard Interface`.

4. **Scenario Analysis (RQ2)**  
   - Through the dashboard, the user selects a time range, instrument, and scenario parameters (e.g., increase volatility by 20%, double volume, widen spread).  
   - The `Scenario Analysis Engine` takes the original feature matrices and applies the requested perturbations.  
   - Perturbed features are fed through the trained ML models (and optionally baselines) to obtain new regime predictions.  
   - Differences between original and scenario predictions (e.g., regime flips, probability shifts) are summarized by `Evaluation & Metrics` and visualized in the dashboard.

5. **User Interaction and Iteration**  
   - Users can iteratively refine data ranges, models, and scenarios via the dashboard.  
   - New ingestion runs, feature configurations, or model settings produce new experiments, all captured reproducibly in `Data Storage`.

---

### Diagram (architecture_diagram.png)

The architecture diagram in `docs/design/architecture_diagram.png` should reflect the following structure:

- **Left side – Data Sources**  
  - Box: *Data Sources* (APIs, CSV, Raw Trades, Order Book Snapshots).

- **Ingestion and Storage layer**  
  - Box: *Data Ingestion Module* (connected to Data Sources).  
  - Box: *Data Storage* (Raw, Aggregated, Features, Labels, Models, Metrics).

- **Processing and Modeling layer**  
  - Box: *Preprocessing & Feature Engineering* (reads from Storage, writes features + labels).  
  - Box: *ML Classification Pipeline* (Model Training & Inference, reads features + labels, writes models + predictions).  
  - Box: *Evaluation & Metrics* (connected to ML Pipeline and Scenario Engine).

- **Scenario and Visualization layer**  
  - Box: *Scenario Analysis Engine* (takes models, features, user-defined perturbations).  
  - Box: *Visualization / Dashboard Interface* (charts, metrics, scenario comparisons).

- **User**  
  - Box: *Analyst / Researcher* connected to the Visualization / Dashboard Interface.

**Arrows and labels**:

- From *Data Sources* → *Data Ingestion Module* (**raw data**).  
- From *Data Ingestion Module* → *Data Storage* (**raw + aggregated data**).  
- From *Data Storage* → *Preprocessing & Feature Engineering* (**aggregated data**).  
- From *Preprocessing & Feature Engineering* → *Data Storage* (**features + labels**).  
- From *Data Storage* → *ML Classification Pipeline* (**features + labels**).  
- From *ML Classification Pipeline* → *Evaluation & Metrics* (**predictions + baselines**).  
- From *ML Classification Pipeline* → *Scenario Analysis Engine* (**trained models**).  
- From *Scenario Analysis Engine* ↔ *Evaluation & Metrics* (**scenario results, sensitivity stats**).  
- From *Evaluation & Metrics* and *Data Storage* → *Visualization / Dashboard Interface* (**metrics, time-series, regimes, scenarios**).  
- From *Analyst / Researcher* → *Visualization / Dashboard Interface* (**commands: ingest, generate features, train models, run scenarios**).  
- From *Visualization / Dashboard Interface* → *Scenario Analysis Engine* (**scenario definitions / perturbations**).

Together, this design shows how data flows from raw sources through preprocessing and modeling into evaluation and interactive scenario analysis, and how the machine learning pipeline integrates with the user interface to support the project’s research questions.

