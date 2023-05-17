# -*- coding:utf-8 -*-

# Created on 2023/5/13.
import smtplib

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import TemplateNotFound
from email.mime.text import MIMEText
from email.header import Header

from common import logger


class EmailSender:

    def __init__(self, server_host, server_port, sender, sender_authorization_code, receivers):
        self.server_host = server_host
        self.server_port = server_port
        self.sender = sender
        self.sender_authorization_code = sender_authorization_code
        self.receivers = receivers

    def send(self, header, content):
        smtp = None
        try:
            mail = MIMEText(content, "html", "utf-8")
            mail["Subject"] = Header(header, "utf-8")
            mail["From"] = self.sender
            mail["To"] = ', '.join(self.receivers)

            smtp = smtplib.SMTP_SSL(self.server_host, self.server_port)
            smtp.set_debuglevel(1)
            smtp.ehlo()
            smtp.login(self.sender, self.sender_authorization_code)
            smtp.sendmail(self.sender, self.receivers, mail.as_string())
            logger.log_info("send email successfully")
        except Exception as ex:
            logger.log_error(f"send email fail, reason: {ex}")
        finally:
            if smtp:
                smtp.quit()


class Templates:

    def __init__(self, template_dir, template_name):
        self.template_dir = template_dir
        self.template_name = template_name

    def render_template(self, **kwargs):
        env = Environment(loader=FileSystemLoader(self.template_dir), trim_blocks=True)

        try:
            template = env.get_template(self.template_name)
        except TemplateNotFound:
            raise TemplateNotFound(self.template_name)

        content = template.render(kwargs)
        return content

    def render(self, **kwargs):
        content = self.render_template(**kwargs)
        return content
