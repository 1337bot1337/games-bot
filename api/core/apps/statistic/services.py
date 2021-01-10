from core.apps.statistic import models as statistic_models
from core.apps.account import models as account_models
from core.apps.game import models as game_models
from core.apps.game.utils import GAME_LIST
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
            created__range=(obj.date_1, obj.date_2))
    else:
        invoice_data = game_models.InvoiceData.objects.filter(account__in=accounts)
    return invoice_data


def create_values_for_pygsheet(obj, accounts):
    invoice_data = game_models.InvoiceData.objects.filter(account__in=accounts)
    if obj.type_setup == "default":
        statistic = _get_statistic(obj, accounts)
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


def update_gsheet(obj: "statistic_models.StatisticRequest"):
    accounts = get_accounts_from_request(obj)
    gs = pygsheets.authorize("/src/gsheets/client_secret.json", credentials_directory="/src/gsheets/")
    default_stat_list = gs.open("test").sheet1
    default_stat_list.clear(start="B3", end=f"L100000")
    if accounts:
        statistic = _get_statistic(obj, accounts)
        if statistic.count() == 0:
            return

        if obj.type_setup == "default":
            len_queryset = accounts.count()
            first_cord = "B3"
            last_cord = f"L{3+len_queryset}"
            values = create_values_for_pygsheet(obj, accounts)

            default_stat_list.update_values(values=values, crange=f"{first_cord}:{last_cord}")
            return True

        if obj.type_setup == "top_games":
            first_cord = "B3"


# def _get_game_stat_dict(statistic: DjangoQuerySet, invoice_data):
#     game_dict = defaultdict(str)
#     for stat in statistic:
#         if stat.type_action == "start_game":
#             game_name = stat.data["name"]
#             d = defaultdict(str)
#             game_dict[game_name] += defaultdict(str)
