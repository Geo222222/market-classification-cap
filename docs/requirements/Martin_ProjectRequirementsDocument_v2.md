## Market Classification and Scenario Analysis System

### Project Requirements Specification Document – Version 2

**Author**: Djuvane Martin  
**Program**: CSMS Degree Program  
**Date**: March 12, 2026

---

### Contents

1. [Introduction](#introduction)  
2. [Research Questions](#research-questions)  
3. [Project Objectives](#project-objectives)  
4. [Competitors & Market Trends](#competitors--market-trends)  
5. [Competitors and Market Research](#competitors-and-market-research)  
6. [Stakeholders](#stakeholders)  
7. [Stakeholder Needs](#stakeholder-needs)  
8. [Target Audience / End User](#target-audience--end-user)  
9. [User Stories](#user-stories)  
10. [Use Cases](#use-cases)  
11. [Define Scope & Features](#define-scope--features)  
12. [System Requirements](#system-requirements)  
13. [Interface Requirements](#interface-requirements)  
14. [Challenges](#challenges)  
15. [Research and Findings](#research-and-findings)  
16. [References](#references)

---

### Introduction

Financial markets generate large volumes of high-frequency time-series data that reflect rapidly changing market conditions. Market environments do not remain static; instead, they transition between different regimes such as bullish, bearish, ranging, and highly volatile states. Detecting these regime shifts and understanding the quantitative variables that influence price action remains a challenge for analysts and researchers.

Traditional financial analysis tools rely heavily on chart interpretation and manually applied technical indicators, which can introduce subjectivity and limit the ability to systematically evaluate market behavior over time.

Modern financial analytics platforms such as TradingView provide powerful visualization tools and scripting capabilities that allow users to design rule-based strategies and indicators. However, these systems primarily rely on user-defined rules and technical indicators rather than data-driven models that automatically learn patterns in financial datasets. Additionally, many platforms focus on strategy execution and trading automation rather than exploratory research into the quantitative relationships between market variables, time, and price behavior.

The Market Classification and Scenario Analysis System addresses these gaps by:

- **Classifying market regimes** using machine learning models.  
- **Identifying short-horizon directional movements** in financial markets.  
- Providing an **interactive what-if scenario analysis interface** that allows users to explore hypothetical market conditions by adjusting parameters such as asset selection, time interval, quantity, and analytical model.

By combining quantitative market analysis, machine learning classification, and interactive decision-support tools, the system aims to provide a research-oriented platform for studying financial market dynamics and exploring short-term directional market behavior.

---

### Research Questions

The capstone project is organized around two primary research questions:

1. **RQ1 – Regime Classification Quality**  
   To what extent can machine learning models, trained on short-horizon price-change and microstructure/indicator features, reliably classify intraday market regimes (e.g., trending, ranging, volatile) compared to rule-based indicator baselines?

2. **RQ2 – Scenario Sensitivity and Robustness**  
   How sensitive and robust are these regime classifications to controlled changes in key market features (such as volatility, volume, order-book imbalance, and money flow indicators), as explored through a systematic what-if scenario analysis?

These questions focus the system on both **predictive performance** (RQ1) and **behavior under perturbations and counterfactual scenarios** (RQ2).

---

### Project Objectives

The objectives of this project are:

1. **Develop a market data ingestion and aggregation system**  
   Retrieve raw financial market trade data and aggregate it across multiple time intervals such as seconds, minutes, and larger time windows to analyze short-horizon market behavior.

2. **Capture market microstructure signals**  
   Incorporate trade activity and optional order book snapshots to represent the underlying liquidity and trade flow dynamics that influence short-term price movement.

3. **Implement a quantitative feature engineering pipeline**  
   Transform raw market data into engineered analytical variables such as percentage price change, trade intensity, liquidity measures, and time-based trading indicators.

4. **Build machine learning models capable of classifying market regimes**  
   Use supervised and exploratory machine learning techniques to classify market conditions such as bullish, bearish, ranging, or volatile states, and evaluate these models against rule-based baselines (RQ1).

5. **Analyze short-horizon directional market movement**  
   Study how price direction evolves over short intervals by linking changes in price, trade activity, and liquidity conditions.

6. **Provide an interactive what-if scenario analysis interface**  
   Allow users to explore hypothetical analytical conditions by adjusting parameters such as asset selection, quantity, time intervals, and analytical models, and observe how classifications respond (RQ2).

7. **Create a visualization interface for exploring analytical results**  
   Display classification outcomes, market regime shifts, evaluation metrics, and scenario results through interactive charts and data visualization tools.

---

### Competitors & Market Trends

Financial market analysis platforms have evolved significantly with the growth of electronic trading and data-driven financial analytics. Platforms such as **TradingView**, **MetaTrader**, and **QuantConnect** are widely used by traders and researchers for market analysis and strategy development.

- **TradingView**  
  Provides advanced charting tools and the Pine Script programming language, which allows users to build custom indicators and rule-based trading strategies. These scripts enable users to evaluate how predefined conditions behave when applied to historical market data.

- **MetaTrader**  
  Offers automated trading capabilities through its Expert Advisor scripting system. Users can develop algorithmic trading strategies and perform backtesting using historical datasets.

- **QuantConnect**  
  Targets quantitative finance research and provides an environment where developers can build algorithmic trading strategies and evaluate them against large financial datasets, similar in spirit to TradingView’s Pine Script environment.

Despite their strengths, these platforms share several limitations:

- Heavy reliance on **rule-based indicators** and manually defined strategies rather than machine learning models that learn patterns directly from data.  
- Strong emphasis on **strategy execution and trading automation**, rather than exploratory research into market microstructure and model behavior.  
- Many advanced analytical features require **subscription access** or advanced programming expertise.

Unlike these platforms, this project does **not** aim to provide order execution or full trading strategy backtesting. Instead, the Market Classification and Scenario Analysis System focuses on **machine learning-driven regime analysis** and **scenario-based robustness studies**, providing an accessible, research-oriented environment for exploring market dynamics.

---

### Competitors and Market Research

**Table 1 – Competitor Feedback Analysis**

| Competitor Name | Sentiment | Feedback                                                            |
|-----------------|-----------|---------------------------------------------------------------------|
| TradingView     | Positive  | "The charting tools are extremely powerful and easy to use."       |
| TradingView     | Negative  | "Advanced analytics features are locked behind expensive subscriptions." |
| MetaTrader      | Positive  | "Automated trading features are very flexible."                     |
| MetaTrader      | Negative  | "The interface feels outdated and difficult to customize."         |
| QuantConnect    | Positive  | "Excellent platform for quantitative research."                    |
| QuantConnect    | Negative  | "Steep learning curve for beginners."                             |

**Overall positive trends**

1. Users appreciate powerful visualization tools.  
2. Users value access to historical financial data.  
3. Algorithmic trading and automation features are highly valued.

**Overall negative trends**

1. Platforms are often too complex for beginners.  
2. Many analytics features require expensive subscriptions.  
3. Machine learning tools are often not transparent or easy to experiment with.

The proposed system seeks to provide **transparent machine learning experimentation** and **accessible analytical workflows**, reducing complexity for non-expert users.

---

### Stakeholders

The stakeholders for this project include:

- Capstone advisor and committee (academic stakeholders)  
- Financial analysts and traders interested in regime-aware analysis  
- Data scientists and researchers studying market microstructure and ML for markets  
- Software developer (project author) responsible for implementation and experimentation

---

### Stakeholder Needs

**Table 2 – Stakeholder Needs**

| Stakeholder                 | Priority | Needs                                                                 |
|-----------------------------|----------|-----------------------------------------------------------------------|
| Advisor / Committee         | High     | Project aligned with research questions, methodology, and CS rigor    |
| Financial Analysts / Traders| Medium   | Ability to interpret market regimes and scenario outcomes             |
| Data Scientists / Researchers| Medium  | Access to processed datasets, labels, models, and evaluation reports  |
| Developer (Author)          | High     | Scalable, modular platform to run experiments and compare approaches  |

---

### Target Audience / End User

The primary target audience includes:

1. **Financial analysts and traders** who want insights into short-horizon market regimes and volatility conditions.  
2. **Data scientists and quantitative researchers** interested in applying and evaluating machine learning techniques for market regime classification.  
3. **Students and researchers** studying financial analytics, microstructure, and predictive modeling.

These users will interact with the system through an application interface and experimentation workflow that support:

- Data loading and preprocessing  
- Feature generation and regime labeling  
- Market classification model training and evaluation  
- Visualization of regimes, predictions, and error patterns  
- Scenario-based analysis of model sensitivity and robustness

---

### User Stories

1. As a **financial analyst**, I want to fetch historical market data from an API so I can analyze current and past market conditions.  
2. As a **researcher**, I want to load CSV datasets so I can analyze my own financial datasets.  
3. As a **data scientist**, I want the system to automatically generate multi-horizon percentage-change and liquidity features so I can quickly prepare datasets for machine learning.  
4. As a **trader**, I want to visualize classified market regimes and volatility states so I can better understand how conditions evolve over time.  
5. As a **financial analyst**, I want to compare what-if scenarios through an interactive interface so I can see how regime classifications change under different assumptions.  
6. As a **researcher**, I want to run and compare multiple classification models against rule-based baselines so I can quantify improvements in regime detection (RQ1).  
7. As a **researcher**, I want to perturb key features such as volatility, volume, and order-book imbalance so I can study how sensitive the model’s regime predictions are (RQ2).  
8. As a **developer**, I want the system to have a modular architecture so new features, models, and evaluation procedures can be integrated easily.

---

### Use Cases

#### Use Case Title – Analyze Market Data

- **User Type**: Financial Analyst / Researcher  
- **Goal**: Load market data, generate features, and run market classification model training or utilization.

**Preconditions**

- The application must be running.  
- The user must either have access to an API data source or a CSV dataset.

**Trigger**

- User clicks **Fetch Data** to retrieve data from an API.  
- User clicks **Load CSV** to import a local dataset.

**Post-Conditions**

- Raw data is stored locally.  
- Feature engineering calculations are applied.  
- Processed datasets are ready for model analysis.

**Scenario**

1. The user opens the application interface.  
2. The user selects a data source (API or CSV).  
3. The user loads the dataset into the application.  
4. The system stores the dataset locally.  
5. The user triggers the **Generate Features** function.  
6. The system calculates engineered features.  
7. The processed dataset is displayed in the interface.  
8. The user selects the **Run Classification Model** option.  
9. The system processes the dataset through the machine learning model.  
10. Results are displayed in the visualization panel.  
11. The user reviews the classification results and visualizations.  
12. The user selects parameters for a what-if scenario analysis.  
13. The system recomputes outcomes based on the selected scenario.  
14. The system presents a comparison of analytical results.

**Exceptions**

- API connection failure  
- CSV file format errors  
- Insufficient data for model training  
- Feature generation errors due to missing values

---

#### Use Case Title – Evaluate Models

- **User Type**: Researcher / Data Scientist  
- **Goal**: Compare machine learning models and rule-based baselines for regime classification and assess sensitivity to scenarios.

**Preconditions**

- Labeled datasets with engineered features are available.  
- At least one machine learning model and one rule-based baseline are configured.

**Trigger**

- User selects models and baselines to evaluate and starts an evaluation run.

**Post-Conditions**

- Classification metrics (accuracy, F1, per-class metrics) are computed and stored.  
- Confusion matrices and other diagnostic plots are generated.  
- Scenario-sensitivity summaries (e.g., regime flips under feature perturbations) are available for inspection.

**Scenario**

1. The user opens the evaluation interface.  
2. The user selects a dataset split (e.g., validation or test period).  
3. The user selects one or more machine learning models and one or more rule-based baselines.  
4. The system runs classification on the selected data for all models and baselines.  
5. The system computes and displays metrics and visualizations (e.g., confusion matrices, regime timelines).  
6. The user optionally triggers scenario-based evaluations, where selected features are perturbed to study changes in regime predictions.  
7. The system summarizes sensitivity results and stores evaluation outputs for reporting.

**Exceptions**

- Incompatible or missing model configurations  
- Evaluation dataset not found or improperly labeled  
- Evaluation run interrupted due to resource limitations

---

### Define Scope & Features

#### Data Scope and Labeling Strategy

The initial implementation focuses on **intraday market data during regular trading hours**, when liquidity and participation are highest. The system ingests raw trade data and order-book (OB) snapshots and aggregates them into **multi-horizon OHLCV windows**.

- **Aggregation horizons**  
  Trades are aggregated into bar data at several short-horizon intervals, such as:  
  **5s, 15s, 30s, 60s, 5m, 10m, 15m, 30m, and 60m**.  
  These windows are used both for feature construction and for defining regime labels over rolling lookback periods.

- **Regime labels**  
  Market regimes (e.g., uptrend, downtrend, ranging, volatile) are defined using combinations of **rolling percentage price change** and **realized volatility** over selected horizons. Thresholds on cumulative return and volatility create transparent, rule-based labels that also serve as baseline classifiers against which machine learning models are evaluated.

- **Primary feature set**  
  The primary feature set is built around **percentage price change** and **market-defining indicators reflecting both directional and liquidity conditions**. These include:
  - Multi-horizon returns (e.g., over 5s–60m windows).  
  - Volatility and range measures over rolling windows.  
  - Volume-based features, including relative volume and indicators such as the Money Flow Index (MFI).  
  - Order-book features derived from OB snapshots (e.g., bid–ask spread, depth and depth imbalance).  
  - Time-of-day features that capture intraday seasonal patterns during open market hours.

This design ties the feature space directly to the **price dynamics, volatility, trading activity, and liquidity conditions** that define short-term market behavior.

In order to ensure depth of analysis within the capstone timeframe, the initial study will focus on **one highly liquid instrument** over a well-defined historical window of intraday data, restricted to regular trading hours. Additional instruments or longer periods may be explored as extensions if time and resources permit.

#### Non-Goals

To keep the project focused on RQ1 and RQ2, the following items are explicitly out of scope:

- Live trading, order routing, or exchange connectivity for execution  
-(commit message truncated)*** End Patch} mommentary JSON error? Let's see tool output.``` -->
