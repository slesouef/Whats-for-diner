"""
Test file for the forms of the accounts app
"""
from django.test import SimpleTestCase

from .forms import SignUpForm, UpdateForm


class SignupFormTest(SimpleTestCase):
    """
    Verify that the forms of the accounts app behave as expected
    """

    def test_file_field_label(self):
        """verify the file input fields label value"""
        form = SignUpForm()
        self.assertTrue(form.fields["avatar"].label is None
                        or form.fields["avatar"].label == "Avatar")


class UpdateFormTest(SimpleTestCase):
    """
    Verify the update form of the accounts app
    """

    def test_first_name_field_label(self):
        """Verify the label for the first name field"""
        form = UpdateForm
        self.assertEqual("Prénom", form.declared_fields.get("first_name").label)

    def test_last_name_field_label(self):
        """Verify the label for the last name field"""
        form = UpdateForm
        self.assertEqual("Nom de Famille", form.declared_fields.get("last_name").label)

    def test_email_field_label(self):
        """Verify the label for the email field"""
        form = UpdateForm
        self.assertEqual("Adresse Email", form.declared_fields.get("email").label)

    def test_file_field_label(self):
        """Verify the label for the user avatar field"""
        form = UpdateForm
        self.assertEqual("Avatar", form.declared_fields.get("avatar").label)
