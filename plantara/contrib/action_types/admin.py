from django.contrib import admin

from plantara.admin import admin_site

from .models import ActionType


class ActionTypeAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at")
    list_display = ("name", "created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"


admin_site.register(ActionType, ActionTypeAdmin)
