import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import telepot
import json


# Global cache to store URLs of car listings
cache = {}

# Initialize the Chrome driver outside of the function to keep it alive
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def send_telegram_message(text):
    token = '6996244061:AAHZNbYgCIo-Tjx8DrAK-SPxZfGHLaEpWak'
    chat_id = '407569859'
    bot = telepot.Bot(token)
    bot.sendMessage(chat_id=chat_id, text=text)


def save_cache():
    try:
        with open('car_cache.json', 'w') as f:
            json.dump(cache, f, indent=4)
        print("Cache saved successfully.")
    except IOError as e:
        print(f"Failed to save cache: {e}")
    except TypeError as e:
        print(f"Data type not serializable: {e}")


def load_cache():
    try:
        with open('car_cache.json', 'r') as f:
            global cache
            cache = json.load(f)
        print("Cache loaded successfully.")
    except FileNotFoundError:
        print("No cache file found. Starting with an empty cache.")


def establish_driver_connection(url):
    """Fetches the content of the page."""
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("Successfully connected to the website. Status code:",
              driver.execute_script("return document.readyState;"))
        return True
    except Exception as e:
        print(f"An error occurred while fetching the page content: {e}")
        return False


def retrieve_car_listing():
    return driver.find_elements(By.CSS_SELECTOR, '.cldt-summary-full-item')


def populate_cache():
    """Populates the cache with car data from the page content."""
    is_something_added_or_updated = False
    try:
        car_listings = retrieve_car_listing()
        for listing in car_listings:
            car_url = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
            car_details = {
                'name': listing.find_element(By.CSS_SELECTOR, 'h2').text,
                'price': listing.find_element(By.CSS_SELECTOR, 'p.Price_price__APlgs').text,
                'mileage': listing.find_element(By.CSS_SELECTOR, '[data-testid="VehicleDetails-mileage_road"]').text,
                'registration_date': listing.find_element(By.CSS_SELECTOR,
                                                          '[data-testid="VehicleDetails-calendar"]').text,
                'horsepower': listing.find_element(By.CSS_SELECTOR, '[data-testid="VehicleDetails-speedometer"]').text
            }

            if car_url in cache:
                if cache[car_url] != car_details:
                    is_something_added_or_updated = True
                    cache[car_url] = car_details
                    update_message = f"Updated {car_details['name']} in cache: {car_url} with new details: {car_details}"
                    print(update_message)
                    send_telegram_message(update_message)
                else:
                    print(f"No changes detected for {car_url}.")
            else:
                is_something_added_or_updated = True
                cache[car_url] = car_details
                addition_message = f"Added {car_details['name']} to cache: {car_url} with details: {car_details}"
                print(addition_message)
                send_telegram_message(addition_message)

        if is_something_added_or_updated:
            save_cache()

        print("Reviewing cars in the page done")
    except Exception as e:
        print(f"An error occurred while populating the cache: {e}")


def check_url():
    """Coordinates fetching the page content and populating the cache with pagination handling."""
    base_url = 'https://www.autoscout24.com/lst/toyota?atype=C&body=3&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=1&doorfrom=2&doorto=3&fregfrom=2000&fregto=2014&fuel=B&gear=M&mmmv=52%7C%7C%7C&powerfrom=132&powertype=hp&priceto=20000&search_id=r5u8n2wic8&sort=age&source=listpage_pagination&ustate=N%2CU&page='
    page_number = 1

    while True:
        url = f"{base_url}{page_number}"
        if not establish_driver_connection(url):
            return False

        car_listings = retrieve_car_listing()
        if not car_listings:
            print("No more listings found on page", page_number)
            return True

        populate_cache()

        page_number += 1
        print(f"Moving to page {page_number}")


def main():
    try:
        load_cache()
        while True:
            if not check_url():
                break
            time.sleep(10)  # Wait for 5 seconds before the next call
    finally:
        driver.quit()  # Ensure the driver is quit when the script ends


if __name__ == "__main__":
    main()
