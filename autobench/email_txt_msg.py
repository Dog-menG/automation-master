import smtplib
from autobench import log


class Email_Txt_Msg(object):

    def __init__(self):
        self.log = log(self.__class__.__name__)

    def send_msg(self, source, destination, subject, text):
        mail_server = "mail.corp.idt.com"
        message = """
From: %s
To: %s
Subject: %s
%s
        """ % (source, destination, subject, text)
        # Send the mail
        server = smtplib.SMTP(mail_server)
        try:
            server.sendmail(source, destination, message)
            self.log.info('The e-mail sends successfully.')
        except smtplib.SMTPException:
            self.log.warn('The e-mail does not send.')
        server.quit()

