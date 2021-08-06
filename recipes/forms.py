"""
Forms to create and update a recipe
"""
from django.forms import Form, CharField, TextInput, Select, ModelChoiceField, ModelForm
from django.forms.models import inlineformset_factory

from .models import Categories, Ingredients, Content, Recipes


class RecipeNameForm(Form):
    """
    This forms allows the creation of a recipe
    """
    name = CharField(label="Nom de la recette", required=True, max_length=255,
                     widget=TextInput(attrs={"class": "col-8"}))
    category = ModelChoiceField(queryset=Categories.objects.all(), empty_label=None,
                                label="Catégorie", widget=Select(attrs={"class": "col-7"}))


class IngredientForm(ModelForm):
    """
    ModelForm for an ingredient, to be used in a formset
    """

    class Meta:
        model = Ingredients
        exclude = [("creationDate",), ("modificationDate",)]
        labels = {
            "name": "Ingrédient",
            "quantity": "Quantité"
        }


IngredientsFormSet = inlineformset_factory(Recipes, Ingredients, form=IngredientForm, extra=1,
                                           fields=["name", "quantity"], can_delete=False)


class ContentForm(ModelForm):
    """
    ModelForm for a content entry, to be used in a formset
    """

    class Meta:
        model = Content
        exclude = [("index",), ("creationDate",), ("modificationDate",)]
        labels = {
            "instructions": "Etape"
        }


ContentFormSet = inlineformset_factory(Recipes, Content, form=ContentForm, fields=["instructions"],
                                       can_delete=False, extra=1)
