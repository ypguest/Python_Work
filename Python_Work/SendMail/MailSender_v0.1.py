# !/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import datetime
import os
import re
import pandas as pd
import numpy as np
from email.mime.text import MIMEText
from email.header import Header


def gentable():
    """遍历路径，获取文件未尾为当天日期的文件名"""
    _file_path_cp = r'\\arctis\qcxpub\QRE\04_QA(Component)\99_Daily_Report\99_QRE_CP_Yield_Report\QRE_CP_Yield_Report_CP.xls'
    _file_path_count = r'\\arctis\qcxpub\QRE\04_QA(Component)\99_Daily_Report\99_QRE_CP_Yield_Report\QRE_CP_Yield_Report_COUNT.xls'
    _data_cp = pd.read_excel(io=_file_path_cp)
    _data_count = pd.read_excel(io=_file_path_count)
    _data_merge = pd.DataFrame()
    _data_merge = _data_count.copy()
    for i in range(1, _data_cp.shape[1]):
        _data_cp.iloc[:, i:i+1] = round(_data_cp.iloc[:, i:i+1], 2)  # 将yield转换为小数点两位
        for j in range(0, _data_cp.shape[0]):
            if _data_count.iloc[j, i] != 0:
                _data_merge.iloc[j, i] = str(_data_cp.iloc[j, i]) + '/' + str(_data_count.iloc[j, i])
    return _data_merge.to_html()


def sendMail(sender, mail_pwd, receivers, mail_msg, mail_host):
    # 第三方 SMTP 服务
    mail_host = mail_host  # 设置服务器，qq:smtp.qq.com; 163:smtp.163.com; 等
    port = 0    # 端口
    sender = sender  # 用户名
    mail_pwd = mail_pwd  # 密码

    # 设置发件人 & 收件人
    sender = sender  # 发件人，这里设置成与用户名一致
    receivers = receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 邮件的内容，HTML 格式
    mail_msg = mail_msg

    message = MIMEText(mail_msg, 'html', 'utf-8')
    # 三个参数：第一个为邮件内容；第二个 设置文本格式 plain为纯文本，HTML为HTML格式；第三个 utf-8 设置编码

    message['From'] = sender
    message['To'] = ','.join(receivers)

    # 自定义发送邮件主题
    ticks = datetime.date.today()
    subject = "UniIC_CP_Yield_Report-{}[tryrun]".format(ticks)
    message['Subject'] = Header(subject, 'utf-8')

    # 发送邮件
    try:      # 不用SSL认证
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host)  # 25 为 SMTP 端口号
        smtpObj.login(sender, mail_pwd)
    except:  # 需要SSL认证
        smtp = smtplib.SMTP_SSL(mail_host, port)  # ssl认证,例如qq邮箱
        smtp.login(sender, mail_pwd)  # 登录
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()  # 关闭


def main():

    # 定义邮件内容
    text = """
    <p>Hi Sir, </p>
    <p>Please review UniIC CP Yield Report</p>
    """
    table = gentable()   # 产生HTML文件
    mail_msg = text + table

    # 调用函数，这里的密码使用生成的密码；
    # receivers = ['peng.yin@unisemicon.com']
    receivers = ['peng.yin@unisemicon.com', 'gordon.ding@unisemicon.com', 'bin.ma@unisemicon.com', 'shuyuan.ma@unisemicon.com',
                 'xing.guo@unisemicon.com', 'xiaowei.zhu@unisemicon.com', 'qian.wang@unisemicon.com', 'kai.zhang@unisemicon.com']
    sendMail(sender="qre.public@unisemicon.com", mail_pwd="yp0*963", receivers=receivers, mail_msg=mail_msg, mail_host="smtp.263.net")


if __name__ == '__main__':
    main()
