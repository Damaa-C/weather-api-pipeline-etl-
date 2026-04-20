import pandas as pd
from extract import data


def transform_weather(data):

   weather_data = [{
        "City"        : data.get("name"),
        "Country"     : data.get("sys", {}).get("country"),
        "Condition"   : data.get("weather", [{}])[0].get("description"),
        "Temp_K"      : data.get("main", {}).get("temp"),
        "Feels_Like_K": data.get("main", {}).get("feels_like"),
        "Humidity"    : data.get("main", {}).get("humidity")
   }]

   df = pd.DataFrame(weather_data)

   df["Temp_C"] = (df["Temp_K"] - 273.15).round(2)

   df["Feels_Like_C"] = (df["Feels_Like_K"] - 273.15).round(2)

   df = df.drop(columns=["Temp_K", "Feels_Like_K"])

   df["Condition"] = df["Condition"].str.title()

   return df

   
transformed_df = transform_weather(data)

print(transformed_df)



