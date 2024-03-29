from core.env import env


MAX_INT_VALUE = 2_147_483_647

DEFAULT_USER_SOURCE = env.str("DEFAULT_USER_SOURCE", default="default")

CHC_BLACK_API_KEY = env.str("CHC_BLACK_API_KEY", default="")
CHC_BLACK_SECRET_KEY = env.str("CHC_BLACK_SECRET_KEY", default="")

MAX_WITHDRAW_AMOUNT_PER_REQUEST = env.int("MAX_WITHDRAW_AMOUNT_PER_REQUEST", default=1_000_000)
MAX_REFILL_AMOUNT_PER_REQUEST = env.int("MAX_REFILL_AMOUNT_PER_REQUEST", default=1_000_000)

DEFAULT_MULTIPLIER = env.int("DEFAULT_MULTIPLIER", default=1)

DEFAULT_DEMO_AMOUNT = env.int("DEFAULT_DEMO_AMOUNT", default=1_000)


# FreeKassa
MERCHANT_ID = env.str("MERCHANT_ID")
FIRST_SECRET = env.str("FIRST_SECRET")
SECOND_SECRET = env.str("SECOND_SECRET")

# Telegram help bot
TG_API_ID = env.str("TG_API_ID")
TG_API_HASH = env.str("TG_API_HASH")
TG_API_TOKEN = env.str("TG_API_TOKEN")
BOT_USERNAME = env.str("BOT_USERNAME")

