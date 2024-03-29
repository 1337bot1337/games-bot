from django.core.cache import cache
from core.apps.abtest import models as abtest_models


def get_text(tg_id, text_name: str):
    texts = cache.get("texts")
    source = get_user_source(tg_id)
    bot_profile = get_bot_profile(source)

    return texts[(text_name, bot_profile["version_text"])]["text_ru"]


def get_user_source(tg_id):
    users = cache.get("users")
    return users[tg_id]["source"]


def get_source_setup(source: str):
    source_setup = cache.get("sources")
    setup = source_setup.get(source, source_setup["none"])
    return setup


def get_bot_profile(source: str):

    scr_setup = get_source_setup(source)
    bot_profile = cache.get("botprofiles")
    return bot_profile[scr_setup["profile_id"]]


def get_sources_from_botprofile(bot_profile: "abtest_models.BotProfile"):
    sources = abtest_models.SourceSetup.objects.filter(profile=bot_profile)
    if sources.exists():
        return [source.name for source in sources]

    return []


texts = [
    {'name': 'affiliate-invite_friend',
     'text': "Привет друг нашего друга! Приглашаем тебя в казино!\n\nЖми на кнопку и получай бонус {bonus}% за первый депозит",
     'text_ru': "Привет друг нашего друга! Приглашаем тебя в казино!\n\nЖми на кнопку и получай бонус {bonus}% за первый депозит",
     'text_en': '',
     'version': 'a'},
    {'name': 'affiliate-invite_friend',
     'text': "Привет друг нашего друга! Приглашаем тебя в казино!\n\nЖми на кнопку и получай бонус {bonus}% за первый депозит",
     'text_ru': "Привет друг нашего друга! Приглашаем тебя в казино!\n\nЖми на кнопку и получай бонус {bonus}% за первый депозит",
     'text_en': '',
     'version': 'b'},
    {'name': 'balance-conditions',
     'text': 'Минимальная сумма для зачисления на счет - {min_deposit}\n'
             'Минимальная сумма для вывода - {min_withdrawal}\n'
             'Для вывода средств, нужно отыграть желаемую сумму с коэффициентом {wager}',
     'text_ru':'Минимальная сумма для зачисления на счет - {min_deposit}\n'
             'Минимальная сумма для вывода - {min_withdrawal}\n'
             'Для вывода средств, нужно отыграть желаемую сумму с коэффициентом {wager}',
     'text_en': '',
     'version': 'a'},
    {'name': 'balance-conditions',
     'text': 'Минимальная сумма для зачисления на счет - {min_deposit}\n'
             'Минимальная сумма для вывода - {min_withdrawal}\n'
             'Для вывода средств, нужно отыграть желаемую сумму с коэффициентом {wager}',
     'text_ru': 'Минимальная сумма для зачисления на счет - {min_deposit}\n'
             'Минимальная сумма для вывода - {min_withdrawal}\n'
             'Для вывода средств, нужно отыграть желаемую сумму с коэффициентом {wager}',
     'text_en': '',
     'version': 'b'},
    {'name': 'enter_search_game',
     'text': 'Для поискал игры нужно ввести хотя бы 4 буквы из названия игры',
     'text_ru': 'Для поискал игры нужно ввести хотя бы 4 буквы из названия игры',
     'text_en': '',
     'version': 'a'},
    {'name': 'enter_search_game',
     'text': 'Для поискал игры нужно ввести хотя бы 4 буквы из названия игры',
     'text_ru': 'Для поискал игры нужно ввести хотя бы 4 буквы из названия игры',
     'text_en': '',
     'version': 'b'},
    {'name': 'search_game-result-0',
     'text': 'По вашему запросу ничего не найдено.',
     'text_ru': 'По вашему запросу ничего не найдено.',
     'text_en': '',
     'version': 'a'},
    {'name': 'search_game-result-0',
     'text': 'По твоему запросу ничего не найдено.',
     'text_ru': 'По твоему запросу ничего не найдено.',
     'text_en': '',
     'version': 'b'},
    {'name': 'search_game-result',
     'text': 'По вашему запросу найдены следующие игры.',
     'text_ru': 'По вашему запросу найдены следующие игры.',
     'text_en': '',
     'version': 'a'},
    {'name': 'search_game-result',
     'text': 'По твоему запросу найдены следующие игры.',
     'text_ru': 'По твоему запросу найдены следующие игры.',
     'text_en': '',
     'version': 'b'},
    {'name': 'affiliate-menu',
     'text': 'Количество приглашенных пользователей: {ref_count}.\n\nЕсли ваш друг сделает депозит >{min_referral_deposit} р, вы получите {bonus} bonus leo,\n\nДелитесь этой ссылкой с друзьями, чтобы получать бонусы:\n{link}',
     'text_ru': 'Количество приглашенных пользователей: {ref_count}.\n\nЕсли ваш друг сделает депозит >{min_referral_deposit} р, вы получите {bonus} bonus leo,\n\nДелитесь этой ссылкой с друзьями, чтобы получать бонусы:\n{link}',
     'text_en': '',
     'version': 'a'},
    {'name': 'affiliate-menu',
     'text': 'Количество приглашенных пользователей: {ref_count}.\n\nЕсли твой друг сделает депозит >{min_referral_deposit} р, ты получишь {bonus} bonus leo,\n\nДелись этой ссылкой с друзьями, чтобы получать бонусы:\n{link}',
     'text_ru': 'Количество приглашенных пользователей: {ref_count}.\n\nЕсли твой друг сделает депозит >{min_referral_deposit} р, ты получишь {bonus} bonus leo,\n\nДелись этой ссылкой с друзьями, чтобы получать бонусы:\n{link}',
     'text_en': '',
     'version': 'b'},

    {'name': 'replenish_balance',
     'text': '💸 Ваш баланс пополнен на {amount} руб.\n\n{bonus_text}',
     'text_ru': '💸 Ваш баланс пополнен на {amount} руб.\n\n{bonus_text}',
     'text_en': '',
     'version': 'a'},
    {'name': 'replenish_balance',
     'text': '💸 Твой баланс пополнен на {amount} руб.\n\n{bonus_text}',
     'text_ru': '💸 Твой баланс пополнен на {amount} руб.\n\n{bonus_text}',
     'text_en': '',
     'version': 'b'},
    {'name': 'replenish_balance-bonus',
     'text': '🎁 Поздравляем! Ваш бонус за первое пополнение составляет {bonus} Bonus Leo!',
     'text_ru': '🎁 Поздравляем! Ваш бонус за первое пополнение составляет {bonus} Bonus Leo!',
     'text_en': '',
     'version': 'a'},
    {'name': 'replenish_balance-bonus',
     'text': '🎁 Поздравляем! Бонус за первое пополнение - {bonus} Bonus Leo!',
     'text_ru': '🎁 Поздравляем! Бонус за первое пополнение - {bonus} Bonus Leo!',
     'text_en': '',
     'version': 'b'},
    {'name': 'replenish_balance-bonus-source',
     'text': '🎁 Поздравляем! Ваш бонус за пополнение составляет {bonus} Bonus Leo!',
     'text_ru': '🎁 Поздравляем! Ваш бонус за пополнение составляет {bonus} Bonus Leo!',
     'text_en': '',
     'version': 'a'},
    {'name': 'replenish_balance-bonus-source',
     'text': '🎁 Поздравляем! Бонус за пополнение - {bonus} Bonus Leo!',
     'text_ru': '🎁 Поздравляем! Бонус за пополнение - {bonus} Bonus Leo!',
     'text_en': '',
     'version': 'b'},
    {'name': 'affiliate-bonus_for_referrer_from_deposit_referral',
     'text': '🎁 Приглашенный Вами пользователь пополнил свой баланс!\n\n'
             'Ваша награда - **{bonus}** Bonus Leo.\n\n'
             'Делитесь ссылкой и получайте больше наград!',
     'text_ru': '🎁 Приглашенный Вами пользователь пополнил свой баланс!\n\n'
             'Ваша награда - **{bonus}** Bonus Leo.\n\n'
             'Делитесь ссылкой и получайте больше наград!',
     'text_en': '',
     'version': 'a'},
    {'name': 'affiliate-bonus_for_referrer_from_deposit_referral',
     'text': '🎁 Один из приглашенных пользователей пополнил свой баланс.\n\n'
             'Твоя часть - **{bonus}** Bonus Leo. \n\n'
             'Делись ссылкой и получай больше наград!',
     'text_ru': '🎁 Один из приглашенных пользователей пополнил свой баланс.\n\n'
             'Твоя часть - **{bonus}** Bonus Leo. \n\n'
             'Делись ссылкой и получай больше наград!',
     'text_en': '',
     'version': 'b'},
    {'name': 'affiliate-new_referral',
     'text': 'По Вашему приглашению зарегистрировался {friend_name}!\n\n'
             'Теперь за каждое пополнение от этого пользователя свыше {min_referral_deposit} руб. Вы будете получать Bonus Leo.',
     'text_ru': 'По Вашему приглашению зарегистрировался {friend_name}!\n\n'
             'Теперь за каждое пополнение от этого пользователя свыше {min_referral_deposit} руб. Вы будете получать Bonus Leo.',
     'text_en': '',
     'version': 'a'},
    {'name': 'affiliate-new_referral',
     'text': '***{friend_name}*** зарегистрировался по твоему приглашению!\n\n'
             'Теперь за каждое пополнение от этого пользователя свыше {min_referral_deposit} руб. ты получишь Bonus Leo.',
     'text_ru': '***{friend_name}*** зарегистрировался по твоему приглашению!\n\n'
             'Теперь за каждое пополнение от этого пользователя свыше {min_referral_deposit} руб. ты получишь Bonus Leo.',
     'text_en': '',
     'version': 'b'},
    {'name': 'withdrawal-accepted_withdraw_request',
     'text': 'Ваша заявка на вывод {amount} руб. на карту {card} была одобрена.',
     'text_ru': 'Ваша заявка на вывод {amount} руб. на карту {card} была одобрена.',
     'text_en': '',
     'version': 'a'},
    {'name': 'withdrawal-accepted_withdraw_request',
     'text': 'Твоя заявка на вывод {amount} руб. на карту {card} была одобрена.',
     'text_ru': 'Твоя заявка на вывод {amount} руб. на карту {card} была одобрена.',
     'text_en': '',
     'version': 'b'},
    {'name': 'withdrawal-rejected_withdraw_request',
     'text': 'Ваша заявка на вывод {amount} руб. на карту {card} была отклонена.',
     'text_ru': 'Ваша заявка на вывод {amount} руб. на карту {card} была отклонена.',
     'text_en': '',
    'version': 'a'},
    {'name': 'withdrawal-rejected_withdraw_request',
     'text': 'Твоя заявка на вывод {amount} руб.на карту {card} была отклонена.',
     'text_ru': 'Твоя заявка на вывод {amount} руб.на карту {card} была отклонена.',
     'text_en': '',
     'version': 'b'},

    {'name': 'withdrawal-max_limit',
     'text': 'Ты не можешь вывести более, чем {max_amount} руб.',
     'text_ru': 'Ты не можешь вывести более, чем {max_amount} руб.',
     'text_en': '',
     'version': 'b'},
    {'name': 'balance_menu-with_withdraw_in_progress_amount',
     'text': '💼 Баланс:\r\n\r\n💰 {real_balance} руб.\r\n🔅 **Bonus Leo**: {bonus_balance}\r\n\r\n🔱 Доступно к выводу: {max_withdrawal} руб.\r\n\r\n📤 **В обработке запрос на вывод**: {withdraw_in_progress_amount} руб.',
     'text_ru': '💼 Баланс:\r\n\r\n💰 {real_balance} руб.\r\n🔅 **Bonus Leo**: {bonus_balance}\r\n\r\n🔱 Доступно к выводу: {max_withdrawal} руб.\r\n\r\n📤 **В обработке запрос на вывод**: {withdraw_in_progress_amount} руб.',
     'text_en': '',
     'version': 'b'},
    {'name': 'onboarding-step_2',
     'text': '📖 **2/3**\r\n\r\nОсновной валютой всех игр является **Leo**.\r\n1 Leo = 10 руб. Конвертация происходит автоматически.\r\n\r\nПополнить баланс можно в меню "💰 Баланс".',
     'text_ru': '📖 **2/3**\r\n\r\nОсновной валютой всех игр является **Leo**.\r\n1 Leo = 10 руб. Конвертация происходит автоматически.\r\n\r\nПополнить баланс можно в меню "💰 Баланс".',
     'text_en': '',
     'version': 'a'},
    {'name': 'onboarding-step_3',
     'text': '📖 **3/3**\r\n\r\nЕще одна валюта - это 🔅 **Bonus Leo**. (Вы получите немного сразу после этого обучения 😉)\r\nТак же, их можно заработать при каждом пополнении баланса.',
     'text_ru': '📖 **3/3**\r\n\r\nЕще одна валюта - это 🔅 **Bonus Leo**. (Вы получите немного сразу после этого обучения 😉)\r\nТак же, их можно заработать при каждом пополнении баланса.',
     'text_en': '',
     'version': 'a'},
    {'name': 'onboarding-step_0-ref',
     'text': '🖐 Приветствую! Здесь можно играть в самые разные симуляторы игровых автоматов!\r\n\r\n🤝 Вы пришли по приглашению {referer_name}\r\n\r\n🎁  После завершения небольшого обучения, на Ваш счёт будет зачислено {amount} 🔅 **Bonus Leo**.',
     'text_ru': '🖐 Приветствую! Здесь можно играть в самые разные симуляторы игровых автоматов!\r\n\r\n🤝 Вы пришли по приглашению {referer_name}\r\n\r\n🎁  После завершения небольшого обучения, на Ваш счёт будет зачислено {amount} 🔅 **Bonus Leo**.',
     'text_en': '',
     'version': 'a'},
    {'name': 'onboarding-step_0-ref',
     'text': '🖐 Добро пожаловать! Жми Start, чтобы играть в симуляторы игровых автоматов!\r\n\r\n🤝 Тебя пригласил {referer_name}\r\n\r\n🎁 На игровом счету тебя ждет {amount} 🔅 **Bonus Leo**!',
     'text_ru': '🖐 Добро пожаловать! Жми Start, чтобы играть в симуляторы игровых автоматов!\r\n\r\n🤝 Тебя пригласил {referer_name}\r\n\r\n🎁 На игровом счету тебя ждет {amount} 🔅 **Bonus Leo**!',
     'text_en': '',
     'version': 'b'},
    {'name': 'onboarding-step_0-source',
     'text': '🖐 Приветствую! Здесь можно играть в самые разные симуляторы игровых автоматов!\r\n\r\n🎁  После завершения небольшого обучения, на Ваш счёт будет зачислено {amount} 🔅 **Bonus Leo**.',
     'text_ru': '🖐 Приветствую! Здесь можно играть в самые разные симуляторы игровых автоматов!\r\n\r\n🎁  После завершения небольшого обучения, на Ваш счёт будет зачислено {amount} 🔅 **Bonus Leo**.',
     'text_en': '',
     'version': 'a'},
    {'name': 'onboarding-step_0-source',
     'text': '🖐 Добро пожаловать! Жми Start, чтобы играть в симуляторы игровых автоматов!\r\n\r\n🎁 На игровом счету тебя ждет {amount} 🔅 **Bonus Leo**!',
     'text_ru': '🖐 Добро пожаловать! Жми Start, чтобы играть в симуляторы игровых автоматов!\r\n\r\n🎁 На игровом счету тебя ждет {amount} 🔅 **Bonus Leo**!',
     'text_en': '',
     'version': 'b'},
    {'name': 'onboarding-step_0-none',
     'text': '🖐 Приветствую! Здесь можно играть в самые разные симуляторы игровых автоматов!\r\n\r\n🎁  После завершения небольшого обучения, Вы сможете погрузиться в мир игровых автоматов.',
     'text_ru': '🖐 Приветствую! Здесь можно играть в самые разные симуляторы игровых автоматов!\r\n\r\n🎁  После завершения небольшого обучения, Вы сможете погрузиться в мир игровых автоматов.',
     'text_en': '',
     'version': 'a'},
    {'name': 'onboarding-step_0-none',
     'text': '🖐 Добро пожаловать! Жми Start, чтобы играть в симуляторы игровых автоматов!\r\n\r\n',
     'text_ru': '🖐 Добро пожаловать! Жми Start, чтобы играть в симуляторы игровых автоматов!\r\n\r\n',
     'text_en': '',
     'version': 'b'},
    {'name': 'onboarding-step_1',
     'text': '📖 **1/3**\n\n☝️ Используйте кнопки меню, чтобы общаться со мной.\n\nЕсли меню скрыто, нажмите кнопку, которая указана на картинке, чтобы его показать.',
     'text_ru': '📖 **1/3**\n\n☝️ Используйте кнопки меню, чтобы общаться со мной.\n\nЕсли меню скрыто, нажмите кнопку, которая указана на картинке, чтобы его показать.',
     'text_en': None,
     'version': 'a'},
    {'name': 'onboarding-step_1',
     'text': '📖 **1/3**\n\n☝️ Используй кнопки меню, чтобы общаться со мной.\n\nЕсли меню исчезло, жми кнопку как на картинке выше, чтобы его вернуть.',
     'text_ru': '📖 **1/3**\n\n☝️ Используй кнопки меню, чтобы общаться со мной.\n\nЕсли меню исчезло, жми кнопку как на картинке выше, чтобы его вернуть.',
     'text_en': None,
     'version': 'b'},
    {'name': 'onboarding-step_2',
     'text': '📖 **2/3**\n\nОсновной валютой всех игр является Leo.\n\n1 Leo = 10 руб.\nПокупать их не нужно, я позаботился о том, чтобы конвертация твоих рублей в Leo происходила автоматически.\n\nПополнить баланс можно в меню "💰 Баланс".',
     'text_ru': '📖 **2/3**\n\nОсновной валютой всех игр является Leo.\n\n1 Leo = 10 руб.\nПокупать их не нужно, я позаботился о том, чтобы конвертация твоих рублей в Leo происходила автоматически.\n\nПополнить баланс можно в меню "💰 Баланс".',
     'text_en': None,
     'version': 'b'},
    {'name': 'onboarding-step_3',
     'text': '📖 **3/3**\n\nЕще одна валюта - это 🔅 **Bonus Leo**. (я сброшу тебе немного сразу после этого обучения, как и обещал 😉)\nТак же, их можно заработать при каждом пополнении баланса.\n\n**Bonus Leo** 🔅 автоматически активируются при запуске любой из игр.',
     'text_ru': '📖 **3/3**\n\nЕще одна валюта - это 🔅 **Bonus Leo**. (я сброшу тебе немного сразу после этого обучения, как и обещал 😉)\nТак же, их можно заработать при каждом пополнении баланса.\n\n**Bonus Leo** 🔅 автоматически активируются при запуске любой из игр.',
     'text_en': None,
     'version': 'b'},
    {'name': 'onboarding-finish-source',
     'text': '🎉 Поздравляю, Вы завершили обучение!\n🎁 Вам начислено {bonus} 🔅 **Bonus Leo**.',
     'text_ru': '🎉 Поздравляю, Вы завершили обучение!\n🎁 Вам начислено {bonus} 🔅 **Bonus Leo**.',
     'text_en': None,
     'version': 'a'},
    {'name': 'onboarding-finish-source',
     'text': '🎉 Поздравляю, ты завершил обучение!\n{bonus} 🔅 **Bonus Leo** уже у тебя на счету! 🎁',
     'text_ru': '🎉 Поздравляю, ты завершил обучение!\n{bonus} 🔅 **Bonus Leo** уже у тебя на счету! 🎁',
     'text_en': None,
     'version': 'b'},
    {'name': 'onboarding-finish-ref',
     'text': '🎉 Поздравляю, Вы завершили обучение!',
     'text_ru': '🎉 Поздравляю, Вы завершили обучение!',
     'text_en': None,
     'version': 'a'},
    {'name': 'onboarding-finish-ref',
     'text': '🎉 Поздравляю, ты завершил обучение!',
     'text_ru': '🎉 Поздравляю, ты завершил обучение!',
     'text_en': None,
     'version': 'b'},
    {'name': 'onboarding-finish-none',
     'text': '🎉 Поздравляю, Вы завершили обучение!',
     'text_ru': '🎉 Поздравляю, Вы завершили обучение!',
     'text_en': None,
     'version': 'a'},
    {'name': 'onboarding-finish-none',
     'text': '🎉 Поздравляю, ты завершил обучение!',
     'text_ru': '🎉 Поздравляю, ты завершил обучение!',
     'text_en': None,
     'version': 'b'},
    {'name': 'home_text',
     'text': 'Наслаждайтесь превосходными симуляторами игровых автоматов!\n\n🎰 Как играть?\nНажмите кнопку "🎰 Игры", чтобы открыть меню со списком доступных игр.\n\n💰 Пополнение баланса / Вывод стредств\nПерейдите в меню "💰 Баланс" и следуйте моим простым подсказкам.\n\n👤 Есть вопросы?\nВоспользуйтесь кнопкой "❓ Помощь" для связи со специалистом. Вам обязательно помогут!',
     'text_ru': 'Наслаждайтесь превосходными симуляторами игровых автоматов!\n\n🎰 Как играть?\nНажмите кнопку "🎰 Игры", чтобы открыть меню со списком доступных игр.\n\n💰 Пополнение баланса / Вывод стредств\nПерейдите в меню "💰 Баланс" и следуйте моим простым подсказкам.\n\n👤 Есть вопросы?\nВоспользуйтесь кнопкой "❓ Помощь" для связи со специалистом. Вам обязательно помогут!',
     'text_en': None,
     'version': 'a'},
    {'name': 'home_text',
     'text': 'Наслаждайся превосходными симуляторами игровых автоматов!\n\n🎰 Как играть?\nНажми кнопку "🎰 Игры", чтобы открыть меню со списком доступных игр.\n\n💰 Пополнение баланса / Вывод стредств\nПерейди в меню "💰 Баланс" и следуй моим простым подсказкам.\n\n👤 Есть вопросы?\nТебе в меню "❓ Помощь"! Я переключу тебя на специалиста, который сможет решить все вопросы.',
     'text_ru': 'Наслаждайся превосходными симуляторами игровых автоматов!\n\n🎰 Как играть?\nНажми кнопку "🎰 Игры", чтобы открыть меню со списком доступных игр.\n\n💰 Пополнение баланса / Вывод стредств\nПерейди в меню "💰 Баланс" и следуй моим простым подсказкам.\n\n👤 Есть вопросы?\nТебе в меню "❓ Помощь"! Я переключу тебя на специалиста, который сможет решить все вопросы.',
     'text_en': None,
     'version': 'b'},
    {'name': 'select_game',
     'text': 'Ниже представлены доступные игры. Выбирайте!',
     'text_ru': 'Ниже представлены доступные игры. Выбирайте!',
     'text_en': None,
     'version': 'a'},
    {'name': 'game_info',
     'text': '⚠️ После окончания игры, для корректной работы бота, нажмите кнопку "Выход"\n⚠️ Одновременно можно запустить только одну игру!',
     'text_ru': '⚠️ После окончания игры, для корректной работы бота, нажмите кнопку "Выход"\n⚠️ Одновременно можно запустить только одну игру!',
     'text_en': None,
     'version': 'a'},
    {'name': 'game_info',
     'text': '⚠️ После окончания игры, для корректной работы бота, нажми кнопку "Выход"\n⚠️ Одновременно можно запустить только одну игру!',
     'text_ru': '⚠️ После окончания игры, для корректной работы бота, нажми кнопку "Выход"\n⚠️ Одновременно можно запустить только одну игру!',
     'text_en': None,
     'version': 'b'},
    {'name': 'balance_menu-without_withdraw_in_progress_amount',
     'text': '💼 Баланс:\n\n💰 {real_balance} руб.\n🔅 **Bonus Leo**: {bonus_balance}\r\n\r\n🔱 Доступно к выводу: {max_withdrawal} руб.',
     'text_ru': '💼 Баланс:\n\n💰 {real_balance} руб.\n🔅 **Bonus Leo**: {bonus_balance}\r\n\r\n🔱 Доступно к выводу: {max_withdrawal} руб.',
     'text_en': None,
     'version': 'a'},
    {'name': 'balance_menu-without_withdraw_in_progress_amount',
     'text': '💼 Баланс:\n\n💰 {real_balance} руб.\n🔅 **Bonus Leo**: {bonus_balance}\r\n\r\n🔱 Доступно к выводу: {max_withdrawal} руб.',
     'text_ru': '💼 Баланс:\n\n💰 {real_balance} руб.\n🔅 **Bonus Leo**: {bonus_balance}\r\n\r\n🔱 Доступно к выводу: {max_withdrawal} руб.',
     'text_en': None,
     'version': 'b'},
    {'name': 'deposit-canceled',
     'text': 'Пополнение баланса отменено.',
     'text_ru': 'Пополнение баланса отменено.',
     'text_en': None,
     'version': 'a'},
    {'name': 'deposit-canceled',
     'text': 'Пополнение баланса отменено.',
     'text_ru': 'Пополнение баланса отменено.',
     'text_en': None,
     'version': 'b'},
    {'name': 'deposit-replenish_link',
     'text': 'Перейди по ссылке для пополнения счёта на {amount} руб.',
     'text_ru': 'Перейди по ссылке для пополнения счёта на {amount} руб.',
     'text_en': '',
     'version': 'b'},
    {'name': 'select_game',
     'text': 'Выбирай любую из доступных игр!',
     'text_ru': 'Выбирай любую из доступных игр!',
     'text_en': '',
     'version': 'b'},
    {'name': 'balance_menu-with_withdraw_in_progress_amount',
     'text': '💼 Баланс:\r\n\r\n💰 {real_balance} руб.\r\n🔅 **Bonus Leo**: {bonus_balance}\r\n\r\n🔱 Доступно к выводу: {max_withdrawal} руб.\r\n\r\n📤 **В обработке запрос на вывод**: {withdraw_in_progress_amount} руб.',
     'text_ru': '💼 Баланс:\r\n\r\n💰 {real_balance} руб.\r\n🔅 **Bonus Leo**: {bonus_balance}\r\n\r\n🔱 Доступно к выводу: {max_withdrawal} руб.\r\n\r\n📤 **В обработке запрос на вывод**: {withdraw_in_progress_amount} руб.',
     'text_en': '',
     'version': 'a'},
    {'name': 'error_start_game',
     'text': '❌ Возникла неизвестная ошибка... Такое может произойти если Вы не завершили предыдущую игру, или завершили игру закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуйте начать игру заново, и после завершения, нажать на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.',
     'text_ru': '❌ Возникла неизвестная ошибка... Такое может произойти если Вы не завершили предыдущую игру, или завершили игру закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуйте начать игру заново, и после завершения, нажать на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.',
     'text_en': None,
     'version': 'a'},
    {'name': 'error_start_game',
     'text': '❌ Что-то пошло не так... Такое может произойти если ты не завершил предыдущую игру, или завершил игру просто закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуй начать игру заново, и после завершения игры, нажми на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.',
     'text_ru': '❌ Что-то пошло не так... Такое может произойти если ты не завершил предыдущую игру, или завершил игру просто закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуй начать игру заново, и после завершения игры, нажми на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.',
     'text_en': None,
     'version': 'b'},
    {'name': 'error_insufficient_balance',
     'text': '❌ На Вашем балансе надостаточно средств. Чтобы пополнить счет, перейдите в меню "💰 Баланс" и следуйте моим простым подсказкам!',
     'text_ru': '❌ На Вашем балансе надостаточно средств. Чтобы пополнить счет, перейдите в меню "💰 Баланс" и следуйте моим простым подсказкам!',
     'text_en': None,
     'version': 'a'},
    {'name': 'error_insufficient_balance',
     'text': '❌ Баланс на нуле 😿. Чтобы пополнить счет, переходи в меню "💰 Баланс" и следуй моим простым подсказкам!',
     'text_ru': '❌ Баланс на нуле 😿. Чтобы пополнить счет, переходи в меню "💰 Баланс" и следуй моим простым подсказкам!',
     'text_en': None,
     'version': 'b'},
    {'name': 'deposit-enter_amount',
     'text': 'Введите желаемую сумму пополнения\nМинимальная сумма: {min_deposit} руб.',
     'text_ru': 'Введите желаемую сумму пополнения\nМинимальная сумма: {min_deposit} руб.',
     'text_en': None,
     'version': 'a'},
    {'name': 'deposit-enter_amount',
     'text': 'Введи желаемую сумму пополнения\nМинимальная сумма: {min_deposit} руб.',
     'text_ru': 'Введи желаемую сумму пополнения\nМинимальная сумма: {min_deposit} руб.',
     'text_en': None,
     'version': 'b'},
    {'name': 'withdrawal-enter_amount',
     'text': 'Минимальная сумма для вывода {min_withdrawal} руб.\n\nВведите сумму для вывода',
     'text_ru': 'Минимальная сумма для вывода {min_withdrawal} руб.\n\nВведите сумму для вывода',
     'text_en': None,
     'version': 'a'},
    {'name': 'withdrawal-enter_amount',
     'text': 'Минимальная сумма для вывода {min_wirhdrawal} руб.\n\nВведи сумму для вывода',
     'text_ru': 'Минимальная сумма для вывода {min_withdrawal} руб.\n\nВведи сумму для вывода',
     'text_en': None,
     'version': 'b'},
    {'name': 'withdrawal-enter_card',
     'text': 'Введите номер карты',
     'text_ru': 'Введите номер карты',
     'text_en': None,
     'version': 'a'},
    {'name': 'withdrawal-request_created',
     'text': '✅ Заявка на вывод {amount} на карту {card} **успешно создана**.',
     'text_ru': '✅ Заявка на вывод {amount} на карту {card} **успешно создана**.',
     'text_en': None,
     'version': 'a'},
    {'name': 'withdrawal-request_created',
     'text': '✅ Заявка на вывод {amount} на карту {card} **успешно создана**.',
     'text_ru': '✅ Заявка на вывод {amount} на карту {card} **успешно создана**.',
     'text_en': None,
     'version': 'b'},
    {'name': 'withdrawal-null_error',
     'text': 'Вы не можете вывести 0 руб.',
     'text_ru': 'Вы не можете вывести 0 руб.',
     'text_en': None,
     'version': 'a'},
    {'name': 'withdrawal-limit_error',
     'text': 'Вывод не доступен. Для вывода средств, необходимо сделать ставки минимум на {needsumbet} руб. ({in_leo} leo.)',
     'text_ru': 'Вывод не доступен. Для вывода средств, необходимо сделать ставки минимум на {needsumbet} руб. ({in_leo} leo.)',
     'text_en': None,
     'version': 'a'},
    {'name': 'withdrawal-limit_error',
     'text': 'Вывод не доступен. Для вывода средств, необходимо сделать ставки минимум на {needsumbet} руб. ({in_leo} leo.)',
     'text_ru': 'Вывод не доступен. Для вывода средств, необходимо сделать ставки минимум на {needsumbet} руб. ({in_leo} leo.)',
     'text_en': None,
     'version': 'b'},
    {'name': 'withdrawal-invalid_card',
     'text': 'Некорректная карта',
     'text_ru': 'Некорректная карта',
     'text_en': None,
     'version': 'a'},
    {'name': 'withdrawal-invalid_card',
     'text': 'Некорректная карта',
     'text_ru': 'Некорректная карта',
     'text_en': None,
     'version': 'b'},
    {'name': 'invalid_number',
     'text': 'Некорректное число',
     'text_ru': 'Некорректное число',
     'text_en': None,
     'version': 'a'},
    {'name': 'invalid_number',
     'text': 'Некорректное число',
     'text_ru': 'Некорректное число',
     'text_en': None,
     'version': 'b'},
    {'name': 'deposit-min_limit',
     'text': 'Минимальная сумма для пополнения {min_deposit} руб.',
     'text_ru': 'Минимальная сумма для пополнения {min_deposit} руб.',
     'text_en': None,
     'version': 'a'},
    {'name': 'deposit-min_limit',
     'text': 'Минимальная сумма для пополнения {min_deposit} руб.',
     'text_ru': 'Минимальная сумма для пополнения {min_deposit} руб.',
     'text_en': None,
     'version': 'b'},
    {'name': 'deposit-replenish_link',
     'text': 'Перейдите по ссылке для пополнения счёта на {amount} руб.',
     'text_ru': 'Перейдите по ссылке для пополнения счёта на {amount} руб.',
     'text_en': None,
     'version': 'a'},
    {'name': 'withdrawal-max_limit',
     'text': 'Вы не можете вывести более, чем {max_amount} руб.',
     'text_ru': 'Вы не можете вывести более, чем {max_amount} руб.',
     'text_en': '',
     'version': 'a'},
    {'name': 'withdrawal-min_limit',
     'text': 'Минимальная сумма вывода {min_amount} руб.',
     'text_ru': 'Минимальная сумма вывода {min_amount} руб.',
     'text_en': '',
     'version': 'b'},
    {'name': 'withdrawal-min_limit',
     'text': 'Минимальная сумма вывода {min_amount} руб.',
     'text_ru': 'Минимальная сумма выводачем {min_amount} руб.',
     'text_en': '',
     'version': 'a'},
    {'name': 'withdrawal-null_error',
     'text': 'Нельзя вывести 0 руб.',
     'text_ru': 'Нельзя вывести 0 руб.',
     'text_en': '',
     'version': 'b'},
    {'name': 'withdrawal-cancel',
     'text': '❌ Вывод средств отменен',
     'text_ru': '❌ Вывод средств отменен',
     'text_en': '',
     'version': 'a'},
    {'name': 'withdrawal-cancel',
     'text': '❌ Вывод средств отменен',
     'text_ru': '❌ Вывод средств отменен',
     'text_en': '',
     'version': 'b'},
    {'name': 'withdrawal-enter_card',
     'text': 'Введи номер карты',
     'text_ru': 'Введи номер карты',
     'text_en': '',
     'version': 'b'},
    {'name': 'contact_support',
     'text': 'Для того, чтобы связаться с технической поддержкой нажмите кнопку под этим сообщением',
     'text_ru': 'Для того, чтобы связаться с технической поддержкой нажмите кнопку под этим сообщением',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-onboarding_0',
     'text': '👩\u200d🎓 Пройти обучение',
     'text_ru': '👩\u200d🎓 Пройти обучение',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-onboarding_1',
     'text': '👉 Следующий шаг',
     'text_ru': '👉 Следующий шаг',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-onboarding_1',
     'text': '👉 Дальше',
     'text_ru': '👉 Дальше',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-onboarding_2',
     'text': '👉 Cледующий шаг',
     'text_ru': '👉 Cледующий шаг',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-onboarding_2',
     'text': '👉 Дaльше',
     'text_ru': '👉 Дaльше',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-onboarding_final',
     'text': 'Я готов!',
     'text_ru': 'Я готов!',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-balance',
     'text': '💰 Баланс',
     'text_ru': '💰 Баланс',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-balance',
     'text': '💰 Баланс',
     'text_ru': '💰 Баланс',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-balance-conditions',
     'text': '❗️ Условия',
     'text_ru': '❗️ Условия',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-balance-conditions',
     'text': '❗️ Условия',
     'text_ru': '❗️ Условия',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-balance-deposit',
     'text': '💰Пополнить баланс 💳👉💰',
     'text_ru': '💰Пополнить баланс 💳👉💰',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-balance-deposit',
     'text': '💰Пополнить баланс 💳👉💰',
     'text_ru': '💰Пополнить баланс 💳👉💰',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-balance-cancel_deposit',
     'text': '❌ Отменить пополнение',
     'text_ru': '❌ Отменить пополнение',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-balance-cancel_deposit',
     'text': '❌ Отменить пополнение',
     'text_ru': '❌ Отменить пополнение',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-balance-go_to_deposit',
     'text': 'Перейти к пополнению',
     'text_ru': 'Перейти к пополнению',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-balance-go_to_deposit',
     'text': 'Перейти к пополнению',
     'text_ru': 'Перейти к пополнению',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-balance-withdrawal',
     'text': 'Вывести деньги на карту 💰👉💳',
     'text_ru': 'Вывести деньги на карту 💰👉💳',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-balance-withdrawal',
     'text': 'Вывести деньги на карту 💰👉💳',
     'text_ru': 'Вывести деньги на карту 💰👉💳',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-balance-cancel_withdrawal',
     'text': '❌ Отменить вывод',
     'text_ru': '❌ Отменить вывод',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-balance-cancel_withdrawal',
     'text': '❌ Отменить вывод',
     'text_ru': '❌ Отменить вывод',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-affiliate',
     'text': '🤝 Партнёрская программа',
     'text_ru': '🤝 Партнёрская программа',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-affiliate',
     'text': '🤝 Партнёрская программа',
     'text_ru': '🤝 Партнёрская программа',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-games',
     'text': '🎰 Игры',
     'text_ru': '🎰 Игры',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-games',
     'text': '🎰 Игры',
     'text_ru': '🎰 Игры',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-game-start_on_real',
     'text': 'Играть',
     'text_ru': 'Играть',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-game-start_on_real',
     'text': 'Играть',
     'text_ru': 'Играть',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-game-start_on_demo',
     'text': 'Играть на демо-счёт',
     'text_ru': 'Играть на демо-счёт',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-game-start_on_demo',
     'text': 'Играть на демо-счёт',
     'text_ru': 'Играть на демо-счёт',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-help',
     'text': '❓ Помощь',
     'text_ru': '❓ Помощь',
     'text_en': None,
     'version': 'a'},
    {'name': 'kb-help',
     'text': '❓ Помощь',
     'text_ru': '❓ Помощь',
     'text_en': None,
     'version': 'b'},
    {'name': 'kb-contact_support',
     'text': '🟢 Связаться с технической поддержкой',
     'text_ru': '🟢 Связаться с технической поддержкой',
     'text_en': '',
     'version': 'a'},
    {'name': 'kb-contact_support',
     'text': '🟢 Связаться с технической поддержкой',
     'text_ru': '🟢 Связаться с технической поддержкой',
     'text_en': '',
     'version': 'b'},
    {'name': 'kb-onboarding_final',
     'text': 'Понятно, поехали!',
     'text_ru': 'Понятно, поехали!',
     'text_en': '',
     'version': 'a'},
    {'name': 'kb-onboarding_0',
     'text': 'Поехали!',
     'text_ru': 'Поехали!',
     'text_en': '',
     'version': 'b'},
    {'name': 'contact_support',
     'text': 'Для того, чтобы связаться с технической поддержкой нажми кнопку под этим сообщением',
     'text_ru': 'Для того, чтобы связаться с технической поддержкой нажми кнопку под этим сообщением',
     'text_en': None,
     'version': 'b'},

        ]
