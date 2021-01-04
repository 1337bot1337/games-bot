from django.contrib import admin
from django.contrib import messages
from core.apps.affiliate import models as affiliate_models


@admin.register(affiliate_models.UserAffiliate)
class UserAffiliateAdmin(admin.ModelAdmin):
    list_display = ("referral", "referrer", )


@admin.register(affiliate_models.AffiliateSetup)
class AffiliateSetupAdmin(admin.ModelAdmin):
    list_display = ("name", "referrer_deposit_bonus", "referral_deposit_bonus", "type_referral_deposit_bonus", "min_referral_deposit")

    def save_model(self, request, obj, form, change):
        if change:
            if form.initial["name"] == "default" and form.initial["name"] != form.cleaned_data["name"]:
                return

        obj.save()

    def delete_model(self, request, obj):
        if obj.name != "default":
            obj.delete()
