import requests
from time import sleep

def check_url():
    url = 'https://www.autoscout24.com/lst?atype=C&body=3&cy=D%2CA%2CB%2CE%2CF%2CI%2CL%2CNL&damaged_listing=exclude&desc=1&doorfrom=2&doorto=3&fregfrom=2000&fregto=2014&fuel=B&gear=M&powerfrom=132&powertype=hp&priceto=12500&search_id=d8i3umblu0&sort=age&source=detailsearch&ustate=N%2CU'

    response = requests.get(url)

    if response.status_code == 200:
        print("Successfully connected to the website. Status code:", response.status_code)
        print(response.text)
    else:
        print("Failed to connect. Status code:", response.status_code)

if __name__ == "__main__":
    check_url()
