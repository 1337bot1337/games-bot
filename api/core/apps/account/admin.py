from django.contrib import admin

from core.apps.account import models as account_models


@admin.register(account_models.TelegramAccount)
class TelegramAccountAdmin(admin.ModelAdmin):
    list_display = ("tg_id", "username", "first_name", "last_name", "real_balance", "virtual_balance", "source",)
