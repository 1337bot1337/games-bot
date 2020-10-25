from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .services import game_dict as games
from .api import GameAPI
import urllib
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


# games = ReplyKeyboardMarkup(
#             [
#                 [f'Играть - {games["Fire Rage +"]["emoji"]} Fire Rage +', f'Играть - {games["King of Jewels"]["emoji"]} King of Jewels'],
#                 [f'Играть - {games["Gates of Avalon"]["emoji"]} Gates of Avalon', f"Играть - {games['Dolphins Shell']['emoji']} Dolphins Shell"],
#                 [f'Играть - {games["Lady Luck"]["emoji"]} Lady Luck', f'Играть - {games["Pirates Fortune"]["emoji"]} Pirates Fortune'],
#                 [f'Играть - {games["Bananas"]["emoji"]} Bananas', f'Играть - {games["Extra Super 7"]["emoji"]} Extra Super 7'],
#                 [f'Играть - {games["Box of Ra"]["emoji"]} Box of Ra', f'Играть - {games["Rise Of Imperium"]["emoji"]} Rise Of Imperium'],
#                 ['🔙 В главное меню']
#             ],
#             resize_keyboard=True,
#        )


def game_list():
    kb_list = []
    for game in games:
        kb_list.append([InlineKeyboardButton(f'{games[game]["emoji"]} {game}', callback_data=f'game-{games[game]["id"]}')])

    return InlineKeyboardMarkup(kb_list)


def play_game(tg_id, game_id):
    #balance = GameAPI.get_balance(tg_id)
    # base_url = 'https://smarted.store/api/v1/'
    base_url = 'http://127.0.0.1:8000/api/v1/'
    url = base_url+f'games/{game_id}/demo/{tg_id}/'
    # if balance['real_balance'] > 50:
    #     kb = InlineKeyboardMarkup(
    #         [
    #             #[InlineKeyboardButton('Играть на Gambling Tokens')],
    #             [InlineKeyboardButton('Играть на демо-счёт', url=url)]
    #         ]
    #     )
    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('Играть на Gambling Tokens', url=base_url+f'games/{game_id}/real/{tg_id}/')],
            [InlineKeyboardButton("Играть на демо-счёт", url=base_url+f'games/{game_id}/demo/{tg_id}/')]
        ]
    )
    return kb


# def select_type_game(game_id):
#
#     kb = InlineKeyboardMarkup(
#         [
#             [InlineKeyboardButton('Играть на Gambling Tokens', callback_data=f'play-real-{game_id}')],
#             [InlineKeyboardButton('Играть на демо-счёт', callback_data=f'play-demo-{game_id}')]
#         ]
#     )
#     return kb


balance_menu = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('📥 Купить Gambling Tokens', callback_data='balance-buy_token'),
             InlineKeyboardButton('📤 Вывести', callback_data='balance-withdrawal')],
            [InlineKeyboardButton('« Закрыть »', callback_data='close')]
        ]

    )
