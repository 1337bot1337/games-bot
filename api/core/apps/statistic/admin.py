from django.contrib import admin

from core.apps.statistic.models import TelegramAccountStatistic


@admin.register(TelegramAccountStatistic)
class TelegramAccountStatisticAdmin(admin.ModelAdmin):
    list_display = ("tg_id", "type_action", "data_action", "created",)
