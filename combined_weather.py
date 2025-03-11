from datetime import datetime, timedelta
import os
import json
from meteostat import Stations, Daily
import math
import pandas as pd

locations = {
    "Texas": (30.2672, -97.7431),       
    "New York": (40.7128, -74.0060),    
    "Kentucky": (38.2527, -85.7585),     
    "Georgia": (33.7490, -84.3880)      
}


end_date = datetime.today() - timedelta(days=1)
start_date = end_date - timedelta(days=364)
desired_keys = ["tavg", "tmin", "tmax", "prcp", "wdir", "wspd", "pres"]

final_data = {}

for state, (lat, lon) in locations.items():
    
    stations = Stations().nearby(lat, lon)
    station = stations.fetch(1)  
    station_id = station.index[0]
    data = Daily(station_id, start_date, end_date)
    df = data.fetch()
    
    state_dict = {}
    for date, row in df.iterrows():
        cleaned_row = {}
        for key in desired_keys:
            if key in row and not (isinstance(row[key], float) and math.isnan(row[key])):
                cleaned_row[key] = row[key]
        state_dict[str(date.date())] = cleaned_row
    final_data[state] = state_dict

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
if not os.path.isdir(desktop_path):
    desktop_path = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
if not os.path.isdir(desktop_path):
    raise Exception("Desktop folder not found in expected locations.")


file_path = os.path.join(desktop_path, "states_weather_history_meteostat.json")

with open(file_path, "w") as file:
    json.dump(final_data, file, indent=4)


