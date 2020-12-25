import redis
import pickle

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