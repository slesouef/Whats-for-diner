from django.shortcuts import render, redirect

from .search import get_results


def landing(request):
    if request.method == "POST":
        query = request.POST["query"]
        recipes = get_results(query)
        return render(request, "search/results.html", {"results": recipes})
    else:
        return render(request, "search/landing.html")
