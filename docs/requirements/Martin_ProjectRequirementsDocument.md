## Market Classification and Scenario Analysis System

### Project Requirements Specification Document

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
   Use supervised and exploratory machine learning techniques to classify market conditions such as bullish, bearish, ranging, or volatile states.

5. **Analyze short-horizon directional market movement**  
   Study how price direction evolves over short intervals by linking changes in price, trade activity, and liquidity conditions.

6. **Provide an interactive what-if scenario analysis interface**  
   Allow users to explore hypothetical analytical conditions by adjusting parameters such as asset selection, quantity, time intervals, and analytical models.

7. **Create a visualization interface for exploring analytical results**  
   Display classification outcomes, market regime shifts, and scenario evaluation results through interactive charts and data visualization tools.

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

| Stakeholder                | Priority | Needs                                                                 |
|----------------------------|----------|-----------------------------------------------------------------------|
| Advisor / Committee        | High     | Project aligned with research questions, methodology, and CS rigor    |
| Financial Analysts / Traders| Medium  | Ability to interpret market regimes and scenario outcomes             |
| Data Scientists / Researchers| Medium | Access to processed datasets, labels, models, and evaluation reports  |
| Developer (Author)         | High     | Scalable, modular platform to run experiments and compare approaches  |

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
- Full portfolio optimization or end-to-end trading strategy backtesting  
- Long-horizon return forecasting or portfolio-level risk management  
- Production-grade deployment and scaling beyond research and prototyping needs

#### Major Features

1. **Interactive Data Acquisition Module**  
   The application will allow users to retrieve financial data from external APIs or load datasets from local CSV files. Data will be stored locally for further analysis.

2. **Automated Feature Engineering Pipeline**  
   Once data is loaded, the system will automatically compute relevant financial indicators and derived features required for machine learning models.

3. **Market Classification and Scenario Analysis Engine**  
   - Machine learning models will classify financial market conditions based on engineered market features.  
   - The system will support multiple machine learning approaches to analyze market behavior and identify market regimes such as bullish, bearish, ranging, and volatile conditions.  
   - Users will be able to select from different machine learning models when performing analysis. Supported models may include supervised learning algorithms such as Logistic Regression, Random Forest, and Gradient Boosting, as well as unsupervised techniques such as clustering methods used to identify hidden market regimes.  
   - The system will provide an interactive what-if scenario analysis module that allows users to evaluate hypothetical market situations by adjusting scenario parameters such as asset symbol, time, quantity, and model selection. The system will compute analytical outcomes based on these parameters and display the results through interactive visualizations.

**Scenario Input Parameters**

| Scenario Parameter         | Description                                                    |
|---------------------------|----------------------------------------------------------------|
| Asset / Symbol            | Financial instrument selected for analysis                     |
| Date                      | Historical date selected for scenario evaluation               |
| Time                      | Specific time within the dataset used for analysis             |
| Quantity                  | Amount of asset used for hypothetical scenario evaluation      |
| Market Classification Filter | Market condition used for analysis (Trending, Ranging, Volatile) |
| Model Selection           | Machine learning model used for classification                 |

#### Minor Features

1. Dataset preview table for loaded data  
2. Interactive data visualization tools  
3. Feature calculation status indicator  
4. Model results visualization  
5. Dataset export functionality  
6. Logging panel showing system operations

---

### System Requirements

**Table 3 – System Requirements**

| Requirement | Explanation                          | Solution                                           |
|------------|--------------------------------------|---------------------------------------------------|
| SR1        | Data ingestion system                | Retrieve financial market data from APIs or CSV files |
| SR2        | Data storage system                  | Store raw and processed datasets locally          |
| SR3        | Feature engineering module           | Automatically compute derived financial indicators|
| SR4        | Machine learning classification engine | Classify market conditions using trained models  |
| SR5        | Scenario analysis module             | Allow simulation of historical market scenarios   |
| SR6        | Data visualization system            | Present analysis results graphically              |
| SR7        | Scenario input system                | Allow users to define what-if parameters and scenario conditions |
| SR8        | Evaluation and reporting module      | Compare ML models to rule-based baselines and report metrics, confusion matrices, and scenario sensitivity results |

#### Non-Functional Requirements

- **Performance**: The system should be able to ingest and feature-engineer at least hundreds of thousands of trades and corresponding order-book snapshots within a reasonable time on a standard development machine.  
- **Reproducibility**: Data processing, labeling, model training, and evaluation steps must be scriptable and rerunnable using stored configurations.  
- **Transparency and Interpretability**: Models should expose feature importance or explanation artifacts (e.g., via SHAP or permutation importance) to support interpretation of regime classifications and scenario responses.  
- **Modularity**: Data, features, models, and evaluation components should be decoupled so that they can be extended or replaced without rewriting the entire system.

---

### Interface Requirements

**Table 4 – Interface Requirements**

| Requirement | Explanation                           | Solution                                            |
|------------|---------------------------------------|----------------------------------------------------|
| IR1        | Data loading interface                | Users must be able to load datasets through API calls or CSV uploads |
| IR2        | Interactive data preview              | Display raw and processed datasets in a table format |
| IR3        | Feature engineering controls          | Users must be able to trigger feature generation from the interface |
| IR4        | Model execution interface             | Users must be able to run classification models from the interface |
| IR5        | Visualization dashboard               | Display charts and analytical results              |
| IR6        | What-if scenario interface            | Allow users to interactively define scenario parameters and compare outcomes |

---

### Challenges

The most challenging requirements are:

- Designing a responsive interface that integrates data loading, feature engineering, and machine learning workflows.  
- Ensuring that financial datasets are processed efficiently, especially when large datasets are loaded.  
- Implementing machine learning models that provide meaningful classification of market behavior.  
- Maintaining a modular system architecture that allows new models and data sources to be integrated easily.  
- Handling errors related to API connections, CSV parsing, and data preprocessing.

---

### Research and Findings

Modern financial analysis platforms provide a wide range of tools for visualizing and interpreting market behavior. Popular platforms such as TradingView, MetaTrader, and QuantConnect are widely used by traders and analysts for market analysis, strategy testing, and automated trading. These systems provide powerful charting tools, technical indicators, and scripting capabilities that allow users to study financial market trends and develop trading strategies.

Among these platforms, **TradingView** has become one of the most widely adopted financial analytics tools due to its extensive charting capabilities and its scripting language, Pine Script, which allows users to build custom indicators and trading strategies. Pine Script enables users to define analytical conditions and evaluate how those conditions would behave when applied to market data. This functionality is similar to scenario-based analysis because users can define rules and observe how the strategy performs under different market conditions. However, while TradingView provides powerful visualization and scripting capabilities, its analytical methods are primarily rule-based and rely on user-defined indicators rather than machine learning models that can automatically learn patterns from data.

**MetaTrader** is another widely used financial trading platform that supports automated trading through its Expert Advisor (EA) scripting system. MetaTrader allows users to program automated strategies and perform backtesting on historical market data. While the platform provides strong support for algorithmic trading and historical strategy testing, it is primarily focused on execution and trading automation rather than exploratory research or machine learning experimentation.

**QuantConnect** is a platform designed specifically for quantitative finance research and algorithmic trading. It provides an environment where developers can implement complex trading algorithms and backtest strategies using large historical datasets. QuantConnect supports several programming languages and provides access to extensive financial datasets. However, the platform is designed primarily for professional quantitative developers and can present a steep learning curve for new users who are interested in exploring financial analytics and machine learning experimentation.

Analysis of these platforms reveals several common trends:

- Users highly value powerful visualization tools, access to historical financial datasets, and the ability to experiment with analytical strategies.  
- Many existing platforms focus heavily on rule-based strategy scripting or trading automation rather than transparent machine learning experimentation.  
- Many platforms require advanced programming knowledge or restrict advanced analytical tools behind subscription tiers, which can limit accessibility for researchers and students.

The Market Classification and Scenario Analysis System was designed to address these limitations by providing a **simplified research-oriented environment** that integrates machine learning techniques with interactive analysis tools.

Instead of relying exclusively on rule-based strategies, the system applies machine learning models to classify financial market conditions based on engineered financial indicators. These models analyze relationships between price movement, volatility, and other derived features to identify market regimes such as trending, ranging, or volatile environments.

Another key capability of the system is the integration of **parameter-driven scenario analysis**. Inspired by the ability of platforms like TradingView to test analytical conditions, the system allows users to define scenario parameters such as asset selection, quantity, and model selection to explore how different analytical assumptions influence classification outcomes. This capability allows users to experiment with alternative analytical conditions and better understand how machine learning models interpret financial market data.

To answer **RQ1**, the project will implement time-based train/validation/test splits over the chosen instrument and period, and evaluate multiple machine learning models against rule-based regime classifiers using metrics such as accuracy, macro F1, and per-class F1, along with confusion matrices and regime timelines. To answer **RQ2**, the system will apply controlled perturbations to key features (e.g., volatility, volume, order-book imbalance, MFI) and measure how often and how strongly regime predictions change, summarizing the sensitivity and robustness of the models across different market conditions.

From a system architecture perspective, **Python** was selected as the primary development language due to its extensive ecosystem for financial analytics and machine learning. Libraries such as **Pandas** and **NumPy** provide efficient tools for processing financial time-series datasets and computing derived features from market data. Machine learning algorithms available through **Scikit-learn** enable the development of classification models capable of detecting patterns in market behavior.

The architecture of this system separates data ingestion, feature engineering, machine learning models, evaluation procedures, and user interface components into modular layers. This modular design supports experimentation with different datasets and analytical models while improving scalability and maintainability. By combining machine learning techniques with interactive analysis tools and scenario experimentation capabilities, the Market Classification and Scenario Analysis System provides a research-focused platform for exploring financial market dynamics and supporting data-driven analysis.

---

### References

1. J. C. Hull, *Options, Futures, and Other Derivatives*, 10th ed. Pearson, 2022.  
2. M. López de Prado, *Advances in Financial Machine Learning*. Hoboken, NJ, USA: Wiley, 2018.  
3. T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd ed. New York, NY, USA: Springer, 2009.  
4. K. P. Murphy, *Machine Learning: A Probabilistic Perspective*. Cambridge, MA, USA: MIT Press, 2012.  
5. M. O’Hara, *Market Microstructure Theory*. Cambridge, MA, USA: Blackwell Publishers, 1995.  
6. L. Harris, *Trading and Exchanges: Market Microstructure for Practitioners*. Oxford, U.K.: Oxford University Press, 2003.  
7. B. Horvath and Z. Issa, “Clustering Market Regimes using the Wasserstein Distance,” *arXiv preprint* arXiv:2110.11848, 2021.  
8. M. Kearns and Y. Nevmyvaka, “Machine Learning for Market Microstructure and High Frequency Trading,” in *High Frequency Trading: New Realities for Traders, Markets, and Regulators*, London, U.K.: Risk Books, 2013.  
9. E. P. Chan, *Algorithmic Trading: Winning Strategies and Their Rationale*. Hoboken, NJ, USA: Wiley, 2013.  
10. E. P. Chan, *Machine Trading: Deploying Computer Algorithms to Conquer the Markets*. Hoboken, NJ, USA: Wiley, 2021.

