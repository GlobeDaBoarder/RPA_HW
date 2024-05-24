import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Global cache to store URLs of car listings
cache = {}

# Initialize the Chrome driver outside of the function to keep it alive
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


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
                print("Found a duplicate URL in the cache. Stopping the process.")
                return False
            else:
                cache[car_url] = car_details
                print(f"Added car to cache: {car_url} with details: {car_details}")
        print("All unique car details have been added to the cache.")
        return True
    except Exception as e:
        print(f"An error occurred while populating the cache: {e}")
        return False


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

        has_new_content = populate_cache()
        if not has_new_content:
            print("Duplicate found. Stopping the process.")
            return False

        page_number += 1
        print(f"Moving to page {page_number}")


def main():
    try:
        while True:
            if not check_url():
                break
            time.sleep(5)  # Wait for 5 seconds before the next call
    finally:
        driver.quit()  # Ensure the driver is quit when the script ends
        # Print all entries in the cache


if __name__ == "__main__":
    main()
