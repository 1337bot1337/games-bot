from pyrogram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from .api.pyroAPI import HelpBot
from core.apps.abtest import services as abtest_services
from core.apps.game.utils import game_dict, games_1


def send_msg(tg_id: int or str, text: str, session_name: str = None):
    client = HelpBot(session_name=session_name)
    client.send_msg(tg_id, text)


def broadcast(users: iter, message: str, keyboard: str):
    client = HelpBot(session_name="session_broadcast")
    client.start()

    for user in users:
        try:
            if keyboard == "start":
                client.send_message(user.tg_id, message, reply_markup=_menu(user.tg_id))
            elif keyboard == "games":
                client.send_message(user.tg_id, message, reply_markup=_game_list(games_1, 0))
            elif keyboard == "invite":
                kb = InlineKeyboardMarkup([[InlineKeyboardButton("🤝 Пригласить друга", switch_inline_query="start")]])
                client.send_message(user.tg_id, message, reply_markup=kb)
            elif keyboard == "deposit":
                kb = InlineKeyboardMarkup([[InlineKeyboardButton("💳 Пополнить баланс", callback_data="balance-buy_token")]])
                client.send_message(user.tg_id, message, reply_markup=kb)
            elif keyboard == "none":
                client.send_message(user.tg_id, message)
        except:
            continue

    client.stop()


def _menu(tg_id: int):
    kb = ReplyKeyboardMarkup(
        [
            [abtest_services.get_text(tg_id, "kb-games")],
            [abtest_services.get_text(tg_id, "kb-balance"), abtest_services.get_text(tg_id, "kb-help")],
            [abtest_services.get_text(tg_id, "kb-affiliate")]
        ],
        resize_keyboard=True,
    )
    return kb


def _game_list(games, offset):
    kb_list = []
    if offset == 0:
        kb_list = [
            [InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search"),
             InlineKeyboardButton(f'⏩', callback_data="game-move-10")]
        ]
    elif offset == 10:
        kb_list = [
            [InlineKeyboardButton(f'⏪', callback_data="game-move-0"),
             InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search"),
             InlineKeyboardButton(f'⏩', callback_data="game-move-20")]
        ]
    elif offset == 20:
        kb_list = [
            [InlineKeyboardButton(f'⏪', callback_data="game-move-10"),
             InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search"),
             InlineKeyboardButton(f'⏩', callback_data="game-move-30")]
        ]
    elif offset == 30:
        kb_list = [
            [InlineKeyboardButton(f'⏪', callback_data="game-move-20"),
             InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search"),
             InlineKeyboardButton(f'⏩', callback_data="game-move-40")]
        ]
    elif offset == 40:
        kb_list = [
            [InlineKeyboardButton(f'⏪', callback_data="game-move-30"),
             InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search")]
        ]

    for game_id in games:
        game_title = games[game_id]
        emoji = game_dict[game_title]["emoji"]

        kb_list.append(
            [InlineKeyboardButton(f'{emoji} {game_title}', callback_data=f'game-{game_id}')])

    return InlineKeyboardMarkup(kb_list)


def get_tg_user(tg_id: int or str):
    client = HelpBot(session_name="get_tg_user_session")
    client.start()

    tg_user = client.get_users(tg_id)
    user = {
        "id": tg_user.id,
        "username": "[отсутствует]",
        "first_name": "[отсутствует]",
        "last_name": "[отсутствует]",
    }

    if tg_user.username:
        user["username"] = tg_user.username

    if tg_user.first_name:
        user["first_name"] = tg_user.first_name

    if tg_user.last_name:
        user["last_name"] = tg_user.last_name
    client.stop()
    return user
