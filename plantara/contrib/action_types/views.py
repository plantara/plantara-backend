from rest_framework import permissions, viewsets

from .models import ActionType
from .serializers import ActionTypeSerializer


class ActionTypeViewSet(
    viewsets.ModelViewSet,
    viewsets.GenericViewSet,
):
    serializer_class = ActionTypeSerializer
    http_method_names = ("get", "post", "put", "patch", "delete")

    def get_permissions(self):
        permission_classes = super().get_permissions()
        permission_classes.append(permissions.IsAuthenticated())

        return permission_classes

    def get_queryset(self):
        return ActionType.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
