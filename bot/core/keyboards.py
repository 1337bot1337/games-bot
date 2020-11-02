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

onboarding = ReplyKeyboardMarkup(
    [
        ['✅  Пройти обучение']
    ],
        resize_keyboard=True,
)

tutor_1 = ReplyKeyboardMarkup(
    [
        ['⏭ Cледующий шаг']
    ],
        resize_keyboard=True,
)

tutor_2 = ReplyKeyboardMarkup(
    [
        ['✔️ Понятно, спасибо!']
    ],
        resize_keyboard=True,
)

menu = ReplyKeyboardMarkup(
            [
                ['🎰 Игры'],
                ['💰 Баланс', '❓ Помощь']
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
    base_url = GameAPI.base_url
    #base_url = 'http://127.0.0.1:8000/api/v1/'
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
            [InlineKeyboardButton('Играть', url=base_url+f'games/{game_id}/real/{tg_id}/')],
            [InlineKeyboardButton("Играть на демо-счёт", url=base_url+f'games/{game_id}/demo/{tg_id}/')]
        ]
    )
    return kb


cancel_withdrawal = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('❌ Отменить вывод', callback_data='cancel_withdrawal')]
    ]
)

cancel_deposit = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('❌ Отменить депозит', callback_data='cancel_deposit')]
    ]
)

balance_menu = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('📥 Пополнить баланс', callback_data='balance-buy_token')],
            [InlineKeyboardButton('📤 Вывести', callback_data='balance-withdrawal')]
        ]

    )


support = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('🟢 Связаться с тех. поддержкой', url='https://t.me/GamblingGameSupport')]
    ]
)


def deposit_url(tg_id, amount):
    url = GameAPI.deposit_user(tg_id, amount)
    return InlineKeyboardMarkup(
    [
        [InlineKeyboardButton('Перейти к оплате', url=url)]
    ]
)