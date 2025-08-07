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







## Solar Generation Forecasting: Deployment & Modelling Strategy Update

### Objective  
Enable reliable and accurate solar energy forecasting in Ireland using historical data, while laying the groundwork for future live deployment once real-time data access becomes viable.

---

### Context  
The original goal of the project was to build a **live forecasting pipeline** using up-to-date weather and solar generation data. While forecastable weather metrics were accessible via Met Éireann, **real-time solar generation data** proved significantly harder to obtain.

EirGrid publishes 15-minute solar generation figures through its **Smart Grid Dashboard**, but this data is:
- Not accessible via a public API
- Only downloadable as Excel sheets through a user interface
- Inconsistent in terms of historical coverage and format

---

### Attempted Solutions  
Efforts to automate solar data ingestion included:
- Modifying the open-source [EirGrid Data Downloader](https://github.com/Daniel-Parke/EirGrid_Data_Download)
- Analysing network traffic to extract endpoints from the [EirGrid Solar Dashboard](https://www.smartgriddashboard.com/roi/solar/)
- Investigating web scraping or `.xlsx` automation pipelines

Despite extensive attempts, these methods were either **unsuccessful**, **unstable**, or **unsuitable** for production use.

---

### New Strategy: Historical Time Series Forecasting

Given the inability to reliably automate recent solar data ingestion, the project has pivoted to a **purely historical modelling approach**. This will still meet project goals in terms of evaluating forecasting methods and building a viable model.

> **Training Period:** January 2023 – December 2023  
> **Testing Period:** January 2024 – December 2024

This approach allows the model to:
- Learn from a full year of seasonal variation
- Leverage lag features and weather predictors (rain, temperature, calendar features)
- Demonstrate performance in realistic test conditions

---

### Deployment Considerations (Future Use Case)

If EirGrid were to expose a proper API or if a stable scraping pipeline were built, this model could support **daily real-time forecasts** by:
1. Feeding in forecastable weather variables (rain, maxtemp, mintemp)
2. Incorporating yesterday’s solar generation (via a lag feature)
3. Generating predictions for the next day — or recursively, for up to 7 days

A potential pipeline would involve:
- Daily download of solar generation (15-min → daily aggregate)
- Appending data to a master dataset
- Feeding updated features into the model for rolling prediction

This could be automated using tools like `cron`, Task Scheduler, or a CI/CD pipeline.

---

### Summary  
Given current constraints, the forecasting model will be developed using high-quality **historical solar and weather data**, trained on 2023 and tested on 2024. While **live deployment is not feasible at this stage**, the model has been designed with future integration in mind — allowing it to be easily extended into a production-ready forecasting tool when reliable, real-time solar generation data becomes available.




## Journal Entry: Project Direction Update & Refined Modelling Plan

### Project Pivot Summary  
Due to the inaccessibility of **live solar generation data** in Ireland, the original plan to build a real-time solar forecasting model has been re-evaluated. Despite substantial efforts to retrieve current solar data via API access, custom downloaders, and site scraping from the EirGrid Smart Grid Dashboard, the data remains locked behind non-programmatic interfaces. This severely limits the feasibility of real-time deployment.

### Updated Objective  
The project's focus is now to **build a highly accurate historical solar generation forecasting model** using available weather and solar data from 2023 and 2024. The aim is to optimize model performance and predictive accuracy with the available dataset, while ensuring the solution is designed for **future deployment** when live data access becomes viable.

### Feature Selection Rationale  
Earlier experimentation revealed that a simple regression model using only the following features:
- **Global radiation (glorad)**
- **Minimum temperature (mintp)**
- **Maximum temperature (maxtp)**
- **Rainfall (rain)**

…achieved an **R² score of approximately 0.75**, highlighting strong predictive capability from these features alone. This motivated a return to these core variables — now applying them within a more powerful **XGBoost regression model** to further increase predictive performance.

### Updated Modelling Strategy
- Use **2023 data** for training and **2024 data** for testing  
- Focus feature engineering on the strongest weather-based predictors: `glorad`, `mintp`, `maxtp`, `rain`
- Apply **XGBoost**, a gradient-boosted tree algorithm known for handling non-linearities and complex interactions
- Perform **grid search hyperparameter tuning** to maximize performance  
- Evaluate using R², RMSE, and MAE for transparency in both training and test results

### Additional Enhancement: Seasonality Features  
To further improve model performance and robustness, **calendar-based features** will be incorporated:
- `dayofyear` — to capture the seasonal bell-curve shape of solar generation in Ireland
- `month` — to allow for discrete monthly variation
These **seasonality indicators** should help the model learn macro patterns in solar behavior across the year, which may otherwise be missed by purely weather-driven features.

---

### Justification & Future Considerations  
This refined approach achieves several objectives:
- Leverages proven strong predictors in a more advanced model
- Provides a realistic and rigorous historical validation
- Keeps the project scoped and feasible within remaining time
- Aligns with original deployment goals, enabling **future integration** of real-time forecasting when data access improves

---

### Reflection  
This is a **strategically sound** direction for the project. It acknowledges data constraints while still producing a valuable and technically challenging deliverable. By blending **simple regression insights**, **powerful machine learning models**, and **seasonal feature engineering**, the project introduces **innovation** into the modelling process that goes beyond standard techniques — strengthening both the academic rigor and real-world relevance of the work.




## 2024 XGBoost Model – Initial Results and Analysis

### Objective  
To develop a high-performing regression model that predicts daily solar energy generation using observed weather data, specifically:
- glorad (global radiation)
- rain (precipitation)
- maxtp and mintp (maximum and minimum temperatures)

### Modelling Strategy  
A baseline XGBoost regression model was trained using only 2024 data. This approach provides:
- Clean, fully complete data for all calendar months
- The ability to evaluate predictive performance across seasons

Calendar-based seasonality features (month, dayofyear) were also included. Grid search was used to tune hyperparameters, targeting the highest possible R² score.

### Performance  
After hyperparameter tuning, the model achieved the following scores:

- Train: R²: 0.977 | RMSE: 830.19 | MAE: 615.32  
- Test: R²: 0.861 | RMSE: 1997.71 | MAE: 1327.05  

These scores show strong generalization to unseen data and a large improvement over the baseline linear regression model developed earlier in the project.

Although there is a performance gap between the training and test sets, this is expected given the smaller dataset size and natural variability in weather data.

### Observations
- The inclusion of glorad and weather features significantly improves accuracy  
- Additional features like sin_doy and cos_doy were tested but did not improve performance and were excluded
- Learning curves suggest that more data could reduce overfitting and improve generalization further

### Next Steps
Due to the limited availability of solar generation data (which only began in April 2023), the model currently lacks earlier seasonal data.

#### Planned Actions:
- Download and preprocess solar generation and national weather data from April 2023 to December 2023
- Merge this with the existing 2024 dataset to build a larger, more seasonally diverse training set
- Retrain the model to evaluate whether the additional data improves performance and stability

The updated dataset will help the model better understand solar patterns and increase overall robustness.

---

Model Saved As:  
`../../models/XGBoost_2024_Model.pkl`
