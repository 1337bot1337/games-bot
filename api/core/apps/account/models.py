from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from core.apps.common import models as common_models


class TelegramAccount(common_models.BaseModel):
    tg_id = models.PositiveIntegerField(_("Telegram user ID"), unique=True)
    real_balance = models.DecimalField(_("Real balance amount"), decimal_places=2, max_digits=10, default=0)
    virtual_balance = models.DecimalField(_("Virtual balance amount"), decimal_places=2, max_digits=10, default=0)
    source = models.CharField(_("Source of user"), max_length=50, default=settings.DEFAULT_USER_SOURCE)

    def __str__(self):
        return f"{self.tg_id} (registration date: {self.created})"

