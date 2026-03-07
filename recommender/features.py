import numpy as np
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# Haversine distance in km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def compute_distance_score(req_lat, req_lon, hosp_lat, hosp_lon):
    d = haversine(req_lat, req_lon, hosp_lat, hosp_lon)

    return 1 / (1 + d)


def compute_availability(row):

    beds = (
        row["icu_beds_available"]
        + row["general_beds_available"]
        + row["oxygen_beds_available"]
    )

    if row["total_beds"] == 0:
        return 0

    return beds / row["total_beds"]


def compute_rating(row):

    rating = row["hospital_rating"]

    if pd.isna(rating):
        return 0

    return rating / 5


def compute_facility(row, emergency):

    if emergency == "trauma":
        return int(row["trauma_center"])

    if emergency == "cardiac":
        return int(row["cardiac_center"])

    return 1

if __name__ == "__main__":

    import pandas as pd
    import psycopg2

    conn = psycopg2.connect(
        host="localhost",
        database="savepulse",
        user="postgres",
        password="password",
        port=5432
    )

    hospitals = pd.read_sql("SELECT * FROM my_schema.hospitals", conn)

    req_lat = 22.57
    req_lon = 88.36
    emergency = "cardiac"

    row = hospitals.iloc[0]

    print("Distance score:", compute_distance_score(req_lat, req_lon, row["latitude"], row["longitude"]))
    print("Availability:", compute_availability(row))
    print("Rating:", compute_rating(row))
    print("Facility:", compute_facility(row, emergency))