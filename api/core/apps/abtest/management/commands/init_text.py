from django.core.management.base import BaseCommand

from core.apps.abtest import models as abtest_models
from core.apps.abtest import services as abtest_services


class Command(BaseCommand):

    def handle(self, **options):
        abtest_models.BotText.objects.all().delete()

        texts = abtest_services.texts

        abtest_models.BotText.objects.bulk_create([abtest_models.BotText(**q) for q in texts])
