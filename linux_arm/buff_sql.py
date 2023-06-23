import threading

import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user="root",
    passwd="root",
    db="buff_price",
    charset='utf8',
    autocommit=True
)
cursor = conn.cursor()
lock = threading.Lock()


def write_record(record_time, goods_id, price):
    try:
        lock.acquire()
        sql = """Insert into buff_record(time,goods_id,price) value(%s,%s,%s)"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (record_time, goods_id, price))  # 添加参数
    except Exception as e:
        print("错误类型:", type(e))
        print("插入记录失败:", e)
    finally:
        lock.release()


def get_all_goods():
    try:
        lock.acquire()
        sql = """Select * from  buff_goods;"""
        conn.ping(reconnect=True)
        cursor.execute(sql)  # 添加参数
        return cursor.fetchall()

    except Exception as e:
        print("错误类型:", type(e))
        print("获取所有商品失败:", e)
    finally:
        lock.release()


def get_good_expected_price(goods_id):
    try:
        lock.acquire()
        sql = """Select expected_price from  buff_goods where goods_id=%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, goods_id)  # 添加参数
        temp = cursor.fetchall()
        for i in temp:
            return i[0]

    except Exception as e:
        print("错误类型:", type(e))
        print("获取商品预期价格失败:", e)
    finally:
        lock.release()


def get_good_lowest_price(goods_id):
    try:
        lock.acquire()
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
        lock.release()


def get_good_last_record(goods_id):
    try:
        lock.acquire()
        sql = """Select price from  buff_record where goods_id=%s order by time desc limit 1;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, goods_id)  # 添加参数
        temp = cursor.fetchall()
        for i in temp:
            return i[0]

    except Exception as e:
        print("错误类型:", type(e))
        print("获取商品预期价格失败:", e)
    finally:
        lock.release()


def update_good_with_trend(goods_id, trend):
    try:
        lock.acquire()
        sql = """Update buff_goods set trend = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (trend, goods_id))  # 添加参数
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品价格趋势失败:", e)
    finally:
        lock.release()


def update_good_without_trend(goods_id, img_url, name, now_price,
                              lowest_price_in_record):
    try:
        lock.acquire()
        sql = """Update buff_goods set  the_lowest_price =%s ,img_url=%s,name=%s,now_price=%s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (lowest_price_in_record, img_url, name, now_price, goods_id))  # 添加参数
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品失败:", e)
    finally:
        lock.release()


def add_new_good(name, goods_id, category, except_price, img_url, now_price):
    try:
        lock.acquire()
        sql = """Insert into buff_goods(name,goods_id,category,expected_price,img_url,now_price) value(%s,%s,%s,%s,%s,%s);"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (name, goods_id, category, except_price, img_url, now_price))  # 添加参数
    except Exception as e:
        print("错误类型:", type(e))
        print("插入新商品失败:", e)
    finally:
        lock.release()


def add_new_mail(content, goods_id, time):
    try:
        lock.acquire()
        sql = """Insert into buff_mail(content,url,time,user_id) value(%s,%s,%s,%s);"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (content, goods_id, time, 1))  # 添加参数
    except Exception as e:
        print("错误类型:", type(e))
        print("插入新邮件失败:", e)
    finally:
        lock.release()
