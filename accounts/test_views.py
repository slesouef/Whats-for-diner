"""
Tests for the views of the accounts app
"""
import shutil

from io import BytesIO
from PIL import Image

from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

from accounts.models import MyUser
from recipe_search.settings import BASE_DIR, LOGOUT_REDIRECT_URL


def create_test_image(name=None):
    """create an image file for file upload test"""
    file = BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(69, 239, 120))
    image.save(file, "png")
    if name:
        file.name = name + ".png"
    else:
        file.name = "test.png"
    file.seek(0)
    return file


class UnauthenticatedUserViewsTestCase(TestCase):
    """
    Verify the behaviour of the accounts app views when a user is not authenticated
    """

    def test_signup_page(self):
        """Test that the signup page returns correctly"""
        response = self.client.get("/account/signup")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_signup_mandatory_only(self):
        """Test the signup process with only mandatory fields"""
        form_data = {"username": "test",
                     "password": "test"}
        response = self.client.post("/account/signup", form_data)
        self.assertRedirects(response, "/account/profile")
        new_row = MyUser.objects.filter(username="test")
        self.assertTrue(len(new_row) == 1)
        self.assertFalse(new_row[0].first_name)
        self.assertFalse(new_row[0].last_name)
        self.assertFalse(new_row[0].email)
        self.assertFalse(new_row[0].avatar)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_signup_all_fields(self):
        """Test the signup with all fields and image file"""
        form_data = {"username": "test",
                     "password": "test",
                     "first_name": "first",
                     "last_name": "last",
                     "email": "email@test.com",
                     "avatar": create_test_image()}
        response = self.client.post("/account/signup", form_data)
        self.assertRedirects(response, "/account/profile")
        new_row = MyUser.objects.filter(username="test")
        self.assertEqual(1, len(new_row))
        self.assertEqual("first", new_row[0].first_name)
        self.assertEqual("last", new_row[0].last_name)
        self.assertEqual("email@test.com", new_row[0].email)
        self.assertTrue(new_row[0].avatar)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        shutil.rmtree(f"{BASE_DIR}/media/te")

    def test_update_page_unauthenticated(self):
        """Test the update page is not displayed when user is unauthenticated"""
        response = self.client.get("/account/update")
        self.assertRedirects(response, "/account/login?next=/account/update")

    def test_profile_page_unauthenticated(self):
        """Test the profile page is not displayed when user is unauthenticated"""
        response = self.client.get("/account/profile")
        self.assertRedirects(response, "/account/login?next=/account/profile")

    def test_delete_page_unauthenticated(self):
        """Test the delete page is not displayed when user is unauthenticated"""
        response = self.client.get("/account/delete")
        self.assertRedirects(response, "/account/login?next=/account/delete")

    def test_login_page(self):
        """Test the login page displays correctly"""
        response = self.client.get("/account/login")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login(self):
        """Validate login process"""
        user = MyUser.objects.create_user(username="test", password="test")
        form_data = {"username": "test",
                     "password": "test"}
        response = self.client.post("/account/login", form_data)
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response, "/account/profile")

    def test_logout_user_not_authenticated(self):
        """validate logout does not throw an error for a user not authenticated"""
        response = self.client.get("/logout")
        self.assertRedirects(response, reverse(LOGOUT_REDIRECT_URL))


class AuthenticatedUserViewsTestCase(TestCase):
    """
    Verify the behaviour of the accounts app views when a user is authenticated
    """

    def setUp(self):
        """Create an authenticated user"""
        self.user = MyUser.objects.create_user(username="test")
        self.client.force_login(self.user)

    def test_signup_page(self):
        """Test than an authenticated user is redirected when calling the signup page"""
        response = self.client.get("/account/signup")
        self.assertRedirects(response, "/account/profile")

    def test_profile_page(self):
        """Test that the profile page displays correctly"""
        response = self.client.get("/account/profile")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_update_page(self):
        """Test the update page is displayed properly"""
        response = self.client.get("/account/update")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "accounts/update.html")

    def test_add_first_name(self):
        """Test adding a first name field"""
        form_data = {"first_name": "new value",
                     "last_name": "",
                     "email": "",
                     "avatar": ""}
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("new value", user[0].first_name)

    def test_update_first_name(self):
        """Test updating the first name field"""
        form_data = {"first_name": "new value",
                     "last_name": "",
                     "email": "",
                     "avatar": ""}
        self.user.first_name = "test"
        self.user.save()
        user = MyUser.objects.filter(username="test")
        self.assertEqual("test", user[0].first_name)
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("new value", user[0].first_name)

    def test_add_last_name(self):
        """Test adding a last name field"""
        form_data = {"first_name": "",
                     "last_name": "new value",
                     "email": "",
                     "avatar": ""}
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("new value", user[0].last_name)

    def test_update_last_name(self):
        """Test updating the last name field"""
        form_data = {"first_name": "",
                     "last_name": "new value",
                     "email": "",
                     "avatar": ""}
        self.user.last_name = "test"
        self.user.save()
        user = MyUser.objects.filter(username="test")
        self.assertEqual("test", user[0].last_name)
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("new value", user[0].last_name)

    def test_add_email(self):
        """Test adding an email field"""
        form_data = {"first_name": "",
                     "last_name": "",
                     "email": "new@mail.com",
                     "avatar": ""}
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("new@mail.com", user[0].email)

    def test_update_email(self):
        """Test updating the email field"""
        form_data = {"first_name": "",
                     "last_name": "",
                     "email": "new@mail.com",
                     "avatar": ""}
        self.user.email = "test@test.com"
        self.user.save()
        user = MyUser.objects.filter(username="test")
        self.assertEqual("test@test.com", user[0].email)
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("new@mail.com", user[0].email)

    def test_add_avatar(self):
        """Test adding an avatar image"""
        form_data = {"first_name": "",
                     "last_name": "",
                     "email": "",
                     "avatar": create_test_image()}
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("te/test/test.png", user[0].avatar)
        shutil.rmtree(f"{BASE_DIR}/media/te")

    def test_update_avatar(self):
        """Test updating the avatar image"""
        form_data = {"first_name": "",
                     "last_name": "",
                     "email": "",
                     "avatar": create_test_image("new_name")}
        self.user.avatar = "te/test/test.png"
        self.user.save()
        user = MyUser.objects.filter(username="test")
        self.assertEqual("te/test/test.png", user[0].avatar)
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("te/test/new_name.png", user[0].avatar)
        shutil.rmtree(f"{BASE_DIR}/media/te")

    def test_add_all_user_information(self):
        """Test adding all user information"""
        form_data = {"first_name": "first name",
                     "last_name": "last name",
                     "email": "test@test.com",
                     "avatar": create_test_image()}
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("first name", user[0].first_name)
        self.assertEqual("last name", user[0].last_name)
        self.assertEqual("test@test.com", user[0].email)
        self.assertEqual("te/test/test.png", user[0].avatar)
        shutil.rmtree(f"{BASE_DIR}/media/te")

    def test_update_all_user_information(self):
        """Test updating all user information"""
        form_data = {"first_name": "new first name",
                     "last_name": "new last name",
                     "email": "new@mail.com",
                     "avatar": create_test_image("new_name")}
        self.user.first_name = "test"
        self.user.last_name = "test"
        self.user.email = "test@test.com"
        self.user.avatar = "te/test/test.png"
        self.user.save()
        user = MyUser.objects.filter(username="test")
        self.assertEqual("test", user[0].first_name)
        self.assertEqual("test", user[0].last_name)
        self.assertEqual("test@test.com", user[0].email)
        self.assertEqual("te/test/test.png", user[0].avatar)
        response = self.client.post("/account/update", form_data)
        self.assertRedirects(response, "/account/profile")
        user = MyUser.objects.filter(username="test")
        self.assertEqual("new first name", user[0].first_name)
        self.assertEqual("new last name", user[0].last_name)
        self.assertEqual("new@mail.com", user[0].email)
        self.assertEqual("te/test/new_name.png", user[0].avatar)
        shutil.rmtree(f"{BASE_DIR}/media/te")

    def test_delete_page(self):
        """Test the display of the delete page"""
        response = self.client.get("/account/delete")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "accounts/confirmation.html")

    def test_delete_user_account(self):
        """Test the user account deletion process"""
        original_user = MyUser.objects.filter(username="test")
        self.assertEqual(1, original_user.count(), "the user does not exist")
        response = self.client.post("/account/delete")
        self.assertRedirects(response, "/account/signup")
        deleted_user = MyUser.objects.filter(username="test")
        self.assertEqual(0, deleted_user.count(), "the user was not deleted")

    def test_logout_user_authenticated(self):
        """Test the logout redirect for an authenticated user"""
        response = self.client.get("/logout")
        self.assertRedirects(response, reverse(LOGOUT_REDIRECT_URL))
