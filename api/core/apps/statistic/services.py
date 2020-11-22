from .models import TelegramAccountStatistic
from core.apps.account.models import TelegramAccount


def register_statistic(tg_id: int,
                       username: str,
                       first_name: str,
                       last_name: str,
                       type_action: str,
                       data: dict
                       ):
    source = TelegramAccount.objects.get(tg_id=tg_id).source
    return TelegramAccountStatistic.objects.create(
        tg_id=tg_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        type_action=type_action,
        source=source, data=data)
