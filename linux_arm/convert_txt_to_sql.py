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