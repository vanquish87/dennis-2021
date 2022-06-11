import django
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # importing signals in this user app
    def ready(self):
        import users.signals
