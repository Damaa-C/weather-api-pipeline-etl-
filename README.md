 # Weather Pipeline Overview
 
This pipeline follows the ETL (Extract, Transform, Load) architecture.
It pulls real-time weather data from an API, cleans it for analysis, and stores it in a database.
Using Airflow allows us to automate this so it runs every day (or hour) without manual intervention.

##  Dependencies & Setup 
Before running any code, you must set up your environment and install the necessary libraries.environment Creation.
```
# Windows
python -m venv data_env
data_env\Scripts\activate

# Linux/macOS
python3 -m venv data_env
source data_env/bin/activate
```
 ### Required Libraries
 
Install these inside your activated environment:
```
pip install pandas sqlalchemy psycopg2-binary requests python-dotenv apache-airflow
```
 ### Run this in Airflow;
 
You need a DAG (Directed Acyclic Graph).
Airflow acts as the "manager" that watches the clock and starts your main.py logic automatically.

# Airflow Dependencies

**Webserver**: The UI where you see your pipeline graph.
**Scheduler**: The "brain" that triggers tasks.
**Database** : Airflow's internal tracker (usually SQLite or Postgres).

## How to Run Airflow
Once Airflow is installed (on WSL or Linux), use these commands:

Initialize: `airflow db init`
Create User: `airflow users create --username admin 
              --firstname YourName 
              --lastname YourName 
              --role Admin 
              --email admin@example.com `
              
Start Webserver: `airflow webserver -p 8080`
Start Scheduler: `airflow scheduler` (Run this in a second terminal)

# Execution Summary Task
#### Test Script
```
# Windows Command 
python main.py

#Linux Command
python3 main.py
```
#### Test Success

Run pipeline_test [run.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/run.py)

# Run Airflow 
Use WSL2 or Dockerairflow scheduler

## Testing in Jupyter [deploy.ipynb](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/deploy.ipynb)

Running your pipeline in a Jupyter Notebook is the best way to verify "Successability" because:
- You can see the DataFrame visually before it hits the database.
- You can test the Database Connection separately to ensure your credentials in .env are correct.
It provides an immediate feedback loop for debugging errors in the Transform logic.

##  The Python ETL Logic
These three modules form the core of your pipeline. They are designed to be imported into either a main.py script or an Airflow DAG.

### Extract [extract.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/extract.py)
Uses the requests library to handle HTTP communication.
```
import requests # Library for making API calls

def extract_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url) # Sending the GET request
    return response.json() # Converting raw bytes to a Python dictionary
```
### Transform [transform.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/transform.py) 

Uses pandas for data manipulation and datetime for logging.
```
import pandas as pd # Library for data structures (DataFrames)
from datetime import datetime # Library for handling time

def transform_weather(raw_data):
    # Core transformation: Kelvin to Celsius
    temp_c = round(raw_data['main']['temp'] - 273.15, 2)
    
    clean_data = {
        "City": raw_data['name'],
        "Temp_C": temp_c,
        "Condition": raw_data['weather'][0]['description'],
        "Timestamp": datetime.now() # Adding a 'when' to our data
    }
    return clean_data
  ```

### Load [load.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/load.py)

Uses sqlalchemy as the bridge to the database and pandas for the upload.

```
from sqlalchemy import create_engine # Library to manage DB connections
import pandas as pd

def load_to_postgres(data_dict, config):
    # Constructing the connection string
    conn_str = f"postgresql://{config['user']}:{config['pass']}@{config['host']}/{config['db']}"
    engine = create_engine(conn_str)
    
    df = pd.DataFrame([data_dict])
    # The 'magic' method that handles the SQL INSERT
    df.to_sql('weather_table', engine, if_exists='append', index=False)
    return True
 ```

##  The Airflow Orchestrator

**Airflow** doesn't "run" your code in the traditional sense; it manages the execution of your Python functions using Operators.

### Airflow DAG [main.py](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/main.py)

Uses airflow core libraries to define the schedule and tasks

```
from airflow import DAG # The core workflow object
from airflow.operators.python import PythonOperator 
from datetime import datetime

# Import your logic from the files above
from extract import extract_weather
# ... other imports ...

with DAG(
    dag_id="weather_etl_v1",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly", # Runs automatically every 60 minutes
    catchup=False
) as dag:

    task_extract = PythonOperator(
        task_id="extract_api_data",
        python_callable=extract_weather
    )
    
    # task_extract >> task_transform >> task_load (Dependency logic)
```

## Key Libraries Summary

Library Purpose; 
- `requests`: Fetches the raw data from the web.
- `pandas`: The "Excel of Python"—converts JSON into tables.
- `sqlalchemy`: Talk to any SQL database (Postgres, MySQL, etc.) without writing manual SQL.
- `python-dotenv`: Keeps your API keys and passwords secret (loads from .env).
- `apache-airflow`: The "Boss" that handles scheduling, retries, and failure alerts.

## Testing "Successability" in [deploy.ipynb](https://github.com/Damaa-C/weather-api-pipeline-etl-/blob/main/deploy.ipynb)

In your Jupyter Notebook, you should have a "Verification Cell" that looks like this:
```
from extract import extract_weather
from transform import transform_weather
from load import load_to_postgres
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os 

def run_pipeline ():
    print("--- Starting Weather API ETL Pipeline ---")

    # STAGE 1: EXTRACT
    print("[1/3] Extracting data from OpenWeather...")

    API_KEY = os.getenv("API_KEY")
    LAT     = os.getenv("LAT")
    LON     = os.getenv("LON")

    raw_data = extract_weather(LAT, LON, API_KEY)
    
    if not raw_data or raw_data.get("cod") != 200:
        print("ERROR: Extraction failed. Check API key or coordinates.")
        return

    # STAGE 2: TRANSFORM
    print("[2/3] Transforming data (Cleaning & Unit Conversion)...")
    clean_data = transform_weather()
    
    # STAGE 3: LOAD

    host     = os.getenv("DB_HOST")
    port     = os.getenv("DB_PORT")
    user     = os.getenv("DB_USER")
    dbname   = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")
    sslmode  = "require"

    print(f"[3/3] Loading data for {clean_data['City']} into Database...")

    success = load_to_postgres(clean_data)
   

    if success:

        print("--- Pipeline Completed Successfully! ---")
    else:
        print("--- Pipeline Failed at Load Stage ---")

if __name__ == "__main__":
    run_pipeline()
  ```
`
--- Starting Weather API ETL Pipeline ---
[1/3] Extracting data from OpenWeather...
[2/3] Transforming data (Cleaning & Unit Conversion)...
[3/3] Loading data for Zocca into Database...

[SUCCESS] Data successfully pushed to SQL table 'weather_report'

--- Last Row in Database ---
    City Country      Condition  Temp_C  Feels_Like_C  Humidity
0  Zocca      IT  broken clouds   18.97         18.57        63
--- Pipeline Completed Successfully! ---
`
# Conclusion
This project successfully demonstrates a full-lifecycle Data Engineering pipeline, moving from raw, unstructured API responses to a queryable, production-ready database. By decoupling the logic into Extract, Transform, and Load modules, the system achieves high maintainability and satisfies modern software engineering principles.

## Key Takeaways
- Modular Architecture: By separating concerns into dedicated Python scripts, we ensure that a failure in the API (Extract) doesn't break the logic of the transformation or the security of the database connection.

- Scalable Orchestration: Implementing Apache Airflow transforms a manual script into an automated service. This setup handles retries, schedules, and monitoring—essential for any real-world data team.

- Environment Security: Using .env files and python-dotenv ensures that sensitive credentials (like Aiven passwords and OpenWeather keys) are never exposed in the source code, adhering to DevSecOps best practices.

- Successability Testing: The inclusion of Jupyter Notebooks (.ipynb) provides a vital "sandbox" for debugging and validating data integrity before the code is deployed to the Airflow scheduler.

## Future Enhancements
To further evolve this pipeline, the following steps could be taken:

- Data Quality Checks: Integrating a tool like Great Expectations to validate data types and null values automatically during the Transform stage.

- Cloud Deployment: Moving the local Airflow instance to a cloud-native environment like AWS (MWAA) or Google Cloud (Composer).

- Visualization: Connecting a BI tool (like Looker or Grafana) directly to the PostgreSQL database to create real-time weather dashboards.
