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


def day_send_mail(lowest_price, name_elements, url, price, one_day_price, goods_id, time, mail_addr, user_id):
    if len(one_day_price) > 0:
        day_prices = 0
        for day in one_day_price:
            day_prices += float(day)
        day_price = day_prices / len(one_day_price)
        daily_change = round((price - day_price) / day_price, 2)
        buff_sql.update_good_with_trend(goods_id, str(daily_change))
        # buff_sql_server.update_good_with_trend(igxe_id, str(daily_change))
        if daily_change >= 0.3:
            # print(mail.get(url))
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一天内上涨超30% 具体涨幅为' + str(
                    daily_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, daily_change)
                buff_sql.add_new_mail(name_elements + '价格在一天内上涨超30% 具体涨幅为' + str(
                    daily_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time, user_id)
                # buff_sql_server.add_new_mail(name_elements + '价格在一天内上涨超30% 具体涨幅为' + str(
                #     daily_change * 100) + '% 历史最低价格为:' + str(
                #     lowest_price) + '当前价格为' + str(price), url, time, user_id)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一天内上涨超30% 具体涨幅为' + str(
                    daily_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, daily_change)
                buff_sql.add_new_mail(name_elements + '价格在一天内上涨超30% 具体涨幅为' + str(
                    daily_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time, user_id)
                # buff_sql_server.add_new_mail(name_elements + '价格在一天内上涨超30% 具体涨幅为' + str(
                #     daily_change * 100) + '% 历史最低价格为:' + str(
                #     lowest_price) + '当前价格为' + str(price), url, time, user_id)
        elif daily_change < -0.3:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一天内下降超30% 具体降幅为' + str(
                    daily_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, daily_change)
                buff_sql.add_new_mail(name_elements + '价格在一天内下降超30% 具体降幅为' + str(
                    daily_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time, user_id)
                # buff_sql_server.add_new_mail(name_elements + '价格在一天内下降超30% 具体降幅为' + str(
                #     daily_change * 100) + '% 历史最低价格为:' + str(
                #     lowest_price) + '当前价格为' + str(price), url, time, user_id)
            elif mail.get(url) == price:
                pass
                # print("与上次发送邮件时的价格相同，不再发送邮件")
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一天内下降超30% 具体降幅为' + str(
                    daily_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, daily_change)
                buff_sql.add_new_mail(name_elements + '价格在一天内下降超30% 具体降幅为' + str(
                    daily_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time, user_id)
                # buff_sql_server.add_new_mail(name_elements + '价格在一天内下降超30% 具体降幅为' + str(
                #     daily_change * 100) + '% 历史最低价格为:' + str(
                #     lowest_price) + '当前价格为' + str(price), url, time, user_id)


def three_day_send_mail(lowest_price, name_elements, url, price, three_day_price, goods_id, time, mail_addr, user_id):
    if len(three_day_price) > 0:
        three_prices = 0
        for three_day in three_day_price:
            three_prices += float(three_day)
        three_price = three_prices / len(three_day_price)
        three_day_change = round((price - three_price) / three_price, 2)
        buff_sql.update_good_with_trend(goods_id, str(three_day_change))
        # buff_sql_server.update_good_with_trend(igxe_id, str(three_day_change))
        if three_day_change > 0.4:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在三天内上涨超40% 具体涨幅为' + str(
                    three_day_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, three_day_change)
                buff_sql.add_new_mail(name_elements + '价格在三天内上涨超40% 具体涨幅为' + str(
                    three_day_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time, user_id)
                #buff_sql_server.add_new_mail(name_elements + '价格在三天内上涨超40% 具体涨幅为' + str(
                # three_day_change*100) + '% 历史最低价格为:' + str(
                # lowest_price) + '当前价格为' + str(price), url, time, user_id)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在三天内上涨超40% 具体涨幅为' + str(
                    three_day_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, three_day_change)
                buff_sql.add_new_mail(name_elements + '价格在三天内上涨超40% 具体涨幅为' + str(
                    three_day_change * 100) + '% 当前价格为' + str(price) + ' 历史最低价格为:' + str(
                    lowest_price), url, time, user_id)
                #buff_sql_server.add_new_mail(name_elements + '价格在三天内上涨超40% 具体涨幅为' + str(
                # three_day_change*100) + '% 当前价格为' + str(price) + ' 历史最低价格为:' + str(
                # lowest_price), url, time, user_id)

        elif three_day_change < -0.4:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在三天内下降超40% 具体降幅为' + str(
                    three_day_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, three_day_change)
                buff_sql.add_new_mail(name_elements + '价格在三天内下降超40% 具体降幅为' + str(
                    three_day_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time, user_id)
                #buff_sql_server.add_new_mail(name_elements + '价格在三天内下降超40% 具体降幅为' + str(
                # three_day_change*100) + '% 历史最低价格为:' + str(
                # lowest_price) + '当前价格为' + str(price), url, time, user_id)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在三天内下降超40% 具体降幅为' + str(
                    three_day_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, three_day_change)
                buff_sql.add_new_mail(name_elements + '价格在三天内下降超40% 具体降幅为' + str(
                    three_day_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time, user_id)
                #buff_sql_server.add_new_mail(name_elements + '价格在三天内下降超40% 具体降幅为' + str(
                # three_day_change*100) + '% 历史最低价格为:' + str(
                # lowest_price) + '当前价格为' + str(price), url, time, user_id)


def week_send_mail(lowest_price, name_elements, url, price, week_day_price, mail_addr):
    if len(week_day_price) > 0:
        week_prices = 0
        for week in week_day_price:
            week_prices += float(week)
        week_price = week_prices / len(week_day_price)

        week_change = round((price - week_price) / week_price, 2)

        if week_change > 0.5:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一周内上涨超50% 具体涨幅为' + str(
                    week_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, week_change)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一周内上涨超50% 具体涨幅为' + str(
                    week_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, week_change)

        elif week_change < -0.5:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一周内下降超50% 具体降幅为' + str(
                    week_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, week_change)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一周内下降超50% 具体降幅为' + str(
                    week_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, week_change)


def month_send_mail(lowest_price, name_elements, url, price, month_price, mail_addr):
    if len(month_price) > 0:
        month_prices = 0
        for month in month_price:
            month_prices += float(month)
        a_month_price = month_prices / len(month_price)
        month_change = round((price - a_month_price) / a_month_price, 2)

        if month_change > 0.6:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一个月内上涨超60% 具体涨幅为' + str(
                    month_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, month_change)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一个月内上涨超60% 具体涨幅为' + str(
                    month_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, month_change)

        elif month_change < -0.5:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一个月内下降超60%  具体降幅为' + str(
                    month_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, month_change)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一个月内下降超60% 具体降幅为' + str(
                    month_change * 100) + '% 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url, mail_addr, month_change)


def get_buff(buff_urls):
    global can_mail
    # import os
    # import socket
    #
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # ip = s.getsockname()[0]
    #
    # print("IP:", ip)
    driver = webdriver.Firefox(service=Service('webdriver/geckodriver.exe'),
                               options=options)
    driver.implicitly_wait(6)
    thread_id = threading.current_thread().thread_id
    pbar = tqdm(total=len(buff_urls), dynamic_ncols=True, mininterval=0, position=thread_id)
    for i, url in enumerate(buff_urls):
        if url=="0":
            pbar.set_description(f"线程{thread_id}:爬取第 {i + 1}/{len(buff_urls)}个商品中")
            pbar.update(1)
            continue
        sleep_time = random.randint(2, 5)
        # start_climb_one_time = time.time()
        while True:
            try:
                driver.get('https://buff.163.com/goods/' + url)
                # print(f"{thread_id}:{url}")
                time_get = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if "429 Too Many Requests" in driver.find_element(By.TAG_NAME, "h1").text:
                    # print(thread_id, "429 Too Many Requests")
                    time.sleep(1)
                    continue
                price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                img_url = driver.find_element(By.CLASS_NAME, "detail-pic").find_element(By.CLASS_NAME,
                                                                                        "t_Center").find_element(
                    By.TAG_NAME, "img").get_attribute("src")

                sale_count = driver.find_element(By.CLASS_NAME, "new-tab").find_element(
                    By.TAG_NAME, "a").text.replace("当前在售(", "").replace(")", "").replace("+", "")
                this_wait_loop_start_time = time.time()
                content = driver.find_element(By.CLASS_NAME, "detail-tab-cont").text
                if '暂无数据' in content:
                    # print("暂无数据")
                    pbar.set_description(f"线程{thread_id}:爬取第 {i + 1}/{len(buff_urls)}个商品中")
                    pbar.update(1)
                    break
                while len(price_elements) <= 1:
                    content = driver.find_element(By.CLASS_NAME, "detail-tab-cont").text
                    if '暂无数据' in content:
                        # print("暂无数据")
                        pbar.set_description(f"线程{thread_id}:爬取第 {i + 1}/{len(buff_urls)}个商品中")
                        pbar.update(1)
                        break
                    price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                    if time.time() - this_wait_loop_start_time > 3:
                        # print("具体价格部分未加载")
                        driver.refresh()
                        this_wait_loop_start_time = time.time()
                if '暂无数据' in content:
                    # print("暂无数据")
                    pbar.set_description(f"线程{thread_id}:爬取第 {i + 1}/{len(buff_urls)}个商品中")
                    pbar.update(1)
                    break
                price = float(price_elements[1].text.replace("¥ ", ""))
                name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                name = name_elements.find_element(By.TAG_NAME, "h1").text
                goods_id = driver.current_url.split('/')[-1].replace('#', '')
                # print("更新商品")
                # start_select_time = time.time()
                all_record=[]
                # buff_sql_server.create_new_record_table(igxe_id)
                all_record = buff_sql.get_good_all_record(goods_id)
                # print("select time:", time.time() - start_select_time)
                user_expect_price_list = buff_sql.get_good_expected_price(goods_id)
                last_price = buff_sql.get_good_last_record(goods_id)
                one_day_price = []
                three_day_price = []
                week_day_price = []
                month_price = []
                days = [1, 3, 7, 30]
                lowest_price = buff_sql.get_good_lowest_price(goods_id, 'buff')
                if lowest_price is None:
                    lowest_price = price
                elif lowest_price > price:
                    lowest_price = price
                for record in all_record:
                    old_time_str = record[0]
                    old_time = datetime.datetime.strptime(old_time_str, "%Y-%m-%d %H:%M:%S")
                    now_time = datetime.datetime.utcnow()
                    diff_time = now_time - old_time
                    if diff_time.days == days[0]:
                        one_day_price.append(
                            record[1])
                    elif diff_time.days == days[1]:
                        three_day_price.append(
                            record[1])

                    elif diff_time.days == days[2]:
                        week_day_price.append(
                            record[1])
                    elif diff_time.days == days[3]:
                        month_price.append(
                            record[1])
                for temp in user_expect_price_list:
                    if price <= float(temp[0]):
                        # print( f'线程:{thread_id}:{igxe_id}:{time_get} :{name} 的最低价格达到期望值, 当前价格是: {price}
                        # 历史最低价格为:{lowest_price} 爬取该商品花费时间:{time.time() - start_climb_one_time}秒')
                        if can_mail and (time.localtime(time.time()).tm_hour.real < 1 or time.localtime(
                                time.time()).tm_hour.real > 7) and int(sale_count) > 20:
                            buff_mail.send_mail(
                                name + '\n达到预期价格!!历史最低价格为:' + str(
                                    lowest_price) + '预期价格为' + str(temp[0]), price,
                                'https://buff.163.com/goods/' + url,
                                buff_sql.get_user_mail_by_user_id(temp[1]),0)
                        buff_sql.add_new_mail(name + '\n达到预期价格!!历史最低价格为:' + str(
                            lowest_price) + '预期价格为' + str(temp[0]) + '当前价格是:' + str(
                            price), goods_id, time_get, temp[1])
                        buff_sql_server.add_new_mail(name + '\n达到预期价格!!历史最低价格为:' + str(
                            lowest_price) + '预期价格为' + str(temp[0]) + '当前价格是:' + str(
                            price), goods_id, time_get, temp[1])
                    else:
                        pass
                        # print(
                        #     f'{igxe_id}:{time_get} :{name} 的最低价格未达到期望值, 当前价格是: {price}历史最低价格为:{lowest_price}')
                if  0.5<price < float(lowest_price):
                    print(
                        f'{goods_id}:{time_get} :{name} 的最低价格达到期望值, 当前价格是: {price} 历史最低价格为:{lowest_price}')
                    if can_mail and (time.localtime(time.time()).tm_hour.real < 1 or time.localtime(
                            time.time()).tm_hour.real > 7) and int(sale_count) > 20:
                        buff_mail.send_mail(
                            name + '\n历史新低价!!!!历史最低价格为:' + str(
                                lowest_price), price,
                            'https://buff.163.com/goods/' + url, '1094410998@qq.com')
                    buff_sql.add_new_mail(name + '\n历史新低价!!!!历史最低价格为:' + str(
                        lowest_price) + '当前价格是:' + str(
                        price), goods_id, time_get, 1)
                    buff_sql_server.add_new_mail(name + '\n历史新低价!!!!历史最低价格为:' + str(
                        lowest_price) + '当前价格是:' + str(
                        price), goods_id, time_get, 1)

                if last_price == price:
                    pbar.update(1)
                    pbar.set_description(f"线程{thread_id}:爬取第 {i + 1}/{len(buff_urls)}个商品中")
                    break
                # f.write(f'{time_get};{name} ¥ {price}\n')
                buff_sql.write_record(time_get, str(goods_id), str(price), 'buff')
                buff_sql.update_good_without_trend(str(goods_id), img_url, name, price,
                                                   lowest_price)
                #如果已经存在了当天大于两条这个商品的价格记录，就不再插入
                if len(one_day_price) < 2:
                    buff_sql_server.write_record(time_get, str(goods_id), str(price), 'buff')
                buff_sql_server.update_good_without_trend(str(goods_id), img_url, name, price,
                                                          lowest_price)
                # f.close()
                if can_mail and int(sale_count) > 20 and 0.5<price:  # and (time.localtime(time.time()).tm_hour.real < 1 or
                    # time.localtime(time.time()).tm_hour.real > 7)
                    day_send_mail(lowest_price, name, url, price, one_day_price, goods_id,
                                  time_get, '1094410998@qq.com', 1)
                    three_day_send_mail(lowest_price, name, url, price, three_day_price,
                                        goods_id, time_get, '1094410998@qq.com', 1)
                    week_send_mail(lowest_price, name, url, price,
                                   week_day_price, '1094410998@qq.com')
                    month_send_mail(lowest_price, name, url, price, month_price, '1094410998@qq.com')

                if not can_mail and time.localtime(time.time()).tm_hour.real == 0 and time.localtime(
                        time.time()).tm_min == 0:
                    can_mail = True
                pbar.update(1)
                pbar.set_description(f"线程{thread_id}:爬取第 {i + 1}/{len(buff_urls)}个商品中")
                buff_sql.update_good_update_time(goods_id, time_get)
                break
            except StaleElementReferenceException as e:
                # print("try to handle element is not attached to the page document in out loop")
                continue
            except OSError as e:
                if "No space left on device" in str(e):
                    print("No space left on device")
                    buff_mail.send_mail("No space left on device", 0, '111', mail)
                    continue
            except TimeoutException as e:
                continue
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
                                buff_mail.send_mail("need to reboot chroot container", 0, '111', mail)

                            else:
                                time.sleep(20)
                            driver = webdriver.Firefox(service=Service('webdriver/geckodriver.exe'),
                                                       options=options)
                            driver.get('https://buff.163.com/goods/' + url)
                            sleep_time = random.randint(5, 15)
                            break
                        except:
                            crash_time += 1
                continue
            except WebDriverException as e:
                crash_time = 0
                if 'unknown error' in str(e):
                    continue
                print(e)
                while True:
                    try:
                        if crash_time == 2:
                            time.sleep(600)
                            buff_mail.send_mail("need to reboot chroot container", 0, '111', '1094410998@qq.com')
                            crash_time = 0
                        else:
                            time.sleep(20)
                        driver = webdriver.Firefox(service=Service('webdriver/geckodriver.exe'),
                                                   options=options)
                        driver.get('https://buff.163.com/goods/' + url)
                        sleep_time = random.randint(5, 15)
                        break
                    except:
                        crash_time += 1
                continue
            except smtplib.SMTPSenderRefused as e:
                print('发送邮件数量达今日最大值.')
                can_mail = False
                continue
            except smtplib.SMTPAuthenticationError as e:
                continue
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
    pbar.close()
    driver.quit()





class MyThread(threading.Thread):
    def __init__(self, thread_id, urls, is_24_hours_running):
        super().__init__()
        self.thread_id = thread_id
        self.urls = urls
        self.stop_event = threading.Event()
        self.is_24_hours_running = is_24_hours_running

    def stop(self):
        self.stop_event.set()

    def run(self):
        climb_times = 1
        while not self.stop_event.is_set():
            start_time = time.time()
            urls = [url.replace("\n", "") for url in self.urls]
            get_buff(urls)
            end_climb_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            cost_time = (time.time() - start_time) / 60
            print(
                f"{end_climb_time}:线程{self.thread_id}爬取商品{len(self.urls)}个爬取第{climb_times}次消耗的时间为{cost_time} min")
            climb_times += 1
            time.sleep(5)


# 定义启动线程的函数
def start_threads(threads_count, urls, is_24_hours_running):
    thread = []
    urls_per_thread = len(urls) // threads_count
    for i in range(threads_count):
        start = i * urls_per_thread
        end = start + urls_per_thread if i < threads_count - 1 else len(urls)
        sublist = urls[start:end]
        th = MyThread(thread_id=i, urls=sublist, is_24_hours_running=is_24_hours_running)
        thread.append(th)
        time.sleep(1)
        th.start()
    return thread


# 定义关闭线程的函数
def stop_threads(thread):
    for th in thread:
        th.stop()
        # print('stop a thread')
    for th in thread:
        th.join()
    print('stop threads count:' + str(len(thread)))


if __name__ == '__main__':
    mail = {}
    can_mail = True
    # 设置是否24小时运行
    work_24_hours = True
    the_urls = buff_sql.get_all_goods_id()
    threads_count = 8
    threads_status = False
    threads = []
    start_threads(threads_count, the_urls, work_24_hours)
