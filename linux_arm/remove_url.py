import datetime
import os
import random
import threading
import time
import traceback

from selenium import webdriver
from selenium.common import StaleElementReferenceException, WebDriverException, NoSuchElementException

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from linux_arm.test import MyThread


def get_all(urls):
    driver = webdriver.Chrome(service=Service(r'chromedriver.exe'))
    driver.implicitly_wait(15)
    climb_times = 1
    thread_id = threading.current_thread().thread_id
    for url in urls:
        sleep_time = random.randint(2, 5)
        results = set()
        while True:
            try:
                driver.get('https://buff.163.com/goods/' + url)
                # print(f"{thread_id}:{url}")
                start_time = time.time()
                lowest_price_in_txt = 0
                time_get = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # if "429 Too Many Requests" in driver.find_element(By.TAG_NAME, "title").text:
                #     print("超时")
                #     time.sleep(2)
                #     driver.refresh()
                price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                img_url = driver.find_element(By.CLASS_NAME, "detail-pic").find_element(By.CLASS_NAME,
                                                                                        "t_Center").find_element(
                    By.TAG_NAME, "img").get_attribute("src")
                while len(price_elements) <= 1:
                    price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                    # now_time = time.time()
                    name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                    # if now_time - start_time > 20:
                    #     print(f'{time_get} :{url} 超时')
                    #     driver.refresh()
                    #     start_time = time.time()
                # lowest_price = price_elements[1]
                # price = float(lowest_price.replace("¥ ", ""))
                try:
                    price = float(price_elements[1].text.replace("¥ ", ""))
                    name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                    name = name_elements.text.splitlines()[2]
                    category = name_elements.text.split("类型 |")[1].split("\n")[0]
                except StaleElementReferenceException as e:
                    # print("try to handle element is not attached to the page document ")
                    try:
                        while True:
                            price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                            name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                            while len(price_elements) <= 1:
                                price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                                name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                            price = float(price_elements[1].text.replace("¥ ", ""))
                            name = name_elements.text.splitlines()[2]
                            # category = name_elements.text.split("类型 |")[1].split("\n")[0]
                            break
                    except:
                        pass

                goods_id = driver.current_url.split('/')[-1]
                with open('../source/22里约全息+金色+胶囊', '+a') as f:
                    if '金色' in name or '全息' in name or '胶囊' in name and url not in results:
                        f.write(url)
                        results.add(url)
                        print("保留:" + url)

                    else:
                        print("移除:" + url)
                break
            except StaleElementReferenceException as e:
                print("try to handle element is not attached to the page document in out loop")
                continue
                # try:
                #     while True:
                #         price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                #         while len(price_elements) <= 1:
                #             price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                #         price = float(price_elements[1].text.replace("¥ ", ""))
                #         break
                # except:
                #     pass
            except NoSuchElementException as e:
                # print(url+":超时")
                try:
                    time.sleep(sleep_time)
                    driver.refresh()
                except WebDriverException as e:
                    crash_time = 0
                    print(e)
                    while True:
                        try:
                            if crash_time == 2:
                                time.sleep(600)

                            else:
                                time.sleep(20)
                            driver = webdriver.Chrome(service=Service(r'chromedriver.exe'))
                            driver.get('https://buff.163.com/goods/' + url)
                            sleep_time = random.randint(5, 15)
                            break
                        except:
                            crash_time += 1
                continue
            except WebDriverException as e:
                crash_time = 0
                print(e)
                while True:
                    try:
                        if crash_time == 2:
                            time.sleep(600)

                        else:
                            time.sleep(20)
                        driver = webdriver.Chrome(service=Service(r'chromedriver.exe'))
                        driver.get('https://buff.163.com/goods/' + url)
                        sleep_time = random.randint(5, 15)
                        break
                    except:
                        crash_time += 1
            except Exception as e:
                if "远程主机强迫关闭了一个现有的连接" in str(e):
                    print('爬取速度过快,等待服务器响应...')
                    time.sleep(sleep_time)
                    continue
                print(traceback.format_exc())
                print(url)
                while True:
                    try:
                        time.sleep(10)
                        driver.refresh()
                        break
                    except:
                        pass
            finally:
                time.sleep(sleep_time)


def start_threads(threads_count, urls):
    threads = []
    urls_per_thread = len(urls) // threads_count
    for i in range(threads_count):
        start = i * urls_per_thread
        end = start + urls_per_thread if i < threads_count - 1 else len(urls)
        sublist = urls[start:end]
        thread = MyThread(thread_id=i, target=get_all, args=(sublist,))
        threads.append(thread)
        time.sleep(random.randint(3, 5))
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    with open('../source/22里约.txt') as f:
        the_urls = f.readlines()
    threads_count = 20
    start_threads(threads_count, the_urls)
