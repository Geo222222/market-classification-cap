# Market Classification and Scenario Analysis System

**Author:** Djuvane Martin  
**Affiliation:** Computer Science Department, Full Sail University, Orlando, FL, USA  
**Email:** djuvane.martin@student.fullsail.edu  
**Date:** March 22, 2026  
**Program:** CSMS / MSCS Capstone Research

---

## ABSTRACT

Financial markets operate under changing conditions that can be described as different regimes, such as trending, ranging, and volatile states. Identifying these regimes is important for understanding price behavior, yet many existing approaches rely on rule-based indicators that introduce subjectivity. This project proposes a system that uses machine learning models trained on short-horizon price and microstructure features to classify market regimes. The system also includes a scenario analysis framework that evaluates how model predictions change when key features such as volatility, volume, and liquidity are modified. The goal is to compare machine learning models to rule-based baselines and to quantify model sensitivity under controlled perturbations. The result is a research-oriented platform designed to support systematic analysis of financial market behavior. This work is for research and education; it does not constitute investment or trading advice.

---

## KEYWORDS

Market regimes, financial time series, machine learning, classification, scenario analysis, robustness, microstructure

---

## 1. INTRODUCTION

Financial markets generate large volumes of time-series data that reflect continuously changing conditions. These conditions shift between different states such as trending, ranging, and highly volatile environments. Identifying these regimes is important for understanding market behavior and supporting data-driven analysis.

Most current approaches rely on rule-based indicators and visual interpretation. While widely used, they are often subjective and difficult to evaluate in a systematic way. Machine learning provides a more data-driven approach, but many studies focus only on prediction accuracy and do not evaluate how stable predictions are when input conditions change.

This project addresses that gap by designing a system that classifies short-horizon market regimes using machine learning and evaluates model behavior through controlled scenario analysis. The system focuses on both predictive performance and sensitivity to feature perturbations.

The research is guided by the following questions:

- **RQ1 – Regime Classification Quality:**  
  To what extent can machine learning models trained on short-horizon price-change and microstructure features classify intraday market regimes compared to rule-based baselines?

- **RQ2 – Scenario Sensitivity and Robustness:**  
  How do classification results and predicted regimes change when key input features (e.g., volatility, volume, liquidity-related features) are perturbed in a controlled way, and which features drive the largest changes?

The following hypotheses are defined:

- **H₀ (RQ1):** On held-out time periods, machine learning models do not achieve significantly better regime classification (e.g., macro-F1 or per-class F1) than rule-based baselines after accounting for sampling variability (e.g., bootstrap confidence intervals or paired comparison on the same timestamps).

- **H₁ (RQ1):** At least one supervised model significantly outperforms the chosen rule-based baseline on the primary classification metrics.

- **H₀ (RQ2):** Under a standardized set of perturbation magnitudes, the distribution of regime flips (or probability shifts) does not differ meaningfully across feature families (volatility vs. volume vs. liquidity proxies).

- **H₁ (RQ2):** Perturbations to specific feature families produce systematically larger changes in predicted regime or class probabilities than others, indicating differential sensitivity that can be ranked and interpreted.

This research is relevant to financial analysts, data scientists, and researchers interested in applying machine learning to financial markets.

---

## 2. BACKGROUND AND RELATED WORK

Financial analysis has traditionally relied on technical indicators and rule-based systems to interpret price behavior. Common approaches include trend-following indicators, volatility measures, and moving averages. While effective in some cases, these approaches often simplify market behavior and do not capture interactions between price, volume, and liquidity.

Machine learning methods have been applied to financial time-series problems to improve pattern recognition and classification. Supervised models such as logistic regression, random forests, and gradient boosting have been used to classify market conditions based on engineered features. Unsupervised approaches, including clustering and Hidden Markov Models, have also been used to identify latent regimes.

Financial markets are non-stationary: their statistical properties change over time, which challenges generalization. In addition, many studies emphasize predictive accuracy without evaluating how model outputs change when input conditions are modified.

Another limitation is the lack of structured frameworks for testing model robustness under counterfactual or perturbed inputs. Most models are evaluated on static splits and do not include systematic feature-level scenario analysis.

This project extends existing work by combining regime classification with scenario-based sensitivity analysis in one experimental pipeline.

---

## 3. METHODOLOGY / SYSTEM DESIGN

The system is designed as a modular pipeline: data processing, feature engineering, regime labeling, classification, evaluation, and scenario analysis.

### Data Collection and Aggregation

Intraday market data will be collected via APIs or local datasets (e.g., trades and, where available, order-book information). Data will be aggregated into short intervals (e.g., from seconds through multi-minute windows) to capture short-horizon behavior. The initial study will focus on one highly liquid instrument and a defined historical window to keep scope feasible; extensions to additional symbols are optional future work.

### Feature Engineering

The system generates features that capture price movement and liquidity conditions:

- Multi-horizon percentage returns  
- Rolling volatility  
- Volume-based indicators  
- Money Flow Index (MFI)  
- Bid–ask spread (when available)  
- Order book imbalance and depth proxies (when available)  
- Time-of-day and calendar features (e.g., session time, optional quarter-of-year encoding)

### Order Flow Imbalance (OFI)

Order Flow Imbalance summarizes net buyer- versus seller-initiated activity over a window of \(N\) events:

$$
\text{OFI}_t = \sum_{i=1}^{N} s_i \, q_i
$$

where:

- \(q_i\) is the trade size at event \(i\)  
- \(s_i \in \{+1,\,-1\}\), with \(s_i = +1\) for buyer-initiated trades and \(s_i = -1\) for seller-initiated trades  

A positive value indicates net buying pressure; a negative value indicates net selling pressure.

### Realized Volatility

Rolling realized volatility over a window of \(N\) returns is:

$$
\sigma_t = \sqrt{\sum_{i=1}^{N} r_{t-i}^{2}}
$$

where the log return is:

$$
r_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
$$

and \(P_t\) is the price at time \(t\). This measure captures the magnitude of recent price changes and supports labeling and feature construction for high- versus low-volatility regimes.

### Regime Labeling

Market regimes are defined using transparent rule-based thresholds on rolling returns and volatility. These labels serve as training targets and as a baseline classifier for comparison with machine learning models.

### Machine Learning Models

Supervised classification models include logistic regression, random forest, and gradient boosting. Models are trained on engineered features and evaluated against rule-based baselines using time-respecting train/validation/test splits.

### Scenario Analysis

A scenario module applies controlled perturbations to selected features (e.g., volatility, volume, spread or imbalance proxies). Models are re-evaluated on perturbed inputs to measure prediction changes, regime flips, and relative sensitivity across feature families.

---

## 4. RESEARCH METHODS

| Research Question | Hypothesis (summary) | Method | Analysis | Expected Outcome |
| ----------------- | -------------------- | ------ | -------- | ---------------- |
| RQ1 | ML vs. baseline performance | Train classifiers; compare to rule-based labels/baselines on held-out periods | Accuracy, macro-F1, per-class F1, confusion matrices; bootstrap or paired comparison where appropriate | Quantify whether ML improves regime classification |
| RQ2 | Differential sensitivity to perturbations | Standardized perturbations per feature family; re-infer regimes | Regime flip rates, probability shifts, rankings by feature family | Identify which inputs most affect predictions |

Time-based splitting preserves temporal order and reduces lookahead bias. Primary metrics include accuracy, precision, recall, and F1 (including macro- and per-class views where class imbalance matters).

---

## 5. POTENTIAL ANALYSIS

The system supports several analytical views:

- **Classification performance** — How well ML models match or exceed rule-based regime assignment on held-out data.  
- **Feature sensitivity** — How perturbations to volatility, volume, and liquidity-related features change outputs.  
- **Regime transitions** — How predicted and labeled regimes evolve over time.  
- **Robustness summaries** — Aggregated sensitivity under repeated or grid-based scenarios.

---

## 6. CONCLUSION

This project presents a structured approach for analyzing short-horizon market regimes using machine learning and scenario-based evaluation. The system classifies market conditions and assesses how reliable those classifications are when underlying features are changed in a controlled way.

By combining engineered financial and microstructure features with supervised models, the study evaluates whether data-driven methods provide measurable improvements over rule-based approaches (RQ1). The scenario framework quantifies how predictions respond to changes in volatility, volume, and liquidity-related inputs and compares sensitivity across feature families (RQ2).

The main contribution is integrating classification and sensitivity analysis in a single reproducible pipeline, emphasizing interpretable features and transparent labeling rather than black-box prediction alone.

This work is relevant to financial analysts, quantitative researchers, and data scientists who seek more systematic and interpretable approaches to analyzing short-horizon market behavior.

**Limitations** include non-stationarity, possible noise in rule-based labels, dependence on data quality and venue-specific microstructure, and scope limited to research (not live trading or execution).

The expected outcome is a reproducible research platform that supports deeper understanding of short-horizon regime behavior and a foundation for future work in regime detection, model evaluation, and decision-support research.

---

## REFERENCES

[1] J. C. Hull, *Options, Futures, and Other Derivatives*, 10th ed. Pearson, 2022.  
[2] M. López de Prado, *Advances in Financial Machine Learning*. Hoboken, NJ, USA: Wiley, 2018.  
[3] T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning*, 2nd ed. New York, NY, USA: Springer, 2009.  
[4] K. P. Murphy, *Machine Learning: A Probabilistic Perspective*. Cambridge, MA, USA: MIT Press, 2012.  
[5] M. O’Hara, *Market Microstructure Theory*. Cambridge, MA, USA: Blackwell Publishers, 1995.  
[6] L. Harris, *Trading and Exchanges: Market Microstructure for Practitioners*. Oxford, U.K.: Oxford University Press, 2003.  
[7] B. Horvath and Z. Issa, “Clustering Market Regimes using the Wasserstein Distance,” *arXiv preprint* arXiv:2110.11848, 2021.  
[8] M. Kearns and Y. Nevmyvaka, “Machine Learning for Market Microstructure and High Frequency Trading,” in *High Frequency Trading: New Realities for Traders, Markets, and Regulators*, London, U.K.: Risk Books, 2013.  
[9] E. P. Chan, *Algorithmic Trading: Winning Strategies and Their Rationale*. Hoboken, NJ, USA: Wiley, 2013.  
[10] E. P. Chan, *Machine Trading: Deploying Computer Algorithms to Conquer the Markets*. Hoboken, NJ, USA: Wiley, 2021.
