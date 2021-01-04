from core.apps.affiliate import models as affiliate_models
from core.apps.account import models as account_models
from core.apps.helpbot import services as helpbot_services
from core.apps.abtest import services as abtest_services
from core.apps.statistic import services as statistic_services
from decimal import Decimal


def get_user_name(user: "account_models.TelegramAccount"):
    name = None
    # if user.user_name:
    #     return f'@{user.user_name}'

    if user.first_name != "[отсутствует]" and user.last_name == "[отсутствует]":

        name = f'[{user.first_name}](tg://user?id={user.tg_id})'

    elif user.first_name != "[отсутствует]" and user.last_name != "[отсутствует]":
        name = f'[{user.first_name} {user.last_name}](tg://user?id={user.tg_id})'

    return name


def create_new_ref(referral_id: int, referrer_id: int):
    referral = account_models.TelegramAccount.objects.get(tg_id=referral_id)

    if not affiliate_models.UserAffiliate.objects.filter(referral=referral).exists():
        referrer = account_models.TelegramAccount.objects.get(tg_id=referrer_id)
        affiliate_models.UserAffiliate.objects.create(referral=referral, referrer=referrer)

        statistic_services.register_statistic(tg_id=referrer.tg_id,
                                              username=referrer.username,
                                              first_name=referrer.first_name,
                                              last_name=referrer.last_name,
                                              type_action='new_ref',
                                              data={"referral_id": referral_id,
                                                    "username": referral.username,
                                                    "first_name": referral.first_name,
                                                    "last_name": referral.last_name})
        set = account_models.AffiliateSetup.objects.filter()[0]

        helpbot_services.send_msg(referrer_id, abtest_services.get_text(referrer_id, "affiliate-new_referral").format(
            friend_name=get_user_name(referral),
            min_referral_deposit=set.min_referral_deposit),
                                  session_name="new_ref")


def pay_referrer_bonus(referrer: "account_models.TelegramAccount",
                       bonus: Decimal,
                       referral_deposit: Decimal):
    min_deposit = affiliate_models.AffiliateSetup.objects.filter()[0].min_referral_deposit

    if referral_deposit < min_deposit:
        return

    referrer.virtual_balance += bonus
    referrer.save()
    text = abtest_services.get_text(referrer.tg_id, "affiliate-bonus_for_referrer_from_deposit_referral").format(
        bonus=round(bonus, 2))
    helpbot_services.send_msg(referrer.tg_id, text, session_name="pay_ref_sess")

    statistic_services.register_statistic(tg_id=referrer.tg_id,
                                          username=referrer.username,
                                          first_name=referrer.first_name,
                                          last_name=referrer.last_name,
                                          type_action='referrer_bonus', data={"amount": round(float(bonus), 2)})
