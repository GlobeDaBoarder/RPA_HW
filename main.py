import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cache = set()

def check_url():
    url = 'https://www.autoscout24.com/lst?atype=C&body=3&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=1&doorfrom=2&doorto=3&fregfrom=2000&fregto=2014&fuel=B&gear=M&powerfrom=132&powertype=hp&priceto=12500&search_id=d8i3umblu0&sort=age&source=detailsearch&ustate=N%2CU'

    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    try:
        driver.get(url)

        # Wait until the document is ready
        WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        print("Successfully connected to the website. Status code:",
              driver.execute_script("return document.readyState;"))

        # Find all car listing elements (update the selector as needed)
        car_listings = driver.find_elements(By.CSS_SELECTOR, '.cldt-summary-full-item')  # Update the selector

        for listing in car_listings:
            # Extract the URL of each listing (update the attribute as needed)
            car_url = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Check if the URL is already in the cache
            if car_url in cache:
                print("Found a duplicate URL in the cache. Stopping the process.")
                break
            else:
                # Add the new URL to the cache
                cache.add(car_url)
                print(f"Added URL to cache: {car_url}")

        print("All unique URLs have been added to the cache.")
    finally:
        driver.quit()


if __name__ == "__main__":
    while True:
        check_url()
        time.sleep(5)
