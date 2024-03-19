# Generated by Django 5.0.2 on 2024-03-17 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_mailingsettings_message_recipient_mailinglog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailinglog',
            name='server_response',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mailinglog',
            name='status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='mailinglog',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.CharField(max_length=50, verbose_name='Номер версии')),
                ('version_name', models.CharField(max_length=100, verbose_name='Название версии')),
                ('is_current', models.BooleanField(default=False, verbose_name='Признак текущей версии')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='catalog.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Версия',
                'verbose_name_plural': 'Версии',
            },
        ),
    ]
