import datetime
import os
import random
import smtplib
import threading
from email.header import Header
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--shm-size=1024m")
chrome_options.add_argument("--lang=zh_CN")
cap = DesiredCapabilities.CHROME
cap["pageLoadStrategy"] = "none"


def day_send_mail(lowest_price, lowest_price_in_txt, name_elements, url, price, one_day_price):
    if len(one_day_price) > 0:
        day_prices = 0
        for day in one_day_price:
            day_prices += float(day)
        day_price = day_prices / len(one_day_price)
        daily_change = round((price - day_price) / day_price, 2)
        if daily_change > 0.2:
            print(mail.get(url))
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一天内上涨20% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一天内上涨20% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
        elif daily_change < -0.2:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一天内下降20% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                print("与上次发送邮件时的价格相同，不再发送邮件")
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一天内下降20% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)


def three_day_send_mail(lowest_price, lowest_price_in_txt, name_elements, url, price, three_day_price):
    if len(three_day_price) > 0:
        three_prices = 0
        for three_day in three_day_price:
            three_prices += float(three_day)
        three_price = three_prices / len(three_day_price)
        three_day_change = round((price - three_price) / three_price, 2)
        if three_day_change > 0.3:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在三天内上涨30% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在三天内上涨30% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)

        elif three_day_change < -0.3:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在三天内下降30% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在三天内下降30% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)


def week_send_mail(lowest_price, lowest_price_in_txt, name_elements, url, price, week_day_price):
    if len(week_day_price) > 0:
        week_prices = 0
        for week in week_day_price:
            week_prices += float(week)
        week_price = week_prices / len(week_day_price)

        week_change = round((price - week_price) / week_price, 2)

        if week_change > 0.4:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一周内上涨40% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一周内上涨40% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)

        elif week_change < -0.4:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一周内下降40% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一周内下降40% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)


def month_send_mail(lowest_price, lowest_price_in_txt, name_elements, url, price, month_price):
    if len(month_price) > 0:
        month_prices = 0
        for month in month_price:
            month_prices += float(month)
        a_month_price = month_prices / len(month_price)
        month_change = round((price - a_month_price) / a_month_price, 2)

        if month_change > 0.5:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一个月内上涨50% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一个月内上涨50% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)

        elif month_change < -0.5:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一个月内上涨50% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一个月内下降50% the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price.text,
                          'https://buff.163.com/goods/' + url)


def get_all(urls):
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/bin/chromedriver",
                              desired_capabilities=cap)
    while True:
        for url in urls:
            sleep_time = random.randint(5, 15)
            try:
                driver.get('https://buff.163.com/goods/' + url)
                start_time = time.time()
                lowest_price_in_txt = 0
                while True:
                    time_get = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                    now_time = time.time()
                    if len(price_elements) > 1:
                        goods_id = driver.current_url.split('/')[-1]
                        if not os.path.exists('txt/' + str(goods_id) + '.txt'):
                            f = open('txt/' + str(goods_id) + '.txt', 'w', encoding='utf-8')
                            f.close()
                        with open('txt/' + str(goods_id) + '.txt', 'a+', encoding='utf-8') as f:
                            lowest_price = price_elements[1]
                            price = float(lowest_price.text.replace("¥ ", ""))
                            name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                            f.seek(0)
                            lines = f.readlines()
                            if not lines:
                                f.write(str(goods_id) + ':' + str(price / 2) + '\n')
                            else:
                                first_line = lines[0]
                                expect_price = first_line.split(':')[1]
                                last_price = float(lines[-1].split('¥')[1].replace(" ", "").replace("\n", ""))
                                one_day_price = []
                                three_day_price = []
                                week_day_price = []
                                month_price = []
                                days = [1, 3, 7, 30]
                                lines.pop(0)
                                lowest_price_in_txt = 100000

                                for line in lines:
                                    price_data = line.split(';')
                                    # 获取 当前时间并计算与文本时间差
                                    old_time_str = price_data[0].replace('\n', '')
                                    old_time = datetime.datetime.strptime(old_time_str, "%Y-%m-%d %H:%M:%S")
                                    now_time = datetime.datetime.utcnow()
                                    diff_time = now_time - old_time
                                    # # 获取对应天数的历史价格
                                    if lowest_price_in_txt > float(
                                            price_data[1].split('¥')[1].replace(" ", "").replace("\n", "")):
                                        lowest_price_in_txt = float(
                                            price_data[1].split('¥')[1].replace(" ", "").replace("\n", ""))
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
                                day_send_mail(lowest_price, lowest_price_in_txt, name_elements, url, price, one_day_price)
                                three_day_send_mail(lowest_price, lowest_price_in_txt, name_elements, url, price, three_day_price)
                                week_send_mail(lowest_price, lowest_price_in_txt, name_elements, url, price, week_day_price)
                                month_send_mail(lowest_price, lowest_price_in_txt, name_elements, url, price, month_price)
                                if price <= float(expect_price) and lowest_price_in_txt > 0:
                                    print(
                                        f'{time_get} :{name_elements.text.splitlines()[2]} 的最低价格达到期望值, 当前价格是: {lowest_price.text} the lowest price in record is:{lowest_price_in_txt}')
                                    send_mail(
                                        name_elements.text.splitlines()[2] + '\nthe lowest price in record is' + str(
                                            lowest_price_in_txt), lowest_price.text,
                                        'https://buff.163.com/goods/' + url)
                                else:
                                    print(
                                        f'{time_get} :{name_elements.text.splitlines()[2]} 的最低价格未达到期望值, 当前价格是: {lowest_price.text}')
                                if last_price == price:
                                    break

                            f.write(f'{time_get};{name_elements.text.splitlines()[2]} {lowest_price.text}\n')
                            f.close()
                            break
                    elif now_time - start_time > 20:
                        print(f'{time_get} :{url} 超时')
                        driver.refresh()
                        start_time = time.time()
                time.sleep(5)

            except WebDriverException as e:
                crash_time = 0
                print(e)
                send_mail("need to reboot chroot container", 0, '111')
                while True:
                    try:
                        if crash_time == 2:
                            time.sleep(600)
                        else:
                            time.sleep(20)
                        driver = webdriver.Chrome(chrome_options=chrome_options,
                                                  executable_path="/usr/bin/chromedriver")
                        driver.get('https://buff.163.com/goods/' + url)
                        break
                    except:
                        crash_time += 1
            except Exception as e:
                print(e)
                print('网络连接断开,等待网络恢复...')

                while True:
                    try:
                        time.sleep(10)
                        driver.refresh()
                        break
                    except:
                        pass
        time.sleep(60)


def send_mail(name, price, url):
    # 邮件内容
    message = f'{name} \n当前价格为{price}\n链接为{url}'

    # 构造邮件内容,设置编码为gbk,格式为html
    msg = MIMEText(message, 'html', 'utf-8')

    # 发信方的信息:发信邮箱,密码
    from_addr = 'a907993029@163.com'
    password = 'ZVDXBZPBIPTSMYGX'

    # 收信方邮箱
    to_addr = '1094410998@qq.com'

    # 发信服务器
    smtp_server = 'smtp.163.com'

    # SMTP协议默认端口
    smtp_port = 25

    # 设置Content-Type头部也为gbk编码
    msg['Content-Type'] = 'text/html; charset=utf-8'

    # 设置邮件标题
    msg['Subject'] = Header('价格提醒', 'utf-8')

    # 告知邮件服务内容
    msg['Content-Transfer-Encoding'] = 'base64'

    # 发送邮件
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.login(from_addr, password)
    gbk_msg = msg.as_bytes().decode('utf-8')  # 解码msg为gbk字符串
    server.sendmail(from_addr, to_addr, gbk_msg)
    server.quit()


threads = []
urls = []
mail = {}
files = os.listdir('../source')
for file in files:
    with open('source/' + file) as f:
        urls = f.readlines()
    f.close()
    thread = threading.Thread(target=get_all, args=([urls]))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
    time.sleep(5)
