import requests
import csv
import os

SAVE_PATH = "/Users/beratzengin/Desktop/Github/EcoAir SmartCity Predictor/Data"
STATIONS_URL = "https://api.ibb.gov.tr/havakalitesi/OpenDataPortalHandler/GetAQIStations"

def run_station_metadata_ingestion():
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    try:
        response = requests.get(STATIONS_URL, timeout=15)
        
        if response.status_code == 200:
            stations_data = response.json()
            output_file = os.path.join(SAVE_PATH, "stations_info.csv")
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                # Field names based on official documentation
                writer = csv.DictWriter(f, fieldnames=['Id', 'Name', 'Adress', 'Location'])
                writer.writeheader()
                writer.writerows(stations_data)
                
            print(f"Metadata ingestion successful: {len(stations_data)} stations saved.")
        else:
            print(f"API Error: {response.status_code}")
            
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    run_station_metadata_ingestion()