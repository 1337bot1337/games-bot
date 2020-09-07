from core.env import env


DEFAULT_USER_SOURCE = env.str("DEFAULT_USER_SOURCE", default="default")

CHC_BLACK_API_KEY = env.str("CHC_BLACK_API_KEY", default="")
CHC_BLACK_SECRET_KEY = env.str("CHC_BLACK_SECRET_KEY", default="")
