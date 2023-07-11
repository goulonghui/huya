# -*- coding:utf-8 -*-

# Created on 2023/5/13.

import datetime
import json
import os
import traceback

import requests

from common import db, http_request, logger
from common import email
from common.config import email_config


class HuYa:

    huya_code = {
        "normal": [0],
        "need_proxy": [210003],
        "need_notify": [90013, 90030, 90024]
    }

    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "email_template")
    proxy_alarm_template = "proxy_alarm_template.jinja2"
    proxy_alarm_header = "代理服务不可用，请检查"
    user_alarm_template = "user_alarm_template.jinja2"
    user_alarm_header = "存在用户账号异常，请处理"

    alarm_proxy_interval = 20

    def __init__(self):
        self.users = []
        self.proxies = []
        self.last_alarm_proxy_time = None
        self.current_proxy = None

    @staticmethod
    def query_user_ids():
        data = db.query_user()
        return data["users"]

    @staticmethod
    def query_email_config():
        sender, sender_authorization_code, receivers = \
            db.get_config(("sender", "sender_authorization_code", "receivers"))
        email_config.update({
            "sender": sender,
            "sender_authorization_code": sender_authorization_code,
            "receivers": list(map(lambda x: x.strip(), receivers.split(","))),
        })
        logger.log_info(f"email_config: {email_config}")

    @http_request.retry(times=3, delay_interval=10)
    def request_proxy(self, proxy_url):
        """
        {
            "serialNo": "d8b20e1cb05d499f86ae63582a5c894f",
            "code": 0,
            "data": [
                {
                    "realIp": "175.173.223.126",
                    "pid": 6,
                    "cid": 34,
                    "area": "辽宁-盘锦",
                    "ip": "183.162.226.247",
                    "port": 28926
                }
            ]
        }
        :param proxy_url:
        :return:
        """
        logger.log_debug(f"curl {proxy_url}")
        code, content = http_request.get_request(proxy_url)
        logger.log_debug(f"proxy response: code:{code}, content: {content}")
        if code != 200:
            return False
        try:
            content = json.loads(content)
        except json.decoder.JSONDecodeError:
            logger.log_error("proxy response JSONDecodeError!!!")
            return False
        if content.get("code") != 0 or "data" not in content:
            return False
        return content["data"]

    def get_proxies(self):
        logger.log_info("no proxy. start get proxy...")
        proxy_url = db.get_config("proxy_url")
        data = self.request_proxy(proxy_url)
        if not data:
            logger.log_error(f"proxy not working !!!, check proxy: {proxy_url}")
            self.alarm_proxy_not_working(proxy_url)
            raise RuntimeError("proxy not working !!!")
        self.proxies = [f"{_['ip']}:{_['port']}" for _ in data]
        logger.log_info(f"get proxy finish, proxies: {self.proxies}")

    def alarm_proxy_not_working(self, proxy_url):

        def send():
            self.last_alarm_proxy_time = datetime.datetime.now()
            content = email.Templates(self.template_dir, self.proxy_alarm_template).render(proxy_url=proxy_url)
            logger.log_info("render proxy alarm template successfully, start send email")
            self.query_email_config()
            email.EmailSender(**email_config).send(self.proxy_alarm_header, content)

        if not self.last_alarm_proxy_time:
            send()
        elif datetime.datetime.now() > \
                (self.last_alarm_proxy_time + datetime.timedelta(minutes=self.alarm_proxy_interval)):
            send()

    def request_huya_use_proxy(self, huya_url, request_data):
        while True:
            if not self.proxies:
                self.get_proxies()
            if self.proxies:
                self.current_proxy = self.current_proxy or self.proxies.pop()
                try:
                    code, content = http_request.post_request_from_json(
                        huya_url, request_data, proxies=self.current_proxy
                    )
                except requests.exceptions.ProxyError:
                    logger.log_warning(f"this proxy {self.current_proxy} not work, will replace!")
                    self.current_proxy = None
                    continue
                if code != 200:
                    return False
                content = json.loads(content)
                if "returnCode" not in content:
                    return False
                if content["returnCode"] in self.huya_code["need_proxy"]:
                    self.current_proxy = None
                    continue
                return content
            else:
                logger.log_warning("no proxy available!!!")
                return False

    def request_huya_appeal(self, huya_url, request_data):
        if self.current_proxy:
            return self.request_huya_use_proxy(huya_url, request_data)
        else:
            code, content = http_request.post_request_from_json(huya_url, request_data)
        if code != 200:
            return False
        content = json.loads(content)

        if "returnCode" not in content:
            return False

        if content["returnCode"] in self.huya_code["need_proxy"]:
            return self.request_huya_use_proxy(huya_url, request_data)

        return content

    def query_huya_appeal(self):
        """
        https://udbsec.huya.com/web/appeal/launch
        入参： {"uri":0,"data":{"user":"35184444002898"}}
        正常
        返回值： {
            "uri": 0,
            "version": null,
            "context": null,
            "requestId": 0,
            "returnCode": 0,
            "message": null,
            "description": null,
            "data": {
                "result": 0,
                "user": "",
                "uid": 1199530126189,
                "sessionData": "AhUoY3YYjHgRK89AxASsMRWtf_lkHGFo0KNEntVfI1YG6ALF0-hbRJ7HSYqJNQBA_zmjh2fNPWjUUk4uLtXvX-59anfz2-qCJu_ESP-rNPnCgGoRe7ob6QPJHvkfmRrFEa9mTHha8F2vFTEVZ9Sqd20ZNGJFyMAI_Jesw4nPHmNdZjlL0PUXMO3BOqRszeq_RvIQzbA12Dz1La4V1XIiynTFhN6eLADFWkYsfp0Oy6xLJtKWUOrZiGKfC-i6qzV2gzqPL4UqLuhb8L2cTME5JhyeJaAA4WojfVKJ7Us4gKE7qxsa3rNiT5MOhxdf4zEkKg",
                "description": ""
            }
        }
        有申诉记录
        {
            "uri": 0,
            "version": null,
            "context": null,
            "requestId": 0,
            "returnCode": 90013,
            "message": "APPEAL_ORDER_IS_EXIST",
            "description": "此账号的申诉已存在",
            "data": null
        }
        ip限制
        {'uri': 1, 'version': None, 'context': None, 'requestId': 0, 'returnCode': 210003, 'message': '操作过于频繁，请稍后再试', 'description': '操作过于频繁，请稍后再试', 'data': None} <class 'dict'>
        body: {'uri': 0, 'data': {'user': '35184537195586'}}
        :return:
        """
        huya_url = db.get_config("huya_url")
        need_alarm_user_infos = []
        for user_d in self.query_user_ids():
            body = {
                "uri": 0,
                "data": {
                    "user": user_d["user_id"].strip()
                }
            }
            data = None
            try:
                data = self.request_huya_appeal(huya_url, body)
            except Exception as ex:
                logger.log_error(f"InternalError, reason: {ex}")

            if not data:
                logger.log_warning(f"@@@user {user_d['user_id']} request huya appeal failed.@@@")
                continue

            if data["returnCode"] in self.huya_code["need_notify"]:
                need_alarm_user_infos.append({"user_id": user_d["user_id"], "desc": data.get("description")})

        logger.log_warning(f"need_alarm_user_infos: {need_alarm_user_infos}")
        if need_alarm_user_infos:
            self.alarm_user(need_alarm_user_infos)

    def alarm_user(self, need_alarm_user_infos):
        content = email.Templates(self.template_dir, self.user_alarm_template).render(user_infos=need_alarm_user_infos)
        logger.log_info("render user alarm template successfully, start send email")
        self.query_email_config()
        email.EmailSender(**email_config).send(self.user_alarm_header, content)
        return True


def tick():
    logger.log_info(f"{'='*10}query_huya_appeal task wake up. {'='*10}")
    try:
        HuYa().query_huya_appeal()
    except Exception as ex:
        logger.log_error(f"InternalError ex: {ex}")
        logger.log_error(f"traceback: {str(traceback.format_exc())}")













