from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class GetOrNoneManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True, )

    class Meta:
        abstract = True


class BalanceMultiplierConfig(BaseModel):
    amount_from: int = models.PositiveIntegerField(_("Amount from"), default=0)
    amount_to: int = models.PositiveIntegerField(_("Amount to"), default=0)
    multiplier = models.DecimalField(_("Multiplier"), decimal_places=2, max_digits=5, default=Decimal(1.0))
    is_active = models.BooleanField(_("Active"), default=True)

    class Meta:
        unique_together = ("amount_from", "amount_to", "is_active",)

    def clean(self):
        if self.amount_from > self.amount_to:
            raise ValidationError("Amount from cannot be greater then amount to!")

        qs = BalanceMultiplierConfig.objects.filter(
            is_active=True, amount_from__lte=self.amount_to, amount_to__gte=self.amount_from
        )
        if self.pk is not None:
            qs = qs.exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError("Amount from/to intersection")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Settings(models.Model):
    wager = models.PositiveIntegerField()
    min_withdrawal = models.PositiveIntegerField()
    min_deposit = models.PositiveIntegerField()

