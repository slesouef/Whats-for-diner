from django.contrib import auth
from django.test import TestCase
from io import BytesIO
from PIL import Image

from accounts.models import MyUser, user_directory_path


def create_test_image():
    file = BytesIO()
    image = Image.new("RGBA", size=(100, 100), color=(69, 239, 120))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file


class UserFileUploadPathTestCase(TestCase):
    """
    Verify that the file upload path method returns the correct path structure
    """

    def testUploadPath(self):
        """
        The user's file is uploaded in a user specific directory with the following structure
            - directory named after the first two letters of the user's username
            - directory name after the user's username value
        """
        user = MyUser(username="XeRxEs")
        path = user_directory_path(user, "test_file.png")
        self.assertEqual("xe/xerxes/test_file.png", path)


class UnauthenticatedUserViewsTestCase(TestCase):
    """
    Verify the behaviour of the accounts app views when a user is not authenticated
    """

    def testSignupPage(self):
        """Test that the signup page returns correctly"""
        response = self.client.get("/account/signup")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "accounts/base.html")
        self.assertTemplateUsed(response, "accounts/signup.html")

    def testSignupMandatoryOnly(self):
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

    def testSignupAllFields(self):
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
        self.assertTrue(len(new_row) == 1)
        self.assertTrue(new_row[0].first_name == "first")
        self.assertTrue(new_row[0].last_name == "last")
        self.assertTrue(new_row[0].email == "email@test.com")
        self.assertTrue(new_row[0].avatar)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)


class AuthenticatedUserViewsTestCase(TestCase):
    """
    Verify the behaviour of the accounts app views when a user is authenticated
    """

    def setUp(self):
        """Create an authenticated user"""
        self.user = MyUser.objects.create_user(username="test")
        self.client.force_login(self.user)

    def testSignupPage(self):
        """Test than an authenticated user is redirected when calling the signup page"""
        response = self.client.get("/account/signup")
        self.assertRedirects(response, "/account/profile")

    def testProfilePage(self):
        """Test that the profile page displays correctly"""
        response = self.client.get("/account/profile")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "accounts/base.html")
        self.assertTemplateUsed(response, "accounts/profile.html")
