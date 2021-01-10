from django.db.models.signals import post_save
from django.dispatch import receiver
from core.apps.wallet import models as wallet_models
from core.apps.helpbot import services as helpbot_services
from core.apps.abtest import services as abtest_services
from core.apps.statistic import services as statistic_services
from decimal import Decimal


@receiver(post_save, sender=wallet_models.WithdrawRequest)
def my_handler(sender, instance, **kwargs):
    if kwargs["update_fields"] == frozenset({"status"}):
        instance.is_active = False
        instance.save()
        account = instance.account
        if instance.status == "rejected":
            account.real_balance += instance.amount
            account.save()
            helpbot_services.send_msg(account.tg_id,
                                      abtest_services.get_text(account.tg_id, "withdrawal-rejected_withdraw_request").format(
                                          amount=instance.amount,
                                          card=instance.card_number
                                      ), session_name="withdrawal_rejected")
            statistic_services.register_statistic(tg_id=account.tg_id,
                                   username=account.username,
                                   first_name=account.first_name,
                                   last_name=account.last_name,
                                   type_action='withdrawal_rejected',
                                   data={"amount": round(float(instance.amount), 2),
                                         "request_id": instance.id})
        if instance.status == "accepted":
            account.max_withdrawal -= instance.amount
            account.save()
            helpbot_services.send_msg(account.tg_id, abtest_services.get_text(account.tg_id, "withdrawal-accepted_withdraw_request").format(
                                          amount=instance.amount,
                                          card=instance.card_number
                                      ), session_name="withdrawal_accepted")

            statistic_services.register_statistic(tg_id=account.tg_id,
                                                  username=account.username,
                                                  first_name=account.first_name,
                                                  last_name=account.last_name,
                                                  type_action='withdrawal_accepted',
                                                  data={"amount": round(float(instance.amount), 2),
                                                        "request_id": instance.id})
