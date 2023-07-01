import random

import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time

from linux_arm import buff_mail

# 京东商品API
jd_api = ''

# 商品ID列表
product_ids = ['10071348542150']

# 邮件发送配置
smtp_server = 'smtp.163.com'
smtp_port = 25
smtp_user = 'a907993029@163.com'
smtp_password = 'ZVDXBZPBIPTSMYGX'
sender = 'a907993029@163.com'
receivers = ['1094410998@qq.com']

# 上一次商品状态
last_status = {}


def send_email(subject, message):
    # 创建邮件内容
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = Header('京东商品监控', 'utf-8')
    msg['To'] = Header('收件人', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    # 发送邮件
    try:
        smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp.login(smtp_user, smtp_password)
        smtp.sendmail(sender, receivers, msg.as_string())
        smtp.quit()
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败')
        print(e)


def check_product(product_id):
    # 构造请求URL
    url = f'{jd_api}/query?skuId={product_id}&area=1_72_2799_0'

    # 发送请求
    response = requests.get(url)
    print(response.text)
    # 解析响应数据
    data = response.json()
    stock = data['stock']['StockState']

    # 检查商品状态
    if product_id in last_status:
        if stock != last_status[product_id]:
            if stock == 33:
                send_email('商品有货啦', f'商品 {product_id} 已经有货啦！')
                print('商品有货啦')
            else:
                send_email('商品下架啦', f'商品 {product_id} 已经下架啦！')
                print('商品下架啦')
    last_status[product_id] = stock


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.63 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

while True:
    # 检查商品状态
    # for product_id in product_ids:
    #     check_product(product_id)
    url = f'https://item.jd.com/100052404492.html'
    response = requests.get(url, headers=headers)
    # print(response.text)
    if '下柜' in response.text:
        print('商品下架啦')
    elif '无货' in response.text:
        print('商品无货啦')
    else:
        print('商品有货啦')
        buff_mail.send_mail('商品有货啦', '商品有货啦', url)

    # 等待一段时间
    time.sleep(random.randint(30, 60))
