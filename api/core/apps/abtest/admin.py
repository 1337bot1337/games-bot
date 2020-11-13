from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from core.apps.abtest import models as abtest_models


@admin.register(abtest_models.BotText)
class BotTextAdmin(TranslationAdmin):
    list_display = ("name", "version",)


