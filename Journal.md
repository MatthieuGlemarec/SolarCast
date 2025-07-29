# Project Journal: SolarCast

## Data Preprocessing: Weather and Solar Data

### Objective
Prepare a clean, daily national dataset of weather metrics and solar generation for predictive modelling.

### Context
National-level weather summaries for Ireland aren't publicly available. To overcome this, a representative dataset was manually constructed by averaging observations from **nine geographically diverse weather stations** across the Republic of Ireland.

### Steps Taken
- Loaded raw weather station data
- Standardised and cleaned column names and units
- Merged data by date to produce daily averages
- Aggregated 15-minute solar generation data (from EirGrid) into daily totals
- Merged solar generation and national weather datasets by date

### Weather Station Feature Key
- `glorad` – Global Radiation (J/cm²)
- `rain` – Daily Rainfall (mm)
- `maxtp` – Max Air Temperature (°C)
- `mintp` – Min Air Temperature (°C)
- `cbl` – Cloud Base Level Pressure (hPa)

---

## 🔍 Exploratory Data Analysis (EDA)

### Objective
Understand the relationships between weather variables and solar generation to inform feature selection and modelling strategy.

---

### 01: Simple OLS – Single Predictor Regressions

#### Key Findings
- **`glorad`**: Strongest predictor (R² = 0.689)
- **`maxtp`**: Also strong (R² = 0.495)
- **`rain`**: Negative correlation (R² = 0.094)
- **`mintp`**: Statistically significant but weak (R² = 0.145)
- **`cbl`**: Weak and not statistically significant (R² = 0.006)

> `glorad` and `maxtp` are top candidates; `cbl` will likely be excluded.

---

### 02: Multiple OLS – Full vs. Reduced Models

- **Full Model** (all 5 predictors): R² = 0.757
  - `cbl` not statistically significant (p = 0.216)
- **Reduced Model** (excluding `cbl`): R² = 0.756
  - All predictors significant (p < 0.001)

> Dropping `cbl` simplifies the model without loss of accuracy.

---

### 03: Diagnostic & VIF Analysis

- Residuals show heteroscedasticity
- Q-Q plots indicate approximate normality
- **VIF Findings**:
  - `glorad` VIF = 6.2 (acceptable)
  - `maxtp` VIF = 24.63, `mintp` VIF = 12.44 (too high)

> High VIF justifies removing `mintp` from model due to multicollinearity

---

### 04: Reduced2 Model – Dropping `mintp`

- **R²** = 0.743 (slight drop)
- VIF for remaining features improves significantly

> Trade-off accepted: stability and interpretability over a minor loss in R²

---

### 05: Addressing Heteroscedasticity with Log Transform

#### Steps
- Apply log transformation to `solargen`
- Refit model
- Recheck residuals

#### Observations
- Improved residual spread (better homoscedasticity)
- Slight left skew in Q-Q plot and histogram
- **R²** drops to 0.708 (acceptable trade-off)

> Residuals improve, skew slightly worsens — overall benefit justifies transformation.

---

### 06: Polynomial Regression – Add `glorad²`

#### Steps
- Add squared term to model
- Compare RMSE and MAE
- Validate with ANOVA

#### Performance
- **Reduced2**: RMSE = 2756.75 | MAE = 2105.45
- **Log Model**: RMSE = 4337.00 | MAE = 2636.23
- **Polynomial**: RMSE = 2687.25 | MAE = 2041.25

#### ANOVA: Reduced2 vs. Polynomial
- F = 18.92 | p = 0.000018 → Statistically significant improvement

> **Polynomial model is best so far** – better performance without needing back-transformation.

---

## Rainfall Distribution Insight

- Box plots reveal extreme skew and zero-inflation
- Earlier models may have underestimated its complexity

> Future models (e.g., Random Forest) will:
- Use feature transformation
- Add classification flags for "rain day"
- Leverage non-linear methods

### Summary
The project has successfully completed early stage linear modelling using OLS and polynomial regression. These models confirmed strong relationships between solar generation and weather predictors—particularly **global radiation (`glorad`)**. However, in moving toward a more advanced and production-ready model, a key challenge emerged: **Met Éireann does not forecast `glorad`**, which is the most predictive feature.

### Implication
Since the ultimate goal is to forecast solar generation using only publicly available and *future-facing* data, relying on historical `glorad` alone would make the model unusable in practice. This creates a fork in the road: either abandon the most predictive feature, or find a way to *predict* it using other weather variables that are available in forecast datasets.

### Resolution
The project will adopt a **two-stage modelling pipeline**:
1. **Stage 1** – Predict `glorad` using forecastable weather features such as rainfall, temperature.
2. **Stage 2** – Predict solar energy generation using the output from Stage 1 along with other available features.

This design honours physical causality (solar radiation drives generation), mitigates the lack of forecasted `glorad`, and ensures the model remains usable and scalable in a real-world Irish context.