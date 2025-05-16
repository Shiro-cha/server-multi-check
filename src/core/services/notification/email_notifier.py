import smtplib
from email.mime.text import MIMEText
from jinja2 import Template

from .base import Notifier

class EmailNotifier(Notifier):
    def __init__(self, smtp_host, smtp_port, sender, receiver, template_path):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender = sender
        self.receiver = receiver
        self.template_path = template_path

    def notify(self, context: dict):
        with open(self.template_path, 'r') as f:
            template = Template(f.read())
        
        message = template.render(context)
        msg = MIMEText(message)
        msg['Subject'] = '🚨 Server Alert'
        msg['From'] = self.sender
        msg['To'] = self.receiver

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.sendmail(self.sender, [self.receiver], msg.as_string())
