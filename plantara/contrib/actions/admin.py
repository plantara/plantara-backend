from django.contrib import admin

from plantara.admin import admin_site

from .models import Action


class ActionAdmin(admin.ModelAdmin):
    list_filter = ("type", "plant", "executed_on", "created_at", "updated_at")
    list_display = ("type", "plant", "executed_on", "created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"


admin_site.register(Action, ActionAdmin)
