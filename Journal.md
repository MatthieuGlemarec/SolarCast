# Project Journal: SolarCast

## Data Preprocessing: Weather and Solar Data

### Objective
Prepare a clean, aggregated dataset of daily national weather metrics for use in solar generation prediction.

Since aggregated national-level weather data for Ireland is not publicly available, this project manually constructs a representative national dataset by averaging data from nine strategically selected weather stations. These stations are geographically distributed across the Republic of Ireland in a grid-like pattern to ensure balanced regional coverage.

### Steps taken
- Load Raw Station Data
- Standardise & Clean Columns
- Merge Stations by Date
- Load Raw Solar Generation Data (15 minute granularity)
- Convert 15 min granularity to daily form
- Merge Solar Generation data with national Irish aggregated weather

### Original Weather Station Key
date:  -  00 to 00 utc					
rain:  -  Precipitation Amount (mm)					
maxtp: -  Maximum Air Temperature (C)"					
mintp: -  Minimum  Air Temperature (C)					
gmin:  -  09utc Grass Minimum Temperature (C)					
soil:  -  Mean 10cm soil temperature (C)"					
cbl:   -  Mean CBL Pressure (hpa)					
wdsp:  -  Mean Wind Speed (kt)					
hm:    -  Highest ten minute mean wind speed (kt)"					
ddhm:  -  Wind Direction at max 10 min mean (deg)                  					
hg:    -  Highest Gust (kt)					
pe:    -  Potential Evapotranspiration (mm)  					
evap:  -  Evaporation (mm)					
smd_wd:-  Soil Moisture Deficits(mm) well drained					
smd_md:-  Soil Moisture Deficits(mm) moderately drained					
smd_pd:-  Soil Moisture Deficits(mm) poorly drained					
glorad:-  Global Radiation (J/cm sq.)					
ind:   -  Indicator (i)					


## Exploratory Data Analysis (EDA)

### Objective
Explore the cleaned and merged dataset containing daily weather parameters and corresponding solar energy generation for Ireland in 2024.  

The goal is to understand the data's structure, identify trends and patterns, and uncover relationships between variables that can inform modeling strategy.

### Steps taken

## 01: Individual OLS to compare each predictor with the target variable `solargen` to identify predictive power and guide feature selection.

### Observed Result: glorad
glorad shows a strong positive relationship with solargen (R² = 0.689, p < 0.001)
R² (0.689) indicates it explains nearly 69% of the variation in solar generation.
### Observed Result: cbl
cbl shows a weak positive relationship with solargen (R² = 0.006, p = 0.140)  
Low R² (0.006) indicates it explains less than 1% of the variation in solar generation.
### Observed Result: mintp
mintp shows a statistically significant positive relationship with solargen (p < 0.001)  
Low R² (0.145) indicates it explains only a small portion of the variation.mintp shows a statistically significant positive relationship 
### Observed Result: maxtp
maxtp shows a strong positive relationship with solargen (R² = 0.495, p < 0.001)  
R² (0.495) indicates it explains nearly 50% of the variation in solar generation.
### Observed Result: rain
rain shows a strong negative relationship with solargen (R² = 0.094, p < 0.001)  
R² (0.094) indicates it explains just under 10% of the variation in solar generation.

### Key finding:
cbl's weak relationship suggest it may be an inconsequential predictor.

## 02: Multiple OLS to compare all predictor vs only strongly correlated predictors with the target variable `solargen` to identify predictive power and guide feature selection.

### Observed Result: rain, maxtp, mintp, cbl, glorad (all predictors)
Strong linear relationship observed between predictors and solar generation (R² = 0.757, p < 0.001).  
This model explains approximately 76% of the variation in solar generation.  
maxtp, mintp, glorad, and rain are all statistically significant predictors (p < 0.001).  
cbl is not statistically significant (p = 0.216), suggesting it has limited explanatory power.  
High F-statistic (224.7) and very low p-value (p < 0.001) indicate the model fits the data well overall.

Next step: Remove cbl and refit the model to assess impact on adjusted R² and model fit.

### Observed Result: rain, maxtp, mintp, glorad (Reduced predictor)
Almost no loss in explanatory power compared to the full model (Adj. R² was 0.754 with all 5 predictors).  
All remaining predictors are highly significant (p < 0.001)

### Key finding:
This confirms that cbl was not contributing meaningfully, and dropping it was appropriate.
Strong overall model fit (R² = 0.756, p < 0.001) indicating the model explains ~75% of the variation in solar generation.
There’s no immediate statistical reason to remove any of the remaining predictors.

## 03: Create Diagnostic Plots for further analysis of reduced model. Residuals vs Fitted, Residuals Q-Q Plot, Residuals Histogram, VIF

### Observations:
- A widening of the spread of residuals as the fitted values increase indicates non-constant variance (heteroscedasticity).
- Q-Q and Hisogram plots indicate that the observed data is evenly distributed.  
- VIF: glorad shows potential collinarity but remains in a safe zone (VIF 6.2) while maxtp and mintp are likely correlated as both are temperature and show a serious issue. (VIF maxtp = 24.63, mintp = 12.44)   

### Key finding:
- There appears to be heteroscedasticity in the model. This must be addressed.
- As maxtp's R² (0.495) indicates it explains nearly 50% of the variation in solar generation.
While mintp's R² (0.094) indicates it only explains under 10% of the variation in solar generation.
- mintp will be dropped from the model for this proof of concept linear regression model.  
It may later be added back in when more complex models are fitted such as Random Forest which is not sensitive to multicollinearity.

## 04: Drop mintemp from new model as it is likely redundant. Fit OLS model (reduced2).

### Key finding:

- The reduced2 model, excluding mintp, explains 74.3% of the variation in solar generation (R² = 0.743, p < 0.001), showing a slight decrease in explanatory power compared to the previous model of 1.3%.
- VIF: Dropping mintp leads to a notable improvement in multicollinearity, with VIF values for remaining predictors reduced to acceptable levels (maxtp VIF = 6.87).
- This trade-off between a small loss in R² and improved model stability and interpretability suggests that excluding mintp is beneficial for building a more reliable regression model.

## 05: Address heteroscedasticity within current OLS model

### Steps taken
- Apply log-transform on solargen
- Refit model
- Plot residual vs fitted values
- Observe results

### Observations:
- The log transformation of the solargen response has improved the residual distribution, addressing the heteroscedasticity observed in previous models.  
- While some vertical spread remains, particularly in lower predicted values, the transformation results in more stable variance across the range of fitted values.
- The model’s R² (0.708) is slightly lower than reduced2 model but the benefit of satisfying key linear regression assumptions justifies this trade-off.
Note: Predictions from this model will need to be back-transformed to return to the original MWh scale for the intended forecasting task.

### Key finding:
- The Q-Q plot shows residuals closely following the normal line in the center, though:  
The left tail dips slightly below the line, indicating mild left skew.  
The right tail also dips under the line, contrasting the earlier upward deviation in reduced2
- The histogram of residuals remains approximately bell-shaped, though:  
It is now slightly skewed to the left, consistent with the Q-Q plot.  
The distribution still broadly resembles normality, supporting the model's validity.

- Compared to the earlier, untransformed models:  
The residual spread is more even, suggesting an improvement in homoscedasticity.  
The normality of residuals has slightly decreased due to the log transformation.

- Trade-off:
The log transformation improved variance stability (a more critical issue) at the expense of a minor increase in skewness.
This trade off is acceptible and so, model_log_solargen appears to be the reasonable choice for model training

## 06: Apply Polynominal Regression to the Strongest Predictor to Gain Precision.

### Steps take
- Add a quadratic term for 'glorad' to account for non-linear effects in solar generation.
- This aims to improve model performance in higher radiation ranges where the linear model underpredicts.
-Conduct anova test to validate improvements.
- Observe results.

### Observations
- Reduced2 -     	(RMSE: 2756.75)	- (MAE: 2105.45)
- Log-transformed -	(RMSE: 4337.00) - (MAE: 2636.23)
- Quadratic Model -	(RMSE: 2687.25)	- (MAE: 2041.25)

#### Anova Result: reduced2 v model_poly
- F-statistic = 18.92: A high number that suggest meaningful improvement
- P-value - 0.000018: Meaning the improvement is statistically significant.

- The Quadratic Model performs best so far in terms of both RMSE and MAE.
- This suggests that introducing non-linearity (via a polynomial term) better captures the relationship between predictors and solargen.
-The Quadratic Model avoids transformation artifacts (like log-scale back-transform issues), and improves predictive accuracy.

