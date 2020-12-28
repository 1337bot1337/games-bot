from pyrogram import Client, Filters
from core import texts
from core.api import GameAPI
from core import keyboards as kb
from threading import Event
from core.services import BalanceClient, get_user
from decimal import Decimal, InvalidOperation
from core.abtest import get_text
from config import cache


@Client.on_message(Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-balance")))
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
        cache.change_user_cache(tg_id, "await_deposit_amount", True)
        cb.message.reply(get_text(tg_id, "deposit-enter_amount").format(min_deposit=100),
                         reply_markup=kb.cancel_deposit(tg_id))

        GameAPI.send_statistic(user, 'press_button', data={"button_name": "deposit", "location": "main_menu/balance"})

    if action == 'withdrawal':
        GameAPI.send_statistic(user, 'press_button',
                               data={"button_name": "withdrawal", "location": "main_menu/balance"})

        cb.message.reply(get_text(tg_id, "withdrawal-enter_amount"), reply_markup=kb.cancel_withdrawal(tg_id))

        cache.change_user_cache(tg_id, "await_withdraw_amount", True)


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-balance-cancel_withdrawal")))
def cancel_withdraw_kb(cli, m):
    tg_id = m.from_user.id
    if cache.get_user_cache(tg_id)["await_withdraw_amount"] or cache.get_user_cache(tg_id)["await_withdraw_card"]:
        m.reply(get_text(tg_id, "withdrawal-cancel"), reply_markup=kb.menu(tg_id))
        cache.change_user_cache(tg_id, "await_withdraw_amount", False)
        cache.change_user_cache(tg_id, "await_withdraw_card", False)

        user = get_user(m)
        GameAPI.send_statistic(user, 'press_button', data={"button_name": "cancel_withdraw",
                                                            "location": "main_menu/balance/withdrawal"})
    else:
        cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg',
                       reply_markup=kb.menu(tg_id))


@Client.on_message(Filters.create(lambda _, m: cache.get_user_cache(m.from_user.id)["await_withdraw_amount"]))
def withdraw_amount(cli, m):
    tg_id = m.from_user.id
    try:
        amount = Decimal(m.text.replace(',', '.'))
        if amount == 0:
            return m.reply(get_text(tg_id, "withdrawal-null_error"), reply_markup=kb.cancel_withdrawal(tg_id))

        balance = GameAPI.get_balance(tg_id)

        if amount > Decimal(balance['real_balance']):
            return m.reply(get_text(tg_id, "withdrawal-max_limit").format(
                max_amount=round(Decimal(balance["real_balance"]), 2)), reply_markup=kb.cancel_withdrawal(tg_id))

        cache.change_user_cache(tg_id, "withdraw_amount", amount)
        cache.change_user_cache(tg_id, "await_withdraw_amount", False)
        cache.change_user_cache(tg_id, "await_withdraw_card", True)
        m.reply(get_text(tg_id, 'withdrawal-enter_card'), reply_markup=kb.cancel_withdrawal(tg_id))
    except InvalidOperation:
        return m.reply(get_text(tg_id, "invalid_number"), reply_markup=kb.cancel_withdrawal(tg_id))


@Client.on_message(Filters.create(lambda _, m: cache.get_user_cache(m.from_user.id)["await_withdraw_card"]))
def card_withdraw(cli, m):
    tg_id = m.from_user.id
    try:
        card = int(m.text.replace('-', ''))
        if len(m.text.replace('-', '')) != 16:
            raise ValueError

    except ValueError:
        return m.reply(get_text(tg_id, "withdrawal-invalid_card"), reply_markup=kb.cancel_withdrawal(tg_id))

    amount = cache.get_user_cache(tg_id)["withdraw_amount"]

    withdrawal_request = GameAPI.withdrawal_request(tg_id, card, amount)
    if withdrawal_request == 200:
        cache.change_user_cache(tg_id, "await_withdraw_card", False)
        m.reply(get_text(tg_id, "withdrawal-request_created").format(amount=amount, card=card),
                reply_markup=kb.menu(tg_id))


@Client.on_message(
    ~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-balance-cancel_deposit")))
def cancel_deposit_kb(cli, m):
    tg_id = m.from_user.id
    if cache.get_user_cache(tg_id)["await_deposit_amount"]:
        cache.change_user_cache(tg_id, "await_deposit_amount", False)
        m.reply(get_text(tg_id, "deposit-canceled"), reply_markup=kb.menu(tg_id))
        user = get_user(m)
        GameAPI.send_statistic(user, 'press_button', data={"button_name": "cancel_deposit",
                                                            "location": "main_menu/balance/deposit"})
    else:
        cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg',
                       reply_markup=kb.menu(tg_id))


@Client.on_message(Filters.create(lambda _, m: cache.get_user_cache(m.from_user.id)["await_deposit_amount"]))
def deposit_amount(cli, m):
    tg_id = m.from_user.id
    min_deposit = 100

    try:
        amount = Decimal(m.text.replace(',', '.'))
        if amount < min_deposit:
            return m.reply(get_text(tg_id, "deposit-min_limit").format(
                min_deposit=min_deposit
            ), reply_markup=kb.cancel_deposit(tg_id))
        cache.change_user_cache(tg_id, "await_deposit_amount", False)
    except InvalidOperation:
        return m.reply(get_text(tg_id, "invalid_number"), reply_markup=kb.cancel_deposit(tg_id))

    cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg',
                   reply_markup=kb.menu(tg_id))
    m.reply(get_text(tg_id, "deposit-replenish_link").format(
        amount=amount
    ), reply_markup=kb.deposit_url(tg_id, amount))


