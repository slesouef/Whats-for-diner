"""
Forms use to create and update user account
"""
from django.forms import ModelForm, TextInput, EmailInput, ClearableFileInput, PasswordInput

from .models import MyUser


class SignUpForm(ModelForm):
    """
    This form contains all the fields necessary to create a user account
    Mandatory fields are:
        username
    """
    class Meta:
        model = MyUser
        fields = ["username", "first_name", "last_name", "email", "avatar", "password"]
        widgets = {
            "username": TextInput(attrs={"class": "form-control"}),
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "email": EmailInput(attrs={"class": "form-control"}),
            "avatar": ClearableFileInput(attrs={"class": "form-control"}),
            "password": PasswordInput(attrs={"class": "form-control"})
        }
