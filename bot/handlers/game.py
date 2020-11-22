from pyrogram import Client, Filters
from core.services import game_dict, games, get_user
from core import keyboards as kb
from core.api import GameAPI
from core.abtest import get_text


@Client.on_message(Filters.create(lambda _, m: m.text in get_text(m.from_user.id, "kb-games")))
def games_list(cli, m):
    tg_id = m.from_user.id
    cli.send_photo(m.chat.id, photo='media/games.jpg', caption=get_text(tg_id, "select_game"), reply_markup=kb.game_list())
    user = get_user(m)
    GameAPI.send_statistic(user, 'press_button', data={"button_name": "games", "location": "main_menu"})


@Client.on_callback_query(Filters.create(lambda _, cb: cb.data.startswith('game')))
def game_cb(cli, cb):
    tg_id = cb.from_user.id
    game_id = int(cb.data.split('-')[1])
    game_title = games[game_id]
    txt = get_text(tg_id, "game_info").format(game_title=game_title)
    cli.send_photo(cb.message.chat.id, photo=str(game_dict[game_title]["image"]), caption=txt, reply_markup=kb.play_ game(cb.from_user.id, game_id))
