import typing

from . import models as account_models
from decimal import Decimal


def register_user_source(*, tg_id: int, source: str) -> typing.Optional["account_models.TelegramAccount"]:
    if not account_models.TelegramAccount.objects.filter(tg_id=tg_id).exists():
        new_user = account_models.TelegramAccount.objects.create(tg_id=tg_id, source=source, virtual_balance=Decimal(100))
        account_models.TelegramAccountStatistic.objects.create(account=new_user)
        return new_user
