import pandas as pd
from extract import raw_data
import os 


def transform_weather():

   filtered_data = {
        "City"        : raw_data.get("name"),
        "Country"     : raw_data.get("sys", {}).get("country"),
        "Condition"   : raw_data.get("weather", [{}])[0].get("description"),
        "Temp_K"      : raw_data.get("main", {}).get("temp"),
        "Feels_Like_K": raw_data.get("main", {}).get("feels_like"),
        "Humidity"    : raw_data.get("main", {}).get("humidity")
   }

   clean_data = {}
   
   for key, value in filtered_data.items():

    if value is not None and "_K" in key:

        new_key = key.replace("_K", "_C")

        clean_data[new_key] = round(value - 273.15, 2)
    else:

        clean_data[key] = value
    
    
   return clean_data


transformed_data = transform_weather()

df = pd.DataFrame([transformed_data])

print(df)



