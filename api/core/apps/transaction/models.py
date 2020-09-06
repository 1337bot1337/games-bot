from django.db import models
from django.utils.translation import gettext as _

from core.apps.common import choices
from core.apps.common import models as common_models


class Transaction(common_models.BaseModel):
    amount = models.PositiveIntegerField(_("Transaction amount"), default=0)
    kind = models.CharField(_("Transaction kind"), choices=choices.TRANSACTION_KIND_CHOICES, max_length=50)
    status = models.CharField(_("Transaction status"), choices=choices.TRANSACTION_STATUS_CHOICES, max_length=50)


class History(common_models.BaseModel):
    action = models.CharField(_("History action"), max_length=50)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    tg_account = models.ForeignKey("account.TelegramAccount", on_delete=models.SET_NULL, related_name="history")
