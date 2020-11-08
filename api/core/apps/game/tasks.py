from core.apps.game import services as game_services
from ..vendor.exceptions import ThirdPartyVendorException
from core.apps.game.models import InvoiceData
from core.apps.account.models import TelegramAccount
from core.apps.vendor.gambling.chc import CHCAPIClient
from decimal import Decimal
from django.utils import timezone
from core.config.celery import app as celery_app


@celery_app.task
def check_invoice():
    from datetime import timedelta

    last_minute = timezone.now() - timedelta(seconds=15)
    invoices = InvoiceData.objects.filter(status='open', created__lt=last_minute)
    client = CHCAPIClient()
    for invoice in invoices:

        account = TelegramAccount.objects.get(tg_id=invoice.account.tg_id)
        try:
            closed_invoice = client.close_invoice(invoice.invoice_id)
            invoice.status = 'closed'
            invoice.save()

            if invoice.type_invoice == 'real':
                game_services.update_balance_after_game(account, invoice, Decimal(closed_invoice[0]) * Decimal(10))
        except:
            if invoice.type_invoice == 'real':
                chc_invoice = client.check_invoice(invoice.invoice_id)
                actual_amount = Decimal(chc_invoice[0] * 10)
                game_services.update_balance_in_game(account, invoice.last_check_amount, actual_amount)
                invoice.last_check_amount = actual_amount
                invoice.save()




