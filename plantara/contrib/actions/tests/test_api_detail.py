from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from plantara.mixins import TestMixin

from ..models import Action


class ActionDetailTestCase(APITestCase, TestMixin):
    def setUp(self):
        self.user = self.create_user()
        self.plant = self.create_plant()
        self.action_type = self.create_action_type()
        self.action = self.create_action()

        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + token.key)

    def create_action_of_another_user(self):
        user = self.create_user(email="richard.roe@example.com", password="password")
        plant = self.create_plant(owner=user)
        action_type = self.create_action_type(user=user)

        return self.create_action(type=action_type, plant=plant)

    def test_get(self):
        action = self.action
        url = reverse("action-detail", args=[action.pk])
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        # Assert correct data is returned
        expected_response = {
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

        self.assertDictEqual(response.json(), expected_response)

    def test_cannot_get_actions_of_other_users(self):
        action = self.create_action_of_another_user()

        url = reverse("action-detail", args=[action.pk])
        response = self.client.get(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        # Assert correct data is returned
        expected_response = {"detail": _("Not found.")}

        self.assertDictEqual(response.json(), expected_response)

    def test_patch(self):
        url = reverse("action-detail", args=[self.action.pk])
        action_type = self.create_action_type(name="New Action")
        plant = self.create_plant(name="New Plant")

        data = {
            "type": reverse("actiontype-detail", args=[action_type.pk]),
            "plant": reverse("plant-detail", args=[plant.pk]),
            "notes": "New action notes",
        }

        response = self.client.patch(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 200)

        action = Action.objects.get(pk=self.action.pk)

        # Assert action is updated
        self.assertNotEqual(action.updated_at, self.action.updated_at)

        # Assert correct data is returned
        expected_response = {
            "url": response.wsgi_request.build_absolute_uri(url),
            "type": response.wsgi_request.build_absolute_uri(
                reverse("actiontype-detail", args=[action.type.pk])
            ),
            "plant": response.wsgi_request.build_absolute_uri(
                reverse("plant-detail", args=[action.plant.pk])
            ),
            "notes": data["notes"],
            "updated_at": action.updated_at.astimezone().isoformat(),
            "created_at": action.created_at.astimezone().isoformat(),
        }

        self.assertDictEqual(response.json(), expected_response)

    def test_cannot_patch_actions_of_other_users(self):
        action = self.create_action_of_another_user()

        url = reverse("action-detail", args=[action.pk])

        data = {
            "type": reverse("actiontype-detail", args=[action.type.pk]),
            "plant": reverse("plant-detail", args=[action.plant.pk]),
            "notes": "New plant notes",
        }

        response = self.client.patch(url, data=data, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        retrieved_action = Action.objects.get(pk=action.pk)

        # Assert action is not updated
        self.assertEqual(retrieved_action.updated_at, action.updated_at)

        # Assert correct data is returned
        expected_response = {"detail": _("Not found.")}

        self.assertDictEqual(response.json(), expected_response)

    def test_delete(self):
        old_action_count = Action.objects.count()

        url = reverse("action-detail", args=[self.action.pk])
        response = self.client.delete(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 204)

        # Assert action is deleted
        new_action_count = Action.objects.count()
        self.assertEqual(new_action_count, old_action_count - 1)

        with self.assertRaises(Action.DoesNotExist):
            Action.objects.get(pk=self.action.pk)

    def test_cannot_delete_actions_of_other_users(self):
        action = self.create_action_of_another_user()
        old_action_count = Action.objects.count()

        url = reverse("action-detail", args=[action.pk])
        response = self.client.delete(url, format="json")

        # Assert status code is correct
        self.assertEqual(response.status_code, 404)

        # Assert action is not deleted
        new_action_count = Action.objects.count()
        self.assertEqual(new_action_count, old_action_count)
