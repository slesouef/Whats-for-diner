"""
Models for the recipes created by users
"""
from django.db import models
from django.urls import reverse

from accounts.models import MyUser


class Categories(models.Model):
    """
    Classify recipes by categories
    All recipes have a category
    Categories have a name
    """
    name = models.CharField(max_length=255, unique=True)


class Content(models.Model):
    """
    Recipe content
    Links ingredients and recipes with a quantity for each ingredients
    """
    recipe = models.ForeignKey("Recipes", on_delete=models.CASCADE)
    ingredient = models.ForeignKey("Ingredients", on_delete=models.CASCADE)
    quantity = models.CharField(max_length=255)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)


class Ingredients(models.Model):
    """
    Table of all the ingredients used in the recipes
    """
    name = models.CharField(max_length=255, unique=True)
    creationDate = models.DateTimeField(auto_now_add=True)


class Recipes(models.Model):
    """
    Recipes contains the following fields:
        a name, a creator, a category, a list of ingredients, and a rating
    """
    name = models.CharField(max_length=255)
    rating = models.IntegerField(blank=True, null=True)
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)
    ingredients = models.ManyToManyField("Ingredients", through="Content")
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """method to create the url for a specific recipe"""
        return reverse("view_recipe", args=[int(self.id)])
