from django.apps import AppConfig


class DiscoveryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "discovery"

    # def ready(self):
    #     import nltk
    #     nltk.download("stopwords")
    #     nltk.download("punkt")
