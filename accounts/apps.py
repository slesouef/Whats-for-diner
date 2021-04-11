"""
Django app declaration
Accounts is a Django application managing the user accounts
"""
from django.apps import AppConfig


class AccountConfig(AppConfig):
    """accounts configuration"""
    name = 'accounts'
    default_auto_field = 'django.db.models.BigAutoField'
