# Generated by Django 3.0.5 on 2020-12-08 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abtest', '0006_auto_20201208_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcesetup',
            name='channel_name',
            field=models.CharField(default='none', max_length=255, verbose_name='Название канала'),
        ),
    ]
