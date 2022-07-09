from django.contrib import admin

from .models import ActionType


@admin.register(ActionType)
class ActionTypeAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at")
    list_display = ("name", "created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"
