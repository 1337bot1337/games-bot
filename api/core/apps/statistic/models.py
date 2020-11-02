from django.db import models
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import JSONField
from core.apps.common import models as common_models


class TelegramAccountStatistic(common_models.BaseModel):

    tg_id = models.PositiveIntegerField(_('Telegram user ID'))
    # username = models.CharField(_('Telegram username'), max_length=255, default='none')
    # first_name = models.CharField(_('Telegram first name'), max_length=255, default='none')
    # last_name = models.CharField(_('Telegram last name'), max_length=255, default='none')
    source = models.CharField(_('Source user'), max_length=255, default='none')
    type_action = models.CharField(_('Type action'), max_length=255)
    data = JSONField(_('Data action'))
