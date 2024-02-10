import threading

import pymysql

import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import IntegrityError

pool = PooledDB(
    creator=pymysql,
    maxconnections=1000000,
    host='127.0.0.1',
    # host='192.168.6.127',
    port=3306,
    user='root',
    password='jiege666',
    database='buff_price',
    charset='utf8'
)


def create_new_record_table(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """CREATE TABLE IF NOT EXISTS %s_record(
        time VARCHAR(255) PRIMARY KEY,
        goods_id VARCHAR(255) PRIMARY KEY,
        price FLOAT PRIMARY KEY,
        source VARCHAR(255) PRIMARY KEY
        );"""
        cursor.execute(sql,goods_id)
        conn.commit()
    except IntegrityError:
        conn.rollback()
    except Exception as e:
        print("错误类型:", type(e))
        print("创建新表失败:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def write_record(record_time, goods_id, price, source):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO %s_record(time,goods_id,price,source) VALUES(%s,%s,%s,%s)"""
        cursor.execute(sql, (int(goods_id), record_time, goods_id, price, source))
        conn.commit()
    except IntegrityError:
        conn.rollback()
    except Exception as e:
        print("错误类型:", type(e))
        print("插入记录失败:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def delete_repeat_record():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """DELETE FROM buff_record WHERE record_id NOT IN (SELECT * FROM (SELECT MIN(record_id) FROM buff_record GROUP BY time,goods_id,price,source) AS t)"""
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("删除重复记录失败:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_all_goods_id():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select goods_id from  buff_goods;"""
        conn.ping(reconnect=True)
        cursor.execute(sql)  # 添加参数
        goods_ids = []
        for good in cursor.fetchall():
            goods_ids.append(good[0])
        return goods_ids

    except Exception as e:
        print("错误类型:", type(e))
        print("获取所有商品id失败:", e)
    finally:
        cursor.close()
        conn.close()


def get_all_goods_name():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select name from  buff_goods;"""
        conn.ping(reconnect=True)
        cursor.execute(sql)  # 添加参数
        goods_names = []
        for good in cursor.fetchall():
            goods_names.append(good[0])
        return goods_names

    except Exception as e:
        print("错误类型:", type(e))
        print("获取所有商品name失败:", e)
    finally:
        cursor.close()
        conn.close()


def update_good_lowest_price(goods_id, lowest_price, source):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        if source == 'buff':
            sql = """Update buff_goods set the_lowest_price_buff = %s where goods_id =%s;"""
        elif source == 'uu':
            sql = """Update buff_goods set the_lowest_price_uu = %s where goods_id =%s;"""
        elif source == 'igxe':
            sql = """Update buff_goods set the_lowest_price_igxe = %s where goods_id =%s;"""
        elif source == 'c5':
            sql = """Update buff_goods set the_lowest_price_c5 = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (lowest_price, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品最低价格失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def get_good_lowest_price(goods_id, source):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        if source == 'buff':
            sql = """Select the_lowest_price_buff from  buff_goods where goods_id=%s;"""
        elif source == 'uu':
            sql = """Select the_lowest_price_uu from  buff_goods where goods_id=%s;"""
        elif source == 'igxe':
            sql = """Select the_lowest_price_igxe from  buff_goods where goods_id=%s;"""
        elif source == 'c5':
            sql = """Select the_lowest_price_c5 from  buff_goods where goods_id=%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, goods_id)  # 添加参数
        temp = cursor.fetchall()
        for i in temp:
            return i[0]

    except Exception as e:
        print("错误类型:", type(e))
        print("获取商品最低价格失败:", e)
    finally:
        cursor.close()
        conn.close()


def get_all_goods():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select * from  buff_goods;"""
        conn.ping(reconnect=True)
        cursor.execute(sql)  # 添加参数
        return cursor.fetchall()

    except Exception as e:
        print("错误类型:", type(e))
        print("获取所有商品失败:", e)
    finally:
        cursor.close()
        conn.close()


def get_good_all_record(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select * from  %s_record where  source='buff' order by time;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, int(goods_id))  # 添加参数
        return cursor.fetchall()


    except Exception as e:
        print("错误类型:", type(e))
        print("获取商品所有价格记录失败:", e)
    finally:
        cursor.close()
        conn.close()


def get_good_expected_price(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select expected_price,user_id from  buff_user_collect where goods_id=%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, goods_id)  # 添加参数
        return cursor.fetchall()

    except Exception as e:
        print("错误类型:", type(e))
        print("获取商品预期价格失败:", e)
    finally:
        cursor.close()
        conn.close()


def get_user_mail_by_user_id(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select email from  buff_user where id=%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, goods_id)  # 添加参数
        temp = cursor.fetchall()
        for i in temp:
            return i[0]

    except Exception as e:
        print("错误类型:", type(e))
        print("通过用户id获取用户邮件失败:", e)
    finally:
        cursor.close()
        conn.close()


def get_good_last_record(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Select price from  %s_record order by time desc limit 1;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, int(goods_id))  # 添加参数
        temp = cursor.fetchall()
        for i in temp:
            return i[0]

    except Exception as e:
        print("错误类型:", type(e))
        print("获取商品最新价格记录失败:", e)
    finally:
        cursor.close()
        conn.close()


def update_good_with_trend(goods_id, trend):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set trend = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (trend, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品价格趋势失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def update_good_with_now_price_buff(goods_id, now_price_buff):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set now_price_buff = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (now_price_buff, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品现在价格失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def update_good_with_now_price_uu(goods_id, now_price_uu):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set now_price_uu = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (now_price_uu, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品现在价格失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def check_record(record_time, goods_id, price, source):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """SELECT * FROM buff_record WHERE time = %s AND goods_id = %s AND price = %s AND source = %s"""
        cursor.execute(sql, (record_time, goods_id, price, source))
        result = cursor.fetchone()
        if result is None:
            return False
        else:
            return True
    except Exception as e:
        print("错误类型:", type(e))
        print("查询记录失败:", e)
    finally:
        cursor.close()
        conn.close()


def update_good_with_now_price_igxe(goods_id, now_price_igxe):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set now_price_igxe = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (now_price_igxe, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品现在价格失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def update_good_update_time(goods_id, update_time):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set update_time = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (update_time, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品更新时间失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def update_good_with_now_price_c5(goods_id, now_price_c5):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set now_price_c5 = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (now_price_c5, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品现在价格失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def update_good_with_now_price(goods_id, now_price_buff, now_price_uu, now_price_igxe, now_price_c5):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set now_price_buff = %s,now_price_uu = %s,now_price_igxe = %s,now_price_c5 = %s 
        where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (now_price_buff, now_price_uu, now_price_igxe, now_price_c5, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品现在价格失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def add_new_mail(content, goods_id, time, user_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Insert into buff_mail(content,url,time,user_id) value(%s,%s,%s,%s);"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (content, goods_id, time, user_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("插入新邮件失败:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def update_good_without_trend(goods_id, img_url, name, price, lowest_price):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set img_url = %s,name = %s,now_price_buff = %s,the_lowest_price_buff = %s where 
        goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (img_url, name, price, lowest_price, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品信息失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def add_new_good(name, goods_id, category, img_url, price, the_lowest_price):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Insert into buff_goods(name,goods_id,category,img_url,now_price_buff,the_lowest_price_buff) 
        value(%s,%s,%s,%s,%s,%s);"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (name, goods_id, category, img_url, price, the_lowest_price))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("插入新商品失败:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
