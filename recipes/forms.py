"""
Forms to create and update a recipe
"""
from django.forms import ModelForm, CharField, TextInput, Select, ModelChoiceField
from django.forms.models import inlineformset_factory

from .models import Categories, Ingredients, Content, Recipes


class RecipeNameForm(ModelForm):
    """
    This forms allows the creation of a recipe
    """

    class Meta:
        model = Recipes
        fields = ["name", "category"]

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
        fields = ["name", "quantity"]
        labels = {
            "name": "Ingrédient",
            "quantity": "Quantité"
        }


IngredientsFormSet = inlineformset_factory(Recipes, Ingredients, form=IngredientForm, extra=1,
                                           fields=["name", "quantity"], can_delete=True)


class ContentForm(ModelForm):
    """
    ModelForm for a content entry, to be used in a formset
    """

    class Meta:
        model = Content
        fields = ["instructions"]
        labels = {
            "instructions": "Etape"
        }


ContentFormSet = inlineformset_factory(Recipes, Content, form=ContentForm, extra=1,
                                       fields=["instructions"], can_delete=True)
