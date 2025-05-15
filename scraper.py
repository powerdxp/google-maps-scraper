# scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

def scrape_google_maps(search_query, max_results=50):
    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.google.com/maps/search/{search_query}")

    time.sleep(5)  # Let results load
    results = []

    for _ in range(max_results):
        listings = driver.find_elements(By.CLASS_NAME, "Nv2PK")

        for item in listings:
            try:
                name = item.find_element(By.CLASS_NAME, "qBF1Pd").text
                address = item.find_element(By.CLASS_NAME, "rllt__details.lqhpac div:nth-child(2)").text
                phone = item.find_element(By.CLASS_NAME, "rllt__details.lqhpac div:nth-child(3)").text
            except Exception:
                continue

            results.append({
                "Name": name,
                "Address": address,
                "Phone": phone
            })

        # Scroll down
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

    driver.quit()

    df = pd.DataFrame(results)
    df.drop_duplicates(inplace=True)
    df.to_csv("restaurants.csv", index=False)
    print("Scrape complete. Saved to restaurants.csv")

if __name__ == "__main__":
    scrape_google_maps("restaurants in Louisville Kentucky")
