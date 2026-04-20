import os
import psycopg2
import requests
import pandas as pd
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

    try:
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
        
        print("\n--- [SUCCESS] ETL Process Finished Successfully ---")

    except Exception as e:
        # This will catch ANY error in Stage 1, 2, or 3
        print(f"\n--- [FAILURE] Pipeline stopped due to error: ---")

        print(f"Error details: {e}")

if __name__ == "__main__":
    run_weather_pipeline()