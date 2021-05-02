"""
views for the recipes app
"""
from django.shortcuts import render


def create_recipe(request):
    """A page to create a new recipe"""
    return render(request, "recipes/create.html")
