import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Global cache to store URLs of car listings
cache = set()

# Initialize the Chrome driver outside of the function to keep it alive
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def fetch_page_content(url):
    """Fetches the content of the page."""
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("Successfully connected to the website. Status code:",
              driver.execute_script("return document.readyState;"))
        return driver.page_source
    except Exception as e:
        print(f"An error occurred while fetching the page content: {e}")
        return None


def populate_cache(page_content):
    """Populates the cache with URLs from the page content."""
    try:
        car_listings = driver.find_elements(By.CSS_SELECTOR, '.cldt-summary-full-item')  # Update the selector
        for listing in car_listings:
            car_url = listing.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if car_url in cache:
                print("Found a duplicate URL in the cache. Stopping the process.")
                return False
            else:
                cache.add(car_url)
                print(f"Added URL to cache: {car_url}")
        print("All unique URLs have been added to the cache.")
        return True
    except Exception as e:
        print(f"An error occurred while populating the cache: {e}")
        return False


def check_url():
    """Coordinates fetching the page content and populating the cache."""
    url = 'https://www.autoscout24.com/lst?atype=C&body=3&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=1&doorfrom=2&doorto=3&fregfrom=2000&fregto=2014&fuel=B&gear=M&powerfrom=132&powertype=hp&priceto=12500&search_id=d8i3umblu0&sort=age&source=detailsearch&ustate=N%2CU'
    page_content = fetch_page_content(url)
    if page_content:
        return populate_cache(page_content)
    return False


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
