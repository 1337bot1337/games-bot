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
        source = 'none'
        if len(m.command) > 1:
            source = m.command[1]

        GameAPI.registration_user(tg_id=m.from_user.id, source=source)
        m.reply(texts.onboarding, reply_markup=kb.onboarding)


# @Client.on_message(Filters.regex(r'^🇬🇧 English$|^🇷🇺 Русский$'))
# def select_lang(cli, m):
#     user_lang = 'en' if m.text == '🇬🇧 English' else 'ru'
#     GameAPI.registration_user(tg_id=m.from_user.id, source='none')
#     m.reply(texts.license_terms, reply_markup=kb.accept_license_terms)


# @Client.on_message(Filters.regex(r'^✅ Принимаю условия$'))
# def accept_license_terms(cli, m):
#     GameAPI.registration_user(tg_id=m.from_user.id, source='none')
#     cli.send_photo(m.chat.id, caption=texts.home_text, photo='media/hello.jpg', reply_markup=kb.menu)


@Client.on_message(Filters.regex(r'^👩‍🎓 Пройти обучение$'))
def accept_license_terms(cli, m):
    cli.send_photo(m.chat.id, caption=texts.tutor_1, photo='media/tutor_1.jpg', reply_markup=kb.tutor_1)


@Client.on_message(Filters.regex(r'^👉 Следующий шаг$'))
def tutor1_kb(cli, m):
    m.reply(texts.tutor_2)
    m.reply(texts.tutor_3, reply_markup=kb.tutor_2)


@Client.on_message(Filters.regex(r'^Понятно, спасибо!$'))
def tutor2_kb(cli, m):
    m.reply(texts.finish_tutor)
    cli.send_photo(m.chat.id, caption=texts.home_text, photo='media/hello.jpg', reply_markup=kb.menu)
    GameAPI.send_statistic(m.from_user.id, 'finish_tutorial', data={})


@Client.on_message(Filters.regex(r'^🔙 В главное меню$'))
def main_menu(cli, m):
    cli.send_photo(m.chat.id, caption=texts.home_text, photo='media/hello.jpg', reply_markup=kb.menu)


@Client.on_callback_query(Filters.callback_data('close'))
def close_bot_window(cli, cb):
    try:
        cb.message.delete()
    except:
        pass


# @Client.on_message(Filters.regex(r'^🤝 Партнёрская программа$'))
# def affiliate_kb(cli, m):


@Client.on_message(Filters.regex(r'^❓ Помощь$'))
def help_kb(cli, m):
    m.reply('Для того, чтобы связаться с технической поддержкой нажмите кнопку под этим сообщением', reply_markup=kb.support)
    GameAPI.send_statistic(m.from_user.id, 'press_button', data={"button_name": "help", "location": "main_menu"})