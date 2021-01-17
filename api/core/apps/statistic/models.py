from django.db import models
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import JSONField
from core.apps.common import models as common_models


class TelegramAccountStatistic(common_models.BaseModel):

    tg_id = models.PositiveIntegerField(_("Телеграм Юзер ID"))
    username = models.CharField(_('Юзернейм'), max_length=255, default='[отсутствует]')
    first_name = models.CharField(_('Имя'), max_length=255, default='[отсутствует]')
    last_name = models.CharField(_('Фамилия'), max_length=255, default='[отсутствует]')
    source = models.CharField(_("Кто привел пользователя"), max_length=255, default='none')
    type_action = models.CharField(_("Тип события"), max_length=255)
    data = JSONField(_("Информация о событии"))

    class Meta:
        verbose_name = "запись в статистике телеграм аккаунтов"
        verbose_name_plural = "Статистика Телеграм Аккаунтов"


class StatisticRequest(common_models.BaseModel):
    source = models.ForeignKey("abtest.SourceSetup", verbose_name=_("Выбрать канал"), blank=True, null=True, on_delete=models.CASCADE)
    source_list = models.CharField(_("Указать название каналов через запятую"), max_length=250, blank=True, null=True)
    all_user = models.BooleanField(_("Статистика по всем пользователям"), default=False)
    type_setup = models.CharField(_("Тип выгружаемой статистики"), max_length=50, choices=(
        ("default", _("Общая статистика пользователей")),
        ("common", _("Общая статистика бота")),
        ("top_games", _("Топ игр"))
       ), default="default")

    date_1 = models.DateTimeField(_("Дата 1"), blank=True, null=True)
    date_2 = models.DateTimeField(_("Дата 2"), blank=True, null=True)

    class Meta:
        verbose_name = "Выгрузка статистики"
        verbose_name_plural = "Выгрузка статистики"

