class SendMailSender(object):
    def __init__(self, email_service):
        self.email_service = email_service

    def send(self, to, subject, body):
        
        self.email_service.send_email(to, subject, body)