# SolarCast: Solar Generation Forecasting for Ireland

SolarCast is a machine learning project aimed at predicting daily national solar electricity generation in Ireland using historical solar output and daily weather data. The primary goal is to evaluate the feasibility of accurate forecasting using only publicly available Irish datasets, with a focus on supporting renewable energy planning and grid management.

While the original concept included a continuously updated 7-day live forecast, the current system is delivered as an offline prototype due to the absence of forecasted global radiation data and limited historical solar generation records. The modular design allows for straightforward deployment once these data sources become available.

## Project Overview

This project uses data from:

- Met Éireann: daily weather summaries from nine geographically representative stations across the Republic of Ireland
- EirGrid (or SEAI): national solar generation data, aggregated at daily resolution

### Aggregated National Irish Weather and Solar data

The final dataset combines data into a single national-level table with 366 values, covering the year 2024, for model training.

#### Attributes

- `date` – YYYY-MM-DD
- `rain` – Precipitation (mm)
- `maxtp` – Maximum air temperature (°C)
- `mintp` – Minimum air temperature (°C)
- `cbl` – Mean CBL pressure (hPa)
- `glorad` – Global radiation (J/cm²)
- `solargen` – Solar Generation (MWh)

## Project Structure

SolarCast/  
├── Data/                # Raw weather station and solar generation CSVs  
├── Cleaned_Data/        # Processed national-level daily weather data  
├── Notebooks/           # Jupyter notebooks by stage  
├── Models/              # Trained model files  
├── Outputs/             # Graphs, reports, exported forecasts  
├── Src/                 # Reusable Python modules for modelling and preprocessing  
├── Tests/               # Unit tests for Src modules  
├── venv/                # Virtual environment (ignored by Git)  
├── requirements.txt     # Python dependencies  
├── Journal.md           # Project journal  
└── README.md            # Project documentation  


## Dependencies

All dependencies are listed in `requirements.txt`. Core packages include:

- `numpy` – numerical computing  
- `pandas` – data manipulation  
- `matplotlib` – plotting and visualization  
- `scipy` – scientific computing  
- `statsmodels` – statistical modeling and diagnostics  
- `patsy` – formula interface for statsmodels  
- `jupyter` – interactive notebooks environment  
- `xgboost` – gradient boosting model implementation    
- `pytest` – unit testing framework   

To install all dependencies into a clean environment, follow the setup instructions below.

## Setting Up the Virtual Environment

This project uses a virtual environment to isolate dependencies. To create and activate it open the terminal:

### Step 1: Create the environment

python -m venv venv 

### Step 2: Activate the environment

__Windows:__  

venv\Scripts\activate

__macOS/Linux:__  

source venv/bin/activate

### Step 3: Install project requirements

pip install -r requirements.txt

### Step 4: Add the virtual environment as a Jupyter kernel

pip install ipykernel  

python -m ipykernel install --user --name=solarcast-venv --display-name "Python (solarcast-venv)"

## Running the Project

After setting up the environment, you can start exploring the code by opening the Jupyter notebooks inside the notebooks/ folder.

To activate the environment before running notebooks or scripts in future sessions:

**Note:** If you see an error about running scripts being disabled when activating the virtual environment, temporarily allow script execution for the current session by running:  
**Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process**   

__Windows:__  

venv\Scripts\activate

__macOS/Linux:__  

source venv/bin/activate

Then run:  

jupyter notebook

## Select the Correct Kernel in Jupyter

When opening your notebooks, select the kernel named Python (solarcast-venv) via:  

Kernel > Change kernel > Python (solarcast-venv)  

This ensures the notebook uses the correct virtual environment and installed packages.  

## Running Tests

The project includes a full unit and integration test suite for the `Src` modules. To run all tests, ensure your virtual environment is activated, navigate to the project root, and execute:

pytest Tests -v


This will run all test files in the `Tests/` directory, displaying verbose output for each case. All tests should pass before continuing with further development or deployment.


## Updating Requirements

When adding any new packages update requirements.txt with:

pip freeze > requirements.txt

This ensures the project remains reproducible.

## Project Status

- [x] Downloaded and cleaned 9 Met Éireann weather station datasets  
- [x] Aggregated daily weather metrics to create national average  
- [x] Downloaded and cleaned daily EirGrid (or SEAI) solar generation data for 2024  
- [x] Merged weather and solar datasets  
- [x] Conducted Exploratory Data Analysis (EDA)  
- [x] Trained initial ML model  
- [x] Trained advanced tree based ML models
- [x] Evaluated model performance and improvements  
- [x] Scaled historical solar generation data for capacity growth adjustments  
- [x] Built forecast evaluation and visualisation tools  
- [x] Developed and ran unit test suite for reusable functions  



This project is under active development as part of a capstone submission for the AI/ML stream of science in computing at the National College of Ireland.
