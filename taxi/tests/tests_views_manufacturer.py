from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123456"
        )
        self.client.force_login(self.user)

    def test_get_manufacturers(self):
        Manufacturer.objects.create(name="test1", country="country1")
        Manufacturer.objects.create(name="test2", country="country2")

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers)
                         )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {
            "name": "name",
            "country": "country"
        }

        self.client.post(MANUFACTURER_CREATE_URL, data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])

        self.assertEqual(new_manufacturer.name, form_data["name"])
        self.assertEqual(new_manufacturer.country, form_data["country"])

    def test_update_manufacturer(self):
        new_manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )
        update_data = {
            "name": "Update name",
            "country": "Update country"
        }
        self.client.post(reverse("taxi:manufacturer-update", kwargs={"pk": new_manufacturer.id}), data=update_data)

        manufacturer = Manufacturer.objects.get(pk=new_manufacturer.id)
        self.assertEqual(manufacturer.name, update_data["name"])
        self.assertEqual(manufacturer.country, update_data["country"])

    def test_delete_manufacturer(self):
        new_manufacturer = Manufacturer.objects.create(
            name="name",
            country="country"
        )
        Manufacturer.objects.create(
            name="Delete",
            country="Delete"
        )

        self.client.post(reverse("taxi:manufacturer-delete", kwargs={"pk": new_manufacturer.id}))
        self.assertEqual(Manufacturer.objects.count(), 1)
