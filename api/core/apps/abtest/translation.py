from modeltranslation.translator import register, TranslationOptions

from core.apps.abtest import models as common_models


@register(common_models.BotText)
class TextTranslationOptions(TranslationOptions):
    fields = 'text',
