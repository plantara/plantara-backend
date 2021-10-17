from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from plantara.mixins import TestMixin

from ..models import Plant


class PlantDetailTestCase(APITestCase, TestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.plant = self.create_plant()

        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token.key)

    def create_user_and_plant(self):
        user = self.create_user(email="richard.roe@example.com", password="password")
        return self.create_plant(owner=user)

    def test_get(self):
        plant = self.plant
        url = reverse("plant-detail", args=[plant.pk])
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("plant-detail", args=[plant.pk])
            ),
            "name": plant.name,
            "location": plant.location,
            "notes": plant.notes,
            "updated_at": plant.updated_at.astimezone().isoformat(),
            "created_at": plant.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_cannot_get_plants_of_other_users(self):
        plant = self.create_user_and_plant()

        url = reverse("plant-detail", args=[plant.pk])
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        # Assert correct data is returned
        expected_response = {"detail": _("Not found.")}

        self.assertDictEqual(response.json(), expected_response)

    def test_patch(self):
        url = reverse("plant-detail", args=[self.plant.pk])

        data = {
            "name": "New plant name",
            "location": "New plant location",
            "notes": "New plant notes",
        }

        response = self.client.patch(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        plant = Plant.objects.get(pk=self.plant.pk)

        # Assert plant is updated
        self.assertNotEqual(plant.updated_at, self.plant.updated_at)

        # Assert correct data is returned
        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(url),
            "name": data["name"],
            "location": data["location"],
            "notes": data["notes"],
            "updated_at": plant.updated_at.astimezone().isoformat(),
            "created_at": plant.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_cannot_patch_plants_of_other_users(self):
        plant = self.create_user_and_plant()

        url = reverse("plant-detail", args=[plant.pk])

        data = {
            "name": "New plant name",
            "location": "New plant location",
            "notes": "New plant notes",
        }

        response = self.client.patch(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        retrieved_plant = Plant.objects.get(pk=plant.pk)

        # Assert plant is not updated
        self.assertEqual(retrieved_plant.updated_at, plant.updated_at)

        # Assert correct data is returned
        expected_response = {"detail": _("Not found.")}

        self.assertDictEqual(response.json(), expected_response)

    def test_owner_field_is_ignored_on_patch(self):
        url = reverse("plant-detail", args=[self.plant.pk])

        user = self.create_user(email="richard.roe@example.com", password="password")

        data = {
            "owner": reverse("user-detail", args=[user.pk]),
            "name": "New plant name",
            "location": "New plant location",
            "notes": "New plant notes",
        }

        response = self.client.patch(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        plant = Plant.objects.get(pk=self.plant.pk)

        # Assert plant author is not updated
        self.assertEqual(plant.owner, self.plant.owner)

        # Assert correct data is returned
        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(url),
            "name": data["name"],
            "location": data["location"],
            "notes": data["notes"],
            "updated_at": plant.updated_at.astimezone().isoformat(),
            "created_at": plant.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_delete(self):
        old_plant_count = Plant.objects.count()

        url = reverse("plant-detail", args=[self.plant.pk])
        response = self.client.delete(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 204)

        # Assert plant is deleted
        new_plant_count = Plant.objects.count()
        self.assertEqual(new_plant_count, old_plant_count - 1)

        with self.assertRaises(Plant.DoesNotExist):
            Plant.objects.get(pk=self.plant.pk)

    def test_cannot_delete_plants_of_other_users(self):
        plant = self.create_user_and_plant()
        old_plant_count = Plant.objects.count()

        url = reverse("plant-detail", args=[plant.pk])
        response = self.client.delete(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        # Assert plant is not deleted
        new_plant_count = Plant.objects.count()
        self.assertEqual(new_plant_count, old_plant_count)
