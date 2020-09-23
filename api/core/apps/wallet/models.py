from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from core.apps.account import models as account_models
from core.apps.common import choices
from core.apps.common import models as common_models


class WithdrawRequest(common_models.BaseModel):
    account = models.ForeignKey(account_models.TelegramAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(
        _("Desire withdraw amount"),
        decimal_places=2,
        max_digits=9,
        validators=[MinValueValidator(0), MaxValueValidator(settings.MAX_WITHDRAW_AMOUNT_PER_REQUEST)]
    )
    card_number = models.CharField(_("Card number"), max_length=20)
    status = models.CharField(
        _("Withdraw request status"),
        max_length=50,
        choices=choices.WITHDRAW_REQUEST_STATUS_CHOICES,
        default=choices.WithdrawRequestStatus.IN_PROGRESS
    )
    is_active = models.BooleanField(_("Active"), default=True)


class Refill(common_models.BaseModel):
    account = models.ForeignKey(account_models.TelegramAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(
        _("Refill amount"),
        decimal_places=2,
        max_digits=9,
        validators=[MinValueValidator(0), MaxValueValidator(settings.MAX_REFILL_AMOUNT_PER_REQUEST)]
    )
    multiplier = models.DecimalField(
        _("Multiplier snapshot"),
        decimal_places=2,
        max_digits=5,
        default=Decimal(1.0)
    )
    status = models.CharField(
        _("Status"),
        choices=choices.REFILL_STATUS_CHOICES,
        default=choices.RefillStatus.IN_PROGRESS,
        max_length=50,
    )
