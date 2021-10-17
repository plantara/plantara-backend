from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from plantara.mixins import TestMixin

from ..models import Plant


class PlantListTestCase(APITestCase, TestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.plant = self.create_plant()

        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token.key)

    def test_get(self):
        url = reverse("plant-list")
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        plants = Plant.objects.all()

        expected_response = {
            "count": len(plants),
            "next": None,
            "previous": None,
            "results": [
                {
                    "url": response.wsgi_request.build_absolute_uri(
                        reverse("plant-detail", args=[plant.pk])
                    ),
                    "name": plant.name,
                    "location": plant.location,
                    "notes": plant.notes,
                    "updated_at": plant.updated_at.astimezone().isoformat(),
                    "created_at": plant.created_at.astimezone().isoformat(),
                }
                for plant in plants
            ],
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_post_with_base_fields(self):
        url = reverse("plant-list")

        data = {
            "name": "Plant",
        }

        response = self.client.post(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 201)

        # Assert correct data is returned
        plant = Plant.objects.order_by("created_at").last()

        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("plant-detail", args=[plant.pk])
            ),
            "name": data["name"],
            "location": "",
            "notes": "",
            "updated_at": plant.updated_at.astimezone().isoformat(),
            "created_at": plant.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_post_with_all_fields(self):
        url = reverse("plant-list")

        data = {
            "name": "Plant",
            "location": "Location",
            "notes": "Notes",
        }

        response = self.client.post(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 201)

        # Assert correct data is returned
        plant = Plant.objects.order_by("created_at").last()

        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("plant-detail", args=[plant.pk])
            ),
            "name": data["name"],
            "location": data["location"],
            "notes": data["notes"],
            "updated_at": plant.updated_at.astimezone().isoformat(),
            "created_at": plant.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)
