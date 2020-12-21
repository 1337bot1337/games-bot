from decimal import Decimal

from django.conf import settings

from core.apps.vendor.gambling import chc

from core.apps.game import models as game_models
from core.apps.account import models as account_models
from core.apps.vendor.exceptions import ThirdPartyVendorException, FailInvoiceVendorException

from core.apps.statistic import services as statistic_services
from core.apps.helpbot import services as helpbot_services
from core.apps.abtest import services as abtest_services
from core.apps.game.utils import GAME_LIST

AVAILABLE_GAMES = (
    (1003, "Fire Rage +"),
    (1018, "King of Jewels"),
    (1019, "Gates of Avalon"),
    (1024, "Dolphin''s Shell"),
    (1027, "Lady Luck"),
    (1028, "Pirates Fortune"),
    (1031, "Bananas"),
    (1056, "Extra Super 7"),
    (1058, "Box of Ra"),
    (1063, "Rise Of Imperium"),
)


def get_games():

    result = []
    for game_id, game_title in AVAILABLE_GAMES:
        item = {
            "id": game_id,
            "title": game_title,
        }
        result.append(item)

    return result


# def update_balance_after_game(account, game_id, start_real_balance, start_virtual_balance, end_balance):
#     max_start_balance = start_real_balance + start_virtual_balance
#
#     # user in profit
#     if end_balance > max_start_balance:
#         profit = end_balance - max_start_balance
#         account.real_balance += profit
#         account.save()
#
#         statistic_data = {
#             'game_id': str(game_id),
#             'result': 'win',
#             'amount': str(profit),
#             'start_real_balance': str(start_real_balance),
#             'start_bonus_balance': str(start_virtual_balance)}
#
#     elif end_balance < max_start_balance:  # user at a lose
#         loss = max_start_balance - end_balance
#
#         if loss > start_virtual_balance:
#             account.virtual_balance = 0
#             remainder_of_loss = loss - start_virtual_balance
#             account.real_balance -= remainder_of_loss
#         else:
#             account.virtual_balance -= loss
#
#         account.save()
#
#         statistic_data = {
#             'game_id': str(game_id),
#             'result': 'lose',
#             'amount': str(loss),
#             'start_real_balance': str(start_real_balance),
#             'start_bonus_balance': str(start_virtual_balance)        }
#     else:  # draw
#
#         statistic_data = {
#             'game_id': str(game_id),
#             'result': 'draw',
#             'start_real_balance': str(start_real_balance),
#             'start_bonus_balance': str(start_virtual_balance)        }
#
#
#     statistic_services.register_statistic(account.tg_id, type_action='end_game', data=statistic_data)


def update_balance_in_game(account: "account_models.TelegramAccount",
                           last_amount: Decimal,
                           actual_amount: Decimal):
    # user in profit
    if round(actual_amount, 2) > round(last_amount, 2):
        profit = actual_amount - last_amount
        account.real_balance += profit
        account.save()
        helpbot_services.send_msg(account.tg_id, f'🏵 Вы победили!\n'
                                                 f'Ваш выигрыш: **{round(profit/Decimal(10), 2)}** Leo (**{round(profit, 2)}** руб.)')

    # user at a lose
    elif round(actual_amount, 2) < round(last_amount, 2):
        loss = last_amount - actual_amount

        if loss > account.virtual_balance:
            remainder_of_loss = loss - account.virtual_balance
            account.virtual_balance = 0
            account.real_balance -= remainder_of_loss
        else:
            account.virtual_balance -= loss
        account.save()


def update_balance_after_game(account: "account_models.TelegramAccount",
                              invoice: "game_models.InvoiceData",
                              end_amount: Decimal):

    max_start_balance = invoice.start_real_amount + invoice.start_virtual_amount
    last_amount = invoice.last_check_amount
    # user in profit
    if round(end_amount, 2) > round(max_start_balance, 2):
        max_profit = end_amount - max_start_balance
        profit = end_amount - last_amount
        account.real_balance += profit
        account.save()

        statistic_data = {
            'game_id': str(invoice.game_id),
            'name': GAME_LIST[int(invoice.game_id)],
            'result': 'win',
            'amount': round(float(max_profit), 2),
            'start_real_balance': str(invoice.start_real_amount),
            'start_bonus_balance': str(invoice.start_virtual_amount),
            'end_balance': round(float(end_amount), 2)}

    elif round(end_amount, 2) < round(max_start_balance, 2):  # user at a lose
        max_loss = max_start_balance - end_amount
        loss = last_amount - end_amount
        if max_loss > invoice.start_virtual_amount:
            remainder_of_loss = loss - account.virtual_balance
            account.virtual_balance = 0
            account.real_balance -= remainder_of_loss
        else:
            account.virtual_balance -= loss

        account.save()

        statistic_data = {
            'game_id': str(invoice.game_id),
            'name': GAME_LIST[int(invoice.game_id)],
            'result': 'lose',
            'amount': round(float(max_loss), 2),
            'start_real_balance': str(invoice.start_real_amount),
            'start_bonus_balance': str(invoice.start_virtual_amount),
            'end_balance': round(float(end_amount), 2)
        }
    else:  # draw

        statistic_data = {
            'game_id': str(invoice.game_id),
            'name': GAME_LIST[int(invoice.game_id)],
            'result': 'draw',
            'start_real_balance': str(invoice.start_real_amount),
            'start_bonus_balance': str(invoice.start_virtual_amount),
            'end_balance': round(float(end_amount), 2)
        }

    statistic_services.register_statistic(tg_id=account.tg_id,
                                          username=account.username,
                                          first_name=account.first_name,
                                          last_name=account.last_name,
                                          type_action='end_game', data=statistic_data)


# def create_game_session(tg_id, game_id, type_invoice):
#     try:
#         account = TelegramAccount.objects.get(tg_id=tg_id)
#     except:
#         return None, 'Telegram user does not exist'
#
#     client = chc.CHCAPIClient()
#     active_invoice = InvoiceData.objects.get_or_none(account=account, status='open', type_invoice=type_invoice)
#
#     if active_invoice:
#         try:
#             closed_invoice = client.close_invoice(active_invoice.invoice_id)
#             if type_invoice == 'real':
#
#                 update_balance_after_game(account, game_id, active_invoice.start_real_amount, active_invoice.start_virtual_amount, Decimal(closed_invoice[0])*Decimal(10))
#
#             active_invoice.status = 'closed'
#             active_invoice.save()
#         except FailInvoiceVendorException:
#             active_invoice.status = 'closed'
#             active_invoice.save()
#         except ThirdPartyVendorException:
#             helpbot_services.send_msg(tg_id, '❌ Возникла неизвестная ошибка... Такое может произойти если Вы не завершили предыдущую игру, или завершили игру закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуйте начать игру заново, и после завершения, нажать на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.')
#             return None, {'err_txt': 'The previous session is not finished', 'err_code': 2}
#
#     if type_invoice == "demo":
#
#         invoice_id, transaction_id = client.create_invoice(settings.DEFAULT_DEMO_AMOUNT/100)
#         InvoiceData.objects.create(
#             invoice_id=invoice_id,
#             game_id=game_id,
#             tr_id=transaction_id,
#             account=account,
#             type_invoice="demo"
#         )
#         return invoice_id, None
#
#
#     if account.real_balance > Decimal(0) or account.virtual_balance > Decimal(0):
#         invoice_id, transaction_id = client.create_invoice(Decimal(sum((account.real_balance, account.virtual_balance))/Decimal(10)))
#
#         InvoiceData.objects.create(
#             invoice_id=invoice_id,
#             game_id=game_id,
#             tr_id=transaction_id,
#             account=account,
#             type_invoice='real',
#             start_real_amount=account.real_balance,
#             start_virtual_amount=account.virtual_balance
#         )
#         return invoice_id, None
#     helpbot_services.send_msg(tg_id, '❌ На Вашем балансе надостаточно средств. Чтобы пополнить счет, перейдите в меню "💰 Баланс" и следуйте моим простым подсказкам!')
#     return None, {"err_txt": "Insufficient funds", "err_code": 1}
#


def create_game_session(tg_id, game_id, type_invoice):
    try:
        account = account_models.TelegramAccount.objects.get(tg_id=tg_id)
    except:
        return None, 'Telegram user does not exist'

    client = chc.CHCAPIClient()
    active_invoice = game_models.InvoiceData.objects.get_or_none(account=account, status='open', type_invoice=type_invoice)

    if active_invoice:
        try:
            closed_invoice = client.close_invoice(active_invoice.invoice_id)
            if type_invoice == 'real':
                update_balance_after_game(account, active_invoice, Decimal(closed_invoice[0])*Decimal(10))

            active_invoice.status = 'closed'
            active_invoice.save()
        except FailInvoiceVendorException:
            active_invoice.status = 'closed'
            active_invoice.save()
        except ThirdPartyVendorException:
            helpbot_services.send_msg(tg_id, abtest_services.get_text(tg_id, "error_start_game"))
            return None, {'err_txt': 'The previous session is not finished', 'err_code': 2}

    if type_invoice == "demo":

        invoice_id, transaction_id = client.create_invoice(settings.DEFAULT_DEMO_AMOUNT/100)
        game_models.InvoiceData.objects.create(
            invoice_id=invoice_id,
            game_id=game_id,
            tr_id=transaction_id,
            account=account,
            type_invoice="demo"
        )
        return invoice_id, None

    if account.real_balance > Decimal(0) or account.virtual_balance > Decimal(0):
        invoice_id, transaction_id = client.create_invoice(Decimal(sum((account.real_balance, account.virtual_balance))/Decimal(10)))

        game_models.InvoiceData.objects.create(
            invoice_id=invoice_id,
            game_id=game_id,
            tr_id=transaction_id,
            account=account,
            type_invoice='real',
            start_real_amount=account.real_balance,
            start_virtual_amount=account.virtual_balance,
            last_check_amount=account.real_balance+account.virtual_balance
        )
        return invoice_id, None
    helpbot_services.send_msg(tg_id, abtest_services.get_text(tg_id, "error_insufficient_balance"))
    return None, {"err_txt": "Insufficient funds", "err_code": 1}


def get_game(game_id, tg_id, type_game):
    invoice, falied_invoice = create_game_session(tg_id, game_id, type_game)
    result = {
        "id": game_id,
        "type": type_game
    }

    if invoice:
        link = chc.get_game_url(invoice, game_id)
        result["url"] = link
    else:
        err = falied_invoice
        result["url"] = None
        result["err_text"] = err["err_txt"],
        result["err_code"] = err["err_code"]

    return result

