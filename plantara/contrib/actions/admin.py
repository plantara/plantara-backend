from django.contrib import admin

from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_filter = ("type", "plant", "created_at", "updated_at")
    list_display = ("type", "plant", "created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"
