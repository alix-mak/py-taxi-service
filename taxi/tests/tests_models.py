from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    username = "test"
    password = "test123456"
    first_name = "test"
    last_name = "test"
    license_number = "AAA00000"

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test"
        )
        self.assertEqual(str(manufacturer), manufacturer.name)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username=ModelTests.username,
            password=ModelTests.password,
            first_name=ModelTests.first_name,
            last_name=ModelTests.last_name
        )
        self.assertEqual(str(driver), f"{driver.username} "
                                      f"({driver.first_name} "
                                      f"{driver.last_name})")

    def test_create_driver_with_license_number(self):
        driver = get_user_model().objects.create_user(
            username=ModelTests.username,
            password=ModelTests.password,
            license_number=ModelTests.license_number
        )

        self.assertEqual(driver.username, ModelTests.username)
        self.assertTrue(driver.check_password(ModelTests.password))
        self.assertEqual(driver.license_number, ModelTests.license_number)

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test"
        )
        car = Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )

        self.assertEqual(str(car), car.model)
