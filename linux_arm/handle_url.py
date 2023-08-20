from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

with open('../source/all.txt') as f:
    urls = f.readlines()

results = set()
with open('../source/all.txt', 'w') as f:
    for url in urls:
        if 'page' not in url and url not in results:
            f.write(url)
            results.add(url)
        else:
            print("删除了："+url)

print('all.txt去重更新完成!')
