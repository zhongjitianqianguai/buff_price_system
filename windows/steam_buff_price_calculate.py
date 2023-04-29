import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(r'webdriver\chromedriver.exe'))
driver.implicitly_wait(10)
with open('../all.txt') as f:
    urls = f.readlines()
difference = {}

for url in urls:
    driver.get(url)
    time.sleep(3)
    while True:
        price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
        on_sale_count = driver.find_element(By.CLASS_NAME, "new-tab").text.split("在售")[1].split(")")[0].replace(
            "(", "").replace("+", "")
        if int(on_sale_count) < 100:
            break
        if len(price_elements) > 1:
            steam_price = price_elements[0]
            lowest_price = price_elements[1]
            if float(lowest_price.text.replace("¥ ", "")) > 100:
                break
            different = float(lowest_price.text.replace("¥ ", "")) - float(
                steam_price.text.replace("¥ ", "")) / 0.15
            difference[url] = different
            break
    time.sleep(5)
the_best_url = ''
price_difference = 0
for di in difference:
    if difference[di] > price_difference:
        the_best_url = di
        price_difference = difference[di]
print(the_best_url + ":" + str(price_difference))
