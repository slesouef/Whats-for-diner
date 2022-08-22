"""
Tests for the views of the recipes app
"""
from django.test import TestCase, Client

from accounts.models import MyUser
from recipes.forms import RecipeNameForm, IngredientsFormSet, ContentFormSet
from recipes.models import Recipes, Content, Ingredients, Categories


class RecipesCreateTestCase(TestCase):
    """
    Validate the behaviour of the recipes create view
    """

    @classmethod
    def setUpTestData(cls):
        """Create category entry for tests"""
        super().setUpTestData()
        category = Categories()
        category.name = "test category"
        category.save()
        cls.category_id = category.id

    def setUp(self):
        """Create an authenticated user"""
        self.user = MyUser.objects.create_user(username="test")
        self.client.force_login(self.user)

    def test_get_recipe_create_page(self):
        """Test the create page is displayed properly"""
        response = self.client.get("/recipe/create")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "recipes/create.html")
        self.assertIsInstance(response.context["recipe"], RecipeNameForm)
        self.assertIsInstance(response.context["ingredients"],
                              IngredientsFormSet)
        self.assertIsInstance(response.context["steps"], ContentFormSet)

    def test_post_create_invalid_recipe_name(self):
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
        self.assertFalse(response.context["recipe"].is_valid())
        self.assertFormError(response, "recipe", "name",
                             "This field is required.")

    def test_post_create_invalid_ingredient_name(self):
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
        self.assertFalse(response.context["ingredients"].is_valid())
        self.assertFormsetError(response, "ingredients", 0, "name",
                                "This field is required.")

    def test_post_create_invalid_ingredient_quantity(self):
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
        self.assertFalse(response.context["ingredients"].is_valid())
        self.assertFormsetError(response, "ingredients", 0, "quantity",
                                "This field is required.")

    def test_post_create_valid_forms(self):  # TODO: 2+ entries per formsets
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


class UnauthenticatedUserTestCases(TestCase):
    """
    Validate the behaviour of the recipes details view
    Validate the redirections in case the recipe create, recipe update,
    and show user list pages are called by an unauthenticated user
    """

    @classmethod
    def setUpTestData(cls):
        """Create recipe entry for tests"""
        super().setUpTestData()
        category = Categories()
        category.name = "test category"
        category.save()
        form_data = {'name': 'view',
                     'category': category.id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'another',
                     'ingredient-0-quantity': '1',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'extra'}
        client = Client()
        user = MyUser.objects.create_user(username="test")
        client.force_login(user)
        client.post("/recipe/create", data=form_data)
        new_recipe = Recipes.objects.filter(name="view").first()
        cls.detailsUrl = f"/recipe/details/{new_recipe.id}"
        cls.updateUrl = f"/recipe/update/{new_recipe.id}"
        client.logout()

    def test_get_recipe_details(self):
        """Test the page is displayed properly"""
        response = self.client.get(self.detailsUrl)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "recipes/details.html")
        self.assertTrue("recipe" in response.context)
        self.assertTrue("ingredients_list" in response.context)
        self.assertTrue("steps_list" in response.context)
        self.assertTrue("rating" in response.context)

    def test_get_recipe_create_unauthenticated(self):
        """Verify user redirect to login"""
        response = self.client.get("/recipe/create")
        self.assertRedirects(response, "/account/login?next=/recipe/create")

    def test_post_recipe_create_unauthenticated(self):
        """Verify user redirect to login"""
        response = self.client.post("/recipe/create")
        self.assertRedirects(response, "/account/login?next=/recipe/create")

    def test_get_recipe_update_unauthenticated(self):
        """Verify user redirect to login"""
        response = self.client.get(self.updateUrl)
        self.assertRedirects(response, f"/account/login?next={self.updateUrl}")

    def test_post_recipe_update_unauthenticated(self):
        """Verify user redirect to login"""
        response = self.client.post(self.updateUrl)
        self.assertRedirects(response, f"/account/login?next={self.updateUrl}")

    def test_get_user_list_unauthenticated(self):
        """Verify user redirect to login"""
        response = self.client.post("/recipe/list")
        self.assertRedirects(response, "/account/login?next=/recipe/list")


class RecipesUpdateTestCase(TestCase):
    """
    Validate the behaviour of the recipes create view
    """

    @classmethod
    def setUpTestData(cls):
        """Create category entry for tests"""
        super().setUpTestData()
        category = Categories()
        category.name = "test category"
        category.save()
        cls.category_id = category.id

    def setUp(self):
        """Create an authenticated user and create a recipe for that user"""
        self.user = MyUser.objects.create_user(username="test")
        self.client.force_login(self.user)
        form_data = {'name': 'test',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'petit pois',
                     'ingredient-0-quantity': '1b',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'test'}
        self.client.post("/recipe/create", data=form_data)
        new_recipe = Recipes.objects.filter(name="test").first()
        self.recipe_id = new_recipe.id
        self.url = f"/recipe/update/{self.recipe_id}"

    def test_get_update_recipe(self):
        """Test the update page is displayed properly"""
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "recipes/update.html")
        self.assertIsInstance(response.context["recipe"], RecipeNameForm)
        self.assertIsInstance(response.context["ingredients"],
                              IngredientsFormSet)
        self.assertIsInstance(response.context["steps"], ContentFormSet)

    def test_post_update_invalid_recipe_name(self):
        """Validate the error raised if recipe name is invalid after update"""
        form_data = {'name': '',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'petit pois',
                     'ingredient-0-quantity': '1b',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'test'}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context["recipe"].is_valid())
        self.assertFormError(response, "recipe", "name",
                             "This field is required.")

    def test_post_update_invalid_ingredient_name(self):
        """
        Validate the error raised if the ingredient name is invalid
        after update
        """
        form_data = {'name': 'test',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': '',
                     'ingredient-0-quantity': '1b',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'test'}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context["ingredients"].is_valid())
        self.assertFormsetError(response, "ingredients", 0, "name",
                                "This field is required.")

    def test_post_update_invalid_ingredient_quantity(self):
        """
        Validate the error raised if the ingredient quantity is invalid
        after update
        """
        form_data = {'name': 'test',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'petit pois',
                     'ingredient-0-quantity': '',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'test'}
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context["ingredients"].is_valid())
        self.assertFormsetError(response, "ingredients", 0, "quantity",
                                "This field is required.")

    def test_post_update_valid_forms(self):
        """
        Verify that the recipe is created if all the forms are valid
        after update
        """
        form_data = {'name': 'test updated',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'new ingredient',
                     'ingredient-0-quantity': '42',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'new step'}
        response = self.client.post(self.url, data=form_data)
        self.assertRedirects(response, f'/recipe/details/{self.recipe_id}')
        updated_recipe = Recipes.objects.filter(id=self.recipe_id)
        self.assertEqual(1, len(updated_recipe))
        self.assertEqual("test updated", updated_recipe[0].name)
        self.assertEqual("test category", updated_recipe[0].category.name)
        updated_ingredients = Ingredients.objects.filter(
            recipe_id=self.recipe_id)
        self.assertEqual(2, len(updated_ingredients))
        self.assertEqual("petit pois", updated_ingredients[0].name)
        self.assertEqual("1b", updated_ingredients[0].quantity)
        self.assertEqual("new ingredient", updated_ingredients[1].name)
        self.assertEqual("42", updated_ingredients[1].quantity)
        updated_steps = Content.objects.filter(recipe_id=self.recipe_id)
        self.assertEqual(2, len(updated_steps))
        self.assertEqual("test", updated_steps[0].instructions)
        self.assertEqual(0, updated_steps[0].index)
        self.assertEqual("new step", updated_steps[1].instructions)
        # not testing index of new step as the passed form
        # does not allow correct ordering


class UserRecipeListTestCases(TestCase):
    """
    Validate the behaviour of the user list page
    """

    def setUp(self):
        """Create an authenticated user"""
        self.user = MyUser.objects.create_user(username="test")
        self.client.force_login(self.user)

    def test_get_user_list(self):
        """test the page is displayed properly"""
        response = self.client.get("/recipe/list")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "recipes/list.html")


class RecipeRatingTestCases(TestCase):
    """
    Validate the behaviour of the add vote result method
    """

    @classmethod
    def setUpTestData(cls):
        """Create category entry for tests"""
        super().setUpTestData()
        category = Categories()
        category.name = "test category"
        category.save()
        cls.category_id = category.id

    def setUp(self):
        """Create an authenticated user and create a recipe for that user"""
        self.user = MyUser.objects.create_user(username="voter")
        self.client.force_login(self.user)
        form_data = {'name': 'vote_test',
                     'category': self.category_id,
                     'ingredient-TOTAL_FORMS': '1',
                     'ingredient-INITIAL_FORMS': '0',
                     'ingredient-0-name': 'petit pois',
                     'ingredient-0-quantity': '1b',
                     'step-TOTAL_FORMS': '1',
                     'step-INITIAL_FORMS': '0',
                     'step-0-instructions': 'test'}
        self.client.post("/recipe/create", data=form_data)
        new_recipe = Recipes.objects.filter(name="vote_test").first()
        self.recipe_id = new_recipe.id

    def test_default_recipe_rating_is_none(self):
        """ Validate the default rating of a recipe"""
        response = self.client.get(f"/recipe/details/{self.recipe_id}")
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.context["rating"])

    def test_add_first_rating_to_recipe(self):
        """Add a rating for the first time"""
        response = self.client.post(f"/recipe/vote/{self.recipe_id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json",
                         response.headers.get("Content-Type"))
        self.assertEqual(b'{"status": "success", '
                         b'"rating": {"liked": 1, "total votes": 1}}',
                         response.content)

    def test_add_rating_to_recipe(self):
        """increment the rating of a rated recipe"""
        self.client.post(f"/recipe/vote/{self.recipe_id}")
        response = self.client.post(f"/recipe/vote/{self.recipe_id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json",
                         response.headers.get("Content-Type"))
        self.assertEqual(b'{"status": "success", '
                         b'"rating": {"liked": 2, "total votes": 2}}',
                         response.content)
