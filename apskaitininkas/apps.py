from django.apps import AppConfig


class ApskaitininkasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apskaitininkas'

    def ready(self):
        import apskaitininkas.signals
