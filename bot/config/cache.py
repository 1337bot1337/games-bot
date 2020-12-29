import redis
import pickle
import asyncio
cache = redis.Redis(host="redis")


def get_users():
    return pickle.loads(cache.get(":1:users"))


def get_texts():
    return pickle.loads(cache.get(":1:texts"))


def get_botprofiles():
    return pickle.loads(cache.get(":1:botprofiles"))


def get_sources():
    return pickle.loads(cache.get(":1:sources"))


def get_affiliate_setup():
    return pickle.loads(cache.get(":1:affiliate"))


def get_user_cache(tg_id):
    if not cache.get(f":1:{tg_id}"):
        return None
    return pickle.loads(cache.get(f":1:{tg_id}"))


def change_user_cache(tg_id: int, flag_name: str, value):
    user_cache = get_user_cache(tg_id)

    if user_cache:
        user_cache[flag_name] = value
        cache.set(f":1:{tg_id}", pickle.dumps(user_cache))


def get_withdraw_amount(tg_id: int):
    user_cache = get_user_cache(tg_id)
    return user_cache["withdraw_amount"]


def get_settings():
    settings = pickle.loads(cache.get(f":1:settings"))
    return settings