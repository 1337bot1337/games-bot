from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.apps.common import models as common_models

from ..common.models import GetOrNoneManager


class InvoiceData(common_models.BaseModel):
    objects = GetOrNoneManager()

    account = models.ForeignKey('account.TelegramAccount', related_name='invoices', on_delete=models.CASCADE)
    game_id = models.PositiveIntegerField(_("Game ID"), max_length=250)
    invoice_id = models.CharField(_("Invoice ID"), max_length=250)
    tr_id = models.CharField(_("Transaction ID"), max_length=250)
    type_invoice = models.CharField(_("Type invoice"), max_length=250)
    start_real_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    start_virtual_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    end_real_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    end_virtual_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    status = models.CharField(_("Status"), max_length=250, default='open')
