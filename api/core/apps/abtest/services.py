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
    return source_setup[source]


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
            {"name": "onboarding-step_0",
             "text": "🖐 Приветствую! Я менеджер Gambling Games. У нас можно играть в самые разные симуляторы игровых автоматов!\n\n"
                     "🎁  После завершения небольшого обучения, на Ваш счёт будет зачислено 100 бонусных жетонов.",
             "text_ru": "🖐 Приветствую! Я менеджер Gambling Games. У нас можно играть в самые разные симуляторы игровых автоматов!\n\n"
                        "🎁  После завершения небольшого обучения, на Ваш счёт будет зачислено 100 бонусных жетонов.",
             "version": "a"},

            {"name": "onboarding-step_0",
             "text": "🖐 Привет! Я менеджер Gambling Games. У нас можно играть в самые разные симуляторы игровых автоматов!\n\n"
                     "🎁  После завершения небольшого обучения, я сброшу на твой счёт 100 🔅 бонусных жетонов.",
             "text_ru": "🖐 Привет! Я менеджер Gambling Games. У нас можно играть в самые разные симуляторы игровых автоматов!\n\n"
                        "🎁  После завершения небольшого обучения, я сброшу на твой счёт 100 🔅 бонусных жетонов.",
             "version": "b"},

            {"name": "onboarding-step_1",
             "text": "📖 **1/3**\n\n"
                     "☝️ Используйте кнопки меню, чтобы общаться со мной.\n\n"
                     "Если меню скрыто, нажмите кнопку, которая указана на картинке, чтобы его показать.",

             "text_ru": "📖 **1/3**\n\n"
                        "☝️ Используйте кнопки меню, чтобы общаться со мной.\n\n"
                        "Если меню скрыто, нажмите кнопку, которая указана на картинке, чтобы его показать.",
             "version": "a"},

            {"name": "onboarding-step_1",
             "text": "☝️ Используйте кнопки меню, чтобы общаться со мной.\n\n"
                     "Если меню скрыто, нажмите кнопку, которая указана на картинке, чтобы его показать",

             "text_ru": "📖 **1/3**\n\n"
                        "☝️ Используй кнопки меню, чтобы общаться со мной.\n\n"
                        "Если меню исчезло, жми кнопку как на картинке выше, чтобы его вернуть.",
             "version": "b"},

            {"name": "onboarding-step_2",
             "text": '📖 **2/3**\n\n'
                     'Основной валютой всех игр является **Leo**.\n'
                     '1 Leo = 10 руб.\n'
                     'Покупать их не нужно, я позаботился о том, чтобы конвертация ваших рублей в Leo происходила автоматически.\n\n'
                     'Пополнить баланс можно в меню "💰 Баланс".',
             "text_ru": '📖 **2/3**\n\n'
                        'Основной валютой всех игр является **Leo**.\n'
                        '1 Leo = 10 руб.\n'
                        'Покупать их не нужно, я позаботился о том, чтобы конвертация ваших рублей в Leo происходила автоматически.\n\n'
                        'Пополнить баланс можно в меню "💰 Баланс".',
             "version": 'a'},

            {"name": "onboarding-step_2",
             "text": '📖 **2/3**\n\n'
                     'Основной валютой всех игр является Leo.\n\n'
                     '1 Leo = 10 руб.\n'
                     'Покупать их не нужно, я позаботился о том, чтобы конвертация твоих рублей в Leo происходила автоматически.\n\n'
                     'Пополнить баланс можно в меню "💰 Баланс".',
             "text_ru": '📖 **2/3**\n\n'
                        'Основной валютой всех игр является Leo.\n\n'
                        '1 Leo = 10 руб.\n'
                        'Покупать их не нужно, я позаботился о том, чтобы конвертация твоих рублей в Leo происходила автоматически.\n\n'
                        'Пополнить баланс можно в меню "💰 Баланс".',
             "version": "b"},

            {"name": "onboarding-step_3",
             "text": "📖 **3/3**\n\n"
                     "Еще одна валюта - это 🔅 бонусные жетоны. (Вы получите немного сразу после этого обучения 😉)\n"
                     "Бонусные жетоны 🔅 автоматически активируются при запуске любой из игр.",
             "text_ru": "📖 **3/3**\n\n"
                        "Еще одна валюта - это 🔅 бонусные жетоны. (Вы получите немного сразу после этого обучения 😉)\n"
                        "Так же, их можно заработать при каждом пополнении баланса.\n\n"
                        "Бонусные жетоны 🔅 автоматически активируются при запуске любой из игр.",
             "version": "a"},

            {"name": "onboarding-step_3",
             "text": "📖 **3/3**\n\n"
                     "Еще одна валюта - это 🔅 бонусные жетоны. (я сброшу тебе немного сразу после этого обучения, как и обещал 😉)\n"
                     "Так же, их можно заработать при каждом пополнении баланса.\n\n"
                     "Бонусные жетоны 🔅 автоматически активируются при запуске любой из игр.",
             "text_ru": "📖 **3/3**\n\n"
                        "Еще одна валюта - это 🔅 бонусные жетоны. (я сброшу тебе немного сразу после этого обучения, как и обещал 😉)\n"
                        "Так же, их можно заработать при каждом пополнении баланса.\n\n"
                        "Бонусные жетоны 🔅 автоматически активируются при запуске любой из игр.",
             "version": "b"},

            {"name": "onboarding-finish",
             "text": "🎉 Поздравляю, Вы завершили обучение!\n"
                     "🎁 Вам начислено {bonus_amount} 🔅 бонусных жетонов.",
             "text_ru": "🎉 Поздравляю, Вы завершили обучение!\n"
                        "🎁 Вам начислено {bonus_amount} 🔅 бонусных жетонов.",
             "version": "a"},

            {"name": "onboarding-finish",
             "text": "🎉 Поздравляю, ты завершил обучение!\n"
                     "{bonus_amount} 🔅 бонусных жетонов уже у тебя на счету! 🎁",
             "text_ru": "🎉 Поздравляю, ты завершил обучение!\n"
                        "{bonus_amount} 🔅 бонусных жетонов уже у тебя на счету! 🎁",
             "version": "b"},

            {"name": 'home_text',
             "text": 'Наслаждайтесь превосходными симуляторами игровых автоматов!\n\n'
                     '🎰 Как играть?\n'
                     'Нажмите кнопку "🎰 Игры", чтобы открыть меню со списком доступных игр.\n\n'
                     '💰 Пополнение баланса / Вывод стредств\n'
                     'Перейдите в меню "💰 Баланс" и следуйте моим простым подсказкам.\n'
                     '⚠️ Если ваш баланс исчерпан, ничего страшного. Все игры доступны в демо-режиме!\n\n'
                     '👤 Есть вопросы?\n'
                     'Воспользуйтесь кнопкой "❓ Помощь" для связи со специалистом. Вам обязательно помогут!',
             "text_ru": 'Наслаждайтесь превосходными симуляторами игровых автоматов!\n\n'
                        '🎰 Как играть?\n'
                        'Нажмите кнопку "🎰 Игры", чтобы открыть меню со списком доступных игр.\n\n'
                        '💰 Пополнение баланса / Вывод стредств\n'
                        'Перейдите в меню "💰 Баланс" и следуйте моим простым подсказкам.\n'
                        '⚠️ Если ваш баланс исчерпан, ничего страшного. Все игры доступны в демо-режиме!\n\n'
                        '👤 Есть вопросы?\n'
                        'Воспользуйтесь кнопкой "❓ Помощь" для связи со специалистом. Вам обязательно помогут!',

             "version": "a"},

            {"name": 'home_text',
             "text": 'Наслаждайся превосходными симуляторами игровых автоматов!\n\n'
                     '🎰 Как играть?\n'
                     'Нажми кнопку "🎰 Игры", чтобы открыть меню со списком доступных игр.\n\n'
                     '💰 Пополнение баланса / Вывод стредств\n'
                     'Перейди в меню "💰 Баланс" и следуй моим простым подсказкам. \n'
                     '⚠️ Если твой баланс на нуле, не переживай! Все игры доступны в демо-режиме!\n\n'
                     '👤 Есть вопросы?\n'
                     'Тебе в меню "❓ Помощь"! Я переключу тебя на специалиста, который сможет решить все вопросы.',
             "text_ru": 'Наслаждайся превосходными симуляторами игровых автоматов!\n\n'
                        '🎰 Как играть?\n'
                        'Нажми кнопку "🎰 Игры", чтобы открыть меню со списком доступных игр.\n\n'
                        '💰 Пополнение баланса / Вывод стредств\n'
                        'Перейди в меню "💰 Баланс" и следуй моим простым подсказкам. \n'
                        '⚠️ Если твой баланс на нуле, не переживай! Все игры доступны в демо-режиме!\n\n'
                        '👤 Есть вопросы?\n'
                        'Тебе в меню "❓ Помощь"! Я переключу тебя на специалиста, который сможет решить все вопросы.',

             "version": "b"},

            {"name": "select_game",
             "text": "Ниже представлены доступные игры. Выбирайте!",
             "text_ru": "Ниже представлены доступные игры. Выбирайте!",
             "version": "a"},

            {"name": "select_game",
             "text": "Ниже все доступные игры. Выбирай!",
             "text_ru": "Ниже все доступные игры. Выбирай!",
             "version": "b"},

            {"name": "game_info",
             "text": '**{game_title}**\n'
                     'Играйте на Leo или попробуйте демо-режим!\n\n'
                     '⚠️ После окончания игры, для корректной работы бота, нажмите кнопку "Выход"\n'
                     '⚠️ Одновременно можно запустить только одну игру!',
             "text_ru": 'Играйте на Leo или попробуйте демо-режим!\n\n'
                     '⚠️ После окончания игры, для корректной работы бота, нажмите кнопку "Выход"\n'
                     '⚠️ Одновременно можно запустить только одну игру!',
             "version": "a"},

            {"name": "game_info",
             "text": '**{game_title}**\n'
                     'Играйте на Leo или попробуйте демо-режим!\n\n'
                     '⚠️ После окончания игры, для корректной работы бота, нажмите кнопку "Выход"\n'
                     '⚠️ Одновременно можно запустить только одну игру!',
             "text_ru": 'Играй на Leo или попробуй демо-режим!\n\n'
                        '⚠️ После окончания игры, для корректной работы бота, нажми кнопку "Выход"\n'
                        '⚠️ Одновременно можно запустить только одну игру!',
             "version": "b"},

            {"name": "balance_menu-with_withdraw_in_progress_amount",
             "text": "💼 Баланс:\n\n"
                     "💰 {real_balance} руб.\n"
                     "🔅 Бонусные жетоны: {bonus_balance}\n\n"
                     "📤 **Ожидание на вывод**: {withdraw_in_progress_amount} руб.",
             "text_ru": "💼 Баланс:\n\n"
                        "💰 {real_balance} руб.\n"
                        "🔅 Бонусные жетоны: {bonus_balance}\n\n"
                        "📤 **Ожидание на вывод**: {withdraw_in_progress_amount} руб.",
             "version": "a"},

            {"name": "balance_menu-with_withdraw_in_progress_amount",
             "text": "💼 Баланс:\n\n"
                     "💰 {real_balance} руб.\n"
                     "🔅 Бонусные жетоны: {bonus_balance}\n\n"
                     "📤 **Ожидание на вывод**: {withdraw_in_progress_amount} руб.",
             "text_ru": "💼 Баланс:\n\n"
                        "💰 {real_balance} руб.\n"
                        "🔅 Бонусные жетоны: {bonus_balance}\n\n"
                        "📤 **Ожидание на вывод**: {withdraw_in_progress_amount} руб.",
             "version": "b"},

            {"name": "balance_menu-without_withdraw_in_progress_amount",
             "text": "💼 Баланс:\n\n"
                     "💰 {real_balance} руб.\n"
                     "🔅 Бонусные жетоны: {bonus_balance}\n\n",
             "text_ru": "💼 Баланс:\n\n"
                        "💰 {real_balance} руб.\n"
                        "🔅 Бонусные жетоны: {bonus_balance}\n\n",
             "version": "a"},

            {"name": "balance_menu-without_withdraw_in_progress_amount",
             "text": "💼 Баланс:\n\n"
                     "💰 {real_balance} руб.\n"
                     "🔅 Бонусные жетоны: {bonus_balance}\n\n",
             "text_ru": "💼 Баланс:\n\n"
                        "💰 {real_balance} руб.\n"
                        "🔅 Бонусные жетоны: {bonus_balance}\n\n",
             "version": "b"},

            {"name": "error_start_game",
             "text": '❌ Возникла неизвестная ошибка... Такое может произойти если Вы не завершили предыдущую игру, или завершили игру закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуйте начать игру заново, и после завершения, нажать на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.',
             "text_ru": '❌ Возникла неизвестная ошибка... Такое может произойти если Вы не завершили предыдущую игру, или завершили игру закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуйте начать игру заново, и после завершения, нажать на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.',
             "version": "a"},

            {"name": "error_start_game",
             "text": '❌ Что-то пошло не так... Такое может произойти если ты не завершил предыдущую игру, или завершил игру просто закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуй начать игру заново, и после завершения игры, нажми на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.',
             "text_ru": '❌ Что-то пошло не так... Такое может произойти если ты не завершил предыдущую игру, или завершил игру просто закрыв вкладку в браузере. Я рекомендую завершать игру нажатием на кнопку "Выход". Попробуй начать игру заново, и после завершения игры, нажми на кнопку "Выход". Так же, рекомендую закрыть все остальные вкладки с другими играми и подождать несколько секунд.',
             "version": "b"},

            {"name": "error_insufficient_balance",
             "text": '❌ На Вашем балансе надостаточно средств. Чтобы пополнить счет, перейдите в меню "💰 Баланс" и следуйте моим простым подсказкам!',
             "text_ru": '❌ На Вашем балансе надостаточно средств. Чтобы пополнить счет, перейдите в меню "💰 Баланс" и следуйте моим простым подсказкам!',
             "version": "a"},

            {"name": "error_insufficient_balance",
             "text": '❌ Баланс на нуле 😿. Чтобы пополнить счет, переходи в меню "💰 Баланс" и следуй моим простым подсказкам!',
             "text_ru": '❌ Баланс на нуле 😿. Чтобы пополнить счет, переходи в меню "💰 Баланс" и следуй моим простым подсказкам!',
             "version": "b"},

            {"name": "deposit-enter_amount",
             "text": "Введите желаемую сумму пополнения\n"
                     "Минимальная сумма: {min_deposit} руб.",
             "text_ru": "Введите желаемую сумму пополнения\n"
                        "Минимальная сумма: {min_deposit} руб.",
             "version": "a"},

            {"name": "deposit-enter_amount",
             "text": "Введи желаемую сумму пополнения\n"
                     "Минимальная сумма: {min_deposit} руб.",
             "text_ru": "Введи желаемую сумму пополнения\n"
                        "Минимальная сумма: {min_deposit} руб.",
             "version": "b"},

            {"name": "withdrawal-enter_amount",
             "text": "Введите сумму для вывода",
             "text_ru": "Введите сумму для вывода",
             "version": "a"},

            {"name": "withdrawal-enter_amount",
             "text": "Введи сумму для вывода",
             "text_ru": "Введи сумму для вывода",
             "version": "b"},

            {"name": "withdrawal-enter_card",
             "text": "Введите номер карты",
             "text_ru": "Введите номер карты",
             "version": "a"},

            {"name": "withdrawal-enter_card",
             "text": "Введи номер карты",
             "text_ru": "Введи  номер карты",
             "version": "b"},

            {"name": "withdrawal-request_created",
             "text": "✅ Заявка на вывод {amount} на карту {card} **успешно создана**.",
             "text_ru": "✅ Заявка на вывод {amount} на карту {card} **успешно создана**.",
             "version": "a"},

            {"name": "withdrawal-request_created",
             "text": "✅ Заявка на вывод {amount} на карту {card} **успешно создана**.",
             "text_ru": "✅ Заявка на вывод {amount} на карту {card} **успешно создана**.",
             "version": "b"},

            {"name": "withdrawal-cancel",
             "text": "❌ Вывод отменен",
             "text_ru": "❌ Вывод отменен",
             "version": "a"},

            {"name": "withdrawal-cancel",
             "text": "❌ Вывод отменен",
             "text_ru": "❌ Вывод отменен",
             "version": "b"},

            {"name": "withdrawal-null_error",
             "text": "Вы не можете вывести 0",
             "text_ru": "Вы не можете вывести 0",
             "version": "a"},

            {"name": "withdrawal-null_error",
             "text": "Вы не можете вывести 0",
             "text_ru": "Вы не можете вывести 0",
             "version": "b"},

            {"name": "withdrawal-min_limit",
             "text": "Вы не можете вывести меньше чем {min_amount} руб.",
             "text_ru": "Вы не можете вывести меньше чем {min_amount} руб.",
             "version": "a"},

            {"name": "withdrawal-min_limit",
             "text": "Вы не можете вывести меньше чем {min_amount} руб.",
             "text_ru": "Вы не можете вывести меньше чем {min_amount} руб.",
             "version": "b"},

            {"name": "withdrawal-max_limit",
             "text": "Вы не можете вывести больше чем {max_amount} руб.",
             "text_ru": "Вы не можете вывести больше чем {max_amount} руб.",
             "version": "a"},

            {"name": "withdrawal-max_limit",
             "text": "Вы не можете вывести больше чем {max_amount} руб.",
             "text_ru": "Вы не можете вывести больше чем {max_amount} руб.",
             "version": "b"},

            {"name": "withdrawal-invalid_card",
             "text": "Некорректная карта",
             "text_ru": "Некорректная карта",
             "version": "a"},

            {"name": "withdrawal-invalid_card",
             "text": "Некорректная карта",
             "text_ru": "Некорректная карта",
             "version": "b"},

            {"name": "invalid_number",
             "text": "Некорректное число",
             "text_ru": "Некорректное число",
             "version": "a"},

            {"name": "invalid_number",
             "text": "Некорректное число",
             "text_ru": "Некорректное число",
             "version": "b"},

            {"name": "deposit-min_limit",
             "text": "Минимальная сумма для пополнения {min_deposit} руб.",
             "text_ru": "Минимальная сумма для пополнения {min_deposit} руб.",
             "version": "a"},

            {"name": "deposit-min_limit",
             "text": "Минимальная сумма для пополнения {min_deposit} руб.",
             "text_ru": "Минимальная сумма для пополнения {min_deposit} руб.",
             "version": "b"},

            {"name": "deposit-replenish_link",
             "text": "Перейдите по ссылке для пополнения счёта на {amount} руб.",
             "text_ru": "Перейдите по ссылке для пополнения счёта на {amount} руб.",
             "version": "a"},

            {"name": "deposit-replenish_link",
             "text": "Перейдите по ссылке для пополнения счёта на {amount} руб.",
             "text_ru": "Перейдите по ссылке для пополнения счёта на {amount} руб.",
             "version": "b"},

            {"name": "deposit-canceled",
             "text": "Пополнение баланса отменено.",
             "text_ru": "Пополнение баланса отменено.",
             "version": "a"},

            {"name": "deposit-canceled",
             "text": "Пополнение баланса отменено.",
             "text_ru": "Пополнение баланса отменено.",
             "version": "b"},

            {"name": "contact_support",
             "text": "Для того, чтобы связаться с технической поддержкой нажмите кнопку под этим сообщением",
             "text_ru": "Для того, чтобы связаться с технической поддержкой нажмите кнопку под этим сообщением",
             "version": "a"},

            {"name": "contact_support",
             "text": "Для того, чтобы связаться с технической поддержкой нажми кнопку под этим сообщением",
             "text_ru": "Для того, чтобы связаться с технической поддержкой нажми кнопку под этим сообщением",
             "version": "b"},

            {"name": "kb-onboarding_0",
             "text": "👩‍🎓 Пройти обучение",
             "text_ru": "👩‍🎓 Пройти обучение",
             "version": "a"},

            {"name": "kb-onboarding_0",
             "text": "👩‍🎓 Поехали!",
             "text_ru": "👩‍🎓 Поехали!",
             "version": "b"},

            {"name": "kb-onboarding_1",
             "text": "👉 Следующий шаг",
             "text_ru": "👉 Следующий шаг",
             "version": "a"},

            {"name": "kb-onboarding_1",
             "text": "👉 Дальше",
             "text_ru": "👉 Дальше",
             "version": "b"},

            {"name": "kb-onboarding_2",
             "text": "👉 Cледующий шаг",
             "text_ru": "👉 Cледующий шаг",
             "version": "a"},

            {"name": "kb-onboarding_2",
             "text": "👉 Дaльше",
             "text_ru": "👉 Дaльше",
             "version": "b"},

            {"name": "kb-onboarding_final",
             "text": "Понятно, спасибо!",
             "text_ru": "Понятно, спасибо!",
             "version": "a"},

            {"name": "kb-onboarding_final",
             "text": "Я готов!",
             "text_ru": "Я готов!",
             "version": "b"},

            {"name": "kb-balance",
             "text": "💰 Баланс",
             "text_ru": "💰 Баланс",
             "version": "a"},

            {"name": "kb-balance",
             "text": "💰 Баланс",
             "text_ru": "💰 Баланс",
             "version": "b"},

            {"name": "kb-balance-deposit",
             "text": "Пополнить баланс 💳👉💰",
             "text_ru": "💰Пополнить баланс 💳👉💰",
             "version": "a"},

            {"name": "kb-balance-deposit",
             "text": "Пополнить баланс 💳👉💰",
             "text_ru": "💰Пополнить баланс 💳👉💰",
             "version": "b"},

            {"name": "kb-balance-cancel_deposit",
             "text": "❌ Отменить пополнение",
             "text_ru": "❌ Отменить пополнение",
             "version": "a"},

            {"name": "kb-balance-cancel_deposit",
             "text": "❌ Отменить пополнение",
             "text_ru": "❌ Отменить пополнение",
             "version": "b"},

            {"name": "kb-balance-go_to_deposit",
             "text": "Перейти к пополнению",
             "text_ru": "Перейти к пополнению",
             "version": "a"},

            {"name": "kb-balance-go_to_deposit",
             "text": "Перейти к пополнению",
             "text_ru": "Перейти к пополнению",
             "version": "b"},

            {"name": "kb-balance-withdrawal",
             "text": "Вывести деньги на карту 💰👉💳",
             "text_ru": "Вывести деньги на карту 💰👉💳",
             "version": "a"},

            {"name": "kb-balance-withdrawal",
             "text": "Вывести деньги на карту 💰👉💳",
             "text_ru": "Вывести деньги на карту 💰👉💳",
             "version": "b"},

            {"name": "kb-balance-cancel_withdrawal",
             "text": "❌ Отменить вывод",
             "text_ru": "❌ Отменить вывод",
             "version": "a"},

            {"name": "kb-balance-cancel_withdrawal",
             "text": "❌ Отменить вывод",
             "text_ru": "❌ Отменить вывод",
             "version": "b"},

            {"name": "kb-games",
             "text": "🎰 Игры",
             "text_ru": "🎰 Игры",
             "version": "a"},

            {"name": "kb-games",
             "text": "🎰 Игры",
             "text_ru": "🎰 Игры",
             "version": "b"},

            {"name": "kb-game-start_on_real",
             "text": "Играть",
             "text_ru": "Играть",
             "version": "a"},

            {"name": "kb-game-start_on_real",
             "text": "Играть",
             "text_ru": "Играть",
             "version": "b"},

            {"name": "kb-game-start_on_demo",
             "text": "Играть на демо-счёт",
             "text_ru": "Играть на демо-счёт",
             "version": "a"},

            {"name": "kb-game-start_on_demo",
             "text": "Играть на демо-счёт",
             "text_ru": "Играть на демо-счёт",
             "version": "b"},

            {"name": "kb-help",
             "text": "❓ Помощь",
             "text_ru": "❓ Помощь",
             "version": "a"},

            {"name": "kb-help",
             "text": "❓ Помощь",
             "text_ru": "❓ Помощь",
             "version": "b"},

            {"name": "kb-contact_support",
             "text": "🟢 Связаться с тех. поддержкой",
             "text_ru": "🟢 Связаться с тех. поддержкой",
             "version": "a"},

            {"name": "kb-contact_support",
             "text": "🟢 Связаться с тех. поддержкой",
             "text_ru": "🟢 Связаться с тех. поддержкой",
             "version": "b"}

        ]
