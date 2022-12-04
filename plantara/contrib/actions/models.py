import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from plantara.contrib.action_types.models import ActionType
from plantara.contrib.plants.models import Plant
from plantara.models import TimestampedModel

UserModel = get_user_model()


class Action(TimestampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    type = models.ForeignKey(
        ActionType,
        related_name="actions",
        on_delete=models.CASCADE,
        verbose_name=_("Type"),
    )
    plant = models.ForeignKey(Plant, related_name="actions", on_delete=models.CASCADE)
    executed_on = models.DateField(_("Executed on"), default=timezone.now)
    notes = models.CharField(_("Note"), max_length=1024, blank=True)

    class Meta:
        verbose_name = _("Action")
        verbose_name_plural = _("Actions")

    def __str__(self):
        return f"{self.type.name} - {self.plant.name} - {self.created_at}"

    def get_absolute_url(self):
        return reverse("action:detail", kwargs={"pk": self.pk})

    # TODO: Validate that action type and plant belong to the same user.
