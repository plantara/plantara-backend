from rest_framework import permissions, viewsets

from . import models, serializers


class PlantViewSet(
    viewsets.ModelViewSet,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.PlantSerializer
    http_method_names = ("get", "post", "put", "patch", "delete")

    def get_permissions(self):
        permission_classes = super().get_permissions()
        permission_classes.append(permissions.IsAuthenticated())

        return permission_classes

    def get_queryset(self):
        return models.Plant.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
