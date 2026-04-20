from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine 
from dotenv import load_dotenv



def run_weather_pipeline():

    # 1. Setup & Environment
    load_dotenv(override=True)
    
    # API Config
    API_KEY = os.getenv("API_KEY")
    LAT = os.getenv("LAT")
    LON = os.getenv("LON")
    
    # DB Config
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    user = os.getenv("DB_USER")
    dbname = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")

    print("--- Starting Weather ETL Pipeline ---")

        # --- STAGE 1: EXTRACT ---
    print("[1/3] Extracting data...")

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}"
        
    response = requests.get(url, timeout=10)

    response.raise_for_status()

    raw_data = response.json()

        # --- STAGE 2: TRANSFORM ---
    print("[2/3] Transforming data...")
        # Create dictionary for DataFrame
    weather_data = {
            "City": raw_data.get("name"),
            "Country": raw_data.get("sys", {}).get("country"),
            "Condition": raw_data.get("weather", [{}])[0].get("description", "").title(),
            "Temp_C": round(raw_data.get("main", {}).get("temp", 0) - 273.15, 2),
            "Feels_Like_C": round(raw_data.get("main", {}).get("feels_like", 0) - 273.15, 2),
            "Humidity": raw_data.get("main", {}).get("humidity")
        }
    df = pd.DataFrame([weather_data])

    print(df)

        # --- STAGE 3: LOAD ---
    print(f"[3/3] Connecting to {host}...")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode=require")


    with engine.begin() as conn:
            df.to_sql("weather_report", con=conn, if_exists="append", index=False)
    
    return "ETL SUCCESS"


# DAG Definition
with DAG(
    dag_id="weather_etl_dag",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily", # Same as timedelta(hours=24)
    catchup=False
) as dag:

    run_pipeline_task = PythonOperator(
        task_id="run_weather_pipeline",
        python_callable=run_weather_pipeline
    )