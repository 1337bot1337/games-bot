import typing

from . import models as account_models
from core.apps.statistic import services as statistic_services
from decimal import Decimal
from django.core.cache import cache
from core.apps.abtest import services as abtest_services


def register_user_source(*, tg_id: int,
                         username: str,
                         first_name: str,
                         last_name: str,
                         source: str,
                         type_bonus: str) -> typing.Optional["account_models.TelegramAccount"]:
    if not account_models.TelegramAccount.objects.filter(tg_id=tg_id).exists():
        if type_bonus == "source":
            bonus = get_welcome_bonus(source)
        else:
            bonus = 0

        new_user = account_models.TelegramAccount.objects.create(
            tg_id=tg_id,
            username=username,
            last_name=last_name,
            first_name=first_name,
            source=source,
            virtual_balance=Decimal(bonus))
        add_user_in_cache(new_user)
        statistic_services.register_statistic(
            tg_id=tg_id,
            username=username,
            last_name=last_name,
            first_name=first_name,
            type_action='new_user', data=dict(
                username=username,
                last_name=last_name,
                first_name=first_name,
                source=source,
                bonus=bonus
            ))

        return new_user


def add_user_in_cache(account: "account_models.TelegramAccount"):
    # TODO Не плохо бы поменять ключи
    users = cache.get("users")

    users[account.tg_id] = dict(
        id=account.id,
        tg_id=account.tg_id,
        username=account.username,
        first_name=account.first_name,
        last_name=account.last_name,
        real_balance=account.real_balance,
        virtual_balance=account.virtual_balance,
        source=account.source

    )

    cache.set("users", users, timeout=None)
    cache.set(f"{account.tg_id}", {"await_deposit_amount": False,
                                   "await_withdraw_amount": False,
                                   "await_withdraw_card": False,
                                   "await_game_search": False,
                                   "withdraw_amount": 0}, timeout=None)


def get_welcome_bonus(source):
    abprofile = abtest_services.get_bot_profile(source)
    return abprofile["welcome_bonus"]


def get_deposit_bonus(source):
    abprofile = abtest_services.get_bot_profile(source)
    return Decimal(abprofile["deposit_bonus"]), abprofile["type_deposit_bonus"]
