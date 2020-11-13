from django.core.management.base import BaseCommand

from core.apps.abtest import models as abtest_models


class Command(BaseCommand):

    def handle(self, **options):
        #abtest_models.BotProfile.objects.all().delete()

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

        abtest_models.SourceSetup.objects.create(
            name="none",
            profile=abtest_models.BotProfile.objects.get(name='default')
        )

