import requests
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Auth ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/app/credentials/gcreds.json", scope)
client = gspread.authorize(creds)

# --- Open Your Sheet ---
sheet = client.open("Hood Cleaning Leads").worksheet("Louisville, KY")

# --- API Setup ---
API_KEY = "AIzaSyC4bDmD_Kf3o0M2XUvFNBeEgRGCvc91LAI"  # Replace if you ever rotate your key
LOCATION = "Louisville, KY"
SEARCH_TERM = "restaurants"

url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
params = {
    "query": f"{SEARCH_TERM} in {LOCATION}",
    "key": API_KEY
}

# --- Scrape + Send ---
print("Starting scrape...")

seen = set()
while True:
    response = requests.get(url, params=params)
    data = response.json()

    for place in data.get("results", []):
        name = place.get("name", "")
        address = place.get("formatted_address", "")
        place_id = place.get("place_id", "")

        # Get phone number
        phone_url = "https://maps.googleapis.com/maps/api/place/details/json"
        phone_params = {
            "place_id": place_id,
            "fields": "formatted_phone_number",
            "key": API_KEY
        }
        phone_data = requests.get(phone_url, params=phone_params).json()
        phone = phone_data.get("result", {}).get("formatted_phone_number", "")

        # Check for duplicates
        if (name, address) in seen:
            continue
        seen.add((name, address))

        # Parse city/state/zip
        city = "Louisville"
        state = "KY"
        zip_code = ""

        # Sheet Format
        row = [name, phone, address, city, state, zip_code, "", "", ""]
        sheet.append_row(row)
        print(f"✅ Added: {name}")

    if "next_page_token" in data:
        time.sleep(2)
        params["pagetoken"] = data["next_page_token"]
    else:
        break

print("✅ Done scraping and saving to Google Sheets.")
