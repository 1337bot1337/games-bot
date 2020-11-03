from pyrogram import Client, Filters
from core.services import game_dict, games
from core import keyboards as kb
from core.api import GameAPI
from core import texts


@Client.on_message(Filters.regex(r'^🎰 Игры$'))
def games_list(cli, m):
    cli.send_photo(m.chat.id, photo='media/games.jpg', caption=texts.select_game, reply_markup=kb.game_list())
    GameAPI.send_statistic(m.from_user.id, 'press_button', data={"button_name": "games", "location": "main_menu"})


@Client.on_callback_query(Filters.create(lambda _, cb: cb.data.startswith('game')))
def game_cb(cli, cb):
    game_id = int(cb.data.split('-')[1])
    game_title = games[game_id]
    txt = f'**{game_title}**\n\nИграйте на рубли или попробуйте демо-режим!'
    cli.send_photo(cb.message.chat.id, photo=str(game_dict[game_title]["image"]), caption=txt, reply_markup=kb.play_game(cb.from_user.id, game_id))
