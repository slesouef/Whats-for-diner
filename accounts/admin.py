"""Register model for admin app"""
from django.contrib import admin

from .models import MyUser

admin.site.register(MyUser)
