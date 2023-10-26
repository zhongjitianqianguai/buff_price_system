import threading

import pymysql

import pymysql
from dbutils.pooled_db import PooledDB

pool = PooledDB(
    creator=pymysql,
    maxconnections=10,
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    database='buff_price',
    charset='utf8'
)


def write_record(record_time, goods_id, price):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Insert into buff_record(time,goods_id,price,source) value(%s,%s,%s,'buff')"""
        cursor.execute(sql, (record_time, goods_id, price))
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("插入记录失败:", e)
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
        print("获取所有商品失败:", e)
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
        sql = """Select * from  buff_record where goods_id=%s order by time;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, goods_id)  # 添加参数
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
        sql = """Select mail from  buff_user where user_id=%s;"""
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


def get_good_lowest_price(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select the_lowest_price from  buff_goods where goods_id=%s;"""
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


def get_good_last_record(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Select price from  buff_record where goods_id=%s order by time desc limit 1;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, goods_id)  # 添加参数
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


def change_all_goods_expected_price_div2():
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """UPDATE buff_goods SET expected_price = now_price / 2;"""
        conn.ping(reconnect=True)
        cursor.execute(sql)  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("改变商品预期价格为当前价格的1/2失败:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def update_good_without_trend(goods_id, img_url, name, now_price,
                              lowest_price_in_record):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set  the_lowest_price =%s ,img_url=%s,name=%s,now_price=%s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (lowest_price_in_record, img_url, name, now_price, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品失败:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def add_new_good(name, goods_id, category, except_price, img_url, now_price, lowest_price_in_record):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Insert into buff_goods(name,goods_id,category,expected_price,img_url,now_price,the_lowest_price) value(%s,%s,%s,%s,%s,%s,%s);"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (name, goods_id, category, except_price, img_url, now_price,lowest_price_in_record))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("插入新商品失败:", e)
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
