import json
import os
import threading
import time
import traceback
from threading import Thread

import brotli
from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm
import buff_sql

options = webdriver.FirefoxOptions()
# 去掉"chrome正受到自动化测试软件的控制"的提示条
# options.add_argument('--headless')
options.add_argument("--lang=zh_CN")
options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

lock = threading.Lock()
lock1 = threading.Lock()


def data_insert(good_id, da, pl):
    # the_lowest_price_buff = buff_sql.get_good_lowest_price(good_id, 'buff')
    # the_lowest_price_uu = buff_sql.get_good_lowest_price(good_id, 'uu')
    # the_lowest_price_igxe = buff_sql.get_good_lowest_price(good_id, 'igxe')
    # the_lowest_price_c5 = buff_sql.get_good_lowest_price(good_id, 'c5')
    pbar = tqdm(total=len(da), dynamic_ncols=True)
    time.sleep(10)
    for d in da:
        # print(d)
        timeStamp = d[0]
        timeArray = time.localtime(timeStamp)
        record_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        price = str(d[1])
        price = price[:-2] + '.' + price[-2:]  # 在price后两位前加上一个小数点
        # if pl == 'buff':
        #     if the_lowest_price_buff is not None and float(price) < the_lowest_price_buff:
        #         buff_sql.update_good_lowest_price(good_id, price, pl)
        #     elif the_lowest_price_buff is None:
        #         buff_sql.update_good_lowest_price(good_id, price, pl)
        # elif pl == 'uu':
        #     if the_lowest_price_uu is not None and float(price) < the_lowest_price_uu:
        #         buff_sql.update_good_lowest_price(good_id, price, pl)
        #     elif the_lowest_price_uu is None:
        #         buff_sql.update_good_lowest_price(good_id, price, pl)
        # elif pl == 'igxe':
        #     if the_lowest_price_igxe is not None and float(price) < the_lowest_price_igxe:
        #         buff_sql.update_good_lowest_price(good_id, price, pl)
        #     elif the_lowest_price_igxe is None:
        #         buff_sql.update_good_lowest_price(good_id, price, pl)
        # elif pl == 'c5':
        #     if the_lowest_price_c5 is not None and float(price) < the_lowest_price_c5:
        #         buff_sql.update_good_lowest_price(good_id, price, pl)
        #     elif the_lowest_price_c5 is None:
        #         buff_sql.update_good_lowest_price(good_id, price, pl)
        # with open('already_record.txt', 'a+', encoding='utf-8') as a:
        # already_recorded = a.readlines()
        buff_sql.write_record(record_time, good_id, price, pl)
        pbar.update(1)
        time.sleep(1)
        pbar.set_description(f"商品{good_id},平台{pl}")
    pbar.close()


def get_json(goods, recorded):
    # print("json len", len(json1))
    # is_first = True
    browser = webdriver.Firefox(service=Service('webdriver/geckodriver.exe'),
                                options=options)
    browser.scopes = [
        '.*/api/v1/goods/chart',
    ]
    browser.set_page_load_timeout(300)
    pbar = tqdm(total=len(goods), dynamic_ncols=True)
    for index, (goods_id, trend, name, category, img_url, now_price_buff, the_lowest_price_buff, wear_tear_group,
                the_lowest_price_uu, the_lowest_price_igxe, the_lowest_price_c5, now_price_uu, now_price_igxe,
                now_price_c5,
                now_price_steam, update_time) in enumerate(goods):
        if str(goods_id) + '\n' in recorded:
            pbar.update(1)
            pbar.set_description(f"商品{name}爬取中")
            continue
        if '印花' not in name:
            continue
        mode_change = False
        while True:
            try:
                if (not mode_change and '胶囊' in category or '武器箱' in category or '音乐盒' in category or
                        category == '探员' or category == '金色' or category == '全息'):
                    if name == '音乐盒（StatTrak™） | Neck Deep - 躺平青年':
                        name = '音乐盒（StatTrak） | Neck Deep, 躺平青年'
                    if '—' in name:
                        name = name.replace('—', "-")
                    browser.get('https://csgoob.onet4p.net/goods?name=' + name)
                else:
                    while True:
                        browser.get('https://csgoob.onet4p.net/search')

                        if "(" in name and len(name.split("(")[1]) > 3:
                            search_name = name.split("(")[0]
                        else:
                            search_name = name
                        browser.find_elements(By.XPATH,
                                              '/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/div/span['
                                              '1]/span/span/input')[0].send_keys(search_name)
                        time.sleep(1)
                        browser.find_elements(By.XPATH,
                                              '/html/body/div[1]/div[5]/div/div[1]/div[1]/div[2]/div/span['
                                              '1]/span/span/input')[0].send_keys('\n')
                        time.sleep(3)
                        search_result_names = browser.find_elements(By.CLASS_NAME,
                                                                    'w-full.h-full.text-center.flex.flex-col'
                                                                    '.justify-center.items-center')
                        for search_result_name in search_result_names:
                            name_text = search_result_name.find_element(By.TAG_NAME, "span")
                            if name_text.text == name:
                                name_text.click()
                                break
                        try:
                            WebDriverWait(browser, 10, 0.5).until(ec.presence_of_all_elements_located(
                                (By.CLASS_NAME, 'text-lg.text-orange-400.mr-2.font-bold')))
                            time.sleep(3)
                            ActionChains(browser).move_to_element(
                                browser.find_element(By.CLASS_NAME,
                                                     'text-lg.text-orange-400.mr-2.font-bold')).pause(
                                0.5).perform()
                        except TimeoutException:
                            break
                        time.sleep(1)
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
                print(traceback.format_exc())
                print(e)
                continue
            except WebDriverException as e:
                print(e)
                print(traceback.format_exc())

                # is_first = True
                continue
            while True:
                try:
                    try:
                        WebDriverWait(browser, 10, 0.5).until(ec.presence_of_all_elements_located(
                            (By.CLASS_NAME, 'text-lg.text-orange-400.mr-2.font-bold')))
                        time.sleep(3)
                        ActionChains(browser).move_to_element(
                            browser.find_element(By.CLASS_NAME, 'text-lg.text-orange-400.mr-2.font-bold')).pause(
                            0.5).perform()
                    except TimeoutException:
                        if ('胶囊' in category or '武器箱' in category or '音乐盒' in category or category == '探员' or
                                category == '金色' or category == '全息'):
                            mode_change = True
                        break
                    now_prices_div = browser.find_element(By.CLASS_NAME, 'ant-tooltip-inner').find_elements(By.TAG_NAME,
                                                                                                            'div')
                    if len(now_prices_div) < 2:
                        with lock:
                            with open('already_record.txt', 'a+', encoding='utf-8') as a:
                                a.write(str(goods_id) + '\n')
                        pbar.update(1)
                        pbar.set_description(f"商品{name}爬取中")
                        break
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

                    # if is_first:
                    #     is_first = False
                    #     time.sleep(1)
                    # spans = browser.find_elements(By.TAG_NAME, 'span')
                    # for span in spans:
                    #     if span.text == '近7天':
                    #         browser.execute_script("arguments[0].click()", span)
                    #         break
                    # time.sleep(3)
                    # spans = browser.find_elements(By.TAG_NAME, 'span')
                    # for span in spans:
                    #     if span.text == '自定义时间':
                    #         browser.execute_script("arguments[0].click()", span)
                    #         break
                    # time.sleep(1)
                    # browser.find_elements(By.CSS_SELECTOR, 'input[placeholder="请选择月份"]')[0].send_keys('2022/06')
                    # browser.find_elements(By.CSS_SELECTOR, 'input[placeholder="请选择月份"]')[1].send_keys('2023/05')
                    # browser.find_elements(By.CSS_SELECTOR, 'input[placeholder="请选择月份"]')[1].send_keys('\n')
                    # time.sleep(3)
                    # spans = browser.find_elements(By.TAG_NAME, 'span')
                    # for span in spans:
                    #     if span.text == '确 认':
                    #         browser.execute_script("arguments[0].click()", span)
                    #         break
                    # time.sleep(3)

                    spans = browser.find_elements(By.TAG_NAME, 'span')
                    is_time_want_already = False
                    for span in spans:
                        if span.text == '近7天':
                            browser.execute_script("arguments[0].click()", span)
                            break
                        elif span.text == '近6个月':
                            is_time_want_already = True
                            break
                    time.sleep(1)
                    if not is_time_want_already:
                        spans = browser.find_elements(By.TAG_NAME, 'span')
                        for span in spans:
                            if span.text == '近6个月':
                                browser.execute_script("arguments[0].click()", span)
                                break
                        time.sleep(3)
                    browser.requests.clear()
                    spans = browser.find_elements(By.TAG_NAME, 'span')
                    for span in spans:
                        if span.text == 'BUFF':
                            browser.execute_script("arguments[0].click()", span)
                            break
                    time.sleep(3)
                    lis = browser.find_elements(By.CLASS_NAME,
                                                'ant-dropdown-menu-item.ant-dropdown-menu-item-only-child')
                    for li in lis:
                        spans = li.find_elements(By.TAG_NAME, 'span')
                        for span in spans:
                            if span.text == '总览':
                                browser.execute_script("arguments[0].click()", span)
                                break
                    time.sleep(3)
                    for request in browser.requests:
                        if '/api/v1/goods/chart' in str(request):
                            # print(request.response.headers.get("Content-Encoding"))  # 非常重要的编码识别
                            # decompressed_data = brotli.decompress(request.response.body)  # br解压 br编码
                            # json_str = decompressed_data.decode('utf-8').replace("b'", "").replace("'", "")
                            if request.response is not None:
                                json_str = request.response.body.decode('utf-8').replace("b'", "").replace("'", "")
                                # print(json_str)
                                if (
                                        '"platform":1' in json_str or '"platform":2' in json_str or '"platform":3' in json_str
                                        and '"platform":0' in json_str):
                                    # print(json_str)
                                    json_d = json.loads(str(json_str))
                                    # len(json_d['data']['list'][0]['data'])
                                    for data in json_d['data']['list']:
                                        pl = data['platform']
                                        if pl == 0:
                                            if data['goodsId'] != str(goods_id):
                                                # print(data['goodsId'])
                                                # print(str(goods_id))
                                                # print('goods_id不匹配,不写入')
                                                break
                                            else:
                                                with lock1:
                                                    with open('2024_2_recent_6_month.txt', 'a+', encoding='utf-8') as a:
                                                        a.write(str(json_d) + '\n')
                                                # for data in json_d['data']['list']:
                                                #     platform = data['platform']
                                                #     print(goods_id, "数据长度", len(data['data']))
                                                #     if len(data['data']) > 1:
                                                #         if platform == 0:
                                                #             data_insert(goods_id, data['data'], 'buff')
                                                #
                                                #         elif platform == 1:
                                                #             data_insert(goods_id, data['data'], 'uu')
                                                #
                                                #         elif platform == 2:
                                                #             data_insert(goods_id, data['data'], 'igxe')
                                                #
                                                #         elif platform == 3:
                                                #             data_insert(goods_id, data['data'], 'c5')
                                                os.system("cls")
                                                with lock:
                                                    with open('already_record.txt', 'a+', encoding='utf-8') as a:
                                                        a.write(str(goods_id) + '\n')
                                                pbar.update(1)
                                                pbar.set_description(f"商品{name}爬取中")
                                                break
                        # last = json_d['data']['list'][-1]['data'][-1]
                        # print(last)
                        # timeStamp = last[0]
                        # timeArray = time.localtime(timeStamp)
                        # record_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                        # price = str(last[1])
                        # price = price[:-2] + '.' + price[-2:]  # 在price后两位前加上一个小数点
                        # platform = json_d['data']['list'][-1]['platform']
                        # if platform == 0:
                        #     platform = 'buff'
                        # elif platform == 1:
                        #     platform = 'uu'
                        # elif platform == 2:
                        #     platform = 'igxe'
                        # elif platform == 3:
                        #     platform = 'c5'
                        # if buff_sql.check_record(record_time, goods_id, price, platform):
                        #     continue
                        # Thread(target=handle_json, args=(json_d,)).start()
                    time.sleep(1)
                    mode_change = False
                    buff_sql.update_good_update_time(goods_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    break
                except StaleElementReferenceException as e:
                    # print(e)
                    # print(traceback.format_exc())
                    continue
                except NoSuchElementException as e:
                    # print(e)
                    # print(traceback.format_exc())
                    continue
                except IndexError as e:
                    # print(e)
                    # print(traceback.format_exc())
                    continue
                except TimeoutException as e:
                    # print(traceback.format_exc())
                    # print(e)
                    continue
                except WebDriverException as e:
                    # print(e)
                    # print(traceback.format_exc())

                    # is_first = True
                    continue
                finally:
                    pass
            if not mode_change:
                break
    browser.quit()
    pbar.close()


all_goods = buff_sql.get_all_goods()
# with open('json_data_22-06_23-05_and_year.txt', 'r', encoding='utf-8') as f:
#     json1 = f.readlines()
# already_record = set()
# with open('already_record_goods_id.txt', 'a+', encoding='utf-8') as f:
#     for line in json1:
#         json_d = json.loads(line)
#         for data in json_d['data']['list']:
#             if data['platform'] == 0:
#                 if str(data['goodsId']) not in already_record:
#                     already_record.add(data['goodsId'])
#                     f.write(str(data['goodsId']) + '\n')
with open('already_record.txt', 'r', encoding='utf-8') as f:
    already_record = f.readlines()
# for record in already_record:
#     already_record[already_record.index(record)] = record.replace('\n', '')
# print("已记录数据长度", len(json1) / 2)
thread_count = 10
urls_per_thread = len(all_goods) // thread_count
for i in range(thread_count):
    start = i * urls_per_thread
    end = start + urls_per_thread if i < thread_count - 1 else len(all_goods)
    sublist = list(all_goods)[start:end]
    Thread(target=get_json, args=(sublist, already_record)).start()
    time.sleep(1)
