import requests
import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
LAT     = os.getenv("LAT")
LON     = os.getenv("LON")

def extract_weather(LAT,LON,API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}"
    
    response = requests.get(url)

    response.raise_for_status()

    return  response.json()

data = extract_weather(LAT,LON,API_KEY)

print(data)

    