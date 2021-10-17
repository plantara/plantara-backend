import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from plantara.models import TimestampedModel

UserModel = get_user_model()


class Plant(TimestampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(_("Name"), max_length=254)
    owner = models.ForeignKey(
        UserModel, related_name="plants", on_delete=models.CASCADE
    )
    location = models.CharField(_("Location"), max_length=254, blank=True)
    notes = models.CharField(_("Notes"), max_length=1024, blank=True)

    class Meta:
        verbose_name = _("Plant")
        verbose_name_plural = _("Plants")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plants:detail", kwargs={"pk": self.pk})
