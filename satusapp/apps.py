from django.apps import AppConfig


class SatusappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'satusapp'

    def ready(self):
        import satusapp.signals
