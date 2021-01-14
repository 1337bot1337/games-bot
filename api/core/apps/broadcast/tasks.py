from core.config.celery import app as celery_app
from core.apps.broadcast import models as broadcast_models
from core.apps.account import models as account_models
from core.apps.helpbot import services as helpbot_services
from core.apps.abtest import services as abtest_services
from core.apps.broadcast import services as broadcast_services
from django.utils.translation import gettext as _
from django.utils import timezone


@celery_app.task
def check_broadcast_query():
    query = broadcast_models.BroadcastQuery.objects.filter(action="queue_for_sending", status=False)

    if query.exists():
        for msg in query:
            if msg.broadcast_to_all:

                if msg.timedelta_inactive == timezone.timedelta(0):
                    users = account_models.TelegramAccount.objects.all()
                else:
                    users = broadcast_services.get_users_from_lastactivity(msg.timedelta_inactive)

                helpbot_services.broadcast(users, msg.text, msg.keyboard)

                msg.status = True
                msg.save()
                continue

            sources = abtest_services.get_sources_from_botprofile(msg.bot_profile)
            if msg.timedelta_inactive == timezone.timedelta(0):
                users = account_models.TelegramAccount.objects.filter(source__in=sources)
            else:
                users = broadcast_services.get_users_from_lastactivity(msg.timedelta_inactive, sources=sources)

            helpbot_services.broadcast(users, msg.text, msg.keyboard)
            msg.status = True
            msg.save()
