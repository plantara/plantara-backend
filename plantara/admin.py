from django.contrib.admin import AdminSite
from django.utils import timezone
from django.views.decorators.cache import never_cache

from plantara.contrib.actions.models import Action
from plantara.contrib.schedules.models import Schedule


class PlantaraAdminSite(AdminSite):
    @never_cache
    def index(self, request, extra_context=None):
        if not extra_context:
            extra_context = {}

        schedules = Schedule.objects.all().select_related("action_type", "plant")

        overdue_actions = []

        for schedule in schedules:
            action = (
                Action.objects.filter(type=schedule.action_type, plant=schedule.plant)
                .order_by("-executed_on")
                .first()
            )
            now = timezone.now().date()
            deadline = action.executed_on + schedule.timedelta

            if now > deadline:
                overdue_actions.append(
                    {
                        "schedule": schedule,
                        "action": action,
                        "deadline": deadline,
                        "overdue": now - deadline,
                    }
                )

        extra_context.update({"overdue_actions": overdue_actions})

        return super().index(request, extra_context)


admin_site = PlantaraAdminSite(name="admin")
