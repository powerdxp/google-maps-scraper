import requests
import csv

API_KEY = "AIzaSyC4bDmD_Kf3o0M2XUvFNBeEgRGCvc91LAI"  # <-- Replace with your actual API key
LOCATION = "Louisville, KY"
SEARCH_TERM = "restaurants"
OUTPUT_FILE = "restaurants_louisville.csv"

# Google Maps Places API endpoint
url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

params = {
    "query": f"{SEARCH_TERM} in {LOCATION}",
    "key": API_KEY
}

results = []
while True:
    response = requests.get(url, params=params)
    data = response.json()

    for place in data.get("results", []):
        name = place.get("name")
        address = place.get("formatted_address")
        place_id = place.get("place_id")

        # Optional: get phone number using a details API call
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            "place_id": place_id,
            "fields": "formatted_phone_number",
            "key": API_KEY
        }
        phone_response = requests.get(details_url, params=details_params).json()
        phone = phone_response.get("result", {}).get("formatted_phone_number", "")

        results.append([name, address, phone])

    # Pagination handling
    if "next_page_token" in data:
        import time
        time.sleep(2)  # Wait for token to become active
        params["pagetoken"] = data["next_page_token"]
    else:
        break

# Save results to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Address", "Phone"])
    writer.writerows(results)

print(f"Saved {len(results)} restaurants to {OUTPUT_FILE}")
