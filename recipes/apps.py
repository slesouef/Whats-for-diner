"""
Django app declaration
Recipes is a Django application managing the user created recipes
"""
from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Recipes configuration"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
