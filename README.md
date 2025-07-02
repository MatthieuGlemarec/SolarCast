# SolarCast: Solar Generation Forecasting for Ireland

SolarCast is a machine learning project focused on predicting daily solar electricity generation in Ireland using historical solar output and daily weather data. The aim is to support renewable energy planning and visibility by providing a 7-day solar forecast trained on national-level weather inputs.

## Project Overview

This project uses data from:

- Met Éireann: daily weather summaries from nine stations across the Republic of Ireland
- EirGrid (or SEAI): national solar generation data, aggregated at daily resolution

Weather attributes used include:
- Global radiation (J/cm²)
- Maximum and minimum air temperature (°C)
- Precipitation (mm)
- Mean CBL pressure (hPa)

The final dataset combines these into a single national-level input table for model training.

## Project Structure

SolarCast/
├── data/ # Raw weather station and solar generation CSVs
├── cleaned_data/ # Processed national-level daily weather data
├── notebooks/ # Jupyter notebooks by stage
├── models/ # Trained model files (e.g. .pkl)
├── outputs/ # Graphs, reports, exported forecasts
├── venv/ # Virtual environment (ignored by Git)
├── requirements.txt # Python dependencies
└── README.md # Project documentation

## Dependencies

All dependencies are listed in `requirements.txt`. Core packages include:

- pandas
- numpy
- scikit-learn
- matplotlib
- jupyter

To install all dependencies into a clean environment, follow the setup instructions below.

## Setting Up the Virtual Environment

This project uses a virtual environment to isolate dependencies. To create and activate it:

### Step 1: Create the environment

-in the terminal-

python -m venv venv **

### Step 2: Activate the environment

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

### Step 3: Install project requirements

pip install -r requirements.txt

## Running the Project

After setting up the environment, you can start exploring the code by opening the Jupyter notebooks inside the notebooks/ folder.

To activate the environment before running notebooks or scripts in future sessions:

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

Then run:

jupyter notebook


## Updating Requirements

When adding any new packages update requirements.txt with:

pip freeze > requirements.txt

This ensures the project remains reproducible.

## Project Status

- [x] Downloaded and cleaned 9 Met Éireann weather station datasets  
- [ ] Aggregated daily weather metrics to national level  
- [ ] Cleaned daily solar generation data for 2024  
- [ ] Merged weather and solar datasets  
- [ ] Trained initial ML model  
- [ ] Built forecast evaluation and visualisation tools  
- [ ] (Optional) Deployed a daily prediction dashboard  


This project is under active development as part of a capstone submission for the AI/ML stream.
