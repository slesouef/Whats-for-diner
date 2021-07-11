"""
views for the recipes app
"""
from django.shortcuts import render

from .forms import RecipeNameForm, IngredientsFormSet, ContentFormSet


def create_recipe(request):
    """A page to create a new recipe"""
    form = RecipeNameForm()
    ingredient_list = IngredientsFormSet(auto_id=True, prefix="ingredient")
    step_list = ContentFormSet(auto_id=True, prefix="step")
    if request.method == "POST":
        print(request.POST)
        return render(request, "recipes/create.html",
                      {"form": form, "ingredients": ingredient_list, "steps": step_list})
    else:
        return render(request, "recipes/create.html",
                      {"form": form, "ingredients": ingredient_list, "steps": step_list})
