import typing

from . import models as account_models


def register_user_source(*, tg_id: int, source: str) -> typing.Optional["account_models.TelegramAccount"]:
    if not account_models.TelegramAccount.objects.filter(tg_id=tg_id).exists():
        return account_models.TelegramAccount.objects.create(tg_id=tg_id, source=source)
