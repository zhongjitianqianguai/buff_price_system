import smtplib

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(r'chromedriver.exe'))
driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=1&category_group=knife')
driver.implicitly_wait(10)
time.sleep(100)
index = 2
while True:
    try:
        element = driver.find_element(By.ID, "j_market_card")
        elements = element.find_elements(By.TAG_NAME, "li")

        for li in elements:
            try:
                url = li.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]
                if 'page' not in url:
                    print(url)
            except Exception:
                time.sleep(1)
        driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index)+"&category_group=knife")
        driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index)+"&category_group=knife")
    except NoSuchElementException:
        time.sleep(10)
        element = driver.find_element(By.ID, "j_market_card")
        elements = element.find_elements(By.TAG_NAME, "li")
        for li in elements:
            try:
                url = li.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]
                if 'page' not in url:
                    print(url)
            except Exception:
                time.sleep(1)
        driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index))
        driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index))
    time.sleep(5)
    index = index + 1
#获取单个的url