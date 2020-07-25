#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'zhangyi'


class MonitorPath(object):

    def __init__(self):

        self.path = '/Users/zhangyi/adnice/monitor/monitor/'
        self.pids_path = self.path + 'pids/'
        self.logs_path = self.path + 'logs/'
        self.html_path = self.path + 'html/daily_report.html'
        self.ite_path = self.path + 'config/monitor.db'
        self.conf_path = self.path + 'config/monitor.ini'
        self.python_path = '/Users/zhangyi/.virtualenvs/monitor/bin/python'
        self.daemon_path = self.path + 'daemon.py'


if __name__ == 'monitor.tools.monitorPath':
    monitorPath = MonitorPath()
