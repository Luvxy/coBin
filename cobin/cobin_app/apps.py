from django.apps import AppConfig\

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cobin_app'

    def ready(self):
        import cobin_app.signals  # signals.py 불러오기

class CobinAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cobin_app'