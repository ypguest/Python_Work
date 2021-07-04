# !/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import datetime
import os
import re
import pandas as pd
from email.mime.text import MIMEText
from email.header import Header


def DirFolder(_file_path):
    """遍历路径，获取文件未尾为当天日期的文件名"""
    _file_paths = []
    for root, dirs, files in os.walk(_file_path):
        for file in files:
            matchTimeObj = re.match(r'QRE_CP_Yield_Report-(.*).xlsx', file, re.I)
            filetime = datetime.datetime.strptime(matchTimeObj.group(1), '%Y%m%d').date()
            if filetime == datetime.date.today():
                _file_paths.append(os.path.join(root, file))
    return _file_paths


def mailSender(data):
    # 发邮件相关的参数
    smtpserver = "smtp.263.net"  # 发件服务器
    port = 0  # 端口
    sender = 'peng.yin@unisemicon.com'  # 发信者密码
    pwd = "yp0*963"  # 发信者密码
    receivers = ['peng.yin@unisemicon.com']  # 接收邮件

    ticks = datetime.date.today()

    # 编辑邮件内容
    subject = "UniIC_CP_Yield_Report-{}".format(ticks)  # 自定义发送邮件主题
    body1 = """
    <p>Hi Sir, </p>
    <p>Please review UniIC CP Yield Report</p>
    """
    body = body1 + data
    # 自定义邮件正文，这里为html格式

    msg = MIMEText(body, 'html', 'utf-8')
    msg['From'] = Header("peng.yin@unisemicon.com", 'utf-8')  # 发送者
    msg['Subject'] = Header(subject, 'utf-8')
    # 发送邮件
    try:  # 不用SSL认证
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)  # 连接服务器
        smtp.login(sender, pwd)  # 登录
    except:  # 需要SSL认证
        smtp = smtplib.SMTP_SSL(smtpserver, port)  # ssl认证,例如qq邮箱
        smtp.login(sender, pwd)  # 登录
    smtp.sendmail(sender, receivers, msg.as_string())  # 发送
    smtp.quit()  # 关闭


def main():
    filepath = r'\\arctis\qcxpub\QRE\04_QA(Component)\99_Daily_Report\99_QRE_CP_Yield_Report'
    files = DirFolder(filepath)
    for file in files:
        data = pd.read_excel(io=file)
        htmldata = data.to_html()
        mailSender(htmldata)


if __name__ == '__main__':
    main()
    # title = [u'日期', u'姓名']
    # result = [[u'2016-08-25', u'2016-08-26', u'2016-08-27'], [u'张三', u'李四', u'王二']]
    # print(convertToHtml(result, title))
