"""
views for the recipes app
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import RecipeNameForm, IngredientsFormSet, ContentFormSet
from .models import Recipes, Ingredients, Content


@login_required
def create_recipe(request):
    """A page to create a new recipe"""
    recipe = RecipeNameForm()
    ingredients = IngredientsFormSet(prefix="ingredient")
    steps = ContentFormSet(prefix="step")
    if request.method == "POST":
        recipe = RecipeNameForm(request.POST)
        ingredients = IngredientsFormSet(request.POST, prefix="ingredient")
        steps = ContentFormSet(request.POST, prefix="step")
        if recipe.is_valid() and ingredients.is_valid() and steps.is_valid():
            r = Recipes()
            r.creator = request.user
            r.name = recipe.cleaned_data["name"]
            r.category = recipe.cleaned_data["category"]
            r.save()
            for form in ingredients.forms:
                if form.cleaned_data:
                    ingredient = Ingredients()
                    ingredient.recipe = r
                    ingredient.name = form.cleaned_data["name"]
                    ingredient.quantity = form.cleaned_data["quantity"]
                    ingredient.save()
            index = 0
            for form in steps.forms:
                if form.cleaned_data:
                    content = Content()
                    content.recipe = r
                    content.index = index
                    content.instructions = form.cleaned_data["instructions"]
                    content.save()
                    index += 1
            return redirect(r.get_absolute_url())
        else:
            return render(request, "recipes/create.html",
                          {"form": recipe, "ingredients": ingredients, "steps": steps})
    else:
        return render(request, "recipes/create.html",
                      {"form": recipe, "ingredients": ingredients, "steps": steps})


@login_required
def update_recipe(request, rid):
    recipe = get_object_or_404(Recipes, id=rid)
    recipe_form = RecipeNameForm(request.POST or None, instance=recipe)
    ingredients_formset = IngredientsFormSet(prefix="ingredient", instance=recipe)
    steps_formset = ContentFormSet(prefix="step", instance=recipe)
    return render(request, "recipes/update.html", {"recipe": recipe_form,
                                                   "ingredients": ingredients_formset,
                                                   "steps": steps_formset})


def recipe_details(request, rid):
    recipe = Recipes.objects.filter(id=rid).first()
    ingredients = Ingredients.objects.filter(recipe_id=recipe.id)
    steps = Content.objects.filter(recipe_id=recipe.id).order_by("index")
    return render(request, "recipes/details.html",
                  {"recipe": recipe, "ingredients_list": ingredients, "steps_list": steps})
