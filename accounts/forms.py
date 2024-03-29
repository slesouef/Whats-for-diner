"""
Forms use to create and update user account
"""
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, TextInput, EmailInput, ClearableFileInput,\
                         PasswordInput, Form, CharField, EmailField, ImageField
from django.utils.translation import gettext_lazy as _

from .models import MyUser


class SignUpForm(ModelForm):
    """
    This form contains all the fields necessary to create a user account
    Mandatory fields are:
        username, password
    """

    class Meta:
        model = MyUser
        fields = ["username", "first_name", "last_name", "email", "avatar",
                  "password"]
        labels = {
            "username": _("Nom d'Utilisateur"),
            "first_name": _("Prénom"),
            "last_name": _("Nom de Famille"),
            "email": _("Adresse Email"),
            "password": _("Mot de Passe")
        }
        widgets = {
            "username": TextInput(attrs={"class": "form-control"}),
            "first_name": TextInput(attrs={"class": "form-control"}),
            "last_name": TextInput(attrs={"class": "form-control"}),
            "email": EmailInput(attrs={"class": "form-control"}),
            "avatar": ClearableFileInput(),
            "password": PasswordInput(attrs={"class": "form-control"})
        }


class UpdateForm(Form):
    """
    Form to update the non-mandatory user information
    """
    first_name = CharField(required=False, max_length=150, label="Prénom",
                           widget=TextInput(attrs={"class": "form-control"}))
    last_name = CharField(required=False, max_length=150,
                          label="Nom de Famille",
                          widget=TextInput(attrs={"class": "form-control"}))
    email = EmailField(required=False, max_length=254, label="Adresse Email",
                       widget=EmailInput(attrs={"class": "form-control"}))
    avatar = ImageField(required=False, label="Avatar",
                        widget=ClearableFileInput())


class CustomAuthenticationForm(AuthenticationForm):
    """
    Modify the authentication form to have labels in French
    """

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields["username"].label = "Nom d'Utilisateur"
        self.fields["password"].label = "Mot de Passe"
