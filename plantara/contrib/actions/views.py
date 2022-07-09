from rest_framework import permissions, viewsets

from .models import Action
from .serializers import ActionSerializer


class ActionViewSet(
    viewsets.ModelViewSet,
    viewsets.GenericViewSet,
):
    serializer_class = ActionSerializer
    http_method_names = ("get", "post", "put", "patch", "delete")

    def get_permissions(self):
        permission_classes = super().get_permissions()
        permission_classes.append(permissions.IsAuthenticated())

        return permission_classes

    def get_queryset(self):
        return Action.objects.filter(plant__owner=self.request.user)
