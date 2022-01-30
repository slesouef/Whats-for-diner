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
            new_recipe = recipe.save(commit=False)
            new_recipe.creator = request.user
            new_recipe.save()
            for form in ingredients.forms:
                if form.cleaned_data:
                    ingredient = form.save(commit=False)
                    ingredient.recipe = new_recipe
                    ingredient.save()
            for num, form in enumerate(steps.forms):
                if form.cleaned_data:
                    step = form.save(commit=False)
                    step.recipe = new_recipe
                    step.index = num
                    step.save()
            return redirect(new_recipe.get_absolute_url())
        return render(request, "recipes/create.html",
                      {"recipe": recipe, "ingredients": ingredients, "steps": steps})
    return render(request, "recipes/create.html",
                  {"recipe": recipe, "ingredients": ingredients, "steps": steps})


@login_required
def update_recipe(request, rid):
    """A page to update an existing recipe"""
    recipe = get_object_or_404(Recipes, id=rid)
    recipe_form = RecipeNameForm(request.POST or None, instance=recipe)
    ingredients_formset = IngredientsFormSet(request.POST or None, prefix="ingredient",
                                             instance=recipe)
    steps_formset = ContentFormSet(request.POST or None, prefix="step", instance=recipe)
    if request.method == "POST":
        if recipe_form.is_valid() and ingredients_formset.is_valid() and steps_formset.is_valid():
            recipe_form.save()
            ingredients_formset.save()
            steps_formset.save(commit=False)
            for num, obj in enumerate(steps_formset.new_objects):
                obj.index = num
                obj.save()
            steps_formset.save()
            return redirect(recipe.get_absolute_url())
        return render(request, "recipes/update.html", {"recipe": recipe_form,
                                                       "ingredients": ingredients_formset,
                                                       "steps": steps_formset})
    return render(request, "recipes/update.html", {"recipe": recipe_form,
                                                   "ingredients": ingredients_formset,
                                                   "steps": steps_formset})


def recipe_details(request, rid):
    """A page displaying the content of a recipe"""
    recipe = get_object_or_404(Recipes.objects.filter(id=rid))
    ingredients = Ingredients.objects.filter(recipe_id=recipe.id)
    steps = Content.objects.filter(recipe_id=recipe.id)
    return render(request, "recipes/details.html",
                  {"recipe": recipe, "ingredients_list": ingredients, "steps_list": steps})


@login_required
def show_list(request):
    """A page displaying all the user's recipe"""
    user = request.user
    recipes = Recipes.objects.filter(creator=user)
    return render(request, 'recipes/list.html', {"results": recipes})
