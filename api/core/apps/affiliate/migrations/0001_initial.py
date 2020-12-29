# Generated by Django 3.0.5 on 2020-12-28 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0004_auto_20201122_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliateSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=255, verbose_name='Имя профиля')),
                ('referrer_deposit_bonus', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Бонус рефереру от депозита реферала')),
                ('referral_deposit_bonus', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Разовый бонус рефералу на депозит')),
            ],
            options={
                'verbose_name': 'Настройки партнёрской программы',
                'verbose_name_plural': 'Настройки партнёрской программы',
            },
        ),
        migrations.CreateModel(
            name='UserAffiliate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('referral', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='refl', to='account.TelegramAccount', verbose_name='Реферал')),
                ('referrer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refr', to='account.TelegramAccount', verbose_name='Реферер')),
            ],
            options={
                'verbose_name': 'Реестр рефералов',
                'verbose_name_plural': 'Реестр рефералов',
            },
        ),
    ]