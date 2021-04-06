from django.test import TestCase

from accounts.models import MyUser, user_directory_path


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
        user = MyUser(username="Xerxes")
        path = user_directory_path(user, "test_file.png")
        self.assertEqual("xe/xerxes/test_file.png", path)
