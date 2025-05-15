import requests
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
client = gspread.authorize(creds)

# Open the spreadsheet and worksheet
sheet = client.open("Hood Cleaning Leads").worksheet("Louisville, KY")

# --- Google Places API Setup ---
API_KEY = "YOUR_GOOGLE_PLACES_API_KEY"
LOCATION = "Louisville, KY"
SEARCH_TERM = "restaurants"

url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
params = {
    "query": f"{SEARCH_TERM} in {LOCATION}",
    "key": API_KEY
}

# --- Scrape and Push to Google Sheets ---
results = []
while True:
    response = requests.get(url, params=params)
    data = response.json()

    for place in data.get("results", []):
        name = place.get("name", "")
        address = place.get("formatted_address", "")
        place_id = place.get("place_id", "")

        # Get phone number using details endpoint
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        details_params = {
            "place_id": place_id,
            "fields": "formatted_phone_number",
            "key": API_KEY
        }
        phone_data = requests.get(details_url, params=details_params).json()
        phone = phone_data.get("result", {}).get("formatted_phone_number", "")

        # Try to extract city/state/zip if possible (you can improve this with regex or better parsing)
        city = "Louisville"
        state = "KY"
        zip_code = ""

        row = [name, phone, address, city, state, zip_code, "", "", ""]
        sheet.append_row(row)
        print(f"Added: {name}")

    if "next_page_token" in data:
        time.sleep(2)
        params["pagetoken"] = data["next_page_token"]
    else:
        break

print("✅ Done scraping and saving to Google Sheets.")
