from pyrogram import Client, Filters, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from core.abtest import get_text
from core.api import GameAPI
from config.settings.bot import BOT_USERNAME
from config import cache

from core.services import get_user


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-affiliate")))
def affiliate_kb(cli, m):
    tg_id = m.from_user.id
    set = cache.get_affiliate_setup()
    ref_link = f"https://telegram.me/{BOT_USERNAME}?start=ref{tg_id}"
    txt = get_text(tg_id, "affiliate-menu").format(ref_count=GameAPI.check_ref_count(tg_id),
                                                   min_referral_deposit=set["min_referral_deposit"],
                                                   bonus=set["referrer_deposit_bonus"],
                                                   link=ref_link)

    m.reply(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🤝 Пригласить друга", switch_inline_query="start")]]))
    user = get_user(m)
    GameAPI.send_statistic(user, 'press_button', data={"button_name": "affiliate", "location": "main_menu"})


@Client.on_inline_query()
def send_ref_request(cli, m):
    set = cache.get_affiliate_setup()
    factor_deposit = int(round(set["referral_deposit_bonus"] * 100 - 100, 2))
    txt = get_text(m.from_user.id, "affiliate-invite_friend").format(bonus=factor_deposit)
    ref_link = f"https://telegram.me/{BOT_USERNAME}?start=ref{m.from_user.id}"
    cli.answer_inline_query(inline_query_id=m.id,  results=[
            InlineQueryResultArticle(
                "🤝 Пригласить друга",
                InputTextMessageContent(txt),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="🎰 Пойти играть", url=ref_link)]]),
            )
        ],
    )