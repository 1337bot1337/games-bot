from pyrogram import Client, Filters
from core.abtest import get_text
from core.api import GameAPI
from config.settings.bot import BOT_USERNAME


@Client.on_message(Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-affiliate")))
def affiliate_kb(cli, m):
    tg_id = m.from_user.id
    ref_link = f"https://telegram.me/{BOT_USERNAME}?start=ref{tg_id}"
    txt = get_text(tg_id, "affiliate-menu").format(ref_count=GameAPI.check_ref_count(tg_id), link=ref_link)
    m.reply(txt)
