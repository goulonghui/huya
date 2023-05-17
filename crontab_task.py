# -*- coding:utf-8 -*-

# Created on 2023/5/13.
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone

from common import config
from common import db
from common import logger
from query_huya_appeal import tick


class CronTabServer:

    def __init__(self, interval_minutes):
        # 阻塞式任务
        self.scheduler = BlockingScheduler(timezone=timezone('Asia/Shanghai'))
        self.interval_minutes = int(interval_minutes) or 60

    def add_job(self):
        """
        添加定时任务
        Usage:
            每10秒执行一次
            add_job(func, trigger="interval", seconds=10, args=(A,B))
            每天10点至11点,每5分钟执行一次
            add_job(func, trigger="cron", hour="10-11", minute="0-59/5", args=(A,B))
            args:
                func:           callable对象
                trigger:        触发器 (eg. date/interval/cron)
                seconds:        间隔时间(interval trigger)
                hour/minute:    时间点(cron trigger)
                args:           func的参数

        详见: https://apscheduler.readthedocs.io/en/latest/py-monindex.html
        """
        logger.log_info("add job ")
        logger.log_info(f"self.interval_minutes: {self.interval_minutes}")
        self.scheduler.add_job(tick, trigger="interval", minutes=self.interval_minutes, name="check huya user.")
        # test
        # self.scheduler.add_job(tick, trigger="interval", minutes=1, name="check huya user.")

        logger.log_info("add job done! ")

    def start(self):
        logger.log_info("start...")
        try:
            self.add_job()
            self.scheduler.start()
        except Exception as e:
            logger.log_error("Error occur, scheduler Exit! error:{}".format(e))


def run():
    logger.log_init("huya", config.log_config['log_dir'], "huya", config.log_config['log_level'])
    logger.log_info(f"crontab start， process id: {os.getpid()}")
    task_interval_minutes = db.get_config("task_interval_minutes")
    logger.log_info(f"task_interval_minutes: {task_interval_minutes}")
    try:
        int(task_interval_minutes)
    except ValueError:
        task_interval_minutes = 60
    crontab_server = CronTabServer(task_interval_minutes)
    crontab_server.start()
