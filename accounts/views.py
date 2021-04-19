"""
views for the accounts app
"""
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from recipe_search.settings import LOGOUT_REDIRECT_URL
from .forms import SignUpForm, UpdateForm

logger = logging.getLogger(__name__)


@csrf_protect
@sensitive_post_parameters()
@never_cache
def signup(request):
    """
    The signup page renders with the signup form
    """
    if request.user.is_authenticated:
        logger.info("signup page requested for logged in user")
        return redirect("profile")
    else:
        if request.method == "POST":
            form = SignUpForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password")
                user.set_password(raw_password)
                user.save()
                authenticated_user = authenticate(request, username=username, password=raw_password)
                login(request, authenticated_user)
                logger.info("new account created successfully")
                return redirect("profile")
        else:
            form = SignUpForm()
            logger.debug("signup requested")
        return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    """
    display the user's profile page
    """
    context = {}
    user = request.user
    context["username"] = user.username
    context["first_name"] = user.first_name
    context["last_name"] = user.last_name
    context["email"] = user.email
    if user.avatar:
        context["avatar"] = user.avatar
    else:
        context["avatar"] = False
    return render(request, "accounts/profile.html", context)


@login_required
@csrf_protect
@sensitive_post_parameters()
def update(request):
    """
    Display the user information update page
    """
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            if form.data["first_name"] != "":
                user.first_name = form.data["first_name"]
                logger.debug("user %s updated first name", {user.username})
            if form.data["last_name"] != "":
                user.last_name = form.data["last_name"]
                logger.debug("user %s updated last name", {user.username})
            if form.data["email"] != "":
                user.email = form.data["email"]
                logger.debug("user %s updated email", {user.username})
            if form.files:
                user.avatar = form.files["avatar"]
                logger.debug("user %s updated user icon", {user.username})
            user.save()
            logger.info("user %s information update successful", {user.username})
            return redirect("profile")
    else:
        form = UpdateForm()
        logger.debug("update page requested")
    return render(request, "accounts/update.html", {"form": form})


@login_required
def delete(request):
    """
    Displays the delete confirmation page
    """
    if request.method == 'POST':
        user = request.user
        user.delete()
        logger.info("account deleted successfully")
        logger.debug("account for user %s deleted successfully", {user.username})
        return redirect("signup")
    else:
        return render(request, "accounts/confirmation.html")


@csrf_protect
@sensitive_post_parameters()
@never_cache
def user_login(request):
    """
    Display the login page for a user
    """
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                logger.debug("user successfully logged in")
                return redirect("profile")
            else:
                logger.debug("user authentication failed for user %s", {username})
        else:
            logger.debug("Login attempt with incorrect credentials")
    else:
        form = AuthenticationForm
        logger.debug("Login page requested")
        return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    """
    Terminate the user session and redirect to the landing page
    """
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
