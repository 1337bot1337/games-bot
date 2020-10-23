from pyrogram import Client, Filters
from core import texts
from core.api import GameAPI
from core import keyboards as kb


@Client.on_message(Filters.regex(r'^💰 Баланс$'))
def balance_menu(cli, m):
    balances = GameAPI.get_balance(m.from_user.id)
    m.reply(texts.balance(balances), reply_markup=kb.balance_menu)
