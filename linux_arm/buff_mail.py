import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_mail(name, price, url):
    # 邮件内容
    message = f'{name} \n当前价格为{price}\n链接为{url}'

    # 构造邮件内容,设置编码为gbk,格式为html
    msg = MIMEText(message, 'html', 'utf-8')

    # 发信方的信息:发信邮箱,密码
    from_addr = 'a907993029@163.com'
    password = 'ZVDXBZPBIPTSMYGX'

    # 收信方邮箱
    to_addr = '1094410998@qq.com'

    # 发信服务器
    smtp_server = 'smtp.163.com'

    # SMTP协议默认端口
    smtp_port = 25

    # 设置Content-Type头部也为gbk编码
    msg['Content-Type'] = 'text/html; charset=utf-8'

    # 设置邮件标题
    msg['Subject'] = Header('价格提醒', 'utf-8')

    # 告知邮件服务内容
    msg['Content-Transfer-Encoding'] = 'base64'

    # 发送邮件
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.login(from_addr, password)
    gbk_msg = msg.as_bytes().decode('utf-8')  # 解码msg为gbk字符串
    server.sendmail(from_addr, to_addr, gbk_msg)
    server.quit()
