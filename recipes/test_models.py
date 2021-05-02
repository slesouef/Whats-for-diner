"""
Test of the recipes app models
"""
import datetime

from unittest import skip
from django.test import TestCase

from accounts.models import MyUser
from .models import Categories, Content, Ingredients, Recipes


class RecipesAppModelsTest(TestCase):
    """Validate the implementation of the models of the recipes app"""

    @classmethod
    def setUpClass(cls):
        super(RecipesAppModelsTest, cls).setUpClass()
        cls.user = MyUser.objects.create(username="test")
        cls.category = Categories.objects.create(name="test")
        cls.ingredient = Ingredients.objects.create(name="test")
        cls.recipe = Recipes.objects.create(name="test",
                                            category=cls.category,
                                            creator=cls.user,
                                            rating=5)
        cls.content = Content.objects.create(quantity="test",
                                             ingredient=cls.ingredient,
                                             recipe=cls.recipe)

    def test_category_name_max_length(self):
        """The category name should have a max length of 255"""
        self.assertEqual(255, self.category._meta.get_field("name").max_length)

    def test_categories_model_fields_implementation(self):
        """A category should have a name and a creation date"""
        self.assertIsInstance(self.category.name, str)
        self.assertIsInstance(self.category.creationDate, datetime.datetime)

    def test_content_quantity_max_length(self):
        """The content of a recipe should have a quantity field with max length 255"""
        self.assertEqual(255, self.content._meta.get_field("quantity").max_length)

    def test_content_model_fields_implementation(self):
        """The content table associates a recipe with an ingredient
         its tracks a quantity with a creation and modification date
         The primary foreign keys are recipe and ingredients"""
        self.assertIsInstance(self.content.quantity, str)
        self.assertIsInstance(self.content.creationDate, datetime.datetime)
        self.assertIsInstance(self.content.modificationDate, datetime.datetime)
        recipe_fk = self.content.recipe.id
        self.assertTrue(self.recipe.id, recipe_fk)
        ingredient_fk = self.content.ingredient.id
        self.assertTrue(self.ingredient.id, ingredient_fk)

    def test_ingredient_name_max_length(self):
        """The ingredient name has a max length of 255"""
        self.assertEqual(255, self.ingredient._meta.get_field("name").max_length)

    def test_ingredients_model_fields_implementation(self):
        """An Ingredient has a name and a creation date"""
        self.assertIsInstance(self.ingredient.name, str)
        self.assertIsInstance(self.ingredient.creationDate, datetime.datetime)

    def test_recipe_name_max_length(self):
        """The recipe name should have a max length of 255"""
        self.assertEqual(255, self.recipe._meta.get_field("name").max_length)

    def test_recipes_model_fields_implementation(self):
        """Validate the Recipe model fields
        A recipe has a name, a rating, a creation date, and a modification date
        The foreign keys are user and category
        The associated ingredients are reachable"""
        self.assertIsInstance(self.recipe.name, str)
        self.assertIsInstance(self.recipe.rating, int)
        user_fk = self.recipe.creator.id
        self.assertTrue(self.user.id, user_fk)
        category_fk = self.recipe.category.id
        self.assertTrue(self.category.id, category_fk)
        self.assertIsInstance(self.recipe.creationDate, datetime.datetime)
        self.assertIsInstance(self.recipe.modificationDate, datetime.datetime)
        self.assertEqual(1, len(self.recipe.ingredients.values()))
        self.assertTrue(self.ingredient in self.recipe.ingredients.all())

    @skip("recipe page not implemented")
    def test_recipes_model_get_absolute_url(self):
        """validate the recipe URL format"""
        url = self.recipe.get_absolute_url()
        self.assertIn(self.recipe.id, url)
