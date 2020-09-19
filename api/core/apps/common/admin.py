from django.contrib import admin

from core.apps.common import models as common_models


@admin.register(common_models.BalanceMultiplierConfig)
class BalanceMultiplierConfigAdmin(admin.ModelAdmin):
    list_display = ("amount_from", "amount_to", "multiplier", "is_active",)
