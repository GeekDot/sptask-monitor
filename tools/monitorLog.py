#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

__author__ = 'zhangyi'

from monitor.tools.monitorPath import monitorPath
from monitor.tools.datetimeTool import dtts
import logging


class MonitorLog(object):

    def __init__(self):

        self.log_path = monitorPath.logs_path
        self.log_file = monitorPath.logs_path + dtts.date + '.log'

        self.log_conf = {
                    'filename': self.log_file,
                    'filemode': 'a',
                    'datefmt': '%Y-%m-%d %X',
                    'level': logging.INFO,
                    'format': '%(asctime)s - [%(levelname)s]: %(message)s'
                     }

        logging.basicConfig(**self.log_conf)
        self.logger = logging.getLogger()

    def send(self, log_data, log_type='info'):

        log_list = {
                    'fatal': self.logger.fatal,
                    'critical':  self.logger.critical,
                    'error':  self.logger.error,
                    'warning':  self.logger.warning,
                    'info':  self.logger.info,
                    'debug':  self.logger.debug,
                    }

        send_log = log_list[log_type]
        send_log(log_data)


if __name__ == 'monitor.tools.monitorLog':
    monitorLog = MonitorLog()
