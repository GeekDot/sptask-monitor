#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from monitor import monitor
import time


@monitor(1)
def main():
    print("....... 被监控程序 .......")
    time.sleep(10)


if __name__ == '__main__':
    main()
