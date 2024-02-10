import json
import threading
import time
import traceback
from threading import Thread
from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from windows import buff_sql

options = Options()
# 去掉"chrome正受到自动化测试软件的控制"的提示条
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--no-sandbox")
options.add_argument("--lang=zh_CN")
lock = threading.Lock()


def split_tuple(tup, num):
    list_tup = list(tup)
    return [list_tup[i::num] for i in range(num)]


def update(urls):
    browser = webdriver.Chrome(service=Service('../windows/webdriver/chromedriver.exe'), options=options)
    browser.scopes = [
        '.*/api/v1/goods/chart',
    ]
    browser.set_page_load_timeout(300)
    first = True
    for (goods_id, trend, name, category, img_url, now_price_buff, the_lowest_price_buff, wear_tear_group,
         the_lowest_price_uu,
         the_lowest_price_igxe, the_lowest_price_c5, now_price_uu, now_price_igxe, now_price_c5,
         now_price_steam, update_time) in urls:
        while True:
            try:
                browser.get('http://csgoob.onet4p.net/goods?name=' + name)
                if first:
                    time.sleep(5)
                    browser.get('http://csgoob.onet4p.net/goods?name=' + name)
                WebDriverWait(browser, 60, 0.5).until(ec.presence_of_all_elements_located(
                    (By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]/span[3]')))
                time.sleep(1)
                ActionChains(browser).move_to_element(
                    browser.find_element(By.CLASS_NAME, 'text-lg.text-orange-400.mr-2.font-bold')).pause(0.5).perform()
                time.sleep(1)
                now_prices_div = browser.find_element(By.CLASS_NAME, 'ant-tooltip-inner').find_elements(By.TAG_NAME,
                                                                                                        'div')
                for div in now_prices_div:
                    span_text = div.find_elements(By.TAG_NAME, 'span')[1]
                    if span_text.text.split('￥')[0].replace("\n", "") == '悠悠有品:':
                        uu_now = span_text.text.split('￥')[1].split(' ')[0]
                        buff_sql.update_good_with_now_price_uu(goods_id, uu_now)
                    elif span_text.text.split('￥')[0].replace("\n", "") == 'IGXE:':
                        igxe_now = span_text.text.split('￥')[1].split(' ')[0]
                        buff_sql.update_good_with_now_price_igxe(goods_id, igxe_now)
                    elif span_text.text.split('￥')[0].replace("\n", "") == 'C5:':
                        c5_now = span_text.text.split('￥')[1].split(' ')[0]
                        buff_sql.update_good_with_now_price_c5(goods_id, c5_now)
                    elif span_text.text.split('￥')[0].replace("\n", "") == 'BUFF:':
                        buff_now = span_text.text.split('￥')[1].split(' ')[0]
                        buff_sql.update_good_with_now_price_buff(goods_id, buff_now)
                time.sleep(1)
                buff_sql.update_good_update_time(goods_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                break
            except StaleElementReferenceException as e:
                print(e)
                print(traceback.format_exc())
                continue
            except NoSuchElementException as e:
                print(e)
                print(traceback.format_exc())
                continue
            except IndexError as e:
                print(e)
                print(traceback.format_exc())
                continue
            except TimeoutException as e:
                print(e)
                continue
            except WebDriverException as e:
                print(e)
                print(traceback.format_exc())
                browser = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
                browser.scopes = [
                    '.*/api/v1/goods/chart',
                ]
                browser.set_page_load_timeout(300)
                continue


all_goods = buff_sql.get_all_goods()

all_goods_parts = split_tuple(all_goods, 5)
for i in range(5):
    Thread(target=update, args=(all_goods_parts[i],)).start()
    time.sleep(1)