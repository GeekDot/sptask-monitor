#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# -----------------------------------------------------------------------------
#
# 增加状态判断，是为了监控系统在临界状态、及时监控的时候都能保证写入数据库的状态是正确的
#
# * 所谓及时监控：是不设置延时时间，sleep(0) 这样会导致频繁读取硬盘，影响正常任务
# * 所谓临界状态：是考虑程序在微观世界内，发生在几微秒的时间内，所有有可能遇到的问题
#
# 例如：监控模块可能在第 10μs 的时候拿到了任务的 pid，在第 11μs 的时候记录模块可能执行完成释放了 pid
# 并将数据库的状态改为 5，而此时的监控模块拿到的还是 10μs 时候的 pid，没来得及进行下一轮判断就直接将此
# 时数据库的状态 5 改为 3，这样就导致一个悖论出现，数据是执行完成后的数据，而状态却是运行时候的状态......
#
# 例子中 3 是[正在执行]状态， 5 是[执行完成]状态
#
# 下面的[执行中断]状态判断和这个一样
#
# -----------------------------------------------------------------------------

"""
" 监控程序：监控模块 & 守护进程
" @mointor_daemon
"""

__author__ = 'zhangyi'

from monitor.tools.monitorPath import monitorPath
from monitor.tools.emailAlert import emailAlert
from monitor.tools.monitorLog import monitorLog
from monitor.tools.monitorDB import monitorDB
from monitor.tools.datetimeTool import dtts
import time
import os


class Daemon(object):
        
    # 构造函数
    def __init__(self):

        self.cursor, self.db = monitorDB.get()
        self._put_task_status = self._get_task_status

    # 获取状态
    def _get_task_status(self, sql):

        self.cursor.execute(sql)
        task_data = self.cursor.fetchone()
        self.db.commit()

        return task_data

    # 雷达扫描 - 数据库自检
    def _radar_scanning(self):

        sql = 'UPDATE ad_task_info SET task_status=5 WHERE task_status=3 AND run_time IS NOT NULL'

        code = self.cursor.execute(sql)
        self.db.commit()

        if code != 0:
            error_log = '[监控模块] - 检测到数据库存在状态数据遗漏 - 雷达扫描已启动 - 已完成数据库自检'
            monitorLog.send(error_log, log_type='warning')

    # 邮件报警信息
    @staticmethod
    def _email_alert_info(task_data, db_id, db_pid):

        alert_title = '[Python 监控程序报警]：%s 执行中断' % task_data['program_name']
        alert_data = '''
                        %s 检测到有任务中断，中断详情如下：

                        任务名称：%s
                        程序名称：%s
                        中断时间：%s
                        文件路径：%s
                        服务器名：%s
                        服务器ip：%s
                        任务id：%s
                        任务pid：%s
                    ''' % (__doc__, task_data['task_name'], task_data['program_name'], dtts.datetime,
                           task_data['file_path'], task_data['server_name'], task_data['server_ip'],
                           db_id, db_pid)

        return alert_title, alert_data

    # 监控程序启动
    def run(self):

        try:
            pid_list = os.listdir(monitorPath.pids_path)
            self._radar_scanning()

            if pid_list is None:
                return None

            for pid in pid_list:
                db_id = str(pid.split('·')[0])
                db_pid = str(pid.split('·')[1])

                cmd = "ps aux | grep %s | grep -v grep | awk '{print $2}'" % db_pid
                os_pid = os.popen(cmd).read().split('\n')

                # 正在执行
                if db_pid in os_pid:
                    sql = 'SELECT * FROM ad_task_info WHERE id=%s' % db_id
                    task_data = self._get_task_status(sql)
                    task_status = task_data['task_status']

                    # 程序正在执行，写入状态 3
                    if task_status != 5:
                        sql = 'UPDATE ad_task_info SET task_status=3 WHERE id=%s' % db_id
                        self._put_task_status(sql)

                    print('* [程序正在执行] - id: ' + db_id + ' - 已写入状态(3) ==> 程序正常执行')

                # 执行中断
                else:
                    sql = 'SELECT * FROM ad_task_info WHERE id=%s' % db_id
                    task_data = self._get_task_status(sql)
                    task_status = task_data['task_status']

                    # 程序执行中断，写入状态 4
                    if task_status != 5:
                        sql = 'UPDATE ad_task_info SET task_status=4 WHERE id=%s' % db_id
                        self._put_task_status(sql)

                        # 发送邮件
                        alert_title, alert_data = self._email_alert_info(task_data, db_id, db_pid)
                        emailAlert.send(alert_title, alert_data)

                        # 写入日志
                        error_log = '[监控模块] - 程序执行中断 - %s - id:%s ==> (db_pid:%s | os_pid:%s)' % (
                            task_data['program_name'], db_id, db_pid, os_pid)
                        monitorLog.send(error_log, log_type='error')

                        # 删除文件
                        os.remove(monitorPath.pids_path + pid)

                        print('* [程序执行中断] - id: ' + db_id + ' - 已写入状态(4) ==> 报警邮件已发送')

        except Exception as e:
            error_log = '[监控模块] - 内部发生严重错误 - ' + str(e)
            monitorLog.send(error_log, log_type='fatal')


if __name__ == '__main__':

    daemon = Daemon()

    while True:
        daemon.run()
        time.sleep(3)
