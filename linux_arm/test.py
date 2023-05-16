import datetime
import os
import random
import smtplib
import threading
from email.header import Header
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.common import WebDriverException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pymysql

chrome_options = Options()
# chrome_options.add_argument('--headless')
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
        if daily_change >= 0.2:
            print(mail.get(url))
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements + '价格在一天内上涨超20% 具体涨幅为' + str(
                    daily_change) + ' the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements + '价格在一天内上涨超20% 具体涨幅为' + str(
                    daily_change) + 'the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
        elif daily_change < -0.2:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements + '价格在一天内下降超20% 具体涨幅为' + str(
                    daily_change) + 'the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                print("与上次发送邮件时的价格相同，不再发送邮件")
            else:
                mail[url] = price
                send_mail(name_elements + '价格在一天内下降超20% 具体涨幅为' + str(
                    daily_change) + 'the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
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
                send_mail(name_elements + '价格在三天内上涨30% 具体涨幅为' + str(
                    three_day_change) + ' the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements + '价格在三天内上涨30% 具体涨幅为' + str(
                    three_day_change) + 'the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)

        elif three_day_change < -0.3:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements + '价格在三天内下降30% 具体涨幅为' + str(
                    three_day_change) + 'the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements + '价格在三天内下降30% 具体涨幅为' + str(
                    three_day_change) + 'the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
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
                send_mail(name_elements + '价格在一周内上涨40% 具体涨幅为' + str(
                    week_change) + ' the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements + '价格在一周内上涨40% 具体涨幅为' + str(
                    week_change) + ' the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)

        elif week_change < -0.4:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements + '价格在一周内下降40% 具体涨幅为' + str(
                    week_change) + ' the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements + '价格在一周内下降40% 具体涨幅为' + str(
                    week_change) + ' the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
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
                              2] + '价格在一个月内上涨50% 具体涨幅为' + str(
                    month_change) + ' the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一个月内上涨50%  具体涨幅为' + str(
                    month_change) + 'the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)

        elif month_change < -0.5:
            if mail.get(url) is None:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一个月内上涨50%  具体涨幅为' + str(
                    month_change) + 'the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)
            elif mail.get(url) == price:
                pass
            else:
                mail[url] = price
                send_mail(name_elements.text.splitlines()[
                              2] + '价格在一个月内下降50% 具体涨幅为' + str(
                    month_change) + ' the lowest price in record is' + str(
                    lowest_price_in_txt),
                          lowest_price,
                          'https://buff.163.com/goods/' + url)


def write_record(conn,cursor, record_time, goods_id, price):
    try:
        sql = """Insert into buff_record(time,goods_id,price) value(%s,%s,%s)"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (record_time, goods_id, price))  # 添加参数
    except Exception as e:
        print("错误类型:", type(e))
        print("插入记录失败:", e)
        conn = pymysql.connect(
            host="192.168.6.169",
            port=3306,
            user="root",
            passwd="root",
            db="buff_price",
            charset='utf8',
            autocommit=True
        )
        cursor = conn.cursor()
        sql = """Insert into buff_record(time,goods_id,price) value(%s,%s,%s);"""
        cursor.execute(sql, (record_time, goods_id, price))  # 添加参数


def get_all_goods(conn,cursor):
    try:
        sql = """Select * from  buff_goods;"""
        conn.ping(reconnect=True)
        cursor.execute(sql)  # 添加参数
        return cursor.fetchall()

    except Exception as e:
        print("错误类型:", type(e))
        print("插入新商品失败失败:", e)
        conn = pymysql.connect(
            host="192.168.6.169",
            port=3306,
            user="root",
            passwd="root",
            db="buff_price",
            charset='utf8',
            autocommit=True
        )
        cursor = conn.cursor()
        sql = """Select * from  buff_goods;"""
        cursor.execute(sql)  # 添加参数
        return cursor.fetchall()


def add_new_good(conn,cursor, name, goods_id, category, except_price,img_url):
    try:
        sql = """Insert into buff_goods(name,goods_id,category,expected_price,img_url) value(%s,%s,%s,%s,%s);"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (name, goods_id, category, except_price,img_url))  # 添加参数
    except Exception as e:
        print("错误类型:", type(e))
        print("插入新商品失败失败:", e)
        conn = pymysql.connect(
            host="192.168.6.169",
            port=3306,
            user="root",
            passwd="root",
            db="buff_price",
            charset='utf8',
            autocommit=True
        )
        cursor = conn.cursor()
        sql = """Insert into buff_goods(name,goods_id,category,expected_price) value(%s,%s,%s,%s)"""
        cursor.execute(sql, (name, goods_id, category, except_price))  # 添加参数


def get_all(urls):
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/bin/chromedriver",
                              desired_capabilities=cap)
    driver.implicitly_wait(60)
    while True:
        for url in urls:
            sleep_time = 6
            try:
                driver.get('https://buff.163.com/goods/' + url)
                start_time = time.time()
                lowest_price_in_txt = 0
                time_get = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # if "429 Too Many Requests" in driver.find_element(By.TAG_NAME, "title").text:
                #     print("超时")
                #     time.sleep(2)
                #     driver.refresh()
                price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                img_url = driver.find_element(By.CLASS_NAME, "detail-pic").find_element(By.CLASS_NAME, "t_Center").find_element(By.TAG_NAME,"img").get_attribute("src")
                while len(price_elements) <= 1:
                    price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                    now_time = time.time()
                    name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                    if now_time - start_time > 20:
                        print(f'{time_get} :{url} 超时')
                        driver.refresh()
                        start_time = time.time()
                # lowest_price = price_elements[1]
                # price = float(lowest_price.replace("¥ ", ""))
                try:
                    price = float(price_elements[1].text.replace("¥ ", ""))
                    name_elements = driver.find_element(By.CLASS_NAME, "detail-cont")
                    name = name_elements.text.splitlines()[2]
                    category = name_elements.text.split("类型 |")[1].split("\n")[0]
                except StaleElementReferenceException as e:
                    print("try to handle element is not attached to the page document ")
                    try:
                        while True:
                            price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
                            while len(price_elements) <= 1:
                                price_elements = driver.find_elements(By.CLASS_NAME, "f_Strong")
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
                        add_new_good(conn,cursor, name, str(goods_id), category, str(price / 2),img_url)
                        goods_id_in_sql.append(goods_id)
                        write_record(conn,cursor, time_get, str(goods_id), str(price))
                        continue
                    else:
                        first_line = lines[0]
                        expect_price = first_line.split(':')[1]
                        if len(lines) == 1:
                            f.write(f'{time_get};{name} ¥ {price}\n')
                            continue
                        if goods_id not in goods_id_in_sql:
                            if "金色" in name:
                                category = "金色"
                            elif "全息" in name:
                                category = "全息"
                            elif "胶囊" in name:
                                category = "胶囊"
                            add_new_good(conn,cursor, name, str(goods_id), category, str(price / 2),img_url)

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

                        if price <= float(expect_price) and lowest_price_in_txt > 0:
                            print(
                                f'{goods_id}:{time_get} :{name} 的最低价格达到期望值, 当前价格是: {price} the lowest price in record is:{lowest_price_in_txt}')
                            send_mail(
                                name + '\nthe lowest price in record is' + str(
                                    lowest_price_in_txt), price,
                                'https://buff.163.com/goods/' + url)
                        else:
                            print(
                                f'{goods_id}:{time_get} :{name} 的最低价格未达到期望值, 当前价格是: {price}')
                        if last_price == price:
                            continue
                        f.write(f'{time_get};{name} ¥ {price}\n')
                        write_record(conn,cursor, time_get, str(goods_id), str(price))
                        f.close()

                        if time.localtime(time.time()).tm_hour.real < 1 or time.localtime(time.time()).tm_hour.real > 7:
                            day_send_mail(price, lowest_price_in_txt, name, url, price,
                                          one_day_price)
                            three_day_send_mail(price, lowest_price_in_txt, name, url, price,
                                                three_day_price)
                            week_send_mail(price, lowest_price_in_txt, name, url, price,
                                           week_day_price)
                            month_send_mail(price, lowest_price_in_txt, name, url, price,
                                            month_price)
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
                print("超时" + e.msg)
                time.sleep(sleep_time)
                continue
            except WebDriverException as e:
                crash_time = 0
                print(e)
                while True:
                    try:
                        if crash_time == 2:
                            time.sleep(600)
                            send_mail("need to reboot chroot container", 0, '111')

                        else:
                            time.sleep(20)
                        driver = webdriver.Chrome(chrome_options=chrome_options,
                                                  executable_path="/usr/bin/chromedriver")
                        driver.get('https://buff.163.com/goods/' + url)
                        sleep_time = random.randint(5, 15)
                        break
                    except:
                        crash_time += 1
            except Exception as e:
                print(e)
                print('网络连接断开,等待网络恢复...')
                if "please see" in str(e):
                    continue
                while True:
                    try:
                        time.sleep(10)
                        driver.refresh()
                        break
                    except:
                        pass
            finally:
                time.sleep(sleep_time)

        time.sleep(10)


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
# conn = pymysql.connect(
#     host="120.25.145.148",
#     port=3306,
#     user="homework",
#     passwd="root",
#     db="homework",
#     charset='utf8',
#     autocommit=True
# )
conn = pymysql.connect(
    host="192.168.6.169",
    port=3306,
    user="root",
    passwd="root",
    db="buff_price",
    charset='utf8',
    autocommit=True
)
cursor = conn.cursor()
goods_id_in_sql = []
all_goods_from_sql = get_all_goods(conn,cursor)
for goods in all_goods_from_sql:
    goods_id_in_sql.append(goods[0])
for file in files:
    with open('../source/' + file) as f:
        urls = f.readlines()
    f.close()
    thread = threading.Thread(target=get_all, args=([urls]))
    threads.append(thread)
    time.sleep(5)
    thread.start()

for thread in threads:
    thread.join()
