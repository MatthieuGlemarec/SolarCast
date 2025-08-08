# Project Journal: SolarCast

## Data Preprocessing: Weather and Solar Data

### Objective
Prepare a clean, daily national dataset of weather metrics and solar generation for predictive modelling.

### Context
National-level weather summaries for Ireland are not publicly available. To address this, a representative dataset was created by averaging observations from **nine geographically diverse weather stations** across the Republic of Ireland.

### Steps Taken
- Loaded raw weather station data
- Standardised and cleaned column names and units
- Merged daily station data to produce national averages
- Aggregated 15-minute solar generation data from EirGrid into daily totals
- Merged solar generation and national weather datasets by date

### Weather Station Feature Key
- `glorad` – Global Radiation (J/cm²)
- `rain` – Daily Rainfall (mm)
- `maxtp` – Maximum Air Temperature (°C)
- `mintp` – Minimum Air Temperature (°C)
- `cbl` – Cloud Base Level Pressure (hPa)

---

## Exploratory Data Analysis (EDA)

### Objective
Understand the relationships between weather variables and solar generation to guide feature selection and modelling.

---

### 01: Simple OLS – Single Predictor Regressions

**Key Findings**
- `glorad`: Strongest predictor (R² = 0.689)
- `maxtp`: Also strong (R² = 0.495)
- `rain`: Negative correlation (R² = 0.094)
- `mintp`: Statistically significant but weak (R² = 0.145)
- `cbl`: Weak and not statistically significant (R² = 0.006)

> `glorad` and `maxtp` are top candidates; `cbl` will likely be excluded.

---

### 02: Multiple OLS – Full vs. Reduced Models

- **Full Model** (all 5 predictors): R² = 0.757  
  `cbl` not statistically significant (p = 0.216)
- **Reduced Model** (excluding `cbl`): R² = 0.756  
  All predictors significant (p < 0.001)

> Dropping `cbl` simplifies the model without reducing accuracy.

---

### 03: Diagnostic & VIF Analysis

- Residuals show heteroscedasticity
- Q-Q plots indicate approximate normality
- **VIF**:
  - `glorad`: 6.2 (acceptable)
  - `maxtp`: 24.63, `mintp`: 12.44 (too high)

> High multicollinearity justifies removing `mintp` from the model.

---

### 04: Reduced2 Model – Dropping `mintp`

- R² = 0.743 (slight drop from full model)
- VIF for remaining features greatly improved

> Chose stability and interpretability over a minor drop in R².

---

### 05: Addressing Heteroscedasticity with Log Transform

- Applied log transformation to `solargen`
- Residual spread improved (better homoscedasticity)
- Slight left skew introduced in Q-Q plot
- R² dropped to 0.708 (acceptable)

> Improved residual distribution outweighs small performance loss.

---

### 06: Polynomial Regression – Add `glorad²`

**Performance**
- Reduced2: RMSE = 2756.75 | MAE = 2105.45
- Log Model: RMSE = 4337.00 | MAE = 2636.23
- Polynomial: RMSE = 2687.25 | MAE = 2041.25

**ANOVA** (Reduced2 vs Polynomial):  
F = 18.92, p = 0.000018 → Statistically significant improvement.

> Polynomial regression emerged as the best early-stage model.

---

## Rainfall Distribution Insight

- Rainfall highly skewed with zero-inflation
- Likely underrepresented in linear modelling

> Future work should consider transformations, rain/no-rain flags, and non-linear methods.

---

## Summary of Early Modelling

Early-stage modelling confirmed **global radiation (`glorad`)** as the strongest predictor of solar generation. Polynomial regression outperformed other OLS models but relied heavily on `glorad`, which is **not forecasted** by Met Éireann. This prompted a pivot in modelling strategy.

---

## Pivot: From Two-Stage Pipeline to Historical Forecasting

### Objective
Adapt the modelling approach to forecast solar generation without depending on unforecasted `glorad`.

### Context
The original plan:
1. Predict `glorad` using forecastable weather variables (`rain`, `maxtp`, `mintp`)
2. Predict `solargen` from the predicted `glorad`

However, even advanced models (XGBoost) achieved only ~0.45 R² when predicting `glorad`, limiting Stage 2 performance.

### Resolution
Pivot to **time series forecasting** using historical solar generation directly.

**Key Steps**
- Create lag features (`lag_1`, `lag_2`, `lag_7`)
- Optionally include lagged weather variables
- Train regression models (XGBoost/Random Forest)
- Evaluate using R², RMSE, MAE

**Justification**
- No reliance on unavailable variables
- Leverages strong autocorrelation in solar generation
- Scalable and deployable once live data becomes accessible

---

## Solar Generation Forecasting: Deployment & Modelling Strategy Update

### Objective
Build a robust historical forecasting model using 2023–2024 data, with a design ready for future real-time deployment.

### Context
EirGrid’s solar data is:
- Only available via manual download
- Not accessible via API
- Inconsistent in historical coverage

### Strategy
Train on 2023, test on 2024 using lag features, weather data, and seasonality indicators (`dayofyear`, `month`).

**Future Use Case**
Once live data access is available, automate daily forecasts using:
- Weather forecasts
- Previous day’s solar generation

---

## 2024 XGBoost Model – Initial Results

**Train**: R² = 0.977 | RMSE = 830.19 | MAE = 615.32  
**Test**: R² = 0.861 | RMSE = 1997.71 | MAE = 1327.05  

- Strong generalisation across seasons
- Inclusion of `glorad` and weather features critical
- Additional trigonometric seasonality features did not improve results

---

## Capacity Growth Impact on Multi-Year Models

When expanding to April 2023 – June 2025, test R² fell from 0.861 (2024-only) to ~0.47.  
Analysis revealed a **160% increase in installed capacity** since 2023, altering the weather–generation relationship.

**Solution Options**
1. Add annual capacity proxy features
2. Scale generation by capacity before training
3. Include `year` or time index features

---

## Model Evaluation: Polynomial Linear vs XGBoost (2023–2025, Scaled)

### Objective
Compare the proof-of-concept polynomial model against the tuned XGBoost model using capacity-adjusted data.

### Results — Full Test Set
**Polynomial Linear (glorad²)**  
R² (Train) – 0.742  
R² (Test) – 0.716  
RMSE (Test) – 2,183.21  
MAE (Test) – 1,656.04  

**XGBoost (scaled 2023–2025)**  
R² (Train) – 0.988  
R² (Test) – 0.833  
RMSE (Test) – 2,074.54  
MAE (Test) – 1,478.73   

---

### Visual Insights
- XGBoost predictions follow seasonal patterns more closely
- Both models under-predict summer peaks, especially in 2025
- XGBoost consistently has tighter residuals and lower MAE in all months

---

### Interpretation
- XGBoost outperforms polynomial regression on all metrics
- Polynomial model remains interpretable but is less accurate, especially for peak days
- Shared weakness in both models indicates need for additional peak-related predictors

---

### Next Steps
- Add weather-based cloudiness indicators
- Experiment with quantile regression to better capture high-generation days
- Test time-based validation to assess year-on-year robustness
