from django.core.management.base import BaseCommand

from core.apps.vendor.management.flow import main


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()
