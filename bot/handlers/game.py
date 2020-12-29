from pyrogram import Client, Filters
from core.services import game_dict, games, get_user, games_1, games_2, games_3, games_4, games_5, SearchGameClient, search_game
from core import keyboards as kb
from core.api import GameAPI
from core.abtest import get_text
from config import cache


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-games")))
def games_list(cli, m):
    tg_id = m.from_user.id
    cli.send_photo(m.chat.id, photo='media/games.jpg', caption=get_text(tg_id, "select_game"), reply_markup=kb.game_list(games_1, 0))
    user = get_user(m)
    GameAPI.send_statistic(user, 'press_button', data={"button_name": "games", "location": "main_menu"})


@Client.on_callback_query(Filters.create(lambda _, cb: cb.data.startswith('game')))
def game_cb(cli, cb):
    tg_id = cb.from_user.id
    offs = {0: games_1,
            10: games_2,
            20: games_3,
            30: games_4,
            40: games_5}

    if cb.data.split('-')[1] == "move":
        offset = int(cb.data.split('-')[2])
        cb.edit_message_reply_markup(reply_markup=kb.game_list(offs[offset], offset))
        return

    if cb.data.split('-')[1] == "search":
        cb.message.reply(get_text(tg_id, "enter_search_game"))
        cache.change_user_cache(tg_id, "await_game_search", True)
        return

    game_id = int(cb.data.split('-')[1])
    game_title = games[game_id]
    txt = get_text(tg_id, "game_info").format(game_title=game_title)
    cli.send_photo(cb.message.chat.id, photo=str(game_dict[game_title]["image"]), caption=txt, reply_markup=kb.play_game(cb.from_user.id, game_id))


@Client.on_callback_query(Filters.callback_data("try_search"))
def research_game(cli, cb):
    tg_id = cb.from_user.id
    cache.change_user_cache(tg_id, "await_game_search", True)
    cb.message.reply(get_text(tg_id, "enter_search_game"))
    cb.message.edit(cb.message.text)


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: cache.get_user_cache(m.from_user.id)["await_game_search"]))
def game_search(cli, m):
    tg_id = m.from_user.id
    game_search = m.text
    if len(m.text) < 4:
        cache.change_user_cache(tg_id, "await_game_search", False)
        m.reply(get_text(tg_id, "enter_search_game"))
        return

    games = search_game(game_search)
    cache.change_user_cache(tg_id, "await_game_search", False)
    if len(games) == 0:
        m.reply(get_text(tg_id, "search_game-result-0"), reply_markup=kb.try_search)
        return

    m.reply(get_text(tg_id, "search_game-result"), reply_markup=kb.result_game(games))

