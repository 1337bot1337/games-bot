from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .services import game_dict as games

select_language = ReplyKeyboardMarkup(
            [
                ['🇬🇧 English'],
                ['🇷🇺 Русский']
            ],
            resize_keyboard=True,
        )

accept_license_terms = ReplyKeyboardMarkup(
            [
                ['✅ Принимаю условия']
            ],
            resize_keyboard=True,
        )


menu = ReplyKeyboardMarkup(
            [
                ['🎰 Игры'],
                ['💰 Баланс', '🤝 Партнёрская программа'],
                ['❓ Помощь']
            ],
            resize_keyboard=True,
        )


games = ReplyKeyboardMarkup(
            [
                [f'Играть - {games["Fire Rage +"]["emoji"]} Fire Rage +', f'Играть - {games["King of Jewels"]["emoji"]} King of Jewels'],
                [f'Играть - {games["Gates of Avalon"]["emoji"]} Gates of Avalon', f"Играть - {games['Dolphins Shell']['emoji']} Dolphins Shell"],
                [f'Играть - {games["Lady Luck"]["emoji"]} Lady Luck', f'Играть - {games["Pirates Fortune"]["emoji"]} Pirates Fortune'],
                [f'Играть - {games["Bananas"]["emoji"]} Bananas', f'Играть - {games["Extra Super 7"]["emoji"]} Extra Super 7'],
                [f'Играть - {games["Box of Ra"]["emoji"]} Box of Ra', f'Играть - {games["Rise Of Imperium"]["emoji"]} Rise Of Imperium'],
                ['🔙 В главное меню']
            ],
            resize_keyboard=True,
        )


def select_type_game(game_id):

    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('Играть на Gambling Tokens', callback_data=f'play-real-{game_id}')],
            [InlineKeyboardButton('Играть на демо-счёт', callback_data=f'play-demo-{game_id}')]
        ]
    )
    return kb


def play_game(title, url):
    return InlineKeyboardMarkup([[InlineKeyboardButton(f'Играть в {title}', url=url)]])


balance_menu = ReplyKeyboardMarkup(
        [
            ['📥 Купить Gambling Tokens', '📤 Вывести'],
            ['🔙 В главное меню']
        ],
        resize_keyboard=True,
    )
