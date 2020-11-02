from django.db import models

from core.apps.common import models as common_models


class PaymentOrder(common_models.BaseModel):
    order_id = models.PositiveIntegerField(unique=True)
    tg_id = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    payment_api = models.CharField(max_length=255, default='FreeKassa')
    status = models.CharField(max_length=255, default='new')
