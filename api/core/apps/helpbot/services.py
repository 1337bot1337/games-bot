from .api.pyroAPI import HelpBot


def send_msg(tg_id, text: str):
    client = HelpBot()
    client.send_msg(tg_id, text)


def broadcast(users, message):
    client = HelpBot()
    client.start()

    for user in users:
        try:
            client.send_message(user.tg_id, message)
        except:
            continue

    client.stop()


def get_tg_user(tg_id: int or str):
    client = HelpBot()
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
