from django.core.management.base import BaseCommand

from core.apps.abtest.tasks import update_cache


class Command(BaseCommand):

    def handle(self, **options):
        update_cache()
        print("Cache has been updated!")
