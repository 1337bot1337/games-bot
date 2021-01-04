from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from core.apps.common import selectors as common_selectors
from core.apps.account import models as account_models
from core.apps.wallet import models as wallet_models
from core.apps.affiliate import models as affiliate_models
from core.apps.statistic import models as statistic_models
from core.apps.statistic import services as statistic_services
from core.apps.helpbot import services as helpbot_services
from core.apps.affiliate import services as affiliate_services
from core.apps.account import services as account_services


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
        tg_user = helpbot_services.get_tg_user(tg_account.tg_id)
        statistic_services.register_statistic(tg_id=tg_account.tg_id,
                                              username=tg_user["username"],
                                              first_name=tg_user["first_name"],
                                              last_name=tg_user["last_name"],
                                              type_action='withdrawal_request', data={"amount": int(amount), "card": card_number})


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


def refill_wallet(tg_id, amount: Decimal):
    account = account_models.TelegramAccount.objects.get(tg_id=tg_id)
    account.real_balance += Decimal(amount)
    bonus = 0
    if affiliate_models.UserAffiliate.objects.filter(referral=account).exists():
        user_ref = affiliate_models.UserAffiliate.objects.get(referral=account)
        affiliate_setup = affiliate_models.AffiliateSetup.objects.get(name="default")
        if not statistic_models.TelegramAccountStatistic.objects.filter(tg_id=account.tg_id, type_action="deposit").exists():
            bonus = affiliate_setup.referral_deposit_bonus
            if affiliate_setup.referral_type_deposit_bonus == "factor":
                bonus = amount * affiliate_setup.referral_deposit_bonus - amount

            account.virtual_balance += bonus
        referrer_bonus = affiliate_setup.referrer_deposit_bonus
        referrer = user_ref.referrer
        affiliate_services.pay_referrer_bonus(referrer, referrer_bonus, amount)
    elif account.source != "none":
        bonus, type_bonus = account_services.get_deposit_bonus(account.source)
        if type_bonus == "factor":
            bonus = bonus * amount - amount
            account.virtual_balance += bonus
        else:
            account.virtual_balance += bonus
        account.virtual_balance += bonus
    account.save()

    return bonus
