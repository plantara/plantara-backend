from django.utils.translation import gettext_lazy as _

DAYS = "days"
WEEKS = "weeks"
MONTHS = "months"
SEASONS = "seasons"
HALF_YEARS = "half_years"
YEARS = "years"

UNIT_TYPES = (
    (DAYS, _("Days")),
    (WEEKS, _("Weeks")),
    (MONTHS, _("Months")),
    (SEASONS, _("Seasons")),
    (HALF_YEARS, _("Half years")),
    (YEARS, _("Years")),
)
