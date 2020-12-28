from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from core.services import game_dict
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


def game_list(games, offset):
    kb_list = []
    if offset == 0:
        kb_list = [
            [InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search"),
             InlineKeyboardButton(f'⏩', callback_data="game-move-10")]
        ]
    elif offset == 10:
        kb_list = [
            [InlineKeyboardButton(f'⏪', callback_data="game-move-0"),
             InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search"),
             InlineKeyboardButton(f'⏩', callback_data="game-move-20")]
        ]
    elif offset == 20:
        kb_list = [
            [InlineKeyboardButton(f'⏪', callback_data="game-move-10"),
             InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search"),
             InlineKeyboardButton(f'⏩', callback_data="game-move-30")]
        ]
    elif offset == 30:
        kb_list = [
            [InlineKeyboardButton(f'⏪', callback_data="game-move-20"),
             InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search"),
             InlineKeyboardButton(f'⏩', callback_data="game-move-40")]
        ]
    elif offset == 40:
        kb_list = [
            [InlineKeyboardButton(f'⏪', callback_data="game-move-30"),
             InlineKeyboardButton(f'🔍 Поиск', callback_data="game-search")]
        ]

    for game_id in games:
        game_title = games[game_id]
        emoji = game_dict[game_title]["emoji"]

        kb_list.append(
            [InlineKeyboardButton(f'{emoji} {game_title}', callback_data=f'game-{game_id}')])

    return InlineKeyboardMarkup(kb_list)


try_search = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Попробовать ещё", callback_data="try_search")]
    ]
)


def result_game(games):
    kb = [[InlineKeyboardButton("Попробовать ещё", callback_data="try_search")]]

    for game in games:
        kb.append(
            [InlineKeyboardButton(game["name"], callback_data=f"game-{game['id']}")]
        )

    return InlineKeyboardMarkup(kb)


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
