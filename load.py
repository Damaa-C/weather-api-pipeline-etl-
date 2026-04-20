# load to postgres
import pandas as pd
from sqlalchemy import create_engine
from transform import transformed_df
from dotenv import load_dotenv
import os



def load_to_postgres():

    
    load_dotenv(override=True)

    host     = os.getenv("DB_HOST")
    port     = os.getenv("DB_PORT")
    user     = os.getenv("DB_USER")
    dbname   = os.getenv("DB_NAME")
    password = os.getenv("DB_PASSWORD")
    sslmode  = "require"
    
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode=require")


    try:
        with engine.begin() as conn:

            transformed_df.to_sql("weather_report", con=conn, if_exists="append", index=False)

            print("\n[SUCCESS] Data successfully pushed to SQL table 'weather_report'")
        
        with engine.connect() as conn:

            result = pd.read_sql("SELECT * FROM weather_report ORDER BY 1 DESC LIMIT 1", conn)

            print("\n--- Recent Rows in Database ---")

            print(result)

        return True
    
    except Exception as e:
        print(f"\n[ERROR] Postgres Load Failed: {e}")
        return False
    
load_to_postgres()



