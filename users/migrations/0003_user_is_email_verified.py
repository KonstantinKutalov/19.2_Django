# Generated by Django 5.0.2 on 2024-03-25 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_verified',
            field=models.BooleanField(default=False, verbose_name='Адрес электронной почты подтвержден'),
        ),
    ]
