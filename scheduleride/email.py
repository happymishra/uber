import logging
import traceback

from django.core.mail import send_mail

logger = logging.getLogger('custom-module')


class Mail:
    def __int__(self):
        pass

    @staticmethod
    def send_email(subject, message, from_email, to_email_list):
        for i in range(3):
            try:
                send_mail(subject, message, from_email, to_email_list)
                break
            except Exception as ex:
                logger.info(f"Retrying sending email... {i}")
                if i == 2:
                    logger.error(traceback.format_exc())


if __name__ == '__main__':
    Mail.send_email("First email", "hello",
                    "rupeshmishra2517@gmail.com",
                    ['happymishra66@gmail.com'])
