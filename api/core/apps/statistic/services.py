from core.apps.statistic import models as statistic_models
from core.apps.account import models as account_models
from core.apps.game import models as game_models
from core.apps.game.utils import GAME_LIST, game_dict
from django.utils import timezone
from django.db.models import QuerySet as DjangoQuerySet
import pygsheets
from collections import defaultdict


def register_statistic(tg_id: int or str,
                       username: str,
                       first_name: str,
                       last_name: str,
                       type_action: str,
                       data: dict
                       ):
    source = account_models.TelegramAccount.objects.get(tg_id=tg_id).source
    return statistic_models.TelegramAccountStatistic.objects.create(
        tg_id=tg_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        type_action=type_action,
        source=source, data=data)


def get_accounts_from_request(obj: "statistic_models.StatisticRequest"):
    accounts = None
    if obj.source:
        accounts = account_models.TelegramAccount.objects.filter(source=obj.source.name)

    elif obj.source_list and len(obj.source_list) > 3:
        source_list = obj.source_list.replace(" ", "").split(",")
        accounts = account_models.TelegramAccount.objects.filter(source__in=source_list)

    elif obj.all_user:
        accounts = account_models.TelegramAccount.objects.all()

    return accounts


# Для одного юзера
def _get_game_statistic(account: "account_models.TelegramAccount",
                        statistic: DjangoQuerySet,
                        invoice_data: DjangoQuerySet):

    user_stats = statistic.filter(tg_id=account.tg_id)
    sum_start_game = user_stats.filter(type_action="start_game").count()

    bet_count = 0
    sumbet = 0
    for game in invoice_data.filter(account=account):
        for event in game.game_history:
            if "bet" in event["event"]:
                bet_count += 1
                sumbet += event["value"]

    return sum_start_game, bet_count, sumbet * 10


# Общая
def _get_common_game_statistic(statistic: DjangoQuerySet, invoice_data: DjangoQuerySet):
    stat_dict = defaultdict(dict)
    for game in GAME_LIST:
        start_count = 0
        max_sum_win = 0
        max_sum_loss = 0
        bonus_loss = 0
        rub_loss = 0
        spin_count = 0
        sum_spin = 0

        for i in statistic.filter(type_action__in=["start_game", "end_game"]):
            if int(i.data["game_id"]) == game:
                if i.type_action == "start_game":
                    start_count += 1

                if i.type_action == "end_game":
                    if i.data["result"] == "win":
                        max_sum_win += i.data["amount"]

                    if i.data["result"] == "lose":
                        max_sum_loss += i.data["amount"]
                        if float(i.data["start_bonus_balance"]) > 0:
                            if i.data["amount"] <= float(i.data["start_bonus_balance"]):
                                bonus_loss += i.data["amount"]

                            else:
                                remainder_of_loss = i.data["amount"] - float(i.data["start_bonus_balance"])
                                bonus_loss += float(i.data["start_bonus_balance"])
                                rub_loss += remainder_of_loss
                        else:
                            rub_loss += i.data["amount"]

        for i in invoice_data.filter(game_id=game):
            for event in i.game_history:
                if "bet" in event["event"]:
                    spin_count += 1
                    sum_spin += event["value"]

        stat_dict[GAME_LIST[game]] = {
            "start_count": start_count,
            "max_sum_win": max_sum_win*10,
            "max_sum_loss": max_sum_loss*10,
            "bonus_loss": bonus_loss*10,
            "rub_loss": rub_loss*10,
            "spin_count": spin_count,
            "sum_spin": sum_spin*10
        }
    return stat_dict


def _get_deposit_statistic(tg_id: int, statistic: DjangoQuerySet):
    deposit_count = statistic.filter(tg_id=tg_id, type_action="deposit").count()
    sum_deposit = 0
    for i in statistic.filter(tg_id=tg_id, type_action="deposit"):
        sum_deposit += i.data["amount"]
    return deposit_count, sum_deposit


def _get_withdrawal_statistic(tg_id: int, statistic: DjangoQuerySet):
    withdrawal_request_count = statistic.filter(tg_id=tg_id, type_action="withdrawal_request").count()
    successful_withdrawal_sum = 0
    for i in statistic.filter(tg_id=tg_id, type_action="withdrawal_accepted"):
        successful_withdrawal_sum += i.data["amount"]

    return withdrawal_request_count, successful_withdrawal_sum


def _get_affiliate_statistic(tg_id: int, statistic: DjangoQuerySet):
    referral_count = statistic.filter(tg_id=tg_id, type_action="new_ref").count()
    ref_bonus = 0
    for i in statistic.filter(tg_id=tg_id, type_action="referrer_bonus"):
        ref_bonus += i.data["amount"]

    return referral_count, ref_bonus


def _get_bot_stat(statistic: DjangoQuerySet, invoice_data: DjangoQuerySet, accounts: DjangoQuerySet):
    game_statistic = _get_common_game_statistic(statistic, invoice_data)
    user_count = accounts.count()
    deposit_count = statistic.filter(type_action="deposit").count()
    sum_deposit = 0
    withdrawal_request_count = statistic.filter(type_action="withdrawal_request").count()
    withdrawal_request_ok = statistic.filter(type_action="withdrawal_accepted").count()
    sum_withdrawal = 0
    start_game_count = statistic.filter(type_action="start_game").count()
    spin_count = 0
    sum_win = 0
    sum_loss = 0
    rub_loss = 0
    bonus_loss = 0
    press_game = 0
    press_balance = 0
    press_deposit = 0
    press_withdrawal = 0
    press_deposit_cancel = 0
    press_withdrawal_cancel = 0
    press_withdrawal_conditions = 0
    press_help = 0
    press_affiliate = 0

    for i in statistic:
        if i.type_action == "press_button":
            data = i.data
            bt_name = data["button_name"]
            if bt_name == "games":
                press_game += 1

            if bt_name == "balance":
                press_balance += 1
            if bt_name == "deposit":
                press_deposit += 1
            if bt_name == "withdrawal":
                press_withdrawal += 1
            if bt_name == "conditions":
                press_withdrawal_conditions += 1
            if bt_name == "cancel_deposit":
                press_deposit_cancel += 1
            if bt_name == "cancel_withdraw":
                press_withdrawal_cancel += 1
            if bt_name == "help":
                press_help += 1
            if bt_name == "affiliate":
                press_affiliate += 1

        if i.type_action == "deposit":
            sum_deposit += i.data["amount"]
        if i.type_action == "withdrawal_accepted":
            sum_withdrawal += i.data["amount"]

    for game in game_statistic:
        info = game_statistic[game]
        sum_win += info["max_sum_win"]
        sum_loss += info["max_sum_loss"]
        rub_loss += info["rub_loss"]
        bonus_loss += info["bonus_loss"]
        spin_count += info["spin_count"]

    return [user_count, deposit_count, sum_deposit,  withdrawal_request_count, withdrawal_request_ok, sum_withdrawal,
            start_game_count, sum_win, sum_loss, spin_count, rub_loss, bonus_loss, press_game, press_balance,
            press_deposit, press_deposit_cancel, press_withdrawal, press_withdrawal_cancel, press_withdrawal_conditions,
            press_affiliate, press_help]


def _get_statistic(obj, accounts: DjangoQuerySet):
    users_ids = [account.tg_id for account in accounts]
    if obj.date_1 and obj.date_2:

        statistic = statistic_models.TelegramAccountStatistic.objects.filter(
            tg_id__in=users_ids,
            created__range=(obj.date_1, obj.date_2))
    else:
        statistic = statistic_models.TelegramAccountStatistic.objects.filter(tg_id__in=users_ids)

    return statistic


def _get_invoice_data(obj, accounts: DjangoQuerySet):
    if obj.date_1 and obj.date_2:

        invoice_data = game_models.InvoiceData.objects.filter(
            account__in=accounts,
            created__range=(obj.date_1, obj.date_2),
            status="closed")
    else:
        invoice_data = game_models.InvoiceData.objects.filter(account__in=accounts)
    return invoice_data


def create_values_for_pygsheet(obj, accounts):
    invoice_data = game_models.InvoiceData.objects.filter(account__in=accounts)
    statistic = _get_statistic(obj, accounts)
    if obj.type_setup == "default":

        matrix = []
        for account in accounts:
            tg_id = account.tg_id
            source = account.source
            sum_start_game, bet_count, sumbet = _get_game_statistic(account, statistic, invoice_data)
            deposit_count, sum_deposit = _get_deposit_statistic(tg_id, statistic)
            withdrawal_request_count, withdrawal_accepted_sum = _get_withdrawal_statistic(tg_id, statistic)
            referral_count, ref_bonus = _get_affiliate_statistic(tg_id, statistic)

            data_list = [tg_id,
                         source,
                         sum_start_game,
                         bet_count,
                         sumbet,
                         deposit_count,
                         sum_deposit,
                         withdrawal_request_count,
                         withdrawal_accepted_sum,
                         referral_count,
                         ref_bonus]

            matrix.append(data_list)
        return matrix

    if obj.type_setup == "top_games":
        stat_dict = _get_common_game_statistic(statistic, invoice_data)
        sorded_stat = sorted(stat_dict.items(), key=lambda kv: kv[1]["start_count"], reverse=True)
        maxtrix = []

        for game in sorded_stat:
            game_name = game[0]

            maxtrix.append([
                game_name,
                game[1]["start_count"],
                game[1]["spin_count"],
                game[1]["sum_spin"],
                game[1]["max_sum_win"],
                game[1]["max_sum_loss"],
                game[1]["bonus_loss"],
                game[1]["rub_loss"]
            ])
        return maxtrix

    if obj.type_setup == "common":
        return [_get_bot_stat(statistic, invoice_data, accounts)]


def update_gsheet(obj: "statistic_models.StatisticRequest"):
    accounts = get_accounts_from_request(obj)
    gs = pygsheets.authorize("/src/gsheets/client_secret.json", credentials_directory="/src/gsheets/")

    if accounts:
        statistic = _get_statistic(obj, accounts)
        if statistic.count() == 0:
            return

        if obj.type_setup == "default":
            default_stat_list = gs.open("test").sheet1
            default_stat_list.clear(start="B3", end=f"L100000")
            len_queryset = accounts.count()
            first_cord = "B3"
            last_cord = f"L{3+len_queryset}"
            values = create_values_for_pygsheet(obj, accounts)

            default_stat_list.update_values(values=values, crange=f"{first_cord}:{last_cord}")
            return True

        if obj.type_setup == "top_games":
            game_stat_list = gs.open("test").worksheet(property="index", value=2)
            game_stat_list.clear(start="B3", end=f"I100")
            first_cord = "B3"
            last_cord = f"I{3+len(GAME_LIST)}"
            values = create_values_for_pygsheet(obj, accounts)

            game_stat_list.update_values(values=values, crange=f"{first_cord}:{last_cord}")
            return True

        if obj.type_setup == "common":
            game_stat_list = gs.open("test").worksheet(property="index", value=1)
            game_stat_list.clear(start="B3", end=f"V5")
            first_cord = "B3"
            last_cord = f"V5"
            values = create_values_for_pygsheet(obj, accounts)

            game_stat_list.update_values(values=values, crange=f"{first_cord}:{last_cord}")
            return True

# def _get_game_stat_dict(statistic: DjangoQuerySet, invoice_data):
#     game_dict = defaultdict(str)
#     for stat in statistic:
#         if stat.type_action == "start_game":
#             game_name = stat.data["name"]
#             d = defaultdict(str)
#             game_dict[game_name] += defaultdict(str)
