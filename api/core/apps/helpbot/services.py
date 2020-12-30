from .api.pyroAPI import HelpBot


def send_msg(tg_id: int or str, text: str, session_name: str = None):
    client = HelpBot(session_name=session_name)
    client.send_msg(tg_id, text)


def broadcast(users: iter, message: str):
    client = HelpBot(session_name="session_broadcast")
    client.start()

    for user in users:
        try:
            client.send_message(user.tg_id, message)
        except:
            continue

    client.stop()


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
