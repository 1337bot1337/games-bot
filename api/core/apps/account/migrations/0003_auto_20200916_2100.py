# Generated by Django 3.0.5 on 2020-09-16 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20200907_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramaccount',
            name='tg_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='Telegram user ID'),
        ),
    ]
