#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
" 监控程序：统计模块 & 日常报表
" @mointor_daily_report
"""

__author__ = 'zhangyi'

from monitor.tools.monitorPath import monitorPath
from monitor.tools.emailAlert import emailAlert
from monitor.tools.monitorDB import monitorDB
from monitor.tools.datetimeTool import dtts
import pandas


class DailyReport(object):

    # 构造函数
    def __init__(self):

        self.cursor, self.db = monitorDB.get()
        self.table_title = ['媒体id', '任务名称', '程序名称', '开始时间', '结束时间', '耗时(s)', '执行状态']
        self.email_title = '监控程序：%s 日常报表' % dtts.sfdate
        self.email_content = ''

    # 获取数据
    def _get_data(self):

        sql = "SELECT * FROM ad_task_info WHERE start_time LIKE '" + dtts.sfdate + \
              " %' ORDER BY task_status ASC, task_name ASC, start_time DESC"
        self.cursor.execute(sql)
        db_data = self.cursor.fetchall()

        return db_data

    # 自动构造HTML语句
    def _auto_make_html(self, data):

        table = pandas.DataFrame(data, columns=self.table_title)
        html_table = table.to_html(index=False)

        with open(monitorPath.html_path) as f:
            html = f.readlines()
            head = ''.join(html[:104])
            foot = ''.join(html[104:])

        html_data = head + html_table + foot

        return html_data

    def main(self):

        db_data = self._get_data()
        content = []

        for data_dict in db_data:

            data = list()

            data.append(data_dict['media_id'])
            data.append(data_dict['task_name'])
            data.append(data_dict['program_name'])
            data.append(data_dict['start_time'])
            data.append(data_dict['end_time'])
            data.append(data_dict['run_time'])

            # 执行完成
            if data_dict['task_status'] == 5:
                replace_task_status = '🔵'

            # 执行中断
            elif data_dict['task_status'] == 4:
                replace_task_status = '🔴'

            # 数据库异常
            else:
                replace_task_status = '⚫'

            data.append(replace_task_status)
            content.append(data)

        self.email_content = self._auto_make_html(content)

        emailAlert.send(self.email_title, self.email_content, send_type='html')


if __name__ == '__main__':
    dailyReport = DailyReport()
    dailyReport.main()
