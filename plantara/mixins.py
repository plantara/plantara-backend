from django.contrib.auth import get_user_model

from plantara.contrib.action_types.models import ActionType
from plantara.contrib.plants.models import Plant

UserModel = get_user_model()


class TestMixin:
    def create_user(
        self, email="john.doe@example.com", password="password", **extra_fields
    ):
        return UserModel.objects.create_user(
            email=email, password=password, **extra_fields
        )

    def create_plant(
        self, name="Plant name", owner=None, location="Location", notes="Notes"
    ):
        return Plant.objects.create(
            name=name, owner=owner or self.user, location=location, notes=notes
        )

    def create_action_type(self, name="Action type", user=None, notes="Notes"):
        return ActionType.objects.create(
            name=name,
            user=user or self.user,
            notes=notes,
        )
