# Generated by Django 3.0.5 on 2020-11-15 17:25

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)], verbose_name='Desire withdraw amount')),
                ('card_number', models.CharField(max_length=20, verbose_name='Card number')),
                ('status', models.CharField(choices=[('accepted', 'Withdraw request accepted'), ('rejected', 'Withdraw request rejected'), ('in_progress', 'Withdraw request in progress')], default='in_progress', max_length=50, verbose_name='Withdraw request status')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.TelegramAccount')),
            ],
            options={
                'abstract': False,
            },
        ),
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