# -*- coding:utf-8 -*-

# Created on 2023/5/13.

log_config = {
    "log_dir": "/data/log",
    "log_level": 4
}

db_config = {
    "host": "mysql",
    "port": 3306,
    "user": "root",
    "password": "huya123456",
    "database": "huya",
}

task_init_configs = [
    {"configKey": "task_interval_minutes", "configValue": 60, "configDesc": "定时任务执行间隔，单位:分钟"},
    {"configKey": "sender", "configValue": "1792269826@qq.com", "configDesc": "通知邮件发送人"},
    {"configKey": "sender_authorization_code", "configValue": "kzujkulvamfsjfca", "configDesc": "通知邮件发送人QQ邮箱授权码，要获取QQ邮箱授权码，请登录到您的QQ邮箱，然后进入“设置”>“账户”>“POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务”，开启SMTP服务并获取授权码。"},
    {"configKey": "receivers", "configValue": "1633032999@qq.com", "configDesc": "通知邮件接收人，多个接收人使用英文逗号隔开"},
    {"configKey": "huya_url", "configValue": "https://udbsec.huya.com/web/appeal/launch", "configDesc": "huya url"},
    {"configKey": "proxy_url", "configValue": "http://ecs.hailiangip.com:8422/api/getIpEncrypt?dataType=0&encryptParam=k60Va%2B4TTIoiEPFfhUCySK%2FfT7GfQ3maxDbxprdoOkx%2FGQEB0bczI8I1Y8m2yCtLjWqgS6zERlFtF7BqxBumooSjSMhUAc59q1rbh7hrCLDWV4ZRTSE4iW8OGnd9JbBiqdur9u0LopeKHKfGrVuCr92yc5DeNEt1%2BpiEXAmvsidXwMMY2Pp7wRNtgRIJmPbHvs3ERyFHZ9FAgNS8WBDIMl7%2FeDXlL0x6IKTgy4kKtwD10%2FrggxuKwg%2Fa3uSVATqr", "configDesc": "proxy url"}
]

email_config = {
    "server_host": "smtp.qq.com",
    "server_port": 465,
    "sender": "",
    # 要获取QQ邮箱授权码，请登录到您的QQ邮箱，然后进入“设置”>“账户”>“POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务”，开启SMTP服务并获取授权码。
    "sender_authorization_code": "",
    "receivers": [],
}
