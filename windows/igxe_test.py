import datetime
import random
import smtplib
import threading
import traceback

from selenium import webdriver
from selenium.common import WebDriverException, StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

from tqdm import tqdm

import buff_sql
import buff_sql_server
import buff_mail

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
# options.add_argument("window-size=1024,768")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--shm-size=2048m")
options.add_argument("--lang=zh_CN")
options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"


def get_igxe():
    can_mail = True
    driver = webdriver.Firefox(service=Service('webdriver/geckodriver.exe'),
                               options=options)
    driver.implicitly_wait(6)
    goods = buff_sql.get_all_goods()
    start_climb = time.time()
    pbar = tqdm(total=len(goods))
    for index, (goods_id, trend, name, category, img_url, now_price_buff, the_lowest_price_buff, wear_tear_group,
                the_lowest_price_uu, the_lowest_price_igxe, the_lowest_price_c5, now_price_uu, now_price_igxe,
                now_price_c5, now_price_steam, update_time, uu_id, igxe_id, c5_id, csob_update_time) in enumerate(
        goods):
        pbar.set_description(f"爬取第 {index}/{len(goods)}商品中")
        if igxe_id == '0' or igxe_id is None or igxe_id == '':
            pbar.update(1)
            continue
        sleep_time = random.randint(2, 5)

        while True:
            try:
                driver.get('https://www.igxe.cn/product/730/' + igxe_id)
                # print(f"{thread_id}:{url}")
                time_get = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                steam_price = driver.find_element(By.CLASS_NAME, "starting-price.mt-15").find_element(By.CLASS_NAME,
                                                                                                      "c-4").text.replace(
                    "￥", "")
                now_lowest_price = driver.find_element(By.CLASS_NAME, "dataTable.is-show.sell-data").find_element(
                    By.CLASS_NAME, "dib.price.c-4.mt-20.fw-bold").text.replace("￥", "")
                buff_sql.update_good_with_now_price_igxe(igxe_id, now_lowest_price)
                buff_sql.update_good_with_steam_price_igxe(igxe_id, steam_price)
                buff_sql_server.update_good_with_now_price_igxe(igxe_id, now_lowest_price)
                buff_sql.write_record(time_get, str(igxe_id), str(now_lowest_price), 'igxe')
                if now_lowest_price is not None and the_lowest_price_igxe is not None:
                    if float(now_lowest_price) <= float(the_lowest_price_igxe) and can_mail:
                        # buff_mail.send_mail(f"IGXE: {name} 价格低于历史最低价",
                        #                     f"历史最低价格{the_lowest_price_igxe}，现在价格：{now_lowest_price} \n",
                        #                     "IGXE",
                        #                     "1094410998@qq.com")
                        buff_sql.update_good_with_lowest_price_igxe(igxe_id, now_lowest_price)
                if goods_id is not None:
                    expect_price = buff_sql.get_good_expected_price(goods_id)
                    if expect_price is not None:
                        for temp in expect_price:
                            if now_lowest_price is not None:
                                if float(now_lowest_price) <= float(temp[0]) and can_mail:
                                    buff_mail.send_mail(f"IGXE: {name} 价格低于预期",
                                                        f" 历史最低价格{the_lowest_price_igxe}，现在价格：{now_lowest_price} \n",
                                                        "IGXE",
                                                        "1094410998@qq.com",0)

                # print(f"{time_get} {igxe_id} {steam_price} {now_lowest_price}")
                time.sleep(sleep_time)
                pbar.set_description(f"爬取第 {index}/{len(igxe_id)}商品完成")
                pbar.update(1)
                break
            except NoSuchElementException as e:
                try:
                    if '暂无数据' in driver.find_element(By.CLASS_NAME, "t").text:
                        pbar.set_description(f"爬取第 {index}/{len(igxe_id)}商品完成")
                        pbar.update(1)
                        # print(f"{igxe_id} 暂无数据")
                        break
                except NoSuchElementException as e:
                    print(f"{igxe_id} NoSuchElementException")
                    continue
                continue
            except TimeoutException as e:
                print(f"{igxe_id} TimeoutException")
                continue
            except smtplib.SMTPSenderRefused as e:
                print('发送邮件数量达今日最大值.')
                can_mail = False
                continue
            except WebDriverException as e:
                print(f"{igxe_id} WebDriverException")
                driver = webdriver.Firefox(service=Service('webdriver/geckodriver.exe'),
                                           options=options)
                driver.implicitly_wait(6)
                continue
    driver.quit()
    print(f"climb time: {(time.time() - start_climb) / 60} min")
    pbar.close()


while True:
    get_igxe()
