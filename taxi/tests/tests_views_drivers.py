from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456"
        )
        self.client.force_login(self.user)

    def test_get_drivers(self):
        Driver.objects.create(
            username="user",
            password="user123456",
            license_number="AAA12345"
        )
        Driver.objects.create(
            username="user1",
            password="user123456",
            license_number="AAA12346"
        )

        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]),
                         list(drivers)
                         )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123456Test",
            "password2": "user123456Test",
            "license_number": "AAA11111",
            "email": "test@example.uk",
            "first_name": "First name",
            "last_name": "Last name"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)

        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_delete_driver(self):
        new_driver = get_user_model().objects.create_user(
            username="new_user",
            password="user123456Test",
            license_number="AAA11111"

        )
        self.client.force_login(new_driver)
        self.client.post(reverse("taxi:driver-delete", kwargs={"pk": new_driver.id}))
        self.assertEqual(Driver.objects.count(), 1)
