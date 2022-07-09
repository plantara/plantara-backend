from rest_framework import serializers

from .models import ActionType


class ActionTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ActionType
        fields = (
            "url",
            "name",
            "notes",
            "created_at",
            "updated_at",
        )
