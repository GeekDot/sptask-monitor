#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


# 邮件报警类
class EmailAlert(object):

    def __init__(self):

        # 发件人邮箱
        self.user = 'pm@adnice.com'
        # 发件人密码
        self.passwd = 'DCzndl@2017'
        # 邮箱服务器
        self.server = 'smtp.qiye.163.com'
        
        # 邮件主题
        self.subject = ''
        # 邮件正文
        self.content = ''

        # 收件人邮箱
        self.addressee = [
            'zhangyi@adnice.com',
            # 'chanpin@adnice.com',
            # 'chaowang@adnice.com',
            # 'xieqiang@adnice.com',
            # 'chenliang@adnice.com',
            # 'angehui@adnice.com',
            # 'chenyijia@adnice.com',
        ]
        
    def send(self, subject, content, send_type='plain'):

        self.subject = subject
        self.content = content
        
        # 构造头部信息和邮件内容
        email_data = MIMEText(self.content, send_type, 'utf-8')
        email_data['Subject'] = Header(self.subject, 'utf-8')
        email_data['From'] = 'Adnice<pm@adnice.com>'
        email_data['To'] = ','.join(self.addressee)

        try:
            # 连接服务器
            smtp = smtplib.SMTP_SSL(self.server, 465)
            # DEBUG
            # smtp.set_debuglevel(1)
            # 登录服务器
            smtp.login(self.user, self.passwd)
            # 发送邮件
            smtp.sendmail(self.user, self.addressee, email_data.as_string())
            # 关闭服务器
            smtp.quit()
            print('发送邮件成功')

        except Exception as e:
            print('发送邮件成功', e)


if __name__ == 'monitor.tools.emailAlert':
    emailAlert = EmailAlert()
