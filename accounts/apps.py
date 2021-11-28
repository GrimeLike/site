from django.apps import AppConfig
from django.dispatch import Signal

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

user_registered = Signal(providing_args=['instance'])