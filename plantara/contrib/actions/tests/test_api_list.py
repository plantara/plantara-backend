from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from plantara.mixins import TestMixin

from ..models import Action


class ActionListTestCase(APITestCase, TestMixin):
    def setUp(self):
        self.maxDiff = None
        self.user = self.create_user()
        self.plant = self.create_plant()
        self.action_type = self.create_action_type()
        self.action = self.create_action()

        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token.key)

    def test_get(self):
        url = reverse("action-list")
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        actions = Action.objects.all()

        expected_response = {
            "count": len(actions),
            "next": None,
            "previous": None,
            "results": [
                {
                    "url": response.wsgi_request.build_absolute_uri(
                        reverse("action-detail", args=[action.pk])
                    ),
                    "type": response.wsgi_request.build_absolute_uri(
                        reverse("actiontype-detail", args=[action.type.pk])
                    ),
                    "plant": response.wsgi_request.build_absolute_uri(
                        reverse("plant-detail", args=[action.plant.pk])
                    ),
                    "notes": action.notes,
                    "updated_at": action.updated_at.astimezone().isoformat(),
                    "created_at": action.created_at.astimezone().isoformat(),
                }
                for action in actions
            ],
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_post_with_base_fields(self):
        url = reverse("action-list")

        data = {
            "type": reverse("actiontype-detail", args=[self.action_type.pk]),
            "plant": reverse("plant-detail", args=[self.plant.pk]),
        }

        response = self.client.post(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 201)

        # Assert correct data is returned
        action = Action.objects.order_by("created_at").last()

        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("action-detail", args=[action.pk])
            ),
            "type": response.wsgi_request.build_absolute_uri(data["type"]),
            "plant": response.wsgi_request.build_absolute_uri(data["plant"]),
            "notes": "",
            "updated_at": action.updated_at.astimezone().isoformat(),
            "created_at": action.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_post_with_all_fields(self):
        url = reverse("action-list")

        data = {
            "type": reverse("actiontype-detail", args=[self.action_type.pk]),
            "plant": reverse("plant-detail", args=[self.plant.pk]),
            "notes": "Notes",
        }

        response = self.client.post(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 201)

        # Assert correct data is returned
        action = Action.objects.order_by("created_at").last()

        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("action-detail", args=[action.pk])
            ),
            "type": response.wsgi_request.build_absolute_uri(data["type"]),
            "plant": response.wsgi_request.build_absolute_uri(data["plant"]),
            "notes": data["notes"],
            "updated_at": action.updated_at.astimezone().isoformat(),
            "created_at": action.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)
