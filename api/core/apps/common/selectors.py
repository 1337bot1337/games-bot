from decimal import Decimal

from django.conf import settings

from . import models as common_models


def get_active_multipliers():
    return common_models.BalanceMultiplierConfig.objects.filter(is_active=True)


def get_suitable_multiplier(*, amount: Decimal) -> int:
    try:
        multiplier = get_active_multipliers().get(amount_to__gte=amount, amount_from__lte=amount)
    except common_models.BalanceMultiplierConfig.DoesNotExist:
        return settings.DEFAULT_MULTIPLIER
    else:
        return multiplier.multiplier
