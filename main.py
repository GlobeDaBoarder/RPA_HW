from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def check_url():
    url = 'https://en.autoplius.lt/ads/used-cars?make_id_list=&engine_capacity_from=&engine_capacity_to=&power_from=&power_to=&kilometrage_from=&kilometrage_to=&has_damaged_id=&condition_type_id=&make_date_from=2000&make_date_to=2014&sell_price_from=&sell_price_to=20000&fuel_id%5B30%5D=30&body_type_id%5B1%5D=1&co2_from=&co2_to=&euro_id=&fk_place_countries_id=&qt=&number_of_doors_id=&gearbox_id=37&steering_wheel_id=&is_partner=&older_not=&save_search=1&slist=2294798814&category_id=2&order_by=3&order_direction=DESC'

    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        print("Successfully connected to the website. Status code:", driver.execute_script("return document.readyState;"))

        # Print the page source (HTML content)
        print(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    check_url()
