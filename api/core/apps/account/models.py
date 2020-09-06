from django.db import models
from django.utils.translation import gettext as _

from core.apps.common import models as common_models


class TelegramAccount(common_models.BaseModel):
    tg_id = models.PositiveIntegerField(_("Telegram user ID"))
    real_balance = models.PositiveIntegerField(_("Real balance amount"), default=0)
    virtual_balance = models.PositiveIntegerField(_("Virtual balance amount"), default=0)

    def __str__(self):
        return f"{self.tg_id} (registration date: {self.created})"
