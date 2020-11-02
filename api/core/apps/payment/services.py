import random
from .models import PaymentOrder


def generate_order_id():
    while True:
        order_id = random.choice(range(10000, 99999999))

        if not PaymentOrder.objects.filter(order_id=order_id).exists():
            return order_id


