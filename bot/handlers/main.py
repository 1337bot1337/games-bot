from pyrogram import Client, Filters

from core.api import GameAPI
from core import keyboards as kb
from core.abtest import get_text, get_source_welcome_bonus, get_onboarding, check_source
from core.services import get_user, get_referrer_name, get_referral_bonus, ref_source_none


@Client.on_message(~Filters.bot & Filters.command('start'))
def start(cli, m):
    tg_id = m.from_user.id

    # Делает проверку зарегестрирован ли юзер
    response = GameAPI.check_user(tg_id)
    if response.status_code == 200:
        return cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg', reply_markup=kb.menu(tg_id))

    if response.status_code == 404:
        source = "none"
        if len(m.command) > 1:
            if m.command[1][:3] == "ref":
                referrer_id = int(m.command[1][3:])
                referrer_name = get_referrer_name(referrer_id)

                if referrer_name:
                    GameAPI.registration_user(tg_user=m.from_user, source=source, referrer_id=referrer_id)

                    bonus_amount = get_referral_bonus()
                    text = get_text(tg_id, "onboarding-step_0-ref").format(referer_name=referrer_name,
                                                                           amount=bonus_amount)
                    return m.reply(text, reply_markup=kb.onboarding(tg_id))
            else:
                if check_source(m.command[1]):
                    source = m.command[1]
                    GameAPI.registration_user(tg_user=m.from_user, source=source)
                    start_bonus = get_source_welcome_bonus(tg_id)
                    text = get_text(tg_id, "onboarding-step_0-source").format(amount=start_bonus)
                    return m.reply(text, reply_markup=kb.onboarding(tg_id))

        GameAPI.registration_user(tg_user=m.from_user, source=source)
        text = get_text(tg_id, "onboarding-step_0-none")
        m.reply(text, reply_markup=kb.onboarding(tg_id))


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-onboarding_0")))
def tutor1_kb(cli, m):
    tg_id = m.from_user.id
    onboarding = get_onboarding(tg_id)
    if onboarding:
        cli.send_photo(m.chat.id, caption=get_text(tg_id, "onboarding-step_1"), photo='media/tutor_1.jpg', reply_markup=kb.tutor_1(tg_id))
    else:
        cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg',
                       reply_markup=kb.menu(tg_id))


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-onboarding_1")))
def tutor2_kb(cli, m):
    tg_id = m.from_user.id
    m.reply(get_text(tg_id, "onboarding-step_2"), reply_markup=kb.tutor_2(tg_id))


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-onboarding_2")))
def tutor3_kb(cli, m):
    tg_id = m.from_user.id
    m.reply(get_text(tg_id, "onboarding-step_3"), reply_markup=kb.tutor_3(tg_id))


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-onboarding_final")))
def tutor4_kb(cli, m):
    tg_id = m.from_user.id
    bonus_amount = get_source_welcome_bonus(tg_id)

    user = get_user(m)
    ref, source, none = ref_source_none(tg_id)

    if ref:
        m.reply(get_text(tg_id, "onboarding-finish-ref"))
    if source:
        m.reply(get_text(tg_id, "onboarding-finish-source").format(bonus=float(bonus_amount)))

    if none:
        m.reply(get_text(tg_id, "onboarding-finish-none"))

    cli.send_photo(m.chat.id, caption=get_text(tg_id, "home_text"), photo='media/hello.jpg',
                   reply_markup=kb.menu(tg_id))
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


@Client.on_message(~Filters.bot & Filters.create(lambda _, m: m.text == get_text(m.from_user.id, "kb-help")))
def help_kb(cli, m):
    tg_id = m.from_user.id
    m.reply(get_text(tg_id, "contact_support"), reply_markup=kb.support(tg_id))
    user = get_user(m)
    GameAPI.send_statistic(user, 'press_button', data={"button_name": "help", "location": "main_menu"})