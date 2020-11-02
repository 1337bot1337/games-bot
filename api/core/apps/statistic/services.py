from .models import TelegramAccountStatistic


def create_record(tg_id: int, type_action: str, data: dict):

    TelegramAccountStatistic.objects.create(tg_id=tg_id, type_action=type_action, data=data)
