from pyrogram import Client, Filters
from core import texts
from core.api import GameAPI
from core import keyboards as kb
from threading import Event
from core.services import WithdrawalClient
from decimal import Decimal, InvalidOperation


@Client.on_message(Filters.regex(r'^💰 Баланс$'))
def balance_bt(cli, m):
    balances = GameAPI.get_balance(m.from_user.id)
    m.reply(texts.balance(balances), reply_markup=kb.balance_menu)


@Client.on_callback_query(Filters.create(lambda _, cb: cb.data.startswith('balance')))
def balance_menu(cli, cb):
    tg_id = cb.from_user.id
    action = cb.data.split('-')[1]

    if action == 'buy_token':
        cli.answer_callback_query(cb.id, 'Скоро...')

    if action == 'withdrawal':

        cb.message.reply('Введите сумму для вывода', reply_markup=kb.cancel_withdrawal)
        app_amount = WithdrawalClient()
        _amount_withdrawal(app_amount)

        app_amount.start()
        amount_done = app_amount.done.wait()
        app_amount.stop()
        if amount_done:
            if app_amount.withdrawal_canceled is True:
                return cb.message.reply('❌ Вывод отменен')

            cb.message.reply('Введите карту', reply_markup=kb.cancel_withdrawal)

            app_card = WithdrawalClient()
            _card_withdrawal(app_card)
            app_card.start()

            card_done = app_card.done.wait()
            app_card.stop()
            if card_done:
                if app_amount.withdrawal_canceled is True:
                    return cb.message.reply('❌ Вывод отменен')

                card = app_card.value
                amount = app_amount.value
                withdrawal_request = GameAPI.withdrawal_request(tg_id, card, amount)

                if withdrawal_request == 200:
                    cb.message.reply(f'✅ Заявка на вывод {amount} на карту {card} **успешно создана**.')


def _amount_withdrawal(client):

    @client.on_message()
    def amount_for_withdrawal(cli, m):
        try:
            value = Decimal(m.text.replace(',', '.'))
            if value == 0:
                return m.reply('Вы не можете вывести 0', reply_markup=kb.cancel_withdrawal)

            balance = GameAPI.get_balance(m.from_user.id)

            if value > balance['real_balance']:
                return m.reply(f'Вы не можете вывести больше чем {balance["real_balance"]}', reply_markup=kb.cancel_withdrawal)

        except InvalidOperation:
            return m.reply('Некорректное значение', reply_markup=kb.cancel_withdrawal)

        cli.value = value
        cli.done.set()
        return m.text

    @client.on_callback_query(Filters.callback_data('cancel_withdrawal'))
    def cancel_withdrawal_cb(cli, cb):
        cli.withdrawal_canceled = True
        cb.message.edit(cb.message.text)
        cli.done.set()


def _card_withdrawal(client):
    @client.on_message()
    def card_for_withdrawal(cli, m):
        try:
            card = int(m.text.replace('-', ''))
            if len(m.text.replace('-', '')) != 16:
                raise ValueError

        except ValueError:
            return m.reply('Некорректная карта', reply_markup=kb.cancel_withdrawal)

        cli.value = card
        cli.done.set()
        return m.text

    @client.on_callback_query(Filters.callback_data('cancel_withdrawal'))
    def cancel_withdrawal_cb(cli, cb):
        cli.withdrawal_canceled = True
        cb.message.edit(cb.message.text)
        cli.done.set()