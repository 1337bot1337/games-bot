from django.contrib import admin

from core.apps.wallet import models as wallet_models


@admin.register(wallet_models.WithdrawRequest)
class WithdrawRequestAdmin(admin.ModelAdmin):
    list_display = ("account", "amount", "card_number", "status", "is_active", )
    list_filter = ("status", "is_active",)
