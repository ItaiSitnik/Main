import json
import os
from itertools import permutations

import folium
import openrouteservice
from geopy.geocoders import Nominatim

# Your OpenRouteService API key
ORS_API_KEY = "5b3ce3597851110001cf6248254c8a63bf4c412793fc4d9f7079e78f"
CACHE_FILE = "2025_H1/gps_cache.json"

# Addresses
addresses = {
    "Sit": "הספורט 12, חיפה",
    # "Blam": "בית אל 9, חיפה",
    # "Jonch": "אידר 43, חיפה",
    # "Gersh": "דרך הים 137, חיפה",
    # "Technion": 'מל"ל 20, חיפה',
    "Tal": "גדליהו 33, חיפה",
    # "Boga": "אבא הלל סילבר 111, חיפה",
    # "Sister Gersh": "רבין 9, קרית אתא",
    "Tama": "הלל 20, חיפה",
    # "Mai": "R. do Bruxo 36, Portugal",
    # "Bottom": "נתנזון 20, חיפה",
    "Ilya": "נחל שורק 19, יקנעם",
    "Yoni": "סורוקה 42, חיפה",
    "Rawi": "תדהר 9, ורדיה, חיפה",
}

start_name = "Ilya"
end_name = "Yoni"

# Initialize geocoder and client
geolocator = Nominatim(user_agent="haifa_map_app")
client = openrouteservice.Client(key=ORS_API_KEY)
haifa_map = folium.Map(location=(32.81, 34.9896), zoom_start=14)


# --- Caching Logic Start ---
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(cache_data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=4)


# Load existing cache
gps_cache = load_cache()
# --- Caching Logic End ---

# Geocode and place markers
coords = {}
for name, address in addresses.items():
    # Check if address is already in cache
    if address in gps_cache:
        print(f"Using cached location for {name}")
        latlon = tuple(gps_cache[address])
    else:
        # Not in cache, query the API
        print(f"Geocoding {name} from API...")
        location = geolocator.geocode(address)

        if not location:
            print(f"Failed for name {name}, address {address}")
            continue  # Skip to next address if not found

        latlon = (location.latitude, location.longitude)

        # Update cache and save immediately
        gps_cache[address] = latlon
        save_cache(gps_cache)

    coords[name] = latlon
    folium.Marker(latlon, popup=f"{name}: {address}", tooltip=address).add_to(haifa_map)

keys = list(coords.keys())
n = len(keys)

# Coordinates in (lon, lat) format
coords_list = [coords[k][::-1] for k in keys]

matrix = client.distance_matrix(
    locations=coords_list,
    profile="driving-car",
    metrics=["duration"],
    units="m",  # meters and minutes
    resolve_locations=True,
)

# matrix["durations"] is a 2D list of driving times in seconds
dist_matrix = [[duration / 60 for duration in row] for row in matrix["durations"]]


# For storing the overall best path info
overall_best_path = None
overall_best_time = float("inf")
overall_best_start = None

print("\nAll possible paths for each possible starting point:")

# Try each location as a start
for start in range(n):
    others = [i for i in range(n) if i != start]
    print(f"\nStarting at {keys[start]}:")
    best_path_for_start = None
    best_time_for_start = float("inf")

    for perm in permutations(others):
        path = [start] + list(perm)
        total_time = sum(dist_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))
        # Optional: Print every single permutation (can be spammy if N is large)
        # path_names = " → ".join(keys[i] for i in path)
        # print(f"{path_names}: {total_time:.1f} min")

        if total_time < best_time_for_start:
            best_time_for_start = total_time
            best_path_for_start = path

    print(f"Best path for start {keys[start]}: {best_time_for_start:.1f} min")

    # Update overall best path if better
    if best_time_for_start < overall_best_time:
        overall_best_time = best_time_for_start
        overall_best_path = best_path_for_start
        overall_best_start = start

# Print overall best path info
print("\nOverall shortest path (any start):")
print("Start at", keys[overall_best_start])
print(" → ".join(keys[i] for i in overall_best_path))
print(f"Total driving time: {overall_best_time:.1f} minutes")

# Draw the overall best path on the map in red
for i in range(len(overall_best_path) - 1):
    start_coord = coords[keys[overall_best_path[i]]]
    end_coord = coords[keys[overall_best_path[i + 1]]]
    route = client.directions(
        coordinates=[start_coord[::-1], end_coord[::-1]],
        profile="driving-car",
        format="geojson",
    )
    route_coords = route["features"][0]["geometry"]["coordinates"]
    route_latlon = [(lat, lon) for lon, lat in route_coords]
    folium.PolyLine(
        locations=route_latlon,
        color="red",
        weight=4,
        opacity=0.8,
        tooltip=f"{keys[overall_best_path[i]]} → {keys[overall_best_path[i + 1]]}",
    ).add_to(haifa_map)

# Save the map
haifa_map.save("2025_H1/haifa_tsp_any_start_path.html")

# Sort specific start/end paths
if start_name in keys and end_name in keys:
    start_idx = keys.index(start_name)
    end_idx = keys.index(end_name)

    middle_indices = [i for i in range(n) if i not in (start_idx, end_idx)]

    paths_with_times = []
    for perm in permutations(middle_indices):
        path = [start_idx] + list(perm) + [end_idx]
        total_time = sum(dist_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))
        paths_with_times.append((total_time, path))

    paths_with_times.sort()

    print(f"\nAll paths from '{start_name}' to '{end_name}' sorted by total time:")
    num_paths = len(paths_with_times)

    if num_paths <= 14:
        # If list is short, print everything
        for total_time, path in paths_with_times:
            path_names = " → ".join(keys[i] for i in path)
            print(f"{path_names}: {total_time:.1f} min")
    else:
        # Print first 7
        for total_time, path in paths_with_times[:7]:
            path_names = " → ".join(keys[i] for i in path)
            print(f"{path_names}: {total_time:.1f} min")

        print("...")

        # Print last 7
        for total_time, path in paths_with_times[-7:]:
            path_names = " → ".join(keys[i] for i in path)
            print(f"{path_names}: {total_time:.1f} min")
else:
    print(f"\nCould not run specific start/end sort: {start_name} or {end_name} not found in valid coordinates.")
