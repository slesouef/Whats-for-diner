import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from .forms import SignUpForm

logger = logging.getLogger(__name__)


@never_cache
def signup(request):
    """
    The signup page renders with the signup form
    """
    if request.user.is_authenticated:
        logger.info("signup page requested for logged in user")
        return redirect("/")
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
    return render(request, "accounts/profile.html")
