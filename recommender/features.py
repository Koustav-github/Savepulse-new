import pandas as pd
import numpy as np
import requests
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def get_osrm_distances(req_lat, req_lon, df_hospitals):
    """
    Fetches real road distances for ALL hospitals in one API call.
    Returns a list of distances (km). Falls back to Haversine on error.
    """
    
    coords_list = [f"{req_lon},{req_lat}"] 
    
    for _, row in df_hospitals.iterrows():
        coords_list.append(f"{row['longitude']},{row['latitude']}")
    
    coordinates = ";".join(coords_list)
    
    url = f"http://router.project-osrm.org/table/v1/driving/{coordinates}?sources=0&annotations=distance"
    
    try:
        response = requests.get(url, timeout=3) 
        data = response.json()
        
        if data.get("code") == "Ok":
            return [d / 1000.0 for d in data['distances'][0][1:]]
    except Exception as e:
        print(f"OSRM Error: {e}. Falling back to Haversine.")
    
    return df_hospitals.apply(
        lambda row: haversine(req_lat, req_lon, row['latitude'], row['longitude']), 
        axis=1
    ).tolist()

# --- Scoring Functions ---

def compute_availability(row):
    total_avail = row["icu_beds_available"] + row["general_beds_available"] + row["oxygen_beds_available"]
    return total_avail / row["total_beds"] if row["total_beds"] > 0 else 0

def compute_rating(row):
    return (row["hospital_rating"] / 5) if pd.notna(row["hospital_rating"]) else 0

def compute_facility(row, emergency):
    if emergency == "trauma": return int(row["trauma_center"])
    if emergency == "cardiac": return int(row["cardiac_center"])
    return 1

if __name__ == "__main__":
    data = {
        'latitude': [22.58, 22.55],
        'longitude': [88.35, 88.39],
        'icu_beds_available': [5, 2],
        'general_beds_available': [10, 0],
        'oxygen_beds_available': [2, 1],
        'total_beds': [20, 10],
        'hospital_rating': [4.5, 3.8],
        'trauma_center': [1, 0],
        'cardiac_center': [1, 1]
    }
    hospitals = pd.DataFrame(data)
    
    req_lat, req_lon = 22.57, 88.36
    emergency = "cardiac"

    road_distances = get_osrm_distances(req_lat, req_lon, hospitals)
    hospitals['road_distance_km'] = road_distances
    results = []
    for i, row in hospitals.iterrows():
        dist_score = 1 / (1 + row['road_distance_km'])
        
        final_score = (
            dist_score * 0.4 + 
            compute_availability(row) * 0.3 + 
            compute_rating(row) * 0.2 + 
            compute_facility(row, emergency) * 0.1
        )
        
        results.append({
            "index": i,
            "distance_km": round(row['road_distance_km'], 2),
            "score": round(final_score, 4)
        })

    results = sorted(results, key=lambda x: x['score'], reverse=True)
    print("Ranked Hospitals:", results)