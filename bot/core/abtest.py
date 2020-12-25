from config import cache


def get_text(tg_id: int, text_name: str):
    texts = cache.get_texts()

    try:
        source = _get_user_source(tg_id)
    except:
        return []

    try:
        src_dict = _get_source_setup(source)
    except:
        src_dict = _get_source_setup("none")

    bot_profile = _get_bot_profile(src_dict)

    try:
        texts = texts[(text_name, bot_profile["version_text"])]["text_ru"]
    except:
        texts = texts[(text_name, "a")]["text_ru"]

    return texts


def get_onboarding(tg_id: int):
    source = _get_user_source(tg_id)
    src_dict = _get_source_setup(source)
    bot_profile = _get_bot_profile(src_dict)
    return bot_profile["onboarding"]


def get_source_welcome_bonus(tg_id: int):
    source = _get_user_source(tg_id)
    src_dict = _get_source_setup(source)
    bot_profile = _get_bot_profile(src_dict)
    return bot_profile["welcome_bonus"]


def _get_user_source(tg_id: int):
    return cache.get_users()[tg_id]["source"]


def _get_source_setup(source: str) -> dict:
    source_setup = cache.get_sources()
    return source_setup.get(source, None)


def check_source(source: str):
    if _get_source_setup(source):
        return True


def _get_bot_profile(source: dict):
    bot_profile = cache.get_botprofiles()
    return bot_profile[source["profile_id"]]