import random
import threading
import time
import traceback

from selenium import webdriver
from selenium.common import StaleElementReferenceException, WebDriverException, NoSuchElementException

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_all(urls):
    driver = webdriver.Chrome(service=Service(r'../windows/webdriver/chromedriver.exe'))
    driver.implicitly_wait(15)
    for url in urls:
        sleep_time = random.randint(2, 5)
        results = set()
        start_time = time.time()
        while True:
            try:
                driver.get('https://buff.163.com/goods/' + url)
                price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")

                while len(price_elements) <= 1:
                    if time.time() - start_time > 20:
                        driver.refresh()
                    price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                try:
                    price = float(price_elements[1].text.replace("¥ ", ""))
                    name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                    name = name_elements.text.splitlines()[2]
                    category = name_elements.text.split("类型 |")[1].split("\n")[0]
                    sale_count = driver.find_element(By.CLASS_NAME, "new-tab").find_element(
                        By.TAG_NAME, "a").text.replace("当前在售(", "").replace(")", "").replace("+", "")
                except StaleElementReferenceException as e:
                    continue
                with open('../after_remove.txt', '+a') as f:
                    if category == "步枪" and price < 20 or int(sale_count) < 10:
                        print("移除:" + url)
                        break
                    if url not in results:
                        f.write(url)
                        results.add(url)
                        print("保留:" + url)
                    else:
                        print("移除:" + url)
                break
            except StaleElementReferenceException as e:
                print("try to handle element is not attached to the page document in out loop")
                continue
            except NoSuchElementException as e:
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
        thread = threading.Thread(target=get_all, args=(sublist,))
        threads.append(thread)
        time.sleep(random.randint(3, 5))
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    with open('../temp.txt') as f:
        the_urls = f.readlines()
    threads_count = 1
    start_threads(threads_count, the_urls)
