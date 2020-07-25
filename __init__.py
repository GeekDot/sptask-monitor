#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
" 监控程序：记录模块 & 装饰器
" @mointor_mointor
" @mointor_record
"""

__author__ = 'zhangyi'

from monitor.tools.monitorPath import monitorPath
from monitor.tools.monitorLog import monitorLog
from monitor.tools.monitorDB import monitorDB
from monitor.tools.datetimeTool import dtts
import os


# 记录模块
class Record(object):

    def __init__(self):
        self.cursor, self.db = monitorDB.get()

    # 自动构建SQL语句
    @staticmethod
    def _auto_make_sql(data):

        update_list = ['start_time', 'end_time', 'run_time']
        update_data = []
        key = []
        value = []

        for k, v in data.items():
            if k in update_list:
                update_data.append(k + "='" + str(v) + "'")

            key.append(k)
            value.append(str(v))

        block1 = "INSERT INTO ad_task_info ("
        block2 = ", ".join(key)
        block3 = ") VALUES ('"
        block4 = "', '".join(value)
        block5 = "') ON DUPLICATE KEY UPDATE task_status=%s" % str(data.get('task_status', '1'))

        sql = block1 + block2 + block3 + block4 + block5

        if len(update_data) == 1:
            sql = sql + ", " + update_data[0]

        if len(update_data) == 2:
            sql = sql + ", " + update_data[0] + ', ' + update_data[1]

        sql = sql.replace(r"'NULL'", "NULL")

        return sql

    # 将任务id和pid写到文件
    def _put_pid_file(self, data):
        
        this_id = str(data)
        this_pid = str(os.getpid())

        self.pid_path = monitorPath.pids_path
        self.pid_file = this_id + '·' + this_pid
        self.path_file = self.pid_path + self.pid_file

        with open(self.path_file, 'w') as f:
            f.write(self.pid_file + ' ' + dtts.datetime)

    # 将数据放入数据库
    def put_db(self, data):

        sql = self._auto_make_sql(data)
        
        try:
            self.cursor.execute(sql)

            if data['id'] == 'NULL':
                call_id = int(self.cursor.lastrowid)
                self._put_pid_file(call_id)
            else:
                call_id = None

            self.db.commit()

        except Exception as e:
            error_log = '[记录模块] - 写入数据库发生错误 - ' + str(e)
            monitorLog.send(error_log, log_type='critical')
            raise e

        else:
            return call_id

    # 从数据库中获取任务信息
    def get_db(self, data):

        sql = 'SELECT id, media_id, task_name, program_name, task_type, server_name, server_ip, file_path, task_crontab\
               FROM ad_task_list WHERE id=%s' % data
        self.cursor.execute(sql)
        task_data = self.cursor.fetchone()

        return task_data

    # 返回pid文件路径
    def get_pid_path(self):
        return self.path_file


# 装饰器模块 - 用于嵌入任务程序
def monitor(task_id):
    def _core(core):
        def kernel():
            try:
                # 初始化记录模块
                record = Record()

                # 获取任务详情
                data = record.get_db(task_id)

                # 初始化数据
                data['id'] = 'NULL'

                # 数据库回调id
                call_id = record.put_db(data)

                # 未执行
                status = {'id': call_id, 'task_status': 1}
                record.put_db(status)

                # 开始执行
                start_time = dtts.datetime
                status = {'id': call_id, 'task_status': 2, 'start_time': start_time}
                record.put_db(status)
            
                # -----* 核心程序 *-----
                core()

            except Exception as e:
                error_log = '[记录模块] - 程序执行时发生错误 - ' + str(e)
                monitorLog.send(error_log, log_type='error')
                raise e
            
            else:
                # 删除文件
                os.remove(record.get_pid_path())

                # 执行完成
                end_time = dtts.datetime
                run_time = int(dtts.dt2ts(end_time)) - int(dtts.dt2ts(start_time))
                status = {'id': call_id, 'task_status': 5, 'end_time': end_time, 'run_time': run_time}
                record.put_db(status)

        return kernel
    return _core
