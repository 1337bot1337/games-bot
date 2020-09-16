from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from core.apps.account import models as account_models
from core.apps.wallet import models as wallet_models


def withdraw_wallet(*, tg_account: "account_models.TelegramAccount", amount: Decimal, card_number: str) -> None:
    if amount > tg_account.real_balance:
        raise ValidationError(_("Desire withdraw amount is greater than available"))

    with transaction.atomic():
        wallet_models.WithdrawRequest.objects.create(account=tg_account, amount=amount, card_number=card_number)
        tg_account.real_balance = F("real_balance") - amount
        tg_account.save(update_fields=("real_balance", "updated",))


def refill_wallet(*, tg_account: "account_models.TelegramAccount", amount: Decimal, is_testing: bool = True) -> str:
    if is_testing:
        with transaction.atomic():
            tg_account.real_balance = F("real_balance") + amount
            tg_account.save(update_fields=("real_balance", "updated",))

        url = "https://piastrix.docs.apiary.io/#introduction/pay"
    else:
        url = "https://piastrix.docs.apiary.io/#introduction/pay"

    return url
