"""
Forms to create and update a recipe
"""
from django.forms import Form, CharField, TextInput, Textarea, Select, ModelChoiceField, ModelForm
from django.forms.models import inlineformset_factory

from .models import Categories, Ingredients, Content, Recipes


class RecipeNameForm(Form):
    """
    This forms allows the creation of a recipe
    """
    name = CharField(label="Nom de la recette", required=True, max_length=255,
                     widget=TextInput(attrs={"class": "col-8"}))
    category = ModelChoiceField(queryset=
                                Categories.objects.values_list("name", flat=True).distinct(),
                                empty_label=None, label="Catégorie",
                                widget=Select(attrs={"class": "col-7"}))


class IngredientForm(ModelForm):

    class Meta:
        model = Ingredients
        exclude = [("creationDate",), ("modificationDate",)]


IngredientsFormSet = inlineformset_factory(Recipes, Ingredients, form=IngredientForm,
                                           fields=["name", "quantity"], can_delete=True)


class ContentForm(ModelForm):

    class Meta:
        model = Content
        exclude = [("index",), ("creationDate",), ("modificationDate",)]


ContentFormSet = inlineformset_factory(Recipes, Content, form=ContentForm, fields=["instructions"],
                                       can_delete=True)
