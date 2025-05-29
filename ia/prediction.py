import requests
import os

MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_TOKEN")

def predict_ride(depart, arrivee):
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{depart[1]},{depart[0]};{arrivee[1]},{arrivee[0]}"
    params = {
        "access_token": MAPBOX_ACCESS_TOKEN,
        "overview": "simplified",
        "geometries": "geojson"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200 or not data['routes']:
        return {"error": "Aucune route trouvée."}

    route = data['routes'][0]
    distance_km = route['distance'] / 1000  # mètres → km
    duration_min = route['duration'] / 60   # secondes → minutes

    # Formule simple de coût : base 2€, +1.5€/km, +0.5€/min
    cost = 2 + 1.5 * distance_km + 0.5 * duration_min

    return {
        "distance_km": round(distance_km, 2),
        "duration_min": round(duration_min, 1),
        "estimated_cost": round(cost, 2)
    }
