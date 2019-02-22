from django.apps import AppConfig


class PremiumsConfig(AppConfig):
    name = 'web.apps.premiums'

    def ready(self):
        from .signals import process_payment
        from paypal.standard.ipn.signals import valid_ipn_received
        valid_ipn_received.connect(process_payment)
