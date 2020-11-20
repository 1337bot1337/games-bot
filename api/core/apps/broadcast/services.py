from core.apps.statistic import models as statistic_models
from django.utils import timezone


def get_users_from_lastactivity(timedelta, sources=False):
    if sources:
        return statistic_models.TelegramAccountStatistic.objects.filter(
            created__lte=timezone.now() - timedelta, source__in=sources).distinct("tg_id")

    users = statistic_models.TelegramAccountStatistic.objects.filter(created__lte=timezone.now()-timedelta).distinct("tg_id")
    return users
