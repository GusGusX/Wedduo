from django.apps import AppConfig


class RoomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'room'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals