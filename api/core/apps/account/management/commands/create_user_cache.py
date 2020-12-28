from django.core.management.base import BaseCommand
from django.core.cache import cache
from core.apps.account.models import TelegramAccount


class Command(BaseCommand):

    def handle(self, **options):
        users = TelegramAccount.objects.all()

        for user in users:
            user_cache = {"await_deposit_amount": False,
                          "await_withdraw_amount": False,
                          "await_withdraw_card": False,
                          "await_game_search": False,
                          "withdraw_amount": 0}
            cache.set(user.tg_id, user_cache, timeout=None)

        print("OK!")
