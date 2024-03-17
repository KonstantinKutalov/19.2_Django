import os
import sys
import django

sys.path.append('C:\\Users\\kutalov\\Desktop\\19.2_Django\\catalog')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from catalog.models import Recipient, MailingSettings, Message, MailingLog
from catalog.send_email import send_email


def run_mailing():
    # Получение всех активных рассылок
    mailings = MailingSettings.objects.filter(status='created')

    for mailing in mailings:
        recipients = Recipient.objects.all()  # фильтрация по часам для отправки(еще в работе)
        message = Message.objects.latest('id')  # Получение последнего сообщения
        for recipient in recipients:
            send_email(recipient.email, message.subject, message.body)
            # Создание записи в логе рассылок
            log_entry = MailingLog(recipient=recipient, mailing_settings=mailing, status='sent')
            log_entry.save()
        # Изменение статуса рассылки
        mailing.status = 'completed'
        mailing.save()


if __name__ == "__main__":
    run_mailing()
