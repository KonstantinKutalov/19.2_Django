# Generated by Django 5.0.2 on 2024-02-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_product_manufactured_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='attribute1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Атрибут 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='attribute2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Атрибут 2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
