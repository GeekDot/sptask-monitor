#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
" 监控程序：检测模块 & 心跳检测
" @mointor_heart_rate
"""

__author__ = 'zhangyi'

from monitor.tools.monitorPath import monitorPath
from monitor.tools.monitorLog import monitorLog
from monitor.tools.emailAlert import emailAlert
from monitor.tools.datetimeTool import dtts
import os


class HeartRate(object):

    def __init__(self):

        self.restart_daemon = monitorPath.python_path + ' ' + monitorPath.daemon_path + '&'

        self.host_name = os.popen('hostname').read().replace('\n', '')
        self.monitor_title = '[Python 心跳检测报警]：监控程序'
        self.monitor_data = '%s 检测到 [监控程序: 监控模块 & 守护进程 - daemon.py] 中断，中断详情如下：\n\n服务器名：%s\n中断时间：%s\n' % \
                            (__doc__, self.host_name, dtts.datetime)

    def main(self):

        cmd = "ps aux | grep '%s' | grep -v grep | awk '{print $2}'" % monitorPath.daemon_path
        pid = os.popen(cmd).read().replace('\n', '')

        if pid == '':

            code = os.system(self.restart_daemon)

            if code == 0:
                monitor_state = '监控状态：%s\n启动状态码：%s' % ('重启成功', code)
                emailAlert.send(self.monitor_title, self.monitor_data + monitor_state)

                error_log = '[心跳检测] - 监控模块运行中断 - 重启成功 - 启动状态码:%s' % code
                monitorLog.send(error_log, log_type='error')

                print(error_log)

            else:
                monitor_state = '监控状态：%s\n启动状态码：%s' % ('重启失败', code)
                emailAlert.send(self.monitor_title, self.monitor_data + monitor_state)

                error_log = '[心跳检测] - 监控模块运行中断 - 重启失败 - 启动状态码:%s' % code
                monitorLog.send(error_log, log_type='error')

                print(error_log)

        else:
            print('* 监控程序: 监控模块 & 守护进程 - [正常运行] ==> pid:', pid)


if __name__ == '__main__':
    run = HeartRate()
    run.main()
