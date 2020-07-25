#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'zhangyi'

from configparser import ConfigParser
from monitor.tools.monitorPath import monitorPath
import pymysql


class MonitorDB(object):

    # 构造函数
    def __init__(self):

        # 读取数据库配置
        self.ini_path = monitorPath.conf_path
        self.conf = ConfigParser()
        self.conf.read(self.ini_path)

        # 构造数据库连接参数
        self.db_conf = dict(self.conf.items('monitor'))
        self.db_conf['port'] = int(self.db_conf['port'])
        self.db_conf['cursorclass'] = pymysql.cursors.DictCursor

        # 连接数据库
        self.db = pymysql.connect(**self.db_conf)
        self.cursor = self.db.cursor()

    def get(self):
        return self.cursor, self.db

    # 析构函数 & 关闭数据库
    def __del__(self):
        self.cursor.close()
        self.db.close()


if __name__ == 'monitor.tools.monitorDB':
    monitorDB = MonitorDB()
