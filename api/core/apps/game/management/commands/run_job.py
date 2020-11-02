from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BlockingScheduler
from core.apps.game.jobs import check_invoice
shed = BlockingScheduler()


class Command(BaseCommand):

    def handle(self, **options):
        shed.add_job(check_invoice, 'interval', seconds=5)
        shed.start()
