from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from plantara.mixins import TestMixin

from ..models import ActionType


class ActionTypeDetailTestCase(APITestCase, TestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.action_type = self.create_action_type()

        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token.key)

    def create_user_and_action_type(self):
        user = self.create_user(email="richard.roe@example.com", password="password")

        return self.create_action_type(user=user)

    def test_get(self):
        action_type = self.action_type
        url = reverse("actiontype-detail", args=[action_type.pk])
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(
                reverse("actiontype-detail", args=[action_type.pk])
            ),
            "name": action_type.name,
            "notes": action_type.notes,
            "updated_at": action_type.updated_at.astimezone().isoformat(),
            "created_at": action_type.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_cannot_get_actions_of_other_users(self):
        action_type = self.create_user_and_action_type()

        url = reverse("actiontype-detail", args=[action_type.pk])
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        # Assert correct data is returned
        expected_response = {"detail": _("Not found.")}

        self.assertDictEqual(response.json(), expected_response)

    def test_patch(self):
        url = reverse("actiontype-detail", args=[self.action_type.pk])

        data = {
            "name": "New action type name",
            "notes": "New action type notes",
        }

        response = self.client.patch(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        action_type = ActionType.objects.get(pk=self.action_type.pk)

        # Assert action type is updated
        self.assertNotEqual(action_type.updated_at, self.action_type.updated_at)

        # Assert correct data is returned
        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(url),
            "name": action_type.name,
            "notes": data["notes"],
            "updated_at": action_type.updated_at.astimezone().isoformat(),
            "created_at": action_type.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_cannot_patch_action_types_of_other_users(self):
        action = self.create_user_and_action_type()

        url = reverse("actiontype-detail", args=[action.pk])

        data = {
            "name": "New action type name",
            "notes": "New action type notes",
        }

        response = self.client.patch(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        retrieved_action = ActionType.objects.get(pk=action.pk)

        # Assert action type is not updated
        self.assertEqual(retrieved_action.updated_at, action.updated_at)

        # Assert correct data is returned
        expected_response = {"detail": _("Not found.")}

        self.assertDictEqual(response.json(), expected_response)

    def test_delete(self):
        old_action_type_count = ActionType.objects.count()

        url = reverse("actiontype-detail", args=[self.action_type.pk])
        response = self.client.delete(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 204)

        # Assert action type is deleted
        new_action_type_count = ActionType.objects.count()
        self.assertEqual(new_action_type_count, old_action_type_count - 1)

        with self.assertRaises(ActionType.DoesNotExist):
            ActionType.objects.get(pk=self.action_type.pk)

    def test_cannot_delete_action_types_of_other_users(self):
        action = self.create_user_and_action_type()
        old_action_count = ActionType.objects.count()

        url = reverse("actiontype-detail", args=[action.pk])
        response = self.client.delete(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        # Assert action type is not deleted
        new_action_count = ActionType.objects.count()
        self.assertEqual(new_action_count, old_action_count)
