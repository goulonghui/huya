# -*- coding:utf-8 -*-

# Created on 2023/5/13.

import json
import time

import requests

from common import logger


def post_request_from_dict(url, dict_data):
    response = requests.post(url, data=json.dumps(dict_data))
    return response.status_code, response.content.decode('utf-8')


def post_request_from_json(url, data, proxies=None):
    kwargs = {
        "url": url,
        "json": data
    }
    if proxies:
        kwargs["proxies"] = {
            "http": proxies,
            "https": proxies
        }
        logger.log_info(f"request use proxy: {proxies}")
    logger.log_debug(f"curl {url} -d '{json.dumps(data)}'")
    response = requests.post(**kwargs)
    code, content = response.status_code, response.content.decode('utf-8')
    logger.log_debug(f"response: code:{code}, content: {content}")
    return code, content


def get_request(url):
    response = requests.get(url)
    return response.status_code, response.content.decode('utf-8')


def retry(times=5, delay_interval=5):
    def warp(func):
        def inner(*args, **kwargs):
            retry_times = 1
            delay_interval_st = 0
            while retry_times <= times:
                time.sleep(delay_interval_st)
                ret = func(*args, **kwargs)
                if ret is not False:
                    return ret
                logger.log_info("start retrying %s..." % retry_times)
                retry_times += 1
                delay_interval_st += delay_interval
        return inner
    return warp
