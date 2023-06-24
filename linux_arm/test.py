import datetime
import os
import random
import smtplib
import subprocess
import threading
import traceback
from email.header import Header
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.common import WebDriverException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import buff_sql
import buff_mail

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--shm-size=1024m")
chrome_options.add_argument("--lang=zh_CN")
cap = DesiredCapabilities.CHROME
cap["pageLoadStrategy"] = "none"


def day_send_mail(lowest_price, name_elements, url, price, one_day_price, goods_id, time):
    if len(one_day_price) > 0:
        day_prices = 0
        for day in one_day_price:
            day_prices += float(day)
        day_price = day_prices / len(one_day_price)
        daily_change = round((price - day_price) / day_price, 2)
        buff_sql.update_good_with_trend(goods_id, str(daily_change))

        if daily_change >= 0.2:
            # print(mail.get(url))
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一天内上涨超20% 具体涨幅为' + str(
                    daily_change) + ' 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
                buff_sql.add_new_mail(name_elements + '价格在一天内上涨超20% 具体涨幅为' + str(
                    daily_change) + ' 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一天内上涨超20% 具体涨幅为' + str(
                    daily_change) + '历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
                buff_sql.add_new_mail(name_elements + '价格在一天内上涨超20% 具体涨幅为' + str(
                    daily_change) + ' 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time)
        elif daily_change < -0.2:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一天内下降超20% 具体涨幅为' + str(
                    daily_change) + '历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
                buff_sql.add_new_mail(name_elements + '价格在一天内下降超20% 具体涨幅为' + str(
                    daily_change) + '历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time)
            elif mail.get(url) == price:
                print("与上次发送邮件时的价格相同，不再发送邮件")
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一天内下降超20% 具体涨幅为' + str(
                    daily_change) + '历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
                buff_sql.add_new_mail(name_elements + '价格在一天内下降超20% 具体涨幅为' + str(
                    daily_change) + '历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time)


def three_day_send_mail(lowest_price, name_elements, url, price, three_day_price, goods_id, time):
    if len(three_day_price) > 0:
        three_prices = 0
        for three_day in three_day_price:
            three_prices += float(three_day)
        three_price = three_prices / len(three_day_price)
        three_day_change = round((price - three_price) / three_price, 2)
        buff_sql.update_good_with_trend(goods_id, str(three_day_change))
        if three_day_change > 0.3:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在三天内上涨30% 具体涨幅为' + str(
                    three_day_change) + ' 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
                buff_sql.add_new_mail(name_elements + '价格在三天内上涨30% 具体涨幅为' + str(
                    three_day_change) + ' 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在三天内上涨30% 具体涨幅为' + str(
                    three_day_change) + '历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
                buff_sql.add_new_mail(name_elements + '价格在三天内上涨30% 具体涨幅为' + str(
                    three_day_change) + ' 历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time)


        elif three_day_change < -0.3:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在三天内下降30% 具体涨幅为' + str(
                    three_day_change) + '历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
                buff_sql.add_new_mail(name_elements + '价格在三天内下降30% 具体涨幅为' + str(
                    three_day_change) + '历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在三天内下降30% 具体涨幅为' + str(
                    three_day_change) + '历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
                buff_sql.add_new_mail(name_elements + '价格在三天内下降30% 具体涨幅为' + str(
                    three_day_change) + '历史最低价格为:' + str(
                    lowest_price) + '当前价格为' + str(price), url, time)


def week_send_mail(lowest_price, name_elements, url, price, week_day_price):
    if len(week_day_price) > 0:
        week_prices = 0
        for week in week_day_price:
            week_prices += float(week)
        week_price = week_prices / len(week_day_price)

        week_change = round((price - week_price) / week_price, 2)

        if week_change > 0.4:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一周内上涨40% 具体涨幅为' + str(
                    week_change) + ' 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一周内上涨40% 具体涨幅为' + str(
                    week_change) + ' 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)

        elif week_change < -0.4:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一周内下降40% 具体涨幅为' + str(
                    week_change) + ' 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一周内下降40% 具体涨幅为' + str(
                    week_change) + ' 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)


def month_send_mail(lowest_price, name_elements, url, price, month_price):
    if len(month_price) > 0:
        month_prices = 0
        for month in month_price:
            month_prices += float(month)
        a_month_price = month_prices / len(month_price)
        month_change = round((price - a_month_price) / a_month_price, 2)

        if month_change > 0.5:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一个月内上涨50% 具体涨幅为' + str(
                    month_change) + ' 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一个月内上涨50%  具体涨幅为' + str(
                    month_change) + '历史最低价格为:' + str(
                    price),
                                    lowest_price,
                                    'https://buff.163.com/goods/' + url)

        elif month_change < -0.5:
            if mail.get(url) is None:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一个月内下降50%  具体涨幅为' + str(
                    month_change) + '历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                buff_mail.send_mail(name_elements + '价格在一个月内下降50% 具体涨幅为' + str(
                    month_change) + ' 历史最低价格为:' + str(
                    lowest_price),
                                    price,
                                    'https://buff.163.com/goods/' + url)


def get_all(urls):
    global can_mail
    # import os
    # import socket
    #
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(("8.8.8.8", 80))
    # ip = s.getsockname()[0]
    #
    # print("IP:", ip)
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/bin/chromedriver",
                              desired_capabilities=cap)
    driver.implicitly_wait(15)
    climb_times = 1
    thread_id = threading.current_thread().thread_id
    while True:
        start_climb_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print(f"{start_climb_time}:线程{thread_id+1}:开始爬取第{climb_times}次")
        start_time = time.time()
        climb_goods_count = 0
        for url in urls:
            sleep_time = random.randint(2, 5)
            url = url.replace("\n", "")
            while True:
                try:
                    driver.get('https://buff.163.com/goods/' + url)
                    # print(f"{thread_id}:{url}")
                    lowest_price = 0
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
                    if not os.path.exists('txt/' + str(goods_id) + '.txt'):
                        f = open('txt/' + str(goods_id) + '.txt', 'w', encoding='utf-8')
                        f.close()
                    with open('txt/' + str(goods_id) + '.txt', 'a+', encoding='utf-8') as f:
                        f.seek(0)
                        lines = f.readlines()
                        if not lines:
                            f.write(str(goods_id) + ':' + str(price / 2) + '\n')
                            f.write(f'{time_get};{name} ¥ {price}\n')
                            if "金色" in name:
                                category = "金色"
                            elif "全息" in name:
                                category = "全息"
                            elif "胶囊" in name:
                                category = "胶囊"
                            elif "武器箱" in name:
                                category = "武器箱"
                            buff_sql.add_new_good(name, str(goods_id), category, str(price / 2), img_url,
                                                  str(price))
                            buff_sql.write_record(time_get, str(goods_id), str(price))
                            break
                        else:
                            expect_price = buff_sql.get_good_expected_price(goods_id)
                            if len(lines) == 1:
                                f.write(f'{time_get};{name} ¥ {price}\n')
                                buff_sql.write_record(time_get, str(goods_id), str(price))
                                break
                            # if buff_sql.get_good_expected_price(goods_id) is None:
                            #     if "金色" in name:
                            #         category = "金色"
                            #     elif "全息" in name:
                            #         category = "全息"
                            #     elif "胶囊" in name:
                            #         category = "胶囊"
                            #     buff_sql.add_new_good(name, str(goods_id), category, str(price / 2), img_url,
                            #                           str(price))

                            last_price = buff_sql.get_good_last_record(goods_id)
                            one_day_price = []
                            three_day_price = []
                            week_day_price = []
                            month_price = []
                            days = [1, 3, 7, 30]
                            lines.pop(0)
                            lowest_price = buff_sql.get_good_lowest_price(goods_id)

                            for line in lines:
                                price_data = line.split(';')
                                # 获取 当前时间并计算与文本时间差
                                old_time_str = price_data[0].replace('\n', '')
                                old_time = datetime.datetime.strptime(old_time_str, "%Y-%m-%d %H:%M:%S")
                                now_time = datetime.datetime.utcnow()
                                diff_time = now_time - old_time
                                # # 获取对应天数的历史价格
                                # if lowest_price > float(
                                #         price_data[1].split('¥')[1].replace(" ", "").replace("\n", "")):
                                #     lowest_price = float(
                                #         price_data[1].split('¥')[1].replace(" ", "").replace("\n", ""))
                                if diff_time.days == days[0]:
                                    one_day_price.append(
                                        price_data[1].split('¥')[1].replace(" ", "").replace("\n", ""))
                                    # print("have one day ago price")
                                elif diff_time.days == days[1]:
                                    three_day_price.append(
                                        price_data[1].split('¥')[1].replace(" ", "").replace("\n", ""))
                                    # print("have 3 day ago price")

                                elif diff_time.days == days[2]:
                                    week_day_price.append(
                                        price_data[1].split('¥')[1].replace(" ", "").replace("\n", ""))
                                    # print("have 7 day ago price")

                                elif diff_time.days == days[3]:
                                    month_price.append(
                                        price_data[1].split('¥')[1].replace(" ", "").replace("\n", ""))
                                    # print("have 30 day ago price")
                                # 计算各天数的价格变化

                            if price <= float(expect_price):
                                # print( f'{goods_id}:{time_get} :{name} 的最低价格达到期望值, 当前价格是: {price} 历史最低价格为:{
                                # lowest_price}')
                                if can_mail and (time.localtime(time.time()).tm_hour.real < 1 or time.localtime(
                                        time.time()).tm_hour.real > 7):
                                    buff_mail.send_mail(
                                        name + '\n历史新低价!!!!历史最低价格为:' + str(
                                            lowest_price), price,
                                        'https://buff.163.com/goods/' + url)
                                buff_sql.add_new_mail(name + '\n历史新低价!!!!历史最低价格为:' + str(
                                    lowest_price) + '当前价格是:' + str(
                                    price), goods_id, time_get)
                            # else:
                            #     print(
                            #         f'{goods_id}:{time_get} :{name} 的最低价格未达到期望值, 当前价格是: {price}')
                            # 用于首次填充数据库，填充完毕后注释掉
                            # update_good_price(conn, cursor, str(goods_id), str(price), lowest_price)

                            if last_price == price:
                                climb_goods_count += 1
                                break
                            f.write(f'{time_get};{name} ¥ {price}\n')
                            buff_sql.write_record(time_get, str(goods_id), str(price))
                            buff_sql.update_good_without_trend(str(goods_id), img_url, name, price,
                                                               lowest_price)
                            f.close()
                            climb_goods_count += 1
                            if can_mail and (time.localtime(time.time()).tm_hour.real < 1 or time.localtime(
                                    time.time()).tm_hour.real > 7):
                                day_send_mail(lowest_price, name, url, price, one_day_price, goods_id,
                                              time_get)
                                three_day_send_mail(lowest_price, name, url, price, three_day_price,
                                                    goods_id, time_get)
                                week_send_mail(lowest_price, name, url, price,
                                               week_day_price)
                            if not can_mail and time.localtime(time.time()).tm_hour.real == 0 and time.localtime(
                                    time.time()).tm_min == 0:
                                # print("set can_mail=true")
                                can_mail = True
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
                        # print(e)
                        while True:
                            try:
                                if crash_time == 2:
                                    time.sleep(600)
                                    buff_mail.send_mail("need to reboot chroot container", 0, '111')

                                else:
                                    time.sleep(20)
                                driver = webdriver.Chrome(chrome_options=chrome_options,
                                                          executable_path="/usr/bin/chromedriver")
                                driver.get('https://buff.163.com/goods/' + url)
                                sleep_time = random.randint(5, 15)
                                break
                            except:
                                crash_time += 1
                    continue
                except WebDriverException as e:
                    crash_time = 0
                    # print(e)
                    while True:
                        try:
                            if crash_time == 2:
                                time.sleep(600)
                                buff_mail.send_mail("need to reboot chroot container", 0, '111')

                            else:
                                time.sleep(20)
                            driver = webdriver.Chrome(chrome_options=chrome_options,
                                                      executable_path="/usr/bin/chromedriver")
                            driver.get('https://buff.163.com/goods/' + url)
                            sleep_time = random.randint(5, 15)
                            break
                        except:
                            crash_time += 1
                except smtplib.SMTPSenderRefused as e:
                    print('发送邮件数量达今日最大值.')
                    can_mail = False
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
        # print(f'线程{thread_id}:爬取一次完毕,要求爬取商品{len(urls)}个，实际共爬取{climb_goods_count}个商品')
        end_climb_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print(f"{end_climb_time}:线程{thread_id}结束爬取第{climb_times}次")
        cost_time = (time.time() - start_time) / 60
        print(f"{end_climb_time}:线程{thread_id}爬取商品{len(urls)}个爬取第{climb_times}次消耗的时间为{cost_time} min")
        climb_times += 1
        # if cost_time >= 180:
        #     print(f"线程{thread_id}sleep 3600 s then restart new climb")
        #     time.sleep(3600)
        #     driver.close()

        if cost_time >= 60:
            driver.close()
            print(f"线程{thread_id}start new climb")
        time.sleep(5)


class MyThread(threading.Thread):
    def __init__(self, thread_id, target, args):
        super().__init__(target=target, args=args)
        self.thread_id = thread_id


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
    # threads = []
    # urls = []
    mail = {}
    can_mail = True
    # files = os.listdir('../source')
    # conn = pymysql.connect(
    #     host="120.25.145.148",
    #     port=3306,
    #     user="homework",
    #     passwd="root",
    #     db="homework",
    #     charset='utf8',
    #     autocommit=True
    # )
    #
    # with open('../source/all.txt') as f:
    #     urls = f.readlines()
    # get_all(urls)
    # for file in files:
    #     with open('../source/' + file) as f:
    #         urls = f.readlines()
    #     f.close()
    #     thread = threading.Thread(target=get_all, args=([urls]))
    #     threads.append(thread)
    #     time.sleep(random.randint(2, 5))
    #     thread.start()
    #
    # for thread in threads:
    #     thread.join()
    # service mariadb start
    with open('../source/all.txt') as f:
        the_urls = f.readlines()
    threads_count = 8
    start_threads(threads_count, the_urls)
    while True:
        now = datetime.datetime.now()
        next_run_time = datetime.datetime(now.year, now.month, now.day, 11, 50, 0)
        if now >= next_run_time:
            next_run_time += datetime.timedelta(days=1)
        sleep_time = (next_run_time - now).seconds
        print(f"Next restart at {next_run_time}")
        time.sleep(sleep_time)
        print("Restarting...")
        subprocess.Popen(["python", "test.py"])
        time.sleep(10)
    # urls_per_thread = len(the_urls) // threads_count  # 每个线程要处理的行数
    # threads = []
    #
    # for i in range(threads_count):
    #     start = i * urls_per_thread
    #     end = start + urls_per_thread if i < threads_count-1 else len(the_urls)  # 最后一个线程处理剩余行数
    #     sublist = the_urls[start:end]
    #     thread = threading.Thread(target=get_all, args=(sublist,))
    #     threads.append(thread)
    #     time.sleep(random.randint(3, 5))
    #     thread.start()
    #
    # for thread in threads:
    #     thread.join()
