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

## Pivot: From Two-Stage Pipeline to Historical Forecasting

### Objective  
Adapt the modelling approach to deliver an accurate and deployable solar generation forecast without relying on `glorad`, which is not directly forecasted by Met Éireann.

---

### Context  
The project design introduced a two-stage pipeline to resolve a key forecasting constraint:

1. **Stage 1** – Predict `glorad` (global radiation) using forecastable weather inputs (`rain`, `maxtp`, `mintp`)  
2. **Stage 2** – Use predicted `glorad` to forecast solar energy generation (`solargen`)

While this approach upheld physical realism and was theoretically sound, in practice, the Stage 1 model underperformed. Even advanced machine learning methods like XGBoost were unable to predict `glorad` with sufficient accuracy — test R² scores plateaued around **0.45**, despite extensive hyperparameter tuning and regularisation.

This bottleneck undermined Stage 2 performance, since the key driver (`glorad`) was effectively an unreliable estimate.

---

### Resolution  
In light of this, and given project time constraints, the pipeline was restructured to remove the dependency on `glorad`.

> The new approach directly forecasts `solargen` using **historical patterns**, rather than relying on future weather-based predictions.

### New Strategy: Time Series Forecasting of Solar Generation

The revised approach treats solar generation (`solargen`) as a **time-dependent process** that can be forecasted using its own past behaviour. This is a widely used method in energy forecasting and allows for both short-term accuracy and model simplicity.

#### Key Steps:
- Generate **lag features** from historical `solargen` values (e.g., `lag_1`, `lag_2`, `lag_7`)
- Optionally include lagged weather variables if necessary (`maxtp_lag1`, `rain_lag2`)
- Train a regression model (XGBoost or Random Forest) using lag features to predict future `solargen`
- Evaluate using standard metrics (R², RMSE, MAE)


### Justification  
- **Practicality**: Removes reliance on unavailable or unreliable features  
- **Performance**: Leverages autocorrelation within solar generation, which has shown promising predictive power in preliminary tests  
- **Scalability**: Can easily incorporate future enhancements (e.g., seasonality, weather-lag hybrids)  
- **Deployability**: Produces usable forecasts even in the absence of live weather data  


### Summary  
While the original two-stage pipeline conceptually addressed Ireland’s forecasting challenges, the execution revealed a key constraint: forecastable weather variables alone were insufficient to reliably predict `glorad`. In response, the project pivoted to a **time series regression approach**, allowing `solargen` to be forecasted directly using historical data.

This shift aligns with time-tested industry practices, maintains scientific integrity, and ensures the project remains achievable and impactful within the project timeline.









## Deployment Plan: Automating Solar Generation Data Collection

### Objective  
Enable daily, real-time solar generation forecasting by automating the ingestion of live solar generation data from EirGrid.

---

### Context  
To maintain a functional forecasting pipeline, the model requires up-to-date solar generation data at a daily (or sub-daily) resolution. EirGrid publishes 15-minute solar generation figures via its **Smart Grid Dashboard**. However, this data is only available via a downloadable Excel sheet from their public-facing website and is not currently offered through an official API.

Given the absence of a formal endpoint, a practical alternative was required to automate this ingestion process and support live deployment of the forecasting model.

---

### Resolution  
The project will integrate the open-source tool **EirGrid Data Downloader** to fetch solar generation data at 15-minute resolution. This Python-based utility automates data downloads from EirGrid's Smart Grid Dashboard and outputs clean, timestamped CSVs suitable for ingestion into the prediction pipeline.

---

### Steps  
1. Clone the [EirGrid Data Downloader](https://github.com/Daniel-Parke/EirGrid_Data_Download) repository  
2. Modify the script to retrieve only **solar generation data**  
3. Schedule the script to run daily (e.g. via `cron` or Task Scheduler)  
4. Store the data in a local CSV or database  
5. Extract and aggregate daily solar generation totals  
6. Feed this data into the model as lag features (`lag_1`, `lag_2`, etc.) for time-series forecasting

---

### Advantages  
- **Automation**: No manual download steps required  
- **Granularity**: Provides 15-minute solar generation readings  
- **Historical coverage**: Supports access to several years of data for backtesting  
- **Stability**: Widely used community script, tested and maintained

---

### Summary  
This approach ensures that solar generation data is automatically ingested into the forecasting model, enabling reliable and up-to-date predictions without relying on forecast-only features. It forms the foundation of a deployable solar forecasting tool suitable for real-world application in the Irish context.
