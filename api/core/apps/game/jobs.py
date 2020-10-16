from ..game.services import update_balance_after_game
from ..vendor.exceptions import ThirdPartyVendorException
from .models import InvoiceData
from ..account.models import TelegramAccount
from ..vendor.gambling.chc import CHCAPIClient


def check_invoice():

    invoices = InvoiceData.objects.filter(status='open')
    client = CHCAPIClient()
    for invoice in invoices:
        try:
            closed_invoice = client.close_invoice(invoice.invoice_id)
        except ThirdPartyVendorException:
            continue

        if invoice.type_invoice == 'real':
            account = TelegramAccount.objects.get(tg_id=invoice.tg_id)
            update_balance_after_game(account, invoice.start_real_amount, invoice.start_virtual_amount, closed_invoice[0])
        invoice.status = 'closed'
        invoice.save()


