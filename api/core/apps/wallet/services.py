from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from core.apps.account import models as account_models
from core.apps.common import selectors as common_selectors
from core.apps.wallet import models as wallet_models


def apply_multiplier(*, amount: Decimal) -> int:
    multiplier = common_selectors.get_suitable_multiplier(amount=amount)
    return int(amount * multiplier - amount)


def withdraw_wallet(*, tg_account: "account_models.TelegramAccount", amount: Decimal, card_number: str) -> None:
    if amount > tg_account.real_balance:
        raise ValidationError(_("Desire withdraw amount is greater than available"))

    with transaction.atomic():
        wallet_models.WithdrawRequest.objects.create(account=tg_account, amount=amount, card_number=card_number)
        tg_account.real_balance = F("real_balance") - amount
        tg_account.save(update_fields=("real_balance", "updated",))


# # TODO: create refill object; create refill after status
# def refill_wallet(*, tg_account: "account_models.TelegramAccount", amount: Decimal, is_testing: bool = True) -> str:
#     if is_testing:
#         with transaction.atomic():
#             tg_account.real_balance = F("real_balance") + amount
#             tg_account.virtual_balance = F("virtual_balance") + apply_multiplier(amount=amount)
#             tg_account.save(update_fields=("real_balance", "virtual_balance", "updated",))
#
#         url = "https://piastrix.docs.apiary.io/#introduction/pay"
#     else:
#         url = "https://piastrix.docs.apiary.io/#introduction/pay"
#
#     return url


def refill_wallet(tg_id, amount):
    account = account_models.TelegramAccount.objects.get(tg_id)

    account.real_balance += Decimal(amount)
    bonus = apply_multiplier(amount=amount)
    account.virtual_balance += Decimal(bonus)
    account.save()

    return bonus
