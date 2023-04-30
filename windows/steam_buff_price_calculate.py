import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(r'webdriver\chromedriver.exe'))
driver.implicitly_wait(60)
with open('../all.txt') as f:
    urls = f.readlines()
difference = {}
need_price = 200
get_200 = {}
for url in urls:
    try:
        driver.get('https://buff.163.com/goods/' + url)
        start_time = datetime.datetime.utcnow()

        time.sleep(4)
        while True:
            price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
            on_sale_count = driver.find_element(By.CLASS_NAME, "new-tab").text.split("在售")[1].split(")")[0].replace(
                "(", "").replace("+", "")
            now_time = datetime.datetime.utcnow()
            if (now_time - start_time).seconds > 30:
                print("超时")
                driver.refresh()
                continue
            if int(on_sale_count) < 100:
                break
            if len(price_elements) > 1:
                steam_price = price_elements[0]
                lowest_price = price_elements[1]
                if float(lowest_price.text.replace("¥ ", "")) > 100:
                    break
                steam = float(steam_price.text.replace("¥ ", "").split("(")[0])
                different = steam + steam * 0.15 - float(lowest_price.text.replace("¥ ", ""))
                difference[url] = different
                amount = need_price / (steam - steam * 0.15)
                if not isinstance(amount, int):
                    amount = int(amount) + 1
                print("需要在steam售出：" + str(amount))
                need_buff_price = amount * float(lowest_price.text.replace("¥ ", ""))
                print("在buff上购买此数量需要价格：" + str(need_buff_price))
                get_200[url] = need_buff_price
                print(url + ":" + str(different))
                break
    except Exception as e:
        print(e)
        time.sleep(10)
        driver.refresh()
        continue
the_best_url = ''
price_difference = 0
for di in difference:
    if difference[di] > price_difference:
        the_best_url = di
        price_difference = difference[di]
print(the_best_url + ":" + str(price_difference))
the_lowest_url = ''
lowest = 200
print(sorted(get_200.items(), key=lambda kv: (kv[1], kv[0])))
