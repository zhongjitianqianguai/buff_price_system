import pymysql
from dbutils.pooled_db import PooledDB
from pymysql import IntegrityError
import buff_sql_server

pool = PooledDB(
    creator=pymysql,
    maxconnections=1000000,
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    database='buff_price',
    charset='utf8'
)


def detect_table_exist(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = f"""SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'buff_price' AND TABLE_NAME = 
        '{goods_id}_record';"""
        cursor.execute(sql)
        temp = cursor.fetchall()
        if temp[0][0] == 1:
            return True
        else:
            return False
    except Exception as e:
        print("错误类型:", type(e))
        print("检测表是否存在失败:", e)
    finally:
        cursor.close()
        conn.close()


def create_new_record_table(goods_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = f"""CREATE TABLE IF NOT EXISTS {goods_id}_record(
            time VARCHAR(255),
            price FLOAT,
            source VARCHAR(10),
            PRIMARY KEY (time, price, source)
        );"""
        cursor.execute(sql)
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


def delete_goods_id_from_all_tables():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            if "_record" in table[0]:
                sql = f"ALTER TABLE {table[0]} DROP COLUMN goods_id"
                cursor.execute(sql)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_goods_id_from_record_table(table_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        table_name = f"{table_id}_record"
        sql = f"ALTER TABLE {table_name} DROP COLUMN goods_id"
        cursor.execute(sql)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def write_record(record_time, goods_id, price, source):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO %s_record(time,price,source) VALUES(%s,%s,%s)"""
        cursor.execute(sql, (int(goods_id), record_time, price, source))
        conn.commit()
    except IntegrityError:
        conn.rollback()
    except Exception as e:
        if "doesn't exist" in str(e):
            create_new_record_table(goods_id)
            write_record(record_time, goods_id, price, source)
            return
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
        sql = """DELETE FROM buff_record WHERE record_id NOT IN (SELECT * FROM (SELECT MIN(record_id) FROM 
        buff_record GROUP BY time,goods_id,price,source) AS t)"""
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
        sql = """Select goods_id from buff_goods;"""
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
        sql = """Select * from buff_goods;"""
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
        sql = """Select * from  %s_record where source='buff' order by time;"""
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


def get_good_goods_id_by_igxe_id(igxe_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select goods_id from  buff_goods where igxe_id=%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, igxe_id)  # 添加参数
        temp = cursor.fetchall()
        for i in temp:
            return i[0]

    except Exception as e:
        print("错误类型:", type(e))
        print("通过igxe_id获取商品id失败:", e)
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


def set_good_with_uu_id(goods_id, uu_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set uu_id = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (uu_id, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("设置商品悠悠id失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def set_good_with_igxe_id(goods_id, igxe_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set igxe_id = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (igxe_id, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("设置商品igxe_id失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def set_good_with_c5_id(goods_id, c5_id):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set c5_id = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (c5_id, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("设置商品c5_id失败:", e)
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


def update_csob_update_time(goods_id, update_time):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set cs_ob_update_time = %s where goods_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (update_time, goods_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新csob商品更新时间失败:", e)
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


def add_new_good_buff_dont_have(name, goods_id, category, img_url, price, the_lowest_price):
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


def auto_update_the_lowest_price_buff_by_through_record_table():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            if "_record" in table[0]:
                goods_id = table[0].split("_")[0]
                cursor.execute(f"SELECT MIN(price) FROM {table[0]} where source = 'buff'")
                lowest_price = cursor.fetchone()[0]
                if lowest_price is not None:
                    cursor.execute(
                        f"UPDATE buff_goods SET the_lowest_price_buff = {lowest_price} WHERE goods_id = {goods_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def auto_update_the_lowest_price_uu_by_through_record_table():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            if "_record" in table[0]:
                goods_id = table[0].split("_")[0]
                cursor.execute(f"SELECT MIN(price) FROM {table[0]} where source = 'uu'")
                lowest_price = cursor.fetchone()[0]
                if lowest_price is not None:
                    cursor.execute(
                        f"UPDATE buff_goods SET the_lowest_price_uu = {lowest_price} WHERE goods_id = {goods_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def auto_update_the_lowest_price_igxe_by_through_record_table():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            if "_record" in table[0]:
                goods_id = table[0].split("_")[0]
                cursor.execute(f"SELECT MIN(price) FROM {table[0]} where source = 'igxe'")
                lowest_price = cursor.fetchone()[0]
                if lowest_price is not None:
                    cursor.execute(
                        f"UPDATE buff_goods SET the_lowest_price_igxe = {lowest_price} WHERE goods_id = {goods_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def auto_update_the_lowest_price_c5_by_through_record_table():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            if "_record" in table[0]:
                goods_id = table[0].split("_")[0]
                cursor.execute(f"SELECT MIN(price) FROM {table[0]} where source = 'c5'")
                lowest_price = cursor.fetchone()[0]
                if lowest_price is not None:
                    cursor.execute(
                        f"UPDATE buff_goods SET the_lowest_price_c5 = {lowest_price} WHERE goods_id = {goods_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def get_all_goods_id_igxe():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        sql = """Select igxe_id from buff_goods;"""
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


def update_good_with_steam_price_igxe(url, steam_price):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set now_price_steam = %s where igxe_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (steam_price, url))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品steam价格失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def delete_daily_record_to_only_two():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            if "_record" in table[0]:
                sql = f"SELECT * FROM {table[0]} WHERE source = 'buff' ORDER BY time DESC"
                cursor.execute(sql)
                records = cursor.fetchall()
                if len(records) > 2:
                    for record in records[2:]:
                        # Use parameterized query to safely pass values
                        sql = f"DELETE FROM {table[0]} WHERE time = %s AND price = %s AND source = 'buff'"
                        cursor.execute(sql, (record[0], record[1]))
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def only_insert_two_into_server():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            if "_record" in table[0]:
                sql = f"SELECT * FROM {table[0]} WHERE source = 'buff' ORDER BY time DESC"
                cursor.execute(sql)
                records = cursor.fetchall()
                if len(records) > 2:
                    for record in records[2:]:
                        buff_sql_server.write_record(record[0], table[0].split("_")[0], record[1], record[2])
                else:
                    for record in records:
                        buff_sql_server.write_record(record[0], table[0].split("_")[0], record[1], record[2])
                sql = f"SELECT * FROM {table[0]} WHERE source = 'uu' ORDER BY time DESC"
                cursor.execute(sql)
                records = cursor.fetchall()
                if len(records) > 2:
                    for record in records[2:]:
                        buff_sql_server.write_record(record[0], table[0].split("_")[0], record[1], record[2])
                else:
                    for record in records:
                        buff_sql_server.write_record(record[0], table[0].split("_")[0], record[1], record[2])
                sql = f"SELECT * FROM {table[0]} WHERE source = 'igxe' ORDER BY time DESC"
                cursor.execute(sql)
                records = cursor.fetchall()
                if len(records) > 2:
                    for record in records[2:]:
                        buff_sql_server.write_record(record[0], table[0].split("_")[0], record[1], record[2])
                else:
                    for record in records:
                        buff_sql_server.write_record(record[0], table[0].split("_")[0], record[1], record[2])
                sql = f"SELECT * FROM {table[0]} WHERE source = 'c5' ORDER BY time DESC"
                cursor.execute(sql)
                records = cursor.fetchall()
                if len(records) > 2:
                    for record in records[2:]:
                        buff_sql_server.write_record(record[0], table[0].split("_")[0], record[1], record[2])
                else:
                    for record in records:
                        buff_sql_server.write_record(record[0], table[0].split("_")[0], record[1], record[2])

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()


def update_good_with_lowest_price_igxe(igxe_id, now_lowest_price):
    conn = pool.connection()
    cursor = conn.cursor()
    try:

        sql = """Update buff_goods set the_lowest_price_igxe = %s where igxe_id =%s;"""
        conn.ping(reconnect=True)
        cursor.execute(sql, (now_lowest_price, igxe_id))  # 添加参数
        conn.commit()
    except Exception as e:
        print("错误类型:", type(e))
        print("更新商品最低igxe价格失败:", e)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


def make_all_ids_not_null():
    conn = pool.connection()
    cursor = conn.cursor()
    try:
        # Update all goods_id in buff_goods to not null
        cursor.execute("UPDATE buff_goods SET uu_id = %s WHERE uu_id IS NULL", '0')
        cursor.execute("UPDATE buff_goods SET igxe_id = %s WHERE igxe_id IS NULL", '0')
        cursor.execute("UPDATE buff_goods SET c5_id = %s WHERE c5_id IS NULL", '0')
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
