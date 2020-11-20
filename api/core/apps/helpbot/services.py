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
