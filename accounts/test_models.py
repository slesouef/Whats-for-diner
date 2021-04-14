"""
Test for the models of the accounts app
"""
from django.test import SimpleTestCase

from accounts.models import MyUser, user_directory_path


class MyUserModelTest(SimpleTestCase):
    """
    Verify that the file upload path method returns the correct path structure
    """

    def test_avatar_label(self):
        """
        Verify that the user icon label is correct
        """
        user = MyUser(username="test")
        field_label = user._meta.get_field("avatar").verbose_name
        self.assertEqual("avatar", field_label)

    def test_upload_path(self):
        """
        The user's file is uploaded in a user specific directory with the following structure
            - directory named after the first two letters of the user's username
            - directory name after the user's username value
        """
        user = MyUser(username="XeRxEs")
        path = user_directory_path(user, "test_file.png")
        self.assertEqual("xe/xerxes/test_file.png", path)
