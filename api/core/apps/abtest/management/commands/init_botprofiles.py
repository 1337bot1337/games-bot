from django.core.management.base import BaseCommand

from core.apps.abtest import models as abtest_models
from core.apps.affiliate import models as affiliate_models
from core.apps.common import models as common_models
from decimal import Decimal


class Command(BaseCommand):

    def handle(self, **options):
        if not abtest_models.BotProfile.objects.filter(name="default").exists():

            profiles_list = [
                {"name": "default",
                 "version_text": "a",
                 "welcome_bonus": 100,
                 "deposit_bonus": 1.1},

                {"name": "version-b",
                 "version_text": "b",
                 "welcome_bonus": 100,
                 "deposit_bonus": 1.1}
            ]
            abtest_models.BotProfile.objects.bulk_create([abtest_models.BotProfile(**q) for q in profiles_list])

        if not abtest_models.SourceSetup.objects.filter(name='none').exists():
            abtest_models.SourceSetup.objects.create(
                name="none",
                profile=abtest_models.BotProfile.objects.get(name='default')
            )

        if not affiliate_models.AffiliateSetup.objects.filter(name="default").exists():
            affiliate_models.AffiliateSetup.objects.create(
                name="default",
                referrer_deposit_bonus=Decimal(100),
                referral_deposit_bonus=Decimal(100)
            )

        if not common_models.Settings.objects.filter().exists():
            common_models.Settings.objects.create(
                wager=37,
                min_withdrawal=100,
                min_deposit=100
            )
