import smtplib

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(r'../windows/webdriver/chromedriver.exe'))
# driver.get(
#     'https://buff.163.com/market/csgo#tab=selling&page_num=1&category_group=type_customplayer')
#
# time.sleep(30)
# index = 2
# while index < 6:
#     try:
#         element = driver.find_element(By.ID, "j_market_card")
#         elements = element.find_elements(By.TAG_NAME, "li")
#         for li in elements:
#             try:
#                 url = li.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]
#                 if 'page' not in url:
#                     print(url)
#             except Exception:
#                 time.sleep(1)
#         if index < 5:
#             driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index) + '&category_group=type_customplayer')
#             driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index) + '&category_group=type_customplayer')
#     except NoSuchElementException:
#         time.sleep(10)
#         element = driver.find_element(By.ID, "j_market_card")
#         elements = element.find_elements(By.TAG_NAME, "li")
#         for li in elements:
#             try:
#                 url = li.find_element(By.TAG_NAME, "a").get_attribute("href").split("?")[0]
#                 if 'page' not in url:
#                     print(url)
#             except Exception:
#                 time.sleep(1)
#         driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index) + '&category_group=type_customplayer')
#         driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index) + '&category_group=type_customplayer')
#     time.sleep(10)
#     index = index + 1

driver.get(
    'https://buff.163.com/market/csgo#tab=selling&page_num=1&search=%E6%AD%A6%E5%99%A8%E7%AE%B1')
driver.get(
    'https://buff.163.com/market/csgo#tab=selling&page_num=1&search=%E6%AD%A6%E5%99%A8%E7%AE%B1')
print('武器箱')
time.sleep(30)
index = 2
while index <4:
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
        if index < 3:
            driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index) + '&search=%E6%AD%A6%E5%99%A8%E7%AE%B1')
            driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index) + '&search=%E6%AD%A6%E5%99%A8%E7%AE%B1')
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
        driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index) + '&category=csgo_type_weaponcase')
        driver.get('https://buff.163.com/market/csgo#tab=selling&page_num=' + str(index) + '&category=csgo_type_weaponcase')
    time.sleep(10)
    index = index + 1
