from django.contrib import admin
from django.contrib import messages
from modeltranslation.admin import TranslationAdmin

from core.apps.abtest import models as abtest_models


@admin.register(abtest_models.BotText)
class BotTextAdmin(TranslationAdmin):
    list_display = ("name", "text", "version",)

    def save_model(self, request, obj, form, change):
        if change:
            if form.initial["name"] != form.cleaned_data["name"]:
                return

            if form.initial["version"] == "a" and form.initial["version"] != form.cleaned_data["version"]:
                return

            if form.initial["version"] != "a" and form.cleaned_data["version"] == "a":
                return

        obj.save()

    def delete_model(self, request, obj):
        if obj.version != "a":
            obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.version != "a":
                obj.delete()


@admin.register(abtest_models.BotProfile)
class BotProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "version_text", "welcome_bonus", "deposit_bonus", )

    def save_model(self, request, obj, form, change):
        if change:
            if form.initial["name"] == "default" and form.initial["name"] != form.cleaned_data["name"]:
                return

            old_version = form.initial["version_text"]
            new_version = form.cleaned_data["version_text"]
            if form.initial["name"] == "default" and old_version != new_version:
                return

            if old_version != new_version:

                texts = abtest_models.BotText.objects.filter(version=new_version)
                if texts.exists():
                    a_texts = abtest_models.BotText.objects.filter(version="a")
                    if texts.count() != a_texts.count():
                        x = a_texts.count() - texts.count()
                        prf = "текст" if x == 1 else "текста"
                        return self.message_user(request, f"Вы не можете использовать эту версию, т.к в модели BotText отсутствует {x} {prf}",
                                            level=messages.ERROR)
                else:
                    return self.message_user(request, "Такой версии текстов не существует в BotText", level=messages.ERROR)
            return obj.save()

        texts = abtest_models.BotText.objects.filter(version=form.initial)
        if texts.exists():
            a_texts = abtest_models.BotText.objects.filter(version="a")
            if texts.count() != a_texts.count():
                x = a_texts.count() - texts.count()
                prf = "текст" if x == 1 else "текста"
                return self.message_user(request,
                                         f"Вы не можете использовать эту версию, т.к в модели BotText отсутствует {x} {prf}",
                                         level=messages.ERROR)
        else:
            return self.message_user(request, "Такой версии текстов не существует в BotText", level=messages.ERROR)
        obj.save()

    def delete_model(self, request, obj):
        if obj.name != "default":
            obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.name != "default":
                obj.delete()


@admin.register(abtest_models.SourceSetup)
class SourceSetupAdmin(admin.ModelAdmin):
    list_display = ("name", "profile", )

    def save_model(self, request, obj, form, change):
        if change:
            if form.initial["name"] == "none":
                return

        obj.save()

    def delete_model(self, request, obj):
        if obj.name != "none":
            obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.name != "none":
                obj.delete()
