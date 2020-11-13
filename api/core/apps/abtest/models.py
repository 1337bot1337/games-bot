from django.conf import settings
from django.db import models


class BotText(models.Model):
    name = models.CharField(max_length=55)
    text = models.TextField()
    version = models.CharField(max_length=25)


class BotProfile(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    version_text = models.CharField(max_length=25)
    welcome_bonus = models.FloatField()
    deposit_bonus = models.FloatField()


class SourceSetup(models.Model):
    name = models.CharField(max_length=55)
    profile = models.ForeignKey("abtest.BotProfile", on_delete=models.CASCADE)

