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

    def __str__(self):
        return self.name


class Content(models.Model):
    """
    Recipe content
    Links ingredients and recipes with a quantity for each ingredients
    """
    recipe = models.ForeignKey("Recipes", on_delete=models.CASCADE)
    index = models.SmallIntegerField(null=False)
    instructions = models.TextField()
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["index"]


class Ingredients(models.Model):
    """
    Table of all the ingredients used in the recipes
    """
    recipe = models.ForeignKey("Recipes", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)


class Recipes(models.Model):
    """
    Recipes contains the following fields:
        a name, a creator, a category, a list of ingredients, and a rating
    """
    name = models.CharField(max_length=255)
    rating = models.IntegerField(blank=True, null=True)
    creator = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    modificationDate = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """method to create the url for a specific recipe"""
        return reverse("details", args=[int(self.id)])
