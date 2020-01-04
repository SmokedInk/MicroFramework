# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   test
# @Time:    2020-01-02 10:14:27
# @Desc:    test

# 导入发送邮件包
import smtplib
from email.mime.text import MIMEText  # 用来创建文本格式的邮件体内容
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


class Send_Email:

    def __init__(self, num):
        self.num = num
        self.smtp = self.get_conn()
        # print(self.smtp)
        self.send_email()

    def get_conn(self):
        # 创建邮件对象
        smtp_obj = smtplib.SMTP()
        # 连接服务器
        smtp_obj.connect("smtp.163.com")
        # 登录邮箱
        smtp_obj.login("15194654202@163.com", "yy1826")
        return smtp_obj

    def send_email(self):
        # 定义发送邮件的三要素
        sender = "15194654202@163.com"
        receiver = "1375410508@qq.com"
        # 获取发送邮件的 邮件体
        msg = self.get_msg(sender, receiver)
        # 发送邮件
        self.smtp.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
        print("send success")

    def get_msg(self, sender, receiver):
        # 定义邮件主题
        subject = "恭喜你 你已经被阿里巴巴公司录用 "
        # 获取邮件体中的 文本内容（消息体）
        msg = self.get_content()
        # 生成邮件体的 三要素
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject
        return msg

    def get_content(self):

        if self.num == 1:
            content = "请xx准时报到"
            # 将内容写到面板中  文本格式
            msg = MIMEText(content, "plain", "utf-8")
            return msg
        elif self.num==2:
            # 读取文件
            # with open("02.html", "r", encoding="utf-8") as f:
            #     content = f.read()
            # print(type(content))
            content = """
            <html>
                <h1>请xx准时报到<h1>
                <a href="https://www.baidu.com/">baidu</a>
            </html>"""
            print(content)
            msg = MIMEText(content, "html", "utf-8")
            return msg
        elif self.num==3:
            #获取含有内嵌图片资源的HTML格式的邮件体
            msg=self.get_pic()
            return msg
    #获取图片信息
    def get_pic(self):
        #通过cid图片文件关联起来
        content="<b>Some<i>HTML</i>text</b> and an image <br><img src='cid:image1'><br>goood"
        #如果content 中内嵌资源，必须定义related字段
        #使用related定义内嵌套资源的邮件体
        msgRoot=MIMEMultipart("related")
        #创建HTML格式的邮件体
        msgText=MIMEMultipart(content,"html","utf-8")
        #将msgText中的内容附加到MIMEMultipart对象中
        msgRoot.attach(msgText)
        #读取图片文件内容
        with open("2.jpg","rb")as f:
            result=f.read()
        #使用图片信息创建一个图片对象
        msgImage=MIMEImage(result)
        #指定文件的Content-ID 为image1
        msgImage.add_header("Content-ID","image1")
        #将msgImage中的图片内容附加到MIMEMultipart对象的指定image1当中
        msgRoot.attach(msgImage)
        #返回携带有内嵌套图片资源的HTML格式邮件的MIMEMultipart对象
        return msgRoot

    def __del__(self):
        # 关闭
        self.smtp.quit()


if __name__ == '__main__':
    #  1  # 发送的邮件体是字符串
    # 2 发送一个html的邮件体
    # 发送一个图片的邮件体
    num=int(input("请发送邮件所对应的数字"))
    Send_Email(num)


