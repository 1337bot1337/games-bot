from django.apps import AppConfig


class WalletConfig(AppConfig):
    name = 'core.apps.wallet'
    verbose_name = 'кошелёк'

    def ready(self):
        from core.apps.wallet import signals
