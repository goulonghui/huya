# -*- coding:utf-8 -*-

# Created on 2023/5/13.
import logging
from common import logger


def init_log():
    log_path = "./log"
    file_name = "huya"
    log_prefix = "huya"
    log_level = 4
    logger.log_init(file_name, log_path, log_prefix, log_level)


init_log()
logger.log_info("infoxxx")
logger.log_error("errorxxx")