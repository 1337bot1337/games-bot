from pyrogram import Client, Filters

from core.api import GameAPI
from core import keyboards as kb
from core import texts


@Client.on_message(Filters.command('start'))
def start(cli, m):
    tg_id = m.from_user.id

    # Делает проверку зарегестрирован ли юзер
    response = GameAPI.check_user(tg_id)
    if response.status_code == 200:
        return cli.send_photo(m.chat.id, caption=texts.home_text, photo='media/hello.jpg', reply_markup=kb.menu)

    if response.status_code == 404:
        m.reply(texts.license_terms, reply_markup=kb.accept_license_terms)
        #m.reply(texts.select_language, reply_markup=kb.select_language)


# @Client.on_message(Filters.regex(r'^🇬🇧 English$|^🇷🇺 Русский$'))
# def select_lang(cli, m):
#     user_lang = 'en' if m.text == '🇬🇧 English' else 'ru'
#     GameAPI.registration_user(tg_id=m.from_user.id, source='none')
#     m.reply(texts.license_terms, reply_markup=kb.accept_license_terms)


@Client.on_message(Filters.regex(r'^✅ Принимаю условия$'))
def accept_license_terms(cli, m):
    cli.send_photo(m.chat.id, caption=texts.home_text, photo='media/hello.jpg', reply_markup=kb.menu)


@Client.on_message(Filters.regex(r'^🔙 В главное меню$'))
def main_menu(cli, m):
    cli.send_photo(m.chat.id, caption=texts.home_text, photo='media/hello.jpg', reply_markup=kb.menu)