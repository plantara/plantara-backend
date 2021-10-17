from rest_framework import serializers

from .models import Plant


class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plant
        fields = (
            "url",
            "name",
            "location",
            "notes",
            "created_at",
            "updated_at",
        )
