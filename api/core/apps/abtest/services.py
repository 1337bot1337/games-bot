from django.core.cache import cache


def get_text(tg_id, text_name: str):
    texts = cache.get("texts")
    source = get_user_source(tg_id)
    src_dict = get_source_setup(source)
    bot_profile = get_bot_profile(src_dict)

    return texts[(text_name, bot_profile["version_text"])]["text_ru"]


def get_user_source(tg_id):
    users = cache.get("users")
    return users[tg_id]["source"]


def get_source_setup(source: str):
    source_setup = cache.get("sources")
    return source_setup[source]


def get_bot_profile(source: dict):
    bot_profile = cache.get("botprofiles")
    return bot_profile[source["profile_id"]]
