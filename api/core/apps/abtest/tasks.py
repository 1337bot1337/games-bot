from django.utils import timezone
from django.core.cache import cache
from core.config.celery import app as celery_app
from core.apps.abtest import models as abtest_models
from core.apps.account import models as account_models


@celery_app.task
def update_cache():
    user_cache = {}
    for i in account_models.TelegramAccount.objects.all().values():
        user_cache[i["tg_id"]] = i

    text_cache = {}
    for i in abtest_models.BotText.objects.all():
        text_cache[(i.name, i.version)] = {
            "version": i.version,
            "name": i.name,
            "text": i.text,
            "text_ru": i.text_ru,
            "text_en": i.text_en
        }

    botprofile_cache = {}
    for i in abtest_models.BotProfile.objects.all().values():
        botprofile_cache[i["name"]] = i

    source_cache = {}
    for i in abtest_models.SourceSetup.objects.all().values():
        source_cache[i["name"]] = i

    cache.set("users", user_cache, timeout=None)
    cache.set("botprofiles", botprofile_cache, timeout=None)
    cache.set("sources", source_cache, timeout=None)
    cache.set("texts", text_cache, timeout=None)




