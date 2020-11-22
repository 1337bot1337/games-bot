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
