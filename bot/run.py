from pyrogram import Client
import environ
import os

ROOT = environ.Path(__file__) -1

env_file = os.path.join(ROOT, 'config', 'settings', '.env')
env = environ.Env()
environ.Env.read_env(env_file)

TG_API_ID = env.str('TG_API_ID')
TG_API_HASH = env.str('TG_API_HASH')
TG_API_TOKEN = env.str('TG_API_TOKEN')

app = Client(
            'session_main',
            api_id=TG_API_ID, api_hash=TG_API_HASH, bot_token=TG_API_TOKEN,
            plugins=dict(root='handlers'))


if __name__ == "__main__":
    app.run()
