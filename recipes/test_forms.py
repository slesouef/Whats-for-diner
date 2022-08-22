"""
Test file for the forms of the recipes app
"""
from django.test import SimpleTestCase

from .forms import RecipeNameForm, IngredientForm, ContentForm


class RecipeNameFormTest(SimpleTestCase):
    """
    Verify that the recipe form behaves as expected
    """

    def test_recipe_name_field_label(self):
        """Verify the recipe name label"""
        form = RecipeNameForm
        self.assertEqual("Nom de la recette",
                         form.declared_fields.get("name").label)

    def test_recipe_category_field_label(self):
        """Verify the category field label"""
        form = RecipeNameForm
        self.assertEqual("Catégorie",
                         form.declared_fields.get("category").label)


class IngredientFormTest(SimpleTestCase):
    """
    Verify that the ingredient form behaves as expected
    """

    def test_ingredient_name_field_label(self):
        """Verify the ingredient name label"""
        form = IngredientForm
        self.assertEqual("Ingrédient", form.base_fields.get("name").label)

    def test_ingredient_quantity_field_label(self):
        """Verify the ingredient quantity label"""
        form = IngredientForm
        self.assertEqual("Quantité", form.base_fields.get("quantity").label)


class ContentFormTest(SimpleTestCase):
    """
    Verify that the content form behaves as expected
    """

    def test_content_instruction_field_label(self):
        """Verify the content instruction label"""
        form = ContentForm
        self.assertEqual("Etape", form.base_fields.get("instructions").label)
