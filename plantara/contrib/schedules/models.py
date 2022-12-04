import uuid

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from plantara.contrib.action_types.models import ActionType
from plantara.contrib.plants.models import Plant
from plantara.models import TimestampedModel

from . import constants

UserModel = get_user_model()


class Schedule(TimestampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    action_type = models.ForeignKey(
        ActionType, related_name="schedules", on_delete=models.CASCADE
    )
    plant = models.ForeignKey(Plant, related_name="schedules", on_delete=models.CASCADE)
    period = models.IntegerField(_("Period"))
    unit = models.CharField(
        _("Units"), max_length=254, choices=constants.UNIT_TYPES, blank=True
    )
    notes = models.CharField(_("Note"), max_length=1024, blank=True)

    class Meta:
        verbose_name = _("Schedule")
        verbose_name_plural = _("Schedules")

    def __str__(self):
        return (
            f"{self.action_type.name} - {self.plant.name} - {self.period} {self.unit}"
        )

    def get_absolute_url(self):
        return reverse("action:detail", kwargs={"pk": self.pk})

    @property
    def timedelta(self):
        if self.unit == constants.DAYS:
            return relativedelta(days=self.period)

        if self.unit == constants.WEEKS:
            return relativedelta(weeks=self.period)

        if self.unit == constants.MONTHS:
            return relativedelta(months=self.period)

        if self.unit == constants.SEASONS:
            return relativedelta(months=self.period * 3)

        if self.unit == constants.HALF_YEARS:
            return relativedelta(months=self.period * 6)

        if self.unit == constants.YEARS:
            return relativedelta(years=self.period)
