from django.contrib import admin

from plantara.admin import admin_site

from .models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    list_filter = ("action_type", "plant", "period", "unit")
    list_display = ("action_type", "plant", "period", "unit")
    list_per_page = 20
    date_hierarchy = "created_at"


admin_site.register(Schedule, ScheduleAdmin)
