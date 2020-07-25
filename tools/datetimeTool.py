#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import arrow


class DateTimeTools(object):

    @property
    def year(self):
        return str(arrow.now().year)

    @property
    def month(self):
        return str(arrow.now().month)

    @property
    def day(self):
        return str(arrow.now().day)

    @property
    def hour(self):
        return str(arrow.now().hour)
        
    @property
    def minute(self):
        return str(arrow.now().minute)

    @property
    def second(self):
        return str(arrow.now().second)

    @property
    def date(self):
        return str(arrow.now().date())

    @property
    def time(self):
        return str(arrow.now().time()).split('.')[0]

    @property
    def datetime(self):
        return str(arrow.now().datetime).split('.')[0]

    @property
    def timestamp(self):
        return str(arrow.now().timestamp)

    @staticmethod
    def dt2ts(dt_str):
        return str(arrow.get(dt_str).to('local').timestamp)

    @staticmethod
    def ts2dt(ts_str):
        return str(arrow.get(ts_str).to('local')).split('+')[0].replace('T', ' ')

    @property
    def sfdate(self):
        return str(arrow.now().shift(days=-1)).split('T')[0]


if __name__ == 'monitor.tools.datetimeTool':
    dtts = DateTimeTools()
