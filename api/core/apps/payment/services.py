import random
from .models import PaymentOrder
from core.apps.helpbot.api.pyroAPI import HelpBot
from core.apps.payment.freekassa.api import FreeKassaApi
from core.apps.wallet.services import refill_wallet
from core.apps.statistic.services import register_statistic, get_user_source
from decimal import Decimal


def generate_order_id():
    while True:
        order_id = random.choice(range(10000, 99999999))

        if not PaymentOrder.objects.filter(order_id=order_id).exists():
            return order_id


def check_deposit(request):

    remote_ip = str(request.META.get('HTTP_X_FORWARDED_FOR'))
    if remote_ip not in (
    '136.243.38.147', '136.243.38.149', '136.243.38.150', '136.243.38.151', '136.243.38.189', '136.243.38.108'):
        return False

    order_id = int(request.data['MERCHANT_ORDER_ID'])
    request_sign = request.data['SIGN']

    order_query = PaymentOrder.objects.filter(order_id=order_id)
    if not order_query.exists():
        return False
    order = order_query[0]
    client = FreeKassaApi()
    sign = client.generate_form_signature(order.amount, order.order_id)

    if request_sign != sign:
        return False

    return True


def send_successful_deposit(tg_id, amount, bonus: int = False):
    client = HelpBot()

    text = f'💸 Ваш баланс пополнен на {amount} руб.'

    if bonus:
        text += f'\nЗа пополнение начислено {bonus} бонусных жетонов.'

    client.start()
    client.send_msg(tg_id, text=text)


def new_refill(request):
    order_id = int(request.data['MERCHANT_ORDER_ID'])
    order = PaymentOrder.objects.get(order_id)
    amount = int(request.data['AMOUNT'])
    bonus = refill_wallet(order.tg_id, amount)

    order.status = 'payed'
    order.save()

    register_statistic(order.tg_id, 'deposit', data={"amount": amount})
    send_successful_deposit(order.tg_id, amount, bonus)


