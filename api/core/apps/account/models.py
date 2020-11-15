from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from core.apps.common import models as common_models


class TelegramAccount(common_models.BaseModel):
    tg_id = models.PositiveIntegerField(_("Телеграм юзер ID"), unique=True)
    real_balance = models.DecimalField(_("Баланс (рубли)"), decimal_places=2, max_digits=10, default=0)
    virtual_balance = models.DecimalField(_("Баланс (Бонусные жетоны)"), decimal_places=2, max_digits=10, default=0)
    source = models.CharField(_("Кто привел пользователя"), max_length=50, default=settings.DEFAULT_USER_SOURCE)

    class Meta:
        verbose_name = 'Телеграм пользователь'
        verbose_name_plural = 'Телеграм пользователи'

    def __str__(self):
        return f"{self.tg_id} (registration date: {self.created})"


