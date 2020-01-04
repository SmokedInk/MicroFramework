# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   crawler_warning
# @Time:    2020-01-02 09:47:32
# @Desc:    crawler_warning

import smtplib      # 导入发送邮件包
from email.mime.text import MIMEText  # 用来创建文本格式的邮件体内容
from twilio.rest import Client      # 导入twilio客户端

# 邮箱信息
EMAIL_CONFIG = {
    'form_addr': '15194654202@163.com',     # 发件人邮箱账号
    'authorization_code': 'yy1826',  # 发件人邮箱开启SMTP服务时的授权码
    'smpt_server': 'smtp.163.com',  # 发件人SMTP服务器地址
    'to_addrs': '1375410508@qq.com',  # 收件人邮箱地址
}


class CrawlerEmailWarning(object):

    def __init__(self, text):
        self.text = text

    def get_email_connect(self):
        # 创建邮件对象
        email_obj = smtplib.SMTP()
        # 连接服务器
        email_obj.connect(EMAIL_CONFIG['smpt_server'])
        # 登录邮箱
        email_obj.login(EMAIL_CONFIG['form_addr'], EMAIL_CONFIG['authorization_code'])
        return email_obj

    def get_content(self):
        content = f"""
        <html>
            <span style="color:red;font-weight:bold;">{self.text}</span>
        </html>"""
        # msg = MIMEText(content, "plain", "utf-8")       # 文本格式
        msg = MIMEText(content, "html", "utf-8")        # Html格式
        return msg

    def get_msg(self):
        # 定义邮件主题
        subject = "爬虫预警 "
        # 获取邮件体中的消息体（邮件正文）
        msg = self.get_content()
        # 生成邮件体的 三要素
        msg["From"] = EMAIL_CONFIG['form_addr']
        msg["To"] = EMAIL_CONFIG['to_addrs']
        msg["Subject"] = subject
        return msg

    def send_email(self, email_obj):
        """定义发送邮件的三要素"""
        # 获取发送邮件的 邮件体
        msg = self.get_msg()
        # 发送邮件
        email_obj.sendmail(
            from_addr=EMAIL_CONFIG['form_addr'],
            to_addrs=EMAIL_CONFIG['to_addrs'],
            msg=msg.as_string())
        print("send success")

    def run(self):
        # 获取email对象
        email_obj = self.get_email_connect()
        self.send_email(email_obj)
        # 关闭email对象
        email_obj.quit()


TWILIO_CONFIG = {
    'form_phone': '+12563717311',   # 此号码是在Twilio短信项目中获取的手机号
    'auth_token': 'af93282a59781c54f87dd67067b38783',  # 在Twilio短信项目中获取AUTH TOKEN
    'account_sid': 'AC77bc4240ca4c40e4728e470442a2ab76',    # 在Twilio短信项目中获取ACCOUNT SID
    'to_phone': '+8615194654202'    # 接收短信的号码需要加上 + , 不然会报错
}


class CrawlerPhoneWarning(object):
    def __init__(self, text):
        self.text = text

    def get_twilio_client(self):
        # 构建Twilio客户端
        return Client(TWILIO_CONFIG['account_sid'], TWILIO_CONFIG['auth_token'])

    def send_message(self, client):
        msg = client.messages.create(
            from_=TWILIO_CONFIG['form_phone'],
            body=text,
            to=TWILIO_CONFIG['to_phone']
        )
        print("OK", msg)

    def run(self):
        client = self.get_twilio_client()
        self.send_message(client)


if __name__ == '__main__':
    text = "【视频爬虫】爬虫在第16行报错，报错信息为：读写错误"
    CrawlerPhoneWarning(text).run()
