from .api import GameAPI
from pyrogram import Client
from config.settings.bot import TG_API_ID, TG_API_HASH, TG_API_TOKEN
from threading import Event

games = {
    1003: "Fire Rage +",
    1018: "King of Jewels",
    1019: "Gates of Avalon",
    1024: "Dolphins Shell",
    1027: "Lady Luck",
    1028: "Pirates Fortune",
    1031: "Bananas",
    1056: "Extra Super 7",
    1058: "Box of Ra",
    1063: "Rise Of Imperium",
}

game_dict = {
    "Fire Rage +": {"id": 1003, "emoji": "🔥", "image": 'media/1003.jpg', "description": ''},
    "King of Jewels": {"id": 1018, "emoji": "🤴", "image":'media/1018.jpg'},
    "Gates of Avalon": {"id": 1019, "emoji": "⛩", "image": 'media/1019.jpg'},
    "Dolphins Shell": {"id": 1024, "emoji": "🐬", "image": 'media/1024.jpg'},
    "Lady Luck": {"id": 1027, "emoji": "🌟", "image": 'media/1027.jpg'},
    "Pirates Fortune": {"id": 1028, "emoji": "🏴‍☠️", "image": 'media/1028.jpg'},
    "Bananas": {"id": 1031, "emoji": "🍌", "image": 'media/1031.jpg'},
    "Extra Super 7": {"id": 1056, "emoji": "♨️", "image": 'media/1056.jpg'},
    "Box of Ra": {"id": 1058, "emoji": "🥡", "image": 'media/1058.jpg'},
    "Rise Of Imperium": {"id": 1063, "emoji": "🏯", "image": 'media/1063.jpg'},
}


class BalanceClient(Client):

    def __init__(self):

        self.done = Event()
        self.value = None
        self.event_canceled = False
        super().__init__(session_name='session_balance', api_id=TG_API_ID, api_hash=TG_API_HASH, bot_token=TG_API_TOKEN)