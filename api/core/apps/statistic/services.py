from .models import TelegramAccountStatistic
from core.apps.account.models import TelegramAccount


def register_statistic(tg_id: int, type_action: str, data: dict):
    source = TelegramAccount.objects.get(tg_id=tg_id).source
    return TelegramAccountStatistic.objects.create(tg_id=tg_id, type_action=type_action, source=source, data=data)
