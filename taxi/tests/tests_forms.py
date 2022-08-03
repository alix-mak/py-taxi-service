from django.test import TestCase
from taxi.forms import DriverCreationForm


class FormsTest(TestCase):
    def test_driver_creation_form_with_license_first_last_name_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user123456Test",
            "password2": "user123456Test",
            "license_number": "AAA11111",
            "email": "test@example.uk",
            "first_name": "First name",
            "last_name": "Last name"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
