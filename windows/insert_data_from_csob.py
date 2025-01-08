import json
import os
import threading
import time
from threading import Thread
from tqdm import tqdm
import buff_sql

lock = threading.Lock()


def data_insert(good_id, da, pl, index):
    # the_lowest_price_buff = buff_sql.get_good_lowest_price(good_id, 'buff')
    # the_lowest_price_uu = buff_sql.get_good_lowest_price(good_id, 'uu')
    # the_lowest_price_igxe = buff_sql.get_good_lowest_price(good_id, 'igxe')
    # the_lowest_price_c5 = buff_sql.get_good_lowest_price(good_id, 'c5')
    pbar = tqdm(total=len(da), dynamic_ncols=True)
    for d in da:
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
        # if str(d) + '\n' not in already_recorded:
        buff_sql.write_record(record_time, good_id, price, pl)
        pbar.update(1)
        pbar.set_description(f"商品{good_id},平台{pl}:插入第 {index}部分")
    pbar.close()


def handle_json(json_data, recorded, index):
    os.system("cls")
    goods_id = '0'
    for data in json_data['data']['list']:
        platform = data['platform']
        if platform == 0:
            goods_id = data['goodsId']
            break
    if str(goods_id) + "\n" not in recorded:
        for data in json_data['data']['list']:
            platform = data['platform']
            # print(igxe_id, "数据长度", len(data['data']), "序号", index, '/', len(json_datas))
            if len(data['data']) > 1:
                if platform == 0:
                    data_insert(goods_id, data['data'], 'buff', index)

                elif platform == 1:
                    data_insert(goods_id, data['data'], 'uu', index)

                elif platform == 2:
                    data_insert(goods_id, data['data'], 'igxe', index)

                elif platform == 3:
                    data_insert(goods_id, data['data'], 'c5', index)
        os.system("cls")
        with lock:
            with open('already_insert_goods_id.txt', 'a+', encoding='utf-8') as a:
                a.write(str(goods_id) + '\n')
        print("序号", goods_id, "已完成")
    #         urls_per_thread = len(data['data']) // 100
    #         for i in range(100):
    #             if platform == 0:
    #                 if str(igxe_id) + '/' + 'buff' + str(index) + ':' + str(i) + '\n' not in recorded:
    #                     start = i * urls_per_thread
    #                     end = start + urls_per_thread if i < 100 - 1 else len(data['data'])
    #                     sublist = data['data'][start:end]
    #                     Thread(target=data_insert, args=(igxe_id, sublist, 'buff', i, index)).start()
    #                 elif i == 99:
    #                     is_continue = True
    #             elif platform == 1:
    #                 if str(igxe_id) + '/' + 'uu' + str(index) + ':' + str(i) + '\n' not in recorded:
    #                     start = i * urls_per_thread
    #                     end = start + urls_per_thread if i < 100 - 1 else len(data['data'])
    #                     sublist = data['data'][start:end]
    #                     Thread(target=data_insert, args=(igxe_id, sublist, 'uu', i, index)).start()
    #                 elif i == 99:
    #                     is_continue = True
    #             elif platform == 2:
    #                 if str(igxe_id) + '/' + 'igxe' + str(index) + ':' + str(i) + '\n' not in recorded:
    #                     start = i * urls_per_thread
    #                     end = start + urls_per_thread if i < 100 - 1 else len(data['data'])
    #                     sublist = data['data'][start:end]
    #                     Thread(target=data_insert, args=(igxe_id, sublist, 'igxe', i, index)).start()
    #                 elif i == 99:
    #                     is_continue = True
    #             elif platform == 3:
    #                 if str(igxe_id) + '/' + 'c5' + str(index) + ':' + str(i) + '\n' not in recorded:
    #                     start = i * urls_per_thread
    #                     end = start + urls_per_thread if i < 100 - 1 else len(data['data'])
    #                     sublist = data['data'][start:end]
    #                     Thread(target=data_insert, args=(igxe_id, sublist, 'c5', i, index)).start()
    #                 elif i == 99:
    #                     is_continue = True
    # if not is_continue:
    #     time.sleep(10)


def insert_data_from_csob(json_datas):
    with open('already_insert_goods_id.txt', 'r', encoding='utf-8') as f:
        already_record = f.readlines()
        handle_json(json_datas, already_record, 0)  # json格式所有的数据都要使用"，不能使用'，否则会报错


# with open('2024_7_recent_6_month.txt', 'r', encoding='utf-8') as f:
#     json_datas = f.readlines()
# with open('already_insert_goods_id.txt', 'r', encoding='utf-8') as f:
#     already_record = f.readlines()
# print(len(json_datas) / 2)
#
# for i, json1 in enumerate(json_datas):
#     # Thread(target=handle_json, args=(json.loads(json1), already_record, i)).start()
#     handle_json(json.loads(json1.replace("'", "\"")), already_record, i)  # json格式所有的数据都要使用"，不能使用'，否则会报错
