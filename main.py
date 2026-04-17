from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import your custom modules
from extract import extract_weather
from transform import transform_weather
from load import load_to_postgres

load_dotenv()

def run_pipeline():
    print("--- Starting Weather API ETL Pipeline ---")

    # STAGE 1: EXTRACT
    
    api_key = os.getenv("API_KEY")
    lat     = os.getenv("LAT")
    lon     = os.getenv("LON")

    print(f"[1/3] Extracting data for {lat}, {lon}...")
    raw_data = extract_weather(lat, lon, api_key)
    
    if not raw_data or raw_data.get("cod") != 200:
        raise Exception(f"Extraction failed: {raw_data.get('message', 'Unknown error')}")

    # STAGE 2: TRANSFORM
    print("[2/3] Transforming data...")
    clean_data = transform_weather(raw_data)
    
    # STAGE 3: LOAD
    print(f"[3/3] Loading data for {clean_data['City']}...")
    success = load_to_postgres(clean_data)

    if not success:
        raise Exception("Pipeline Failed at Load Stage")
    
    print("--- Pipeline Completed Successfully! ---")

# DAG Definition
with DAG(
    dag_id="weather_etl_dag",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily", # Same as timedelta(hours=24)
    catchup=False
) as dag:

    run_pipeline_task = PythonOperator(
        task_id="run_weather_pipeline",
        python_callable=run_pipeline
    )