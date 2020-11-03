from .api.pyroAPI import HelpBot


def send_msg(tg_id: int, text: str):
    client = HelpBot()
    client.send_msg(tg_id, text)
