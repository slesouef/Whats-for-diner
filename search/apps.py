"""
Django app declaration
Search is a Django application allowing the user to find recipes
"""
from django.apps import AppConfig


class SearchConfig(AppConfig):
    """Recipes configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
