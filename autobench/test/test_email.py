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

a = Email_Txt_Msg()
source = 'jun.gou@idt.com'
destination = 'jun.gou@idt.com'
subject = 'The test is done.'
text = 'The test is done, please take care!'
a.send_msg(source, destination, subject, text)