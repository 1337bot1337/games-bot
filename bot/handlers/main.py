from pyrogram import Client, Filters

from core.api import GameAPI
from core import keyboards as kb
from core.abtest import get_text, get_welcome_bonus, get_onboarding
from core.services import get_user


@Client.on_message(Filters.command('start'))
def start(cli, m):
    tg_id = m.from_user.id

    # Делает проверку зарегестрирован ли юзер
    response = GameAPI.check_user(tg_id)
    if response.status_code == 200:
        return cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg', reply_markup=kb.menu(tg_id))

    if response.status_code == 404:
        source = 'none'
        if len(m.command) > 1:
            source = m.command[1]

        GameAPI.registration_user(tg_user=m.from_user, source=source)

        m.reply(get_text(tg_id, 'onboarding-step_0'), reply_markup=kb.onboarding(tg_id))


@Client.on_message(Filters.create(lambda _, m: m.text in get_text(m.from_user.id, "kb-onboarding_0")))
def tutor1_kb(cli, m):
    tg_id = m.from_user.id
    onboarding = get_onboarding(tg_id)
    if onboarding:
        cli.send_photo(m.chat.id, caption=get_text(tg_id, "onboarding-step_1"), photo='media/tutor_1.jpg', reply_markup=kb.tutor_1(tg_id))
    else:
        cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg',
                       reply_markup=kb.menu(tg_id))


@Client.on_message(Filters.create(lambda _, m: m.text in get_text(m.from_user.id, "kb-onboarding_1")))
def tutor2_kb(cli, m):
    tg_id = m.from_user.id
    m.reply(get_text(tg_id, "onboarding-step_2"), reply_markup=kb.tutor_2(tg_id))


@Client.on_message(Filters.create(lambda _, m: m.text in get_text(m.from_user.id, "kb-onboarding_2")))
def tutor3_kb(cli, m):
    tg_id = m.from_user.id
    m.reply(get_text(tg_id, "onboarding-step_3"), reply_markup=kb.tutor_3(tg_id))


@Client.on_message(Filters.create(lambda _, m: m.text in get_text(m.from_user.id, "kb-onboarding_final")))
def tutor4_kb(cli, m):
    tg_id = m.from_user.id
    bonus_amount = get_welcome_bonus(tg_id)
    m.reply(get_text(tg_id, "onboarding-finish").format(bonus_amount=float(bonus_amount)))
    cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg', reply_markup=kb.menu(tg_id))

    user = get_user(m)
    GameAPI.send_statistic(user, 'finish_tutorial', data={})


# @Client.on_message(Filters.regex(r'^🔙 В главное меню$'))
# def main_menu(cli, m):
#     cli.send_photo(m.chat.id, caption=texts.home_text, photo='media/hello.jpg', reply_markup=kb.menu)


@Client.on_callback_query(Filters.callback_data('close'))
def close_bot_window(cli, cb):
    try:
        cb.message.delete()
    except:
        pass


@Client.on_message(Filters.create(lambda _, m: m.text in get_text(m.from_user.id, "kb-help")))
def help_kb(cli, m):
    tg_id = m.from_user.id
    m.reply(get_text(tg_id, "contact_support"), reply_markup=kb.support(tg_id))
    user = get_user(m)
    GameAPI.send_statistic(user, 'press_button', data={"button_name": "help", "location": "main_menu"})