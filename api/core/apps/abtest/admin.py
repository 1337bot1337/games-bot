from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from core.apps.abtest import models as abtest_models


@admin.register(abtest_models.BotText)
class BotTextAdmin(TranslationAdmin):
    list_display = ("name", "version",)


@admin.register(abtest_models.BotProfile)
class BotProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "version_text", "welcome_bonus", "deposit_bonus", )


@admin.register(abtest_models.SourceSetup)
class BotProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "profile", )
