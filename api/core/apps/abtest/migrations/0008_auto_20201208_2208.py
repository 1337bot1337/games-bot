# Generated by Django 3.0.5 on 2020-12-08 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abtest', '0007_sourcesetup_channel_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sourcesetup',
            name='channel_name',
        ),
        migrations.AddField(
            model_name='sourcesetup',
            name='channel_link',
            field=models.CharField(default='none', max_length=255, verbose_name='Ссылка на канал'),
        ),
    ]
