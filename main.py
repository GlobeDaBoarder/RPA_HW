from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


        print("Successfully connected to the website. Status code:", driver.execute_script("return document.readyState;"))

        # Print the page source (HTML content)
        print(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    check_url()
