import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import os
import re

session = requests_cache.CachedSession('.cache', expire_after=-1)
retry_session = retry(session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

BASE_PATH = "/Users/beratzengin/Desktop/Github/EcoAir SmartCity Predictor/Data"
STATIONS_CSV = os.path.join(BASE_PATH, "stations_info.csv")

def extract_coordinates(location_str):
    match = re.search(r'\((.*?)\)', location_str)
    if match:
        coords = match.group(1).split(' ')
        return float(coords[1]), float(coords[0])
    return None, None

def run_weather_ingestion():
    if not os.path.exists(STATIONS_CSV):
        return
    
    stations_df = pd.read_csv(STATIONS_CSV)
    api_url = "https://archive-api.open-meteo.com/v1/archive"

    for _, row in stations_df.iterrows():
        folder_name = row['Name'].replace(" ", "_").replace("/", "-")
        target_dir = os.path.join(BASE_PATH, folder_name)
        if not os.path.exists(target_dir): 
            os.makedirs(target_dir)

        lat, lon = extract_coordinates(row['Location'])
        
        query_params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "wind_direction_10m"]
        }

        try:
            responses = openmeteo.weather_api(api_url, params=query_params)
            res = responses[0]
            hourly_meta = res.Hourly()
            
            data = {
                "timestamp": pd.date_range(
                    start=pd.to_datetime(hourly_meta.Time(), unit="s", utc=True),
                    end=pd.to_datetime(hourly_meta.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=hourly_meta.Interval()),
                    inclusive="left"
                ),
                "temp": hourly_meta.Variables(0).ValuesAsNumpy(),
                "humidity": hourly_meta.Variables(1).ValuesAsNumpy(),
                "wind_speed": hourly_meta.Variables(2).ValuesAsNumpy(),
                "wind_direction": hourly_meta.Variables(3).ValuesAsNumpy()
            }

            df = pd.DataFrame(data=data)
            df.to_csv(os.path.join(target_dir, "weather_2024.csv"), index=False)
            print(f"Ingested: {folder_name}")

        except Exception as e:
            print(f"Error at {folder_name}: {e}")

if __name__ == "__main__":
    run_weather_ingestion()