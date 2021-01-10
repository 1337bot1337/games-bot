import random
from .models import PaymentOrder
from core.apps.helpbot.api.pyroAPI import HelpBot
from core.apps.payment.freekassa.api import FreeKassaApi
from core.apps.wallet.services import refill_wallet
from core.apps.statistic.services import register_statistic
from core.apps.abtest import services as abtest_services
from core.apps.account import services as account_services
from core.apps.account import models as account_models
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
        return False, 'HACK!'

    order_id = int(request.data['MERCHANT_ORDER_ID'])
    request_sign = request.data['SIGN']

    order_query = PaymentOrder.objects.filter(order_id=order_id)
    if not order_query.exists():
        return False, 'unknown order_id'

    order = order_query[0]
    if order.status != "new":
        return False, 'closed order'

    order = order_query[0]
    client = FreeKassaApi()
    sign = client.generate_callback_signature(order.amount, order.order_id)

    if request_sign != sign:
        return False, 'signatures do not match'

    return True, None


def send_successful_deposit(tg_id, amount, bonus):
    client = HelpBot()
    account = account_models.TelegramAccount.objects.get(tg_id=tg_id)
    bonus_text = " "
    if bonus != 0:
        bonus_text = abtest_services.get_text(tg_id, "replenish_balance-bonus").format(bonus=round(bonus, 2))

    if account.source != "none":
        bonus_text = abtest_services.get_text(tg_id, "replenish_balance-bonus-source").format(bonus=round(bonus, 2))

    text = abtest_services.get_text(tg_id, "replenish_balance").format(amount=amount, bonus_text=bonus_text)
    client.send_msg(tg_id, text=text)


def new_refill(request):
    order_id = int(request.data['MERCHANT_ORDER_ID'])
    order = PaymentOrder.objects.get(order_id=order_id)
    amount = Decimal(request.data['AMOUNT'])
    bonus = refill_wallet(order.tg_id, amount)
    order.status = 'payed'
    order.save()
    account = account_models.TelegramAccount.objects.get(tg_id=int(order.tg_id))
    register_statistic(tg_id=order.tg_id,
                       username=account.username,
                       first_name=account.first_name,
                       last_name=account.last_name,
                       type_action='deposit', data={"amount": round(float(amount), 2), "bonus": round(float(bonus), 2), "order_id": order_id})
    send_successful_deposit(order.tg_id, amount, bonus)


