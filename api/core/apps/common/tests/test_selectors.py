from decimal import Decimal

import pytest
from django.conf import settings

from core.apps.common import models as common_models
from core.apps.common import selectors as common_selectors


@pytest.fixture(autouse=True)
def multipliers_config(db):
    common_models.BalanceMultiplierConfig.objects.create(
        amount_from=0,
        amount_to=5_000,
        multiplier=1.25
    )
    common_models.BalanceMultiplierConfig.objects.create(
        amount_from=5_001,
        amount_to=10_000,
        multiplier=1.5
    )


@pytest.mark.parametrize("amount, expected_multiplier", [
    (Decimal(1_000), 1.25),
    (Decimal(5_000), 1.25),
    (Decimal(5_001), 1.5),
    (Decimal(10_000), 1.5),
    (Decimal(10_001), 2),
    (Decimal(15_000), 2),
])
def test_get_suitable_multiplier(amount, expected_multiplier):
    settings.DEFAULT_MULTIPLIER = 2
    multiplier = common_selectors.get_suitable_multiplier(amount=amount)
    assert expected_multiplier == multiplier
