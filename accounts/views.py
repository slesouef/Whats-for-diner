import logging

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
        form = SignUpForm()
        logger.debug("signup requested")
        return render(request, "accounts/signup.html", {"form": form})
