import psycopg2 as psy
import pandas as pd
from sqlalchemy import create_engine
from transform import transformed_data
from dotenv import load_dotenv
import os

load_dotenv()

host     = os.getenv("DB_HOST")
port     = os.getenv("DB_PORT")
user     = os.getenv("DB_USER")
dbname   = os.getenv("DB_NAME")
password = os.getenv("DB_PASSWORD")
sslmode  = "require"


def load_to_postgres(transformed_data):
    
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode=require")

    df = pd.DataFrame([transformed_data])

    try:
    
        df.to_sql("weather_report", con=engine, if_exists="replace", index=False)

        print("\n[SUCCESS] Data successfully pushed to SQL table 'weather_report'")
        
        with engine.connect() as conn:

            result = pd.read_sql("SELECT * FROM weather_report ", conn)
            
            print("\n--- Last Row in Database ---")

            print(result)

        return True
    
    except Exception as e:
        
        print(f"Postgres Load Error :{e}")

        return False


