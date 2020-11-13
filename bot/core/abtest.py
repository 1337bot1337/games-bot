from config import cache


def get_text(tg_id: int, text_name: str):
    texts = cache.get_texts()
    source = get_user_source(tg_id)
    src_dict = get_source_setup(source)
    bot_profile = get_bot_profile(src_dict)
    return texts[(text_name, bot_profile["version_text"])]["text_ru"]


def get_welcome_bonus(tg_id: int):
    source = get_user_source(tg_id)
    src_dict = get_source_setup(source)
    bot_profile = get_bot_profile(src_dict)
    return bot_profile.welcome_bonus


def get_user_source(tg_id: int):
    return cache.get_users()[tg_id]["source"]


def get_source_setup(source: str) -> dict:
    source_setup = cache.get_sources()
    return source_setup[source]


def get_bot_profile(source: dict):
    bot_profile = cache.get_botprofiles()
    return bot_profile[source["profile_id"]]