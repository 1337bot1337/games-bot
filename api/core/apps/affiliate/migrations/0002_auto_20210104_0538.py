# Generated by Django 3.0.5 on 2021-01-04 05:38

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliatesetup',
            name='min_referral_deposit',
            field=models.DecimalField(decimal_places=2, default=Decimal('1000'), max_digits=10, verbose_name='Минимальная сумма депозита реферала для выплаты бонусов рефереру'),
        ),
        migrations.AddField(
            model_name='affiliatesetup',
            name='type_referral_deposit_bonus',
            field=models.CharField(choices=[('factor', 'Множитель'), ('fixed', 'Фиксированный')], default='factor', max_length=50, verbose_name='Тип бонуса для реферала за разовый депозит'),
        ),
    ]
