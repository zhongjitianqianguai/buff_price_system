import pymysql

import test
conn = pymysql.connect(
    host="192.168.6.169",
    port=3306,
    user="root",
    passwd="root",
    db="buff_price",
    charset='utf8',
    autocommit=True
)

print(test.get_all_goods(conn.cursor()))