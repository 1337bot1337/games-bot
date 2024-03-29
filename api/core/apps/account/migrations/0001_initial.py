# Generated by Django 3.0.5 on 2020-11-15 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('tg_id', models.PositiveIntegerField(unique=True, verbose_name='Telegram user ID')),
                ('real_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Real balance amount')),
                ('virtual_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Virtual balance amount')),
                ('source', models.CharField(default='default', max_length=50, verbose_name='Source of user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
