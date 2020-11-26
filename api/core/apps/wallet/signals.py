from django.db.models.signals import post_save
from django.dispatch import receiver
from core.apps.wallet import models as wallet_models
from core.apps.helpbot import services as helpbot_services
from core.apps.abtest import services as abtest_services


@receiver(post_save, sender=wallet_models.WithdrawRequest)
def my_handler(sender, instance, **kwargs):
    if kwargs["update_fields"] == frozenset({"status"}):
        instance.is_active = False
        instance.save()
        user = instance.account
        if instance.status == "rejected":
            user.real_balance += instance.amount
            user.save()
            helpbot_services.send_msg(user.tg_id,
                                      abtest_services.get_text(user.tg_id, "withdrawal-rejected_withdraw_request").format(
                                          amount=instance.amount,
                                          card=instance.card_number
                                      ))

        if instance.status == "accepted":
            helpbot_services.send_msg(user.tg_id, abtest_services.get_text(user.tg_id, "withdrawal-accepted_withdraw_request").format(
                                          amount=instance.amount,
                                          card=instance.card_number
                                      ))

