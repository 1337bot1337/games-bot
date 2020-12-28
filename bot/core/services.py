from pyrogram import Client
from pyrogram import Message as PyrogramMessage
from config.settings.bot import TG_API_ID, TG_API_HASH, TG_API_TOKEN
from threading import Event
from config import cache
from core.api import GameAPI

games_1 = {
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

games_2 = {1002: "Seven's on Fire+",
           1004: "Roll of Ramses",
           1013: "Rich Fruits",
           1014: "Ultra 7 Hot",
           1017: "European Roulettes",
           1023: "Blackjack",
           1025: "Tropical Fruits",
           1026: "Money",
           1029: "Golden Scatter",
           1030: "Russian Poker"}

games_3 = {1032: "Mysterious Jewels",
           1033: "Always Cherry Lotto",
           1034: "Hot Slot Lotto",
           1035: "Golden Scatter Lotto",
           1036: "Scatter Wins Lotto",
           1037: "Golden Harvest Lotto",
           1038: "Bananas Lotto",
           1039: "Dolphins Lotto",
           1040: "Money Lotto",
           1041: "Lucky Lady Glamour Lotto"}

games_4 = {1042: "Nautilus Lotto",
           1043: "Crazy Barmen Lotto",
           1044: "Gates Of Avalon Lotto",
           1045: "Hot Sevens Lotto",
           1046: "Hit Jewels Lotto",
           1047: "King Of Jewels Lotto",
           1048: "Book Of Winners Lotto",
           1049: "ComputerWorld Lotto",
           1050: "Triple Diamond Lotto",
           1051: "Mariner Lotto"}

games_5 = {1052: "Hearts Lotto",
           1053: "Captain Lotto",
           1054: "Simple Diamond",
           1055: "Book Of Sphinx",
           1057: "Fortune Star"}

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
    1002: "Seven's on Fire+",
    1004: "Roll of Ramses",
    1013: "Rich Fruits",
    1014: "Ultra 7 Hot",
    1017: "European Roulettes",
    1023: "Blackjack",
    1025: "Tropical Fruits",
    1026: "Money",
    1029: "Golden Scatter",
    1030: "Russian Poker",
    1032: "Mysterious Jewels",
    1033: "Always Cherry Lotto",
    1034: "Hot Slot Lotto",
    1035: "Golden Scatter Lotto",
    1036: "Scatter Wins Lotto",
    1037: "Golden Harvest Lotto",
    1038: "Bananas Lotto",
    1039: "Dolphins Lotto",
    1040: "Money Lotto",
    1041: "Lucky Lady Glamour Lotto",
    1042: "Nautilus Lotto",
    1043: "Crazy Barmen Lotto",
    1044: "Gates Of Avalon Lotto",
    1045: "Hot Sevens Lotto",
    1046: "Hit Jewels Lotto",
    1047: "King Of Jewels Lotto",
    1048: "Book Of Winners Lotto",
    1049: "ComputerWorld Lotto",
    1050: "Triple Diamond Lotto",
    1051: "Mariner Lotto",
    1052: "Hearts Lotto",
    1053: "Captain Lotto",
    1054: "Simple Diamond",
    1055: "Book Of Sphinx",
    1057: "Fortune Star"

}

game_dict = {
    "Fire Rage +": {"id": 1003, "emoji": "🔥", "image": 'media/1003.jpg', "description": ''},
    "King of Jewels": {"id": 1018, "emoji": "🤴", "image": 'media/1018.jpg'},
    "Gates of Avalon": {"id": 1019, "emoji": "⛩", "image": 'media/1019.jpg'},
    "Dolphins Shell": {"id": 1024, "emoji": "🐬", "image": 'media/1024.jpg'},
    "Lady Luck": {"id": 1027, "emoji": "🌟", "image": 'media/1027.jpg'},
    "Pirates Fortune": {"id": 1028, "emoji": "🏴‍☠️", "image": 'media/1028.jpg'},
    "Bananas": {"id": 1031, "emoji": "🍌", "image": 'media/1031.jpg'},
    "Extra Super 7": {"id": 1056, "emoji": "♨️", "image": 'media/1056.jpg'},
    "Box of Ra": {"id": 1058, "emoji": "🥡", "image": 'media/1058.jpg'},
    "Rise Of Imperium": {"id": 1063, "emoji": "🏯", "image": 'media/1063.jpg'},
    "Seven's on Fire+": {"id": 1002, "emoji": "7️⃣🔥", "image": "media/1002.jpg"},
    "Roll of Ramses": {"id": 1004, "emoji": "👳🏾", "image": "media/1004.jpg"},
    "Rich Fruits": {"id": 1013, "emoji": "🍎🥭", "image": "media/1013.jpg"},
    "Ultra 7 Hot": {"id": 1014, "emoji": "♨️", "image": "media/1014.jpg"},
    "European Roulettes": {"id": 1017, "emoji": "🏵", "image": "media/1017.jpg"},
    "Blackjack": {"id": 1023, "emoji": "♣️", "image": "media/1023.jpg"},
    "Tropical Fruits": {"id": 1025, "emoji": "🥥🍍", "image": "media/1025.jpg"},
    "Money": {"id": 1026, "emoji": "💵", "image": "media/1026.jpg"},
    "Golden Scatter": {"id": 1029, "emoji": "🛎", "image": "media/1029.jpg"},
    "Russian Poker": {"id": 1030, "emoji": "♥️", "image": "media/1030.jpg"},
    "Mysterious Jewels": {"id": 1032, "emoji": "💠", "image": "media/1032.jpg"},
    "Always Cherry Lotto": {"id": 1033, "emoji": "🍒", "image": "media/1033.jpg"},
    "Hot Slot Lotto": {"id": 1034, "emoji": "🎰", "image": "media/1034.jpg"},
    "Golden Scatter Lotto": {"id": 1035, "emoji": "🛎", "image": "media/1029.jpg"},
    "Scatter Wins Lotto": {"id": 1036, "emoji": "🎯", "image": "media/1036.jpg"},
    "Golden Harvest Lotto": {"id": 1037, "emoji": "🔆", "image": "media/1037.jpg"},
    "Bananas Lotto": {"id": 1038, "emoji": "🍌", "image": "media/1031.jpg"},
    "Dolphins Lotto": {"id": 1039, "emoji": "🐬", "image": "media/1024.jpg"},
    "Money Lotto": {"id": 1040, "emoji": "💵", "image": "media/1026.jpg"},
    "Lucky Lady Glamour Lotto": {"id": 1041, "emoji": "🌟", "image": "media/1041.jpg"},
    "Nautilus Lotto": {"id": 1042, "emoji": "⚓️", "image": "media/1042.jpg"},
    "Crazy Barmen Lotto": {"id": 1043, "emoji": "🍻", "image": "media/1043.jpg"},
    "Gates Of Avalon Lotto": {"id": 1044, "emoji": "⛩", "image": "media/1019.jpg"},
    "Hot Sevens Lotto": {"id": 1045, "emoji": "♨️", "image": "media/1045.jpg"},
    "Hit Jewels Lotto": {"id": 1046, "emoji": "💠", "image": "media/10.jpg"},
    "King Of Jewels Lotto": {"id": 1047, "emoji": "🤴", "image": "media/1018.jpg"},
    "Book Of Winners Lotto": {"id": 1048, "emoji": "📓", "image": "media/1048.jpg"},
    "ComputerWorld Lotto": {"id": 1049, "emoji": "🖥", "image": "media/1049.jpg"},
    "Triple Diamond Lotto": {"id": 1050, "emoji": "💎💎💎", "image": "media/1050.jpg"},
    "Mariner Lotto": {"id": 1051, "emoji": "🚢", "image": "media/1051.jpg"},
    "Hearts Lotto": {"id": 1052, "emoji": "❤️", "image": "media/1052.jpg"},
    "Captain Lotto": {"id": 1053, "emoji": "🧭", "image": "media/1053.jpg"},
    "Simple Diamond": {"id": 1054, "emoji": "💎", "image": "media/1054.jpg"},
    "Book Of Sphinx": {"id": 1055, "emoji": "📘", "image": "media/1055.jpg"},
    "Fortune Star": {"id": 1057, "emoji": "⭐️", "image": "media/1057.jpg"},

}


def search_game(game_name):
    games = []

    for game in game_dict:
        if game_name.lower() in game.lower():
            temp = game_dict[game]
            temp["name"] = game
            games.append(temp)

    return games


class BalanceClient(Client):

    def __init__(self):
        self.done = Event()
        self.value = None
        self.event_canceled = False
        super().__init__(session_name='session_balance', api_id=TG_API_ID, api_hash=TG_API_HASH, bot_token=TG_API_TOKEN)


class SearchGameClient(Client):
    def __init__(self):
        self.done = Event()
        self.search_name = None
        super().__init__(session_name='session_search', api_id=TG_API_ID, api_hash=TG_API_HASH, bot_token=TG_API_TOKEN)


def get_user(message: PyrogramMessage) -> dict:
    user = {
        "id": message.from_user.id,
        "username": "[отсутствует]",
        "first_name": "[отсутствует]",
        "last_name": "[отсутствует]",
    }

    if message.from_user.username:
        user["username"] = message.from_user.username

    if message.from_user.first_name:
        user["first_name"] = message.from_user.first_name

    if message.from_user.last_name:
        user["last_name"] = message.from_user.last_name

    return user


def get_user_from_cache(tg_id):
    users = cache.get_users()
    user = users.get(tg_id, None)

    return user


def get_referrer_name(referrer_id):
    name = None
    # if user.user_name:
    #     return f'@{user.user_name}'

    user = get_user_from_cache(referrer_id)

    if not user:
        return None

    if user["first_name"] != "[отсутствует]" and user["last_name"] == "[отсутствует]":

        name = f'[{user["first_name"]}](tg://user?id={referrer_id})'

    elif user["first_name"] != "[отсутствует]" and user["last_name"] != "[отсутствует]":
        name = f'[{user["first_name"]} {user["last_name"]}](tg://user?id={referrer_id})'

    return name


def get_referral_bonus():
    r = cache.get_affiliate_setup()
    return r["referral_deposit_bonus"]


def ref_source_none(tg_id: int or str):
    user = get_user_from_cache(tg_id)

    if user["source"] != "none":
        return False, True, False

    if GameAPI.check_ref(tg_id):
        return True, False, False

    return False, False, False

