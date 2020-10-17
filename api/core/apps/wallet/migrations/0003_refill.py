# Generated by Django 3.0.5 on 2020-09-20 17:33

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200916_2100'),
        ('wallet', '0002_auto_20200916_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='Refill amount')),
                ('multiplier', models.DecimalField(decimal_places=2, default=Decimal('1'), max_digits=5, verbose_name='Multiplier snapshot')),
                ('status', models.CharField(choices=[('in_progress', 'Refill in progress'), ('succeed', 'Refill succeed'), ('failed', 'Refill failed')], default='in_progress', max_length=50, verbose_name='Status')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.TelegramAccount')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]