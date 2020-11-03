from ..game.services import update_balance_after_game
from ..vendor.exceptions import ThirdPartyVendorException
from .models import InvoiceData
from ..account.models import TelegramAccount
from ..vendor.gambling.chc import CHCAPIClient
from decimal import Decimal
from django.utils import timezone


def check_invoice():
    from datetime import timedelta

    last_minute = timezone.now() - timedelta(seconds=15)
    invoices = InvoiceData.objects.filter(status='open', created__lt=last_minute)
    client = CHCAPIClient()
    for invoice in invoices:
        try:
            closed_invoice = client.close_invoice(invoice.invoice_id)
        except:
            continue

        if invoice.type_invoice == 'real':
            account = TelegramAccount.objects.get(tg_id=invoice.account.tg_id)
            update_balance_after_game(account, invoice.game_id, invoice.start_real_amount, invoice.start_virtual_amount, Decimal(closed_invoice[0]) * Decimal(10))
        invoice.status = 'closed'
        invoice.save()


