from pyrogram import Client, Filters
from core import texts
from core.api import GameAPI
from core import keyboards as kb
from threading import Event
from core.services import BalanceClient, get_user
from decimal import Decimal, InvalidOperation
from core.abtest import get_text


@Client.on_message(Filters.create(lambda _, m: m.text in get_text(m.from_user.id, "kb-balance")))
def balance_bt(cli, m):
    tg_id = m.from_user.id
    balances = GameAPI.get_balance(tg_id)
    if int(balances['withdraw_in_progress_amount']) > 0:

        m.reply(get_text(tg_id, "balance_menu-with_withdraw_in_progress_amount").format(
            real_balance=balances["real_balance"],
            bonus_balance=balances["virtual_balance"],
            withdraw_in_progress_amount=balances['withdraw_in_progress_amount']
        ), reply_markup=kb.balance_menu(tg_id))
    else:
        m.reply(get_text(tg_id, "balance_menu-without_withdraw_in_progress_amount").format(
            real_balance=balances["real_balance"],
            bonus_balance=balances["virtual_balance"]
        ), reply_markup=kb.balance_menu(tg_id))

    user = get_user(m)
    GameAPI.send_statistic(user, 'press_button', data={"button_name": "balance", "location": "main_menu"})


@Client.on_callback_query(Filters.create(lambda _, cb: cb.data.startswith('balance')))
def balance_menu(cli, cb):
    tg_id = cb.from_user.id
    action = cb.data.split('-')[1]
    user = get_user(cb)
    if action == 'buy_token':

        deposit_client = BalanceClient()
        _deposit(deposit_client)
        cb.message.reply(get_text(tg_id, "deposit-enter_amount").format(min_deposit=100), reply_markup=kb.cancel_deposit(tg_id))
        deposit_client.start()

        deposit_client.done.wait()
        deposit_client.stop()

        GameAPI.send_statistic(user, 'press_button', data={"button_name": "deposit", "location": "main_menu/balance"})

    if action == 'withdrawal':
        GameAPI.send_statistic(user, 'press_button',
                               data={"button_name": "withdrawal", "location": "main_menu/balance"})

        cb.message.reply(get_text(tg_id, "withdrawal-enter_amount"), reply_markup=kb.cancel_withdrawal(tg_id))
        app_amount = BalanceClient()
        _amount_withdrawal(app_amount)

        app_amount.start()
        amount_done = app_amount.done.wait()
        app_amount.stop()
        if amount_done:
            if app_amount.event_canceled is True:
                return cb.message.reply(get_text(tg_id, "withdrawal-cancel"), reply_markup=kb.menu(tg_id))

            cb.message.reply(get_text(tg_id, 'withdrawal-enter_card'), reply_markup=kb.cancel_withdrawal(tg_id))

            app_card = BalanceClient()
            _card_withdrawal(app_card)
            app_card.start()

            card_done = app_card.done.wait()
            app_card.stop()
            if card_done:
                if app_amount.event_canceled is True:
                    GameAPI.send_statistic(user, 'press_button', data={"button_name": "cancel_withdrawal",
                                                                                 "location": "main_menu/balance/withdrawal"})
                    return cb.message.reply(get_text(tg_id, "withdrawal-cancel"))

                card = app_card.value
                amount = app_amount.value
                withdrawal_request = GameAPI.withdrawal_request(tg_id, card, amount)

                if withdrawal_request == 200:
                    cb.message.reply(get_text(tg_id, "withdrawal-request_created").format(
                        amount=amount,
                        card=card
                    ), reply_markup=kb.menu(tg_id))


def _amount_withdrawal(client):

    @client.on_message()
    def amount_for_withdrawal(cli, m):
        tg_id = m.from_user.id
        if m.text == get_text(tg_id, "kb-balance-cancel_withdrawal"):
            cli.event_canceled = True
            cli.done.set()
            return

        try:
            value = Decimal(m.text.replace(',', '.'))
            if value == 0:
                return m.reply(get_text(tg_id, "withdrawal-null_error"), reply_markup=kb.cancel_withdrawal(tg_id))

            balance = GameAPI.get_balance(tg_id)

            if value > Decimal(balance['real_balance']):
                return m.reply(get_text(tg_id, "withdrawal-max_limit").format(
                    max_amount=round(Decimal(balance["real_balance"]), 2)), reply_markup=kb.cancel_withdrawal(tg_id))

        except InvalidOperation:
            return m.reply(get_text(tg_id, "invalid_number"), reply_markup=kb.cancel_withdrawal(tg_id))

        cli.value = value
        cli.done.set()
        return m.text

    # @client.on_callback_query(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-balance-cancel_withdrawal")))
    # def cancel_withdrawal_kb(cli, m):
    #     cli.event_canceled = True
    #     cli.done.set()


def _card_withdrawal(client):
    @client.on_message()
    def card_for_withdrawal(cli, m):
        tg_id = m.from_user.id

        if m.text == get_text(tg_id, "kb-balance-cancel_withdrawal"):
            cli.event_canceled = True
            cli.done.set()
            return

        try:
            card = int(m.text.replace('-', ''))
            if len(m.text.replace('-', '')) != 16:
                raise ValueError

        except ValueError:
            return m.reply(get_text(tg_id, "withdrawal-invalid_card"), reply_markup=kb.cancel_withdrawal(tg_id))

        cli.value = card
        cli.done.set()
        return m.text

    # @client.on_callback_query(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-balance-cancel_withdrawal")))
    # def cancel_withdrawal_kb(cli, m):
    #     cli.event_canceled = True
    #     cli.done.set()


def _deposit(client):

    @client.on_message()
    def deposit_amount(cli, m):
        tg_id = m.from_user.id
        min_deposit = 100
        if m.text == get_text(tg_id, "kb-balance-cancel_deposit"):
            m.reply(get_text(tg_id, "deposit-canceled"), reply_markup=kb.menu(tg_id))
            user = get_user(m)
            GameAPI.send_statistic(user, 'press_button', data={"button_name": "cancel_deposit",
                                                                "location": "main_menu/balance/deposit"})
            cli.done.set()
            return

        try:
            amount = Decimal(m.text.replace(',', '.'))
            if amount < min_deposit:
                return m.reply(get_text(tg_id, "deposit-min_limit").format(
                    min_deposit=min_deposit
                ), reply_markup=kb.cancel_deposit(tg_id))

        except InvalidOperation:
            return m.reply(get_text(tg_id, "invalid_number"), reply_markup=kb.cancel_deposit(tg_id))

        m.reply(get_text(tg_id, "deposit-replenish_link").format(
            amount=amount
        ), reply_markup=kb.deposit_url(tg_id, amount))
        cli.done.set()

    # @client.on_callback_query(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-balance-cancel_deposit")))
    # def cancel_deposit_kb(cli, m):
    #     tg_id = m.from_user.id
    #     m.reply(get_text(tg_id, "deposit-canceled"))
    #     cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg', reply_markup=kb.menu(tg_id))
    #     GameAPI.send_statistic(tg_id, 'press_button', data={"button_name": "cancel_deposit",
    #                                                                  "location": "main_menu/balance/deposit"})
    #     cli.done.set()