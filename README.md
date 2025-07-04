# SolarCast: Solar Generation Forecasting for Ireland

SolarCast is a machine learning project focused on predicting daily solar electricity generation in Ireland using historical solar output and daily weather data. The aim is to support renewable energy planning and visibility by providing a 7-day solar forecast trained on national-level weather inputs.

## Project Overview

This project uses data from:

- Met Éireann: daily weather summaries from nine geographically representative stations across the Republic of Ireland
- EirGrid (or SEAI): national solar generation data, aggregated at daily resolution

### Aggregated National Irish Weather and Solar data

The final dataset combines data into a single national-level table with 366 values, covering the year 2024, for model training.

#### Attributes

- date: YYYY-MM-DD
- rain: Precipitation (mm)
- maxtp: Maximum air temperature (°C)
- mintp: Minimum air temperature (°C)
- cbl: Mean CBL pressure (hPa)
- glorad: Global radiation (J/cm²)
- solargen: Solar Generation (MWh)


## Project Structure

SolarCast/  
├── data/ # Raw weather station and solar generation CSVs  
├── cleaned_data/ # Processed national-level daily weather data  
├── notebooks/ # Jupyter notebooks by stage  
├── models/ # Trained model files  
├── outputs/ # Graphs, reports, exported forecasts  
├── venv/ # Virtual environment (ignored by Git)    
├── requirements.txt # Python dependencies  
└── README.md # Project documentation  

## Dependencies

All dependencies are listed in `requirements.txt`. Core packages include:

asttokens==3.0.0
colorama==0.4.6
comm==0.2.2
contourpy==1.3.2
cycler==0.12.1
debugpy==1.8.14
decorator==5.2.1
executing==2.2.0
fonttools==4.58.5
ipykernel==6.29.5
ipython==9.4.0
ipython_pygments_lexers==1.1.1
jedi==0.19.2
jupyter_client==8.6.3
jupyter_core==5.8.1
kiwisolver==1.4.8
matplotlib==3.10.3
matplotlib-inline==0.1.7
nest-asyncio==1.6.0
numpy==2.2.6
packaging==25.0
pandas==2.3.0
parso==0.8.4
patsy==1.0.1
pillow==11.3.0
platformdirs==4.3.8
prompt_toolkit==3.0.51
psutil==7.0.0
pure_eval==0.2.3
Pygments==2.19.2
pyparsing==3.2.3
python-dateutil==2.9.0.post0
pytz==2025.2
pywin32==310
pyzmq==27.0.0
scipy==1.14.1
six==1.17.0
stack-data==0.6.3
statsmodels==0.14.4
tornado==6.5.1
traitlets==5.14.3
tzdata==2025.2
wcwidth==0.2.13
 

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

## Updating Requirements

When adding any new packages update requirements.txt with:

pip freeze > requirements.txt

This ensures the project remains reproducible.

## Project Status

- [x] Downloaded and cleaned 9 Met Éireann weather station datasets  
- [x] Aggregated daily weather metrics to create national average 
- [x] Downloaded and cleaned daily EirGrid (or SEAI) solar generation data for 2024  
- [x] Merged weather and solar datasets  
- [x] Conduct Exploratory Data Analysis (EDA)  
- [ ] Trained initial ML model  
- [ ] Built forecast evaluation and visualisation tools  
- [ ] (Optional) Deployed a daily prediction dashboard  


This project is under active development as part of a capstone submission for the AI/ML stream of science in computing at the National College of Ireland.
