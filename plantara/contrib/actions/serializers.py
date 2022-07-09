from rest_framework import serializers

from .models import ActionType, Action


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Action
        fields = (
            "url",
            "type",
            "plant",
            "notes",
            "created_at",
            "updated_at",
        )
