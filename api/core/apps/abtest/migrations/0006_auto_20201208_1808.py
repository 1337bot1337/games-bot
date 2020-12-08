# Generated by Django 3.0.5 on 2020-12-08 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abtest', '0005_auto_20201128_0401'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sourcesetup',
            options={'verbose_name': 'Конфигурация источника трафика', 'verbose_name_plural': 'Конфигурации источника трафика'},
        ),
        migrations.AddField(
            model_name='sourcesetup',
            name='ad_link',
            field=models.URLField(default='none', verbose_name='Рекламная ссылка'),
        ),
        migrations.AddField(
            model_name='sourcesetup',
            name='creative_link',
            field=models.URLField(default='none', verbose_name='Ссылка на креатив'),
        ),
    ]
