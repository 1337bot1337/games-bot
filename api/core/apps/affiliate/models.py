from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from core.apps.common import models as common_models
from django.utils import timezone


class AffiliateSetup(common_models.BaseModel):
    name = models.CharField(_("Имя профиля"), max_length=255)
    referrer_deposit_bonus = models.DecimalField(_("Бонус рефереру от депозита реферала"), max_digits=10,
                                                 decimal_places=2)
    referral_deposit_bonus = models.DecimalField(_("Коэффициент рефералу на первое пополнение депозита"), max_digits=10,
                                                 decimal_places=2)

    min_referral_deposit = models.DecimalField(_("Минимальная сумма депозита реферала для выплаты бонусов рефереру"),
                                               max_digits=10, decimal_places=2, default=Decimal(1000))

    class Meta:
        verbose_name = "Настройки партнёрской программы"
        verbose_name_plural = "Настройки партнёрской программы"


class UserAffiliate(common_models.BaseModel):
    referral = models.OneToOneField("account.TelegramAccount", verbose_name=_("Реферал"), related_name="refl",
                                    on_delete=models.CASCADE)
    referrer = models.ForeignKey("account.TelegramAccount", verbose_name=_("Реферер"), related_name="refr",
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Реестр рефералов"
        verbose_name_plural = "Реестр рефералов"
