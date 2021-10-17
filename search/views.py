"""
Views for the Search app
"""
from django.shortcuts import render

from .search import get_results


def landing(request):
    """
    The site landing page
    """
    if request.method == "POST":
        query = request.POST["query"]
        recipes = get_results(query)
        return render(request, "search/results.html", {"results": recipes})
    else:
        return render(request, "search/landing.html")
