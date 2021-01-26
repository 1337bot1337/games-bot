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

    last_minute = timezone.now() - timedelta(seconds=7)
    invoices = InvoiceData.objects.filter(status='open', created__lt=last_minute)
    client = CHCAPIClient()
    for invoice in invoices:
        account = TelegramAccount.objects.get(tg_id=invoice.account.tg_id)
        if timezone.now() - invoice.created < timezone.timedelta(seconds=60):
            chc_invoice, check_error = client.check_invoice(invoice.invoice_id)
            if check_error:
                print("1check_invoice_error", invoice.invoice_id, check_error)
                continue
            actual_amount = Decimal(chc_invoice * 10)
            game_services.update_balance_in_game(account, invoice.last_check_amount, actual_amount)
            invoice.last_check_amount = actual_amount
            invoice.save()
            continue

        closed_invoice, invoice_error = client.close_invoice(invoice.invoice_id)
        game_history, game_error = client.invoice_game_history(invoice.invoice_id)

        if closed_invoice:
            invoice.game_history = game_history
            invoice.status = 'closed'
            invoice.save()

            if invoice.type_invoice == 'real':
                game_services.update_balance_after_game(account, invoice, Decimal(closed_invoice) * Decimal(10))
            continue

        if invoice.type_invoice == 'real':
            if invoice_error:
                chc_invoice, check_error = client.check_invoice(invoice.invoice_id)
                if check_error:
                    if game_history:
                        invoice.status = "closed"
                        invoice.game_history = game_history
                        invoice.save()
                    print("2check_invoice_error", invoice.invoice_id, check_error)
                    continue
                actual_amount = Decimal(chc_invoice * 10)
                game_services.update_balance_in_game(account, invoice.last_check_amount, actual_amount)
                invoice.last_check_amount = actual_amount
                invoice.save()


        #
        # try:
        #     closed_invoice = client.close_invoice(invoice.invoice_id)
        #     game_history = client.invoice_game_history(invoice.invoice_id)
        #     invoice.game_history = game_history
        #     invoice.status = 'closed'
        #     invoice.save()
        #
        #     if invoice.type_invoice == 'real':
        #         game_services.update_balance_after_game(account, invoice, Decimal(closed_invoice[0]) * Decimal(10))
        # except:
        #     if invoice.type_invoice == 'real':
        #         try:
        #             chc_invoice = client.check_invoice(invoice.invoice_id)
        #         except:
        #             print("check_invoice_error", invoice.invoice_id)
        #             continue
        #         actual_amount = Decimal(chc_invoice[0] * 10)
        #         game_services.update_balance_in_game(account, invoice.last_check_amount, actual_amount)
        #         invoice.last_check_amount = actual_amount
        #         invoice.save()




