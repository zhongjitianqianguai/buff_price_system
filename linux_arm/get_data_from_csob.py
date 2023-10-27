from seleniumwire import webdriver
from selenium.common import NoSuchElementException, WebDriverException, NoSuchWindowException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from linux_arm import buff_sql

options = Options()
# 去掉"chrome正受到自动化测试软件的控制"的提示条
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--no-sandbox")
options.add_argument("--lang=zh_CN")
browser = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
# browser = webdriver.Chrome(service=Service('../windows/webdriver/chromedriver.exe'), options=options)

browser.set_page_load_timeout(300)

all_names = buff_sql.get_all_goods_name()

for name in all_names:
    browser.get('https://www.csgoob.com/goods?name=' + name)
    for request in browser.requests:
        if 'chart' in str(request):
            print(request.response.body)
            break

