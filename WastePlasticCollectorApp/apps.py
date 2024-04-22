from django.apps import AppConfig


class WasteplasticcollectorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'WastePlasticCollectorApp'

    # 1. 👇 Add this line for signals
    def ready(self):
        import WastePlasticCollectorApp.signals
