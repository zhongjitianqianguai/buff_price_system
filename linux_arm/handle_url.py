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

print('全息.txt去重更新完成!')
#
#
#
#
#
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("window-size=1024,768")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--shm-size=1024m")
# chrome_options.add_argument("--lang=zh_CN")
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/bin/chromedriver")
# driver.implicitly_wait(10)
#
# with open('全息.txt', 'w') as f:
#     for url in urls:
#         driver.get(url)
#         while True:
#             price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
#             if len(price_elements) > 1:
#                 lowest_price = price_elements[1]
#                 if float(lowest_price.text.replace("¥ ", "")) <= 100:
#                     f.write(url)
#                     print("保留了："+url+lowest_price.text)
#
#                     break
#                 else:
#                     print("删除了："+url+lowest_price.text)
#                     break
#         time.sleep(3)


#
# with open('../source/全息.txt') as f:
#     urls = f.readlines()

# results = set()
# with open('胶囊.txt', 'w') as f:
#     for url in urls:
#         if 'page' not in url and url not in results:
#             f.write(url)
#             results.add(url)
#
# print('胶囊.txt去重更新完成!')
# with open('../全息.txt', 'w') as f:
#     for url in urls:
#         driver.get('https://buff.163.com/goods/' +url)
#         time.sleep(3)
#         while True:
#             price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
#             on_sale_count = driver.find_element(By.CLASS_NAME, "new-tab").text.split("Sell")[1].split(")")[0].replace("(", "").replace("+","")
#
#             if len(price_elements) > 1 :
#                 lowest_price = price_elements[1]
#                 if float(lowest_price.text.replace("¥ ", "")) <= 80 and int(on_sale_count) > 200:
#                     f.write(url)
#                     print("save"+url+lowest_price.text)
#                     break
#                 else:
#                     print("delete"+url+lowest_price.text)
#                     break
#         time.sleep(5)