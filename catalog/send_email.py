import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
import django

django.setup()

from catalog.models import Recipient
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from catalog.models import Message

# Загрузка Django
django.setup()

# Настройки для подключения к SMTP-серверу Mail.ru
smtp_server = 'smtp.mail.ru'
smtp_port = 587  # Порт SMTP-сервера Mail.ru
email_address = 'skyprokutalov.k.v@mail.ru'
email_password = 'ud8KsqPUJmPxwHEXJbWd'


def send_email(recipient_email, subject, body):
    try:
        # Установка соединения с SMTP-сервером Mail.ru
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_address, email_password)  # Аутентификация на сервере

        # Формирование сообщения
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Отправка письма
        server.sendmail(email_address, recipient_email, msg.as_string())

        print(f"Письмо успешно отправлено для {recipient_email}")
        server.quit()
        return True
    except Exception as e:
        print(f"Ошибка отправки письма для {recipient_email}:", e)
        return False


def send_emails_to_recipients():
    recipients = Recipient.objects.all()
    messages = Message.objects.all()

    for index, recipient in enumerate(recipients):
        if index < len(messages):
            message = messages[index]
            send_email(recipient.email, message.subject, message.body)
        else:
            print(f"Недостаточно сообщений для отправки получателю {recipient.email}")


# функция отправки писем
send_emails_to_recipients()
