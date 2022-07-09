from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from plantara.mixins import TestMixin

from ..models import ActionType


class ActionTypeListTestCase(APITestCase, TestMixin):
    def setUp(self):
        self.maxDiff = None
        self.user = self.create_user()
        self.action_type = self.create_action_type()

        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token.key)

    def test_get(self):
        url = reverse("actiontype-list")
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        action_types = ActionType.objects.all()

        expected_response = {
            "count": len(action_types),
            "next": None,
            "previous": None,
            "results": [
                {
                    "url": response.wsgi_request.build_absolute_uri(
                        reverse("actiontype-detail", args=[action_type.pk])
                    ),
                    "name": action_type.name,
                    "notes": action_type.notes,
                    "updated_at": action_type.updated_at.astimezone().isoformat(),
                    "created_at": action_type.created_at.astimezone().isoformat(),
                }
                for action_type in action_types
            ],
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_post_with_base_fields(self):
        url = reverse("actiontype-list")

        data = {
            "name": "Action type name",
        }

        response = self.client.post(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 201)

        # Assert correct data is returned
        action_type = ActionType.objects.order_by("created_at").last()

        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("actiontype-detail", args=[action_type.pk])
            ),
            "name": data["name"],
            "notes": "",
            "updated_at": action_type.updated_at.astimezone().isoformat(),
            "created_at": action_type.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_post_with_all_fields(self):
        url = reverse("actiontype-list")

        data = {
            "name": "Action type name",
            "notes": "Notes",
        }

        response = self.client.post(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 201)

        # Assert correct data is returned
        action_type = ActionType.objects.order_by("created_at").last()

        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("actiontype-detail", args=[action_type.pk])
            ),
            "name": data["name"],
            "notes": data["notes"],
            "updated_at": action_type.updated_at.astimezone().isoformat(),
            "created_at": action_type.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)
