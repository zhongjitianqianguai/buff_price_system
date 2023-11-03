import json
import threading
import time
from threading import Thread
from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import buff_sql

options = Options()
# 去掉"chrome正受到自动化测试软件的控制"的提示条
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--no-sandbox")
options.add_argument("--lang=zh_CN")
browser = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
browser.scopes = [
    '.*/api/v1/goods/chart',
]
browser.set_page_load_timeout(300)
lock = threading.Lock()


def write_sql(json_data):
    for datas in json_data['data']['list']:
        platform = datas['platform']
        for data in datas['data']:
            if platform == 0:
                timeStamp = data[0]
                timeArray = time.localtime(timeStamp)
                record_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                price = str(data[1])
                price = price[:-2] + '.' + price[-2:]  # 在price后两位前加上一个小数点
                if the_lowest_price_buff is None:
                    buff_sql.update_good_lowest_price(goods_id, price, 'buff')
                elif float(price) < float(the_lowest_price_buff):
                    buff_sql.update_good_lowest_price(goods_id, price, 'buff')
                # f.write(
                #     "INSERT INTO buff_record(time,goods_id,price,source) SELECT '" +
                #     record_time + "','" + goods_id + "','" + price + "','buff' FROM buff_record WHERE NOT EXISTS(SELECT * FROM buff_record WHERE time = '" +
                #     record_time + "' AND goods_id = '" + goods_id + "' AND price = '" + price + "' AND source = 'buff');\n")
                sql = "INSERT INTO buff_record(time,goods_id,price,source) value('" + record_time + "','" + goods_id + "','" + price + "','buff'); \n"

            elif platform == 1:
                timeStamp = data[0]
                timeArray = time.localtime(timeStamp)
                record_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                price = str(data[1])
                price = price[:-2] + '.' + price[-2:]
                if the_lowest_price_uu is None:
                    buff_sql.update_good_lowest_price(goods_id, price, 'uu')
                elif float(price) < float(the_lowest_price_uu):
                    buff_sql.update_good_lowest_price(goods_id, price, 'uu')
                # f.write( "INSERT INTO buff_record(time,goods_id,price,source) SELECT '"
                # + record_time + "','" + goods_id + "','" + price + "','uu' FROM
                # buff_record WHERE NOT EXISTS(SELECT * FROM buff_record WHERE time = '"
                # + record_time + "' AND goods_id = '" + goods_id + "' AND price = '" +
                # price + "' AND source = 'uu');\n")
                sql = "INSERT INTO buff_record(time,goods_id,price,source) value('" + record_time + "','" + goods_id + "','" + price + "','uu'); \n"

            elif platform == 2:
                timeStamp = data[0]
                timeArray = time.localtime(timeStamp)
                record_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                price = str(data[1])
                price = price[:-2] + '.' + price[-2:]
                if the_lowest_price_igxe is None:
                    buff_sql.update_good_lowest_price(goods_id, price, 'igxe')
                elif float(price) < float(the_lowest_price_igxe):
                    buff_sql.update_good_lowest_price(goods_id, price, 'igxe')
                # f.write(
                #     "INSERT INTO buff_record(time,goods_id,price,source) SELECT '" +
                #     record_time + "','" + goods_id + "','" + price + "','igxe' FROM buff_record WHERE NOT EXISTS(SELECT * FROM buff_record WHERE time = '" +
                #     record_time + "' AND goods_id = '" + goods_id + "' AND price = '" + price + "' AND source = 'igxe');\n")
                sql = "INSERT INTO buff_record(time,goods_id,price,source) value('" + record_time + "','" + goods_id + "','" + price + "','igxe'); \n"

            elif platform == 3:
                timeStamp = data[0]
                timeArray = time.localtime(timeStamp)
                record_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                price = str(data[1])
                price = price[:-2] + '.' + price[-2:]
                if the_lowest_price_c5 is None:
                    buff_sql.update_good_lowest_price(goods_id, price, 'c5')
                elif float(price) < float(the_lowest_price_c5):
                    buff_sql.update_good_lowest_price(goods_id, price, 'c5')
                # f.write(
                #     "INSERT INTO buff_record(time,goods_id,price,source) SELECT '" +
                #     record_time + "','" + goods_id + "','" + price + "','c5' FROM buff_record WHERE NOT EXISTS(SELECT * FROM buff_record WHERE time = '" +
                #     record_time + "' AND goods_id = '" + goods_id + "' AND price = '" + price + "' AND source = 'c5');\n")
                sql = "INSERT INTO buff_record(time,goods_id,price,source) value('" + record_time + "','" + goods_id + "','" + price + "','c5'); \n"
            with lock:
                with open('buff_record_expand.sql', 'a+') as f:
                    all_sql = f.readlines()
                    if sql not in all_sql:
                        f.write(sql)


# def data_insert(da, pl):
#     for d in da:
#         timeStamp = d[0]
#         timeArray = time.localtime(timeStamp)
#         record_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
#         price = str(d[1])
#         price = price[:-2] + '.' + price[-2:]  # 在price后两位前加上一个小数点
#         if pl == 'buff':
#             if the_lowest_price_buff is not None and float(price) < the_lowest_price_buff:
#                 buff_sql.update_good_lowest_price(goods_id, price, pl)
#             elif the_lowest_price_buff is None:
#                 buff_sql.update_good_lowest_price(goods_id, price, pl)
#         elif pl == 'uu':
#             if the_lowest_price_uu is not None and float(price) < the_lowest_price_uu:
#                 buff_sql.update_good_lowest_price(goods_id, price, pl)
#             elif the_lowest_price_uu is None:
#                 buff_sql.update_good_lowest_price(goods_id, price, pl)
#         elif pl == 'igxe':
#             if the_lowest_price_igxe is not None and float(price) < the_lowest_price_igxe:
#                 buff_sql.update_good_lowest_price(goods_id, price, pl)
#             elif the_lowest_price_igxe is None:
#                 buff_sql.update_good_lowest_price(goods_id, price, pl)
#         elif pl == 'c5':
#             if the_lowest_price_c5 is not None and float(price) < the_lowest_price_c5:
#                 buff_sql.update_good_lowest_price(goods_id, price, pl)
#             elif the_lowest_price_c5 is None:
#                 buff_sql.update_good_lowest_price(goods_id, price, pl)
#         buff_sql.write_record(record_time, goods_id, price, pl)


all_goods = buff_sql.get_all_goods()

for (goods_id, trend, name, category, img_url, now_price_buff, the_lowest_price_buff, wear_tear_group,
     the_lowest_price_uu,
     the_lowest_price_igxe, the_lowest_price_c5, now_price_uu, now_price_igxe, now_price_c5,
     now_price_steam) in all_goods:
    while True:
        try:
            browser.get('http://csgoob.onet4p.net/goods?name=' + name)
            WebDriverWait(browser, 60, 0.5).until(ec.presence_of_all_elements_located(
                (By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]/span[3]')))
            time.sleep(3)
            spans = browser.find_elements(By.TAG_NAME, 'span')
            for span in spans:
                if span.text == 'Buff':
                    browser.execute_script("arguments[0].click()", span)
                    break
            time.sleep(3)
            spans = browser.find_elements(By.TAG_NAME, 'span')

            for span in spans:
                if span.text == '总览':
                    browser.execute_script("arguments[0].click()", span)
                    break
            time.sleep(3)
            browser.requests.clear()
            spans = browser.find_elements(By.TAG_NAME, 'span')
            for span in spans:
                if span.text == '近7天':
                    browser.execute_script("arguments[0].click()", span)
                    break
            time.sleep(3)
            spans = browser.find_elements(By.TAG_NAME, 'span')
            for span in spans:
                if span.text == '自定义时间':
                    browser.execute_script("arguments[0].click()", span)
                    break

            time.sleep(1)
            browser.find_elements(By.CSS_SELECTOR, 'input[placeholder="请选择月份"]')[0].send_keys('2022/06')
            browser.find_elements(By.CSS_SELECTOR, 'input[placeholder="请选择月份"]')[1].send_keys('2023/05')
            browser.find_elements(By.CSS_SELECTOR, 'input[placeholder="请选择月份"]')[1].send_keys('\n')
            time.sleep(3)
            spans = browser.find_elements(By.TAG_NAME, 'span')
            browser.requests.clear()
            for span in spans:
                if span.text == '确 认':
                    browser.execute_script("arguments[0].click()", span)
                    break
            time.sleep(5)

            for request in browser.requests:
                if '/api/v1/goods/chart' in str(request):
                    # print(request.response.headers.get("Content-Encoding"))  # 非常重要的编码识别
                    # decompressed_data = brotli.decompress(request.response.body)  # br解压 br编码
                    # json_str = decompressed_data.decode('utf-8').replace("b'", "").replace("'", "")
                    if request.response is not None:
                        json_str = request.response.body.decode('utf-8').replace("b'", "").replace("'", "")
                        if '"platform":1' in json_str:
                            # print(json_str)
                            json_data = json.loads(str(json_str))
                            # print(len(json_data['data']['list'][0]['data']))
                            if json_data['data']['list'][0]['data'][-1][0] > 1698204471:
                                continue
                            t = Thread(target=write_sql, args=(json_data,))
                            t.start()
                            # urls_per_thread = len(datas['data']) // 3
                            # for i in range(3):
                            #     start = i * urls_per_thread
                            #     end = start + urls_per_thread if i < 3 - 1 else len(datas['data'])
                            #     sublist = datas['data'][start:end]
                            #     if platform == 0:
                            #         # th = Thread(target=data_insert, args=(sublist, 'buff'))
                            #         pass
                            #     elif platform == 1:
                            #         th = Thread(target=data_insert, args=(sublist, 'uu'))
                            #     elif platform == 2:
                            #         th = Thread(target=data_insert, args=(sublist, 'igxe'))
                            #     elif platform == 3:
                            #         th = Thread(target=data_insert, args=(sublist, 'c5'))
                            #     th.start()
            time.sleep(1)
            break
        except StaleElementReferenceException as e:
            continue
        except NoSuchElementException as e:
            continue
        except IndexError as e:
            continue
        except TimeoutException as e:
            continue
