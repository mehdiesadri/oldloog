from django.apps import AppConfig


class DiscoveryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "discovery"

    def ready(self):
        """
        This function will execute when application loads completely.
        It's better to import and call signals here.
        """
        from . import signals
