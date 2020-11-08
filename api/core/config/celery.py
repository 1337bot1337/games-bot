import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.settings")

app = Celery("jobs")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
