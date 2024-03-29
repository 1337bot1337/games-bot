from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _


class BotText(models.Model):
    name = models.CharField(_("Название"), max_length=55)
    text = models.TextField(_("Текст"))
    version = models.CharField(max_length=25)

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты бота"


class BotProfile(models.Model):
    name = models.CharField(_("Имя профиля"), max_length=25, primary_key=True)
    version_text = models.CharField(_("Версия текста"), max_length=25)
    welcome_bonus = models.FloatField(_("Вступительный бонус"))
    deposit_bonus = models.FloatField(_("Бонус на депозит"))
    type_deposit_bonus = models.CharField(_("Тип бонуса на депозит"), max_length=255, choices=(
        ("factor", _("Множитель")),
        ("fixed", _("Фиксированный"))), default="factor")

    onboarding = models.BooleanField(_("Вступительное обучение"), default=True)

    class Meta:
        verbose_name = "A/B профиль"
        verbose_name_plural = "A/B профили"


class SourceSetup(models.Model):
    name = models.CharField(_("Название источника трафика"), max_length=55, unique=True)
    profile = models.ForeignKey("abtest.BotProfile", verbose_name="A/B тест профиль", on_delete=models.CASCADE)
    channel_link = models.CharField(_("Ссылка на канал"), max_length=255, default="none")
    ad_link = models.URLField(_("Рекламная ссылка"), default="none")
    creative_link = models.URLField(_("Ссылка на креатив"), default="none")

    class Meta:
        verbose_name = "Конфигурация источника трафика"
        verbose_name_plural = "Конфигурации источника трафика"

    def __str__(self):
        return f"{self.name}"
