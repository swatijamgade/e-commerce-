from django.apps import AppConfig
from django.db.models.signals import post_save


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # implicit signal registration
        from . import signals

        # explicit way
        # post_save.connect(profile_create_receiver)