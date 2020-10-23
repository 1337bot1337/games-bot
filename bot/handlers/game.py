from pyrogram import Client, Filters
from core.services import game_dict, games
from core import keyboards as kb
from core.api import GameAPI
import re
import urllib


@Client.on_message(Filters.regex(r'^🎰 Игры$'))
def games_list(cli, m):
    cli.send_photo(m.chat.id, photo='media/games.jpg', caption='Нажимай на понравившеюся игру', reply_markup=kb.games)


@Client.on_message(Filters.regex(r'^Играть\s-\s'))
def get_game(cli, m):

    response = re.search(r'Играть\s-\s..?\s(?P<game_title>.*)', m.text)

    game_title = response.group('game_title')

    game_id = game_dict[game_title]['id']

    txt = f'**{game_title}**\n\nИграйте на GamblingTokens или попробуйте демо-режим!'
    cli.send_photo(m.chat.id, photo=f'{game_dict[game_title]["image"]}', caption=txt, reply_markup=kb.select_type_game(game_id))


@Client.on_callback_query(Filters.create(lambda _, cb: cb.data.startswith('play')))
def select_type_game(cli, cb):
    tg_id = cb.from_user.id
    data = cb.data.split('-')
    type_game = data[1]
    game_id = int(data[2])
    game_title = games[game_id]
    game = GameAPI.get_game_url(game_id, type_game, tg_id)
    if type_game == 'real':
        if game:
            if game['url']:
                game_url = urllib.parse.quote(game['url'], safe='https://chcplay.net?p=')
                return cb.message.edit('✅ Ваша игра готова!', reply_markup=kb.play_game(game_title, game_url))

            if game['err_code'] == 1:  # Нет денег на счёту
                cli.answer_callback_query(cb.id, 'У вас недостаточно Gamblings Token для игры. Пополните баланс',
                                          show_alert=True)
                return cb.message.reply('TODO:: ссылка на пополнение')

            if game['err_code'] == 2:  # Не закрыта сессия
                cli.answer_callback_query(cb.id,
                                          'Предыдущая сессия игры не завершена. Завершите предыдущую игру и попробуйте снова.',
                                          show_alert=True)
        else:
            cli.answer_callback_query(cb.id, 'Что-то пошло не так')

    if type_game == 'demo':

        if game:
            if game['url']:
                game_url = urllib.parse.quote(game['url'], safe='https://chcplay.net?p=')
                return cb.message.edit('✅ Ваша игра готова!', reply_markup=kb.play_game(game_title, game_url))

            if game['err_code'] == 2:  # Не закрыта сессия
                cli.answer_callback_query(cb.id,
                                          'Предыдущая сессия игры не завершена. Завершите предыдущую игру и попробуйте снова.',
                                          show_alert=True)