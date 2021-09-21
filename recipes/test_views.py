"""
Tests for the views of the recipes app
"""
from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

from accounts.models import MyUser
from recipes.models import Recipes, Content, Ingredients, Categories


class RecipesViewsTestCase(TestCase):
    """
    Validate the behaviour of the recipes views (create, view, and update recipes)
    """

    @classmethod
    def setUpClass(cls):
        """Create category entry for tests"""
        super().setUpClass()
        category = Categories()
        category.name = "test category"
        category.save()
        cls.category_id = category.id

    def setUp(self):
        """Create an authenticated user"""
        self.user = MyUser.objects.create_user(username="test")
        self.client.force_login(self.user)

    def test_get_recipe_create_page(self):
        """Test the page is displayed properly"""
        response = self.client.get("/recipe/create")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "recipes/create.html")

    def test_post_invalid_recipe_name(self):
        """Validate the error raised if recipe name is invalid"""
        form_data = {'name': '',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'one',
                     'ingredient-0-quantity': '1b',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'first'}
        response = self.client.post("/recipe/create", data=form_data)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context["form"].is_valid())

    def test_post_invalid_ingredient_name(self):
        """validate the error raised if the ingredient name is invalid"""
        form_data = {'name': 'test',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': '',
                     'ingredient-0-quantity': '1b',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'first'}
        response = self.client.post("/recipe/create", data=form_data)
        self.assertEqual(200, response.status_code)
        self.assertFormsetError(response, "ingredients", 0, "name", "This field is required.")

    def test_post_invalid_ingredient_quantity(self):
        """Validate the error raised if the ingredient quantity is invalid"""
        form_data = {'name': 'test',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'one',
                     'ingredient-0-quantity': '',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'first'}
        response = self.client.post("/recipe/create", data=form_data)
        self.assertEqual(200, response.status_code)
        self.assertFormsetError(response, "ingredients", 0, "quantity", "This field is required.")

    def test_post_valid_forms(self):
        """Verify that the recipe is created if all the forms are valid"""
        form_data = {'name': 'test',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'one',
                     'ingredient-0-quantity': '1b',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'first'}
        response = self.client.post("/recipe/create", data=form_data)
        new_recipe = Recipes.objects.filter(name="test")
        self.assertRedirects(response, f"/recipe/details/{new_recipe[0].id}")
        self.assertEqual(1, len(new_recipe))
        self.assertEqual("test", new_recipe[0].name)
        self.assertEqual("test category", new_recipe[0].category.name)
        new_ingredient = Ingredients.objects.filter(recipe_id=new_recipe[0].id)
        self.assertEqual(1, len(new_ingredient))
        self.assertEqual("one", new_ingredient[0].name)
        self.assertEqual("1b", new_ingredient[0].quantity)
        new_step = Content.objects.filter(recipe_id=new_recipe[0].id)
        self.assertEqual(1, len(new_step))
        self.assertEqual("first", new_step[0].instructions)
        self.assertEqual(0, new_step[0].index)

    def test_get_recipe_view(self):
        """Test the page is displayed properly"""
        form_data = {'name': 'view',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'another',
                     'ingredient-0-quantity': '1',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'extra'}
        self.client.post("/recipe/create", data=form_data)
        new_recipe = Recipes.objects.filter(name="view").first()
        url = f"/recipe/details/{new_recipe.id}"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "recipes/details.html")


class UnauthenticatedUserTestCases(TestCase):
    """
    Validate the redirections in case the pages are called by an unauthenticated user
    """

    def test_get_recipe_create_unauthenticated(self):
        """Verify user redirect to login"""
        response = self.client.get("/recipe/create")
        self.assertRedirects(response, "/account/login?next=/recipe/create")

    def test_post_recipe_create_unauthenticated(self):
        """Verify user redirect to login"""
        response = self.client.post("/recipe/create")
        self.assertRedirects(response, "/account/login?next=/recipe/create")
