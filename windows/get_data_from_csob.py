import json
import os
import threading
import time
import traceback
from threading import Thread

import brotli
from selenium.common import StaleElementReferenceException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm
import buff_sql
import insert_data_from_csob

options = webdriver.FirefoxOptions()
# 去掉"chrome正受到自动化测试软件的控制"的提示条
# options.add_argument('--headless')
options.add_argument("--lang=zh_CN")
options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

lock = threading.Lock()
lock1 = threading.Lock()


def data_insert(good_id, times, prices, pl):
    pbar = tqdm(total=len(times), dynamic_ncols=True)
    time.sleep(1)
    for index, (t) in enumerate(times):
        time_stamp = t
        time_array = time.localtime(float(time_stamp) / 1000)
        record_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        price = str(prices[index])
        price = price[:-2] + '.' + price[-2:]  # 在price后两位前加上一个小数点
        if pl == 0:
            buff_sql.write_record(record_time, good_id, price, 'buff')
        elif pl == 1:
            buff_sql.write_record(record_time, good_id, price, 'uu')
        elif pl == 2:
            buff_sql.write_record(record_time, good_id, price, 'igxe')
        elif pl == 3:
            buff_sql.write_record(record_time, good_id, price, 'c5')
        pbar.update(1)
        time.sleep(1)
        pbar.set_description(f"商品{good_id},平台{pl}")
    pbar.close()


def get_json(goods):
    # print("json len", len(json1))
    # is_first = True
    browser = webdriver.Firefox(service=Service('webdriver/geckodriver.exe'),
                                options=options)
    browser.scopes = [
        '.*/api/v2/goods/chart',
    ]
    first = True
    browser.set_page_load_timeout(300)
    pbar = tqdm(total=len(goods), dynamic_ncols=True)
    for index, (goods_id, trend, name, category, img_url, now_price_buff, the_lowest_price_buff, wear_tear_group,
                the_lowest_price_uu, the_lowest_price_igxe, the_lowest_price_c5, now_price_uu, now_price_igxe,
                now_price_c5, now_price_steam, update_time, uu_id, igxe_id, c5_id, csob_update_time) in enumerate(
        goods):
        if csob_update_time is not None and igxe_id is not None:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if now[:10] == csob_update_time[:10]:
                pbar.set_description(f"{now}: 商品{name}今日已经爬取过不再爬取")
                pbar.update(1)
                continue
        mode_change = False
        del browser.requests
        while True:
            try:
                if (not mode_change and '胶囊' in category or '武器箱' in category or '音乐盒' in category or
                        category == '探员' or category == '金色' or category == '全息'):
                    if name == '音乐盒（StatTrak™） | Neck Deep - 躺平青年':
                        name = '音乐盒（StatTrak） | Neck Deep, 躺平青年'
                    elif '印花 | 玛丽埃塔（全息）' in name:
                        name = '印花 | 玛丽埃塔'
                        break
                    elif '印花 | 大家动起来（全息）' in name:
                        name = '印花 | 大家动起来'
                        break
                    if '—' in name:
                        name = name.replace('—', "-")
                    browser.get('https://csgoob.onet4p.net/goods?name=' + name)
                    browser.get('https://csgoob.onet4p.net/goods?name=' + name)

                else:
                    while True:
                        if name == '音乐盒（StatTrak™） | Neck Deep - 躺平青年':
                            name = '音乐盒（StatTrak） | Neck Deep, 躺平青年'
                        elif '印花 | 玛丽埃塔（全息）' in name:
                            name = '印花 | 玛丽埃塔'

                        elif '印花 | 大家动起来（全息）' in name:
                            name = '印花 | 大家动起来'
                        elif '音乐盒（StatTrak） | Neck Deep, 躺平青年' in name:
                            name = '音乐盒（StatTrak™） | Neck Deep - 躺平青年'
                        elif '印花 | Hobbit（全息）| 2022年里约热内卢锦标赛' in name:
                            name = '印花 | Hobbit（全息）| 2022年里约热内卢锦标赛'
                        elif '印花 | iM（全息）| 2024年哥本哈根锦标赛' in name:
                            break
                        browser.get('https://csgoob.onet4p.net/search')

                        if "(" in name and len(name.split("(")[1]) > 3:
                            search_name = name.split("(")[0]
                        else:
                            search_name = name
                        browser.find_element(By.CLASS_NAME,
                                             'el-input.el-input--large.el-input--suffix.w-full.h-10.lg\\:h-14').find_element(
                            By.CLASS_NAME, "el-input__inner").send_keys(
                            search_name.replace('*', '').replace("$", "").replace('Hobbit', 'Hobbi'))
                        time.sleep(3)
                        if len(browser.find_elements(By.CLASS_NAME,
                                                     'el-input__suffix-inner')) > 1:
                            browser.find_elements(By.CLASS_NAME,
                                                  'el-input__suffix-inner')[1].click()
                        else:
                            continue
                        time.sleep(3)
                        search_result_names = browser.find_elements(By.CLASS_NAME,
                                                                    'w-full.px-3.py-3')
                        for search_result_name in search_result_names:
                            name_text = search_result_name.find_element(By.TAG_NAME, "a")
                            if name_text.text == name:
                                name_text.click()
                                break
                        # try:
                        #     WebDriverWait(browser, 10, 0.5).until(ec.presence_of_all_elements_located(
                        #         (By.CLASS_NAME, 'mt-2.lg\\:mt-4.grid.grid-cols-2.gap-2.lg\\:gap-4')))
                        #     time.sleep(3)
                        #     # ActionChains(browser).move_to_element(
                        #     #     browser.find_element(By.CLASS_NAME, 'flex.items-baseline.gap-2')).pause(
                        #     #     0.5).perform()
                        # except TimeoutException as e:
                        #     print(e)
                        #     print(traceback.format_exc())
                        #     # pbar.update(1)
                        #     now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        #     # pbar.set_description(f"{now}: 商品{name}爬取失败")
                        #     break
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
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                continue
            while True:
                try:
                    try:
                        # WebDriverWait(browser, 10, 0.5).until(ec.presence_of_all_elements_located(
                        #     (By.CLASS_NAME, 'flex.items-baseline.gap-2')))
                        time.sleep(3)
                    except TimeoutException:
                        print("TimeoutException")
                        if ('胶囊' in category or '武器箱' in category or '音乐盒' in category or category == '探员' or
                                category == '金色' or category == '全息'):
                            mode_change = True
                        break
                    except Exception as e:
                        print(e)
                        print(traceback.format_exc())
                        break
                    now_prices_div = browser.find_elements(By.CLASS_NAME,
                                                           'w-full.p-4.bg-color-bg-secondary.rounded-lg.transition'
                                                           '-colors.truncate')
                    if len(now_prices_div) < 1:
                        pbar.update(1)
                        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        buff_sql.update_csob_update_time(goods_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                        pbar.set_description(f"{now}: 商品{name}爬取中")
                        break
                    buff_exist = False
                    uu_exist = False
                    igxe_exist = False
                    c5_exist = False
                    exist_pl_count = 0
                    for div in now_prices_div:
                        pl = div.find_element(By.CLASS_NAME,
                                              'flex.items-center.justify-between.overflow-hidden').find_element(
                            By.TAG_NAME, 'a')
                        now = \
                            div.find_element(By.CLASS_NAME,
                                             'mt-2.lg\\:mt-3.flex.flex-col.gap-1.lg\\:gap-2.text-sm').find_elements(
                                By.TAG_NAME, 'div')[0].text.replace(
                                '¥ ',
                                '')
                        if pl.text == '悠悠有品':
                            buff_sql.update_good_with_now_price_uu(goods_id, now)
                            uu_exist = True
                            exist_pl_count += 1
                        elif pl.text == 'IGXE':
                            buff_sql.update_good_with_now_price_igxe(goods_id, now)
                            igxe_exist = True
                            exist_pl_count += 1
                        elif pl.text == 'C5':
                            buff_sql.update_good_with_now_price_c5(goods_id, now)
                            c5_exist = True
                            exist_pl_count += 1
                        elif pl.text == 'BUFF':
                            buff_sql.update_good_with_now_price_buff(goods_id, now)
                            buff_exist = True
                            exist_pl_count += 1
                    if not igxe_exist:
                        buff_sql.set_good_with_igxe_id(goods_id, 0)
                    if (browser.find_element(By.CLASS_NAME,
                                             'el-select__selected-item.el-select__placeholder').find_element(
                        By.TAG_NAME,
                        "span").text
                            != '全部'):  #and csob_update_time is None
                        select_icon = browser.find_element(By.CLASS_NAME, 'el-icon.el-select__caret.el-select__icon')
                        browser.execute_script("arguments[0].click()", select_icon)
                        del browser.requests
                        all_select = browser.find_elements(By.CLASS_NAME, 'el-select-dropdown__item')[6]
                        browser.execute_script("arguments[0].click()", all_select)
                    pl = browser.find_element(By.CLASS_NAME, 'text-base.mr-1.hidden.xs\\:inline.whitespace-nowrap').text
                    pl_select_icon = browser.find_element(By.CLASS_NAME, 'el-icon.text-xs')
                    browser.execute_script("arguments[0].click()", pl_select_icon)
                    for pl_select in browser.find_elements(By.CLASS_NAME, 'el-dropdown-menu__item'):
                        if exist_pl_count > 0:
                            if pl_select.find_element(By.TAG_NAME, "span").text != pl:
                                browser.execute_script("arguments[0].click()", pl_select)
                                time.sleep(5)
                                exist_pl_count -= 1
                        else:
                            break
                    time.sleep(3)
                    for request in browser.requests:
                        if '/api/v2/goods/chart' in request.url:
                            json_request_body = json.loads(str(request.body).replace("b'", "").replace("'", ""))
                            pl = json_request_body['platform']
                            json_goods_id = json_request_body['goodsId']
                            # print('pl:' + str(pl) + 'goodsId:' + str(json_goods_id))
                            # print(request.response.headers.get("Content-Encoding"))  # 非常重要的编码识别
                            if request.response is not None:
                                if request.response.headers.get(
                                        "Content-Encoding") == 'br':
                                    decompressed_data = brotli.decompress(request.response.body)
                                    json_str = decompressed_data.decode('utf-8').replace("b'", "").replace("'", "")
                                else:
                                    json_str = request.response.body.decode('utf-8')
                                json_d = json.loads(str(json_str).replace("b'", "").replace("'", ""))
                                time_stamps = json_d['data']['list'][0]
                                prices = json_d['data']['list'][1]
                                # print(len(time_stamps), len(prices))
                                if pl == 0:
                                    pass
                                    # with lock:
                                    #     with open('already_record.txt', 'a+', encoding='utf-8') as a:
                                    #         a.write(str(goods_id) + '\n')
                                    pbar.update(1)
                                    pbar.set_description(f"商品{name}爬取完成")
                                elif pl == 1:
                                    buff_sql.set_good_with_uu_id(goods_id, json_goods_id)
                                elif pl == 2:
                                    buff_sql.set_good_with_igxe_id(goods_id, json_goods_id)
                                elif pl == 3:
                                    buff_sql.set_good_with_c5_id(goods_id, json_goods_id)
                                Thread(target=data_insert, args=(goods_id, time_stamps, prices, pl)).start()
                    time.sleep(1)
                    mode_change = False
                    buff_sql.update_good_update_time(goods_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    buff_sql.update_csob_update_time(goods_id, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
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
                except Exception as e:
                    print(e)
                    print(traceback.format_exc())
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
# with open('already_insert_goods_id.txt', 'a+', encoding='utf-8') as f:
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
thread_count = 1
urls_per_thread = len(all_goods) // thread_count
for i in range(thread_count):
    start = i * urls_per_thread
    end = start + urls_per_thread if i < thread_count - 1 else len(all_goods)
    sublist = list(all_goods)[start:end]
    Thread(target=get_json, args=(sublist,)).start()  # 使用元组传递参数
    time.sleep(5)
