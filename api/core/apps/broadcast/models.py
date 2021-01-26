from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from core.apps.common import models as common_models
from django.utils import timezone


class BroadcastQuery(common_models.BaseModel):
    text = models.TextField(_("Текст рассылки"))
    bot_profile = models.ForeignKey("abtest.BotProfile",
                                    verbose_name=_("Выбрать A\B профиль кому рассылать"),
                                    blank=True,
                                    null=True,
                                    default=None,
                                    on_delete=models.CASCADE)

    broadcast_to_all = models.BooleanField(_("Отправить всем"), default=False)
    action = models.CharField(
        _("Применить действие"),
        max_length=55,
        choices=(
            ("queue_for_sending", _("Поставить в очередь на рассылку")),
            ("await", _("Перевести в ожидание"))))

    keyboard = models.CharField(
        _("Обновить клавиатуру"),
        max_length=50,
        choices=(
            ("none", _("Не обновлять клавиатуру")),
            ("start", _("Основная клавиатура")),
            ("invite", _("Пригласить друга")),
            ("games", _("Игры")),
            ("deposit", _("Пополнить баланс"))
        ),
        default="none")
    timedelta_inactive = models.DurationField(_("Неактивность больше чем"), choices=(
        (timezone.timedelta(seconds=0), _("Не использовать параметр")),
        (timezone.timedelta(days=1), _("Один день")),
        (timezone.timedelta(days=3), _("Три дня")),
        (timezone.timedelta(days=7), _("7 дней")),
        (timezone.timedelta(days=30), _("Тридцать дней"))
    ), default=0)

    status = models.BooleanField(_("Выполно/Не выполнено"), default=False)

    class Meta:
        verbose_name = "Сообщение на рассылку"
        verbose_name_plural = "Рассылка сообщений"
