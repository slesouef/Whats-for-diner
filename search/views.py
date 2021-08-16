from django.shortcuts import render


def landing(request):
    if request.method == "POST":
        print(request.POST)
        return render(request, "search/base.html")
    else:
        return render(request, "search/base.html")
