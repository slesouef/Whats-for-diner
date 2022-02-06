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
        if recipes:
            return render(request, "search/results.html", {"results": recipes})
        return render(request, "search/empty.html")
    return render(request, "search/landing.html")
