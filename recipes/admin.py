"""Register models for admin app"""
from django.contrib import admin

from .models import Categories, Content, Ingredients, Recipes

admin.site.register(Categories)
admin.site.register(Content)
admin.site.register(Ingredients)
admin.site.register(Recipes)
