from pyrogram import Client

from django.conf import settings


class HelpBot(Client):

    def __init__(self):
        super().__init__(session_name='session_helpbot', api_id=settings.TG_API_ID, api_hash=settings.TG_API_HASH, bot_token=settings.TG_API_TOKEN)

    def send_msg(self, tg_id, text):
        app = self.start()

        try:
            app.send_message(tg_id, text)
        except:
            pass
        app.stop()
