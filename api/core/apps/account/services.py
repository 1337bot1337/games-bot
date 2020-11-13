import typing

from . import models as account_models
from core.apps.statistic import services as statistic_services
from decimal import Decimal
from django.core.cache import cache


def register_user_source(*, tg_id: int, source: str) -> typing.Optional["account_models.TelegramAccount"]:
    if not account_models.TelegramAccount.objects.filter(tg_id=tg_id).exists():
        new_user = account_models.TelegramAccount.objects.create(tg_id=tg_id, source=source, virtual_balance=Decimal(100))
        statistic_services.register_statistic(tg_id=tg_id, type_action='new_user', data={})

        return new_user
