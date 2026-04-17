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