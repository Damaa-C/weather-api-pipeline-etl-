import os
from dotenv import load_dotenv

load_dotenv()

# api_config
API_KEY = os.getenv("API_KEY")
LAT     = os.getenv("LAT")
LON     = os.getenv("LON")


# db credentials
host     = os.getenv("DB_HOST")
port     = os.getenv("DB_PORT")
user     = os.getenv("DB_USER")
dbname   = os.getenv("DB_NAME")
password = os.getenv("DB_PASSWORD")
sslmode  = "require"




