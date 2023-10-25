from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

from windows import buff_sql

driver = webdriver.Chrome(service=Service(r'webdriver/chromedriver.exe'))
driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=1&category=csgo_type_musickit')
time.sleep(30)
page = 2
while page < 8:
    try:
        element = driver.find_element(By.ID, "j_market_card")
        elements = element.find_elements(By.TAG_NAME, "li")
        for li in elements:
            try:
                url = li.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]
                if 'page' not in url:
                    goods_id = url.split("/")[-1]
                    all_goods_id = buff_sql.get_all_goods_id()
                    if goods_id not in all_goods_id:
                        print(goods_id)
            except Exception:
                time.sleep(1)
        for element in driver.find_elements(By.CLASS_NAME, "page-link"):
            if element.text == str(page):
                element.click()
                break

    except NoSuchElementException:
        time.sleep(10)
        element = driver.find_element(By.ID, "j_market_card")
        elements = element.find_elements(By.TAG_NAME, "li")
        for li in elements:
            try:
                url = li.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]
                if 'page' not in url:
                    goods_id = url.split("/")[-1]
                    all_goods_id = buff_sql.get_all_goods_id()
                    if goods_id not in all_goods_id:
                        print(goods_id)
            except Exception:
                time.sleep(1)
        for element in driver.find_elements(By.CLASS_NAME, "page-link"):
            if element.text == str(page):
                element.click()
                break

    time.sleep(10)
    page = page + 1
