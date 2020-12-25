from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .services import game_dict as games
from .api import GameAPI
from core.abtest import get_text
import urllib


# select_language = ReplyKeyboardMarkup(
#     [
#         ['🇬🇧 English'],
#         ['🇷🇺 Русский']
#     ],
#     resize_keyboard=True,
# )
#
# accept_license_terms = ReplyKeyboardMarkup(
#     [
#         ['✅ Принимаю условия']
#     ],
#     resize_keyboard=True,
# )


def onboarding(tg_id: int):
    kb = ReplyKeyboardMarkup(

        [
            [get_text(tg_id, "kb-onboarding_0")]
        ],
        resize_keyboard=True,
    )
    return kb


def tutor_1(tg_id: int):
    kb = ReplyKeyboardMarkup(
        [
            [get_text(tg_id, "kb-onboarding_1")]
        ],
        resize_keyboard=True,
    )
    return kb


def tutor_2(tg_id: int):
    kb = ReplyKeyboardMarkup(
        [
            [get_text(tg_id, "kb-onboarding_2")]
        ],
        resize_keyboard=True,
    )
    return kb


def tutor_3(tg_id: int):
    kb = ReplyKeyboardMarkup(
        [
            [get_text(tg_id, "kb-onboarding_final")]
        ],
        resize_keyboard=True,
    )
    return kb


def menu(tg_id: int):
    kb = ReplyKeyboardMarkup(
        [
            [get_text(tg_id, "kb-games")],
            [get_text(tg_id, "kb-balance"), get_text(tg_id, "kb-help")],
            [get_text(tg_id, "kb-affiliate")]
        ],
        resize_keyboard=True,
    )
    return kb


def game_list():
    kb_list = []
    for game in games:
        kb_list.append(
            [InlineKeyboardButton(f'{games[game]["emoji"]} {game}', callback_data=f'game-{games[game]["id"]}')])

    return InlineKeyboardMarkup(kb_list)


def play_game(tg_id: int, game_id: int):
    base_url = GameAPI.base_url
    #base_url = 'http://127.0.0.1:8000/api/v1/'

    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(get_text(tg_id, "kb-game-start_on_real"), url=base_url + f'games/{game_id}/real/{tg_id}/')]
            # [InlineKeyboardButton(get_text(tg_id, "kb-game-start_on_demo"),
            #                       url=base_url + f'games/{game_id}/demo/{tg_id}/')]
        ]
    )
    return kb


def cancel_withdrawal(tg_id: int):
    kb = ReplyKeyboardMarkup(
        [
            [get_text(tg_id, "kb-balance-cancel_withdrawal")]
        ], resize_keyboard=True
    )
    return kb


def cancel_deposit(tg_id: int):
    kb = ReplyKeyboardMarkup(
    [
        [get_text(tg_id, "kb-balance-cancel_deposit")]
    ], resize_keyboard=True
)
    return kb


def balance_menu(tg_id: int):
    kb = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(get_text(tg_id, "kb-balance-deposit"), callback_data='balance-buy_token')],
        [InlineKeyboardButton(get_text(tg_id, "kb-balance-withdrawal"), callback_data='balance-withdrawal')]
    ]

)
    return kb


def support(tg_id: int):
    kb = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(get_text(tg_id, "kb-contact_support"), url='https://t.me/GamblingGameSupport')]
    ]
)
    return kb


def deposit_url(tg_id: int, amount):
    url = GameAPI.deposit_user(tg_id, amount)
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(get_text(tg_id, "kb-balance-go_to_deposit"), url=url)]
        ]
    )
