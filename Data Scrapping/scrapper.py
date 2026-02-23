import requests
import csv
import os
import time

# --- CONFIGURATION ---
SAVE_PATH = "/Users/beratzengin/Desktop/Github/EcoAir SmartCity Predictor/Data"
STATIONS_URL = "https://api.ibb.gov.tr/havakalitesi/OpenDataPortalHandler/GetAQIStations"
DATA_URL = "https://api.ibb.gov.tr/havakalitesi/OpenDataPortalHandler/GetAQIByStationId"

def fetch_complete_2024():
    if not os.path.exists(SAVE_PATH): os.makedirs(SAVE_PATH)
    
    s_res = requests.get(STATIONS_URL)
    if s_res.status_code != 200: return
    stations = s_res.json()
    
    months = [
        ("01.01.2024 00:00:00", "01.02.2024 00:00:00", "01"),
        ("01.02.2024 00:00:00", "01.03.2024 00:00:00", "02"),
        ("01.03.2024 00:00:00", "01.04.2024 00:00:00", "03"),
        ("01.04.2024 00:00:00", "01.05.2024 00:00:00", "04"),
        ("01.05.2024 00:00:00", "01.06.2024 00:00:00", "05"),
        ("01.06.2024 00:00:00", "01.07.2024 00:00:00", "06"),
        ("01.07.2024 00:00:00", "01.08.2024 00:00:00", "07"),
        ("01.08.2024 00:00:00", "01.09.2024 00:00:00", "08"),
        ("01.09.2024 00:00:00", "01.10.2024 00:00:00", "09"),
        ("01.10.2024 00:00:00", "01.11.2024 00:00:00", "10"),
        ("01.11.2024 00:00:00", "01.12.2024 00:00:00", "11"),
        ("01.12.2024 00:00:00", "01.01.2025 00:00:00", "12")
    ]

    for s in stations:
        s_id = s['Id']
        s_name = s['Name'].replace(" ", "_").replace("/", "-")
        station_dir = os.path.join(SAVE_PATH, s_name)
        if not os.path.exists(station_dir): os.makedirs(station_dir)
        
        print(f"\n>>> {s_name} Checking...")
        
        for start, end, m_name in months:
            file_path = os.path.join(station_dir, f"{m_name}_2024.csv")
            
            if os.path.exists(file_path) and os.path.getsize(file_path) > 100:
                print(f"  - {m_name}. allready have, passing.")
                continue
            
            payload = {"StationId": s_id, "StartDate": start, "EndDate": end}
            try:
                res = requests.get(DATA_URL, params=payload, timeout=30)
                if res.status_code == 200:
                    data = res.json()
                    if data:
                        with open(file_path, 'w', newline='', encoding='utf-8') as f:
                            writer = csv.writer(f)
                            writer.writerow(['ReadTime', 'Concentration', 'AQI'])
                            for entry in data:
                                writer.writerow([entry.get('ReadTime'), entry.get('Concentration'), entry.get('AQI')])
                        print(f"  + {m_name}. month downloaded ({len(data)} lines)")
                time.sleep(0.5) 
            except Exception as e:
                print(f"  ! Error ({m_name}. month): {e}")

if __name__ == "__main__":
    fetch_complete_2024()