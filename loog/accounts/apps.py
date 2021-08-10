from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """
        This function will execute when application loads completely.
        It's better to import and call signals here.
        """
        from . import signals
        signals.logger.info("Activated discovery/signals.py")
