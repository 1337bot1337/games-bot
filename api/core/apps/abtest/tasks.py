from django.utils import timezone
from django.core.cache import cache
from core.config.celery import app as celery_app
from core.apps.abtest import models as abtest_models
from core.apps.account import models as account_models
from core.apps.affiliate import models as affiliate_models
from core.apps.common import models as common_models


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

    affiliate_cache = affiliate_models.AffiliateSetup.objects.filter(name="default")
    if affiliate_cache.exists():
        affiliate_cache = affiliate_cache.values()[0]
    else:
        affiliate_cache = {}

    settings_cache = common_models.Settings.objects.filter()
    if settings_cache.exists():
        settings_cache = settings_cache.values()[0]
    else:
        settings_cache = {}

    cache.set("settings", settings_cache, timeout=None)
    cache.set("affiliate", affiliate_cache, timeout=None)
    cache.set("users", user_cache, timeout=None)
    cache.set("botprofiles", botprofile_cache, timeout=None)
    cache.set("sources", source_cache, timeout=None)
    cache.set("texts", text_cache, timeout=None)




