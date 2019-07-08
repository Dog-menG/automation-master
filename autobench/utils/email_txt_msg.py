import smtplib
from autobench import log


class Email_txt_msg(object):

    def __init__(self):
        self.log = self.log(self.__class__.__name__)

    def send_msg(self, source, destination, subject, text):
        SERVER = "mail.corp.idt.com"
        message = """
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (source, destination, subject, text)

        # Send the mail

        server = smtplib.SMTP(SERVER)
        server.sendmail(source, destination, message)
        server.quit()
