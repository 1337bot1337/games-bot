from django.core.cache import cache


def get_text(tg_id: int, text_name: str):
    texts = cache.get("texts")
    source = get_user_source(tg_id)
    bot_profile = get_bot_profile(source)

    return texts[(text_name, bot_profile.version_text)]


def get_user_source(tg_id: int):
    users = cache.get("users")
    return users[tg_id]["source"]


def get_source_setup(source: str):
    source_setup = cache.get("sources")
    return source_setup[source]


def get_bot_profile(source: dict):
    bot_profile = cache.get("bot_profiles")
    return bot_profile[source["profile"]]
