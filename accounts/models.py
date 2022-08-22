"""
Project specific user model based on django's default user model
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

# from search.models import Recipes


def user_directory_path(instance, filename):
    """
    The user's avatar image will be uploaded to a user specific directory
    based on the username
    """
    username = instance.username.lower()
    directory = username[:2]
    return f"{directory}/{username}/{filename}"


class MyUser(AbstractUser):
    """
    The project user can add a picture to the account
    The project user can associate multiple Recipes as favorites
    The project user can associate multiple Recipes as liked
    """
    avatar = models.ImageField(blank=True, upload_to=user_directory_path)
    # favorites = models.ManyToManyField(Recipes, related_name="favorites")
    # likes = models.ManyToManyField(Recipes, related_name="likes")
