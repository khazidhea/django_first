from django.apps import AppConfig


class DjangoFirstConfig(AppConfig):
    name = 'django_first'

    def ready(self, *args, **kwargs):
        import django_first.signals
