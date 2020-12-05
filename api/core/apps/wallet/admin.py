from django.contrib import admin

from core.apps.wallet import models as wallet_models


@admin.register(wallet_models.WithdrawRequest)
class WithdrawRequestAdmin(admin.ModelAdmin):
    list_display = ("account", "amount", "card_number", "status", "is_active", )
    list_filter = ("status", "is_active",)

    def save_model(self, request, obj, form, change):
        update_fields = []

        # True if something changed in model
        # Note that change is False at the very first time
        if change:
            if form.initial["status"] != form.cleaned_data["status"]:
                update_fields.append("status")

                if obj.is_active and update_fields[0] == "status":
                    obj.save(update_fields=update_fields)
        #obj.save()

# @admin.register(wallet_models.Refill)
# class RefillAdmin(admin.ModelAdmin):
#     list_display = ("account", "amount", "multiplier", "status", "created", )
#     list_filter = ("status",)
