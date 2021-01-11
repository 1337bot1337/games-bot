from pyrogram import ReplyKeyboardMarkup

from .api.pyroAPI import HelpBot
from core.apps.abtest import services as abtest_services


def send_msg(tg_id: int or str, text: str, session_name: str = None):
    client = HelpBot(session_name=session_name)
    client.send_msg(tg_id, text)


def broadcast(users: iter, message: str, kb_start=False):
    client = HelpBot(session_name="session_broadcast")
    client.start()

    for user in users:
        try:
            if kb_start:
                client.send_message(user.tg_id, message, reply_markup=_menu(user.tg_id))
            else:
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
